from fastapi import FastAPI, Depends, HTTPException, Response, File, UploadFile, Form
from sqlalchemy.orm import Session
from . import schemas, models, utils, questions
from .database import Base, engine, get_db
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from .token_utils import create_access_token
from typing import List, Optional
from .search import search_in_database
from .schemas import ProductCreate, Product_out1, QuizInput, RoutinePlanOut
from .models import Products
import requests
from .add_product_to_routin import choose_products 
import sqlite3

Base.metadata.create_all(bind=engine)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
AILAB_API_KEY = "cmea2907w0001jo041hntvzpp"
AILAB_URL = "https://api.ailabtools.com/skin/analyze"
user_in_code = None


def read_database():
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    return cursor


def find_user_id(cursor, user_name):
    cursor.execute('SELECT user_id FROM [Users_sign_up] WHERE user_name = ?', (user_name,))

def merge_results(selfie_result: dict, quiz_result: dict) -> dict:
    skin_type_selfie = selfie_result.get("skin_type")
    skin_type_quiz = quiz_result.get("skin_type")
    skin_type_final = skin_type_selfie if skin_type_selfie else skin_type_quiz

    concerns_selfie = []
    for key in ["acne", "wrinkles", "dark_circles", "spots"]:
        if selfie_result.get(key, 0) > 0.1:
            concerns_selfie.append(key)
    concerns_quiz = quiz_result.get("concerns", [])
    final_concerns = list(set(concerns_selfie + concerns_quiz))

    preferences = quiz_result.get("preferences", {})

    return {
        "skin_type": skin_type_final,
        "concerns": final_concerns,
        "preferences": preferences
    }


@app.post("/Account/sign_up", tags=['Account'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["password"] = pwd_context.hash(user.password)
    new_user = models.Users_for_sign_up(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token_data = {"sub": str(user.user_name), "role": 'normal user'} 
    token = create_access_token(token_data)
    global user_in_code
    cursor = read_database()
    user_id = find_user_id(cursor, user.user_name)
    user_in_code = user_id
    return {"message": "user created", "access_token": token, "token_type": "bearer"}


@app.post("/Account/login", tags=['Account'] , response_model=schemas.Token)
def review_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    global user_in_code
    user_review = db.query(models.Users_for_sign_up).filter(models.Users_for_sign_up.user_id == user.user_id).first()
    admin_review = db.query(models.Admins).filter(models.Admins.user_id == user.user_id).first()
    if user_review and pwd_context.verify(user.password, user_review.password):
        user_in_code = user_review.user_id
        token = create_access_token({"sub": str(user.user_id), "role": "user"})
        return {"access_token": token, "token_type": "bearer"}

    if admin_review and pwd_context.verify(user.password, admin_review.password):
        token = create_access_token({"sub": str(user.user_id), "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post("/add_product", response_model=schemas.ProductCreate)
def Product_Create(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    product_data = product.dict()
    new_product = models.Products(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return Response(content='product created', status_code=201)

@app.get("/all_products", response_model=List[schemas.ProductCreate])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    browse_create = {}
    for i in products:

        browse_create['user_id'] = user_in_code
        browse_create['product_id'] = i.product_id
        browse_create['interaction_type'] = 'view'
        new_browse = models.Browsing_History(**browse_create)
        db.add(new_browse)
    db.commit()
    # db.refresh(new_browse)
    return products


@app.post("/shopping", response_model=schemas.PurchaseHistoryCreate)
def Shopping(product: schemas.Purchase_input, db: Session = Depends(get_db)):
    global user_in_code
    new_product_data = {'user_id': user_in_code, 'product_id': product.product_id, 'quantity': product.quantity}
    new_product = models.Purchase_History(**new_product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    browse_create = {}
    browse_create['user_id'] = user_in_code
    browse_create['product_id'] = product.product_id
    browse_create['interaction_type'] = 'view'
    new_browse = models.Browsing_History(**browse_create)
    db.add(new_browse)
    db.commit()
    db.refresh(new_browse)
    return Response(content='You will be happy you choose us', status_code=201)


@app.post("/search", response_model=schemas.Product_out2)
def search_input(search: schemas.Search, db: Session = Depends(get_db)):
    search_result = search_in_database(user_in_code, search.search)
    browse_create = {}
    count1 = 0
    count2 = 0
    submit_list = []
    for items in search_result['items']:
        browse_create['user_id'] = user_in_code
        browse_create['product_id'] = items['product_id']
        browse_create['interaction_type'] = 'view'
        new_browse = models.Browsing_History(**browse_create)
        db.add(new_browse)
        count1 += 1
        if count1 == 3:
            break
    db.commit()
    for items in search_result['items']:
        submit_list.append(items)
        count2 += 1
        if count2 == 3:
            break
    return {'items': submit_list}

@app.post("/add_admin", response_model=schemas.Admin, tags=['Admin'])
def create_user(user: schemas.Admin, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["password"] = pwd_context.hash(user.password)
    new_user = models.Admins(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return Response(content='admin created', status_code=201)


@app.get('/quiz/questions', tags=['Quiz'])
def quiz_questions():
    return {"questions": questions.questions}

# @app.post('/quiz/submit',  tags=['Quiz'])
# def submitting_quiz(data: schemas.QuizQuestions, db: Session = Depends(get_db)):
#     answers = {
#         "q1": data.q1.value,
#         "q2": data.q2.value,
#         "q3": data.q3.value,
#         "q4": data.q4.value,
#         "q5": data.q5.value,
#         "q6": data.q6.value,
#         "q7": data.q7.value,
#         "q8": data.q8.value,
#         "q9": data.q9.value,
#         "q10": data.q10.value,
#     }
#     result = utils.analyze_quiz(answers)
#     quiz = models.Quiz_result(
#         user_id=data.user_id,
#         skin_type=result["skin_type"],
#         concerns=result["concerns"],
#         preferences=result["preferences"]
#     )
#     db.add(quiz)
#     db.commit()
#     db.refresh(quiz)

#     return {"quiz_id": quiz.quiz_id, "message": "Quiz submitted"}


# @app.post("/generate_routine", response_model=list[RoutinePlanOut], tags=['Routine'])
# def generate_routine(data: QuizInput, db: Session = Depends(get_db)):
#     plans = []
#     for plan_name in ["Full Plan", "Hydration Plan", "Minimalist Plan"]:
#         routine = create_routine(db, data.user_id, plan_name, data.skin_type, data.concerns, data.preferences, data.budget_range)
#         plans.append(routine)
#     return plans
# @app.post("/generate_routine", response_model=list[RoutinePlanOut], tags=['Routine'])
# def generate_routine(data: QuizInput, db: Session = Depends(get_db)):
#     plans = []
#     for plan_name in ["Full Plan", "Hydration Plan", "Minimalist Plan"]:
#         routine = create_routine(
#             db, 
#             data.user_id, 
#             plan_name, 
#             data.skin_type, 
#             data.concerns, 
#             data.preferences, 
#             data.budget_range
#         )

        
#         steps_out = [
#             RoutineStepOut(
#                 step_name=step.description,   
#                 product_name=step.product_name
#             )
#             for step in routine.steps
#         ]

#         plans.append(RoutinePlanOut(
#             id=routine.id,
#             name=routine.name,
#             steps=steps_out
#         ))

#     return plans

from . import models


def create_routine(db: Session, user_id: int, plan_name: str,
                   skin_type: str, concerns: list, preferences: list, budget_range: list):
    # routine = models.RoutinePlan(user_id=user_id, plan_name=plan_name)
    # db.add(routine)
    # db.commit()
    # db.refresh(routine)

    steps = choose_products(db, +skin_type, concerns, preferences, plan_name, budget_range)

    for step in steps:
        db_step = models.RoutineStep(
            routine_id=routine.id,
            step_number=step["step_number"],
            description=step["description"],
            product_id=step.get("product_id"),
            product_name=step.get("product_name"),
            price=step.get("price")
        )
        db.add(db_step)

    db.commit()
    db.refresh(routine)
    return routine

@app.post("/generate_routine", response_model=List[schemas.RoutinePlanOut], tags=['Routine'])
def generate_routine(db: Session = Depends(get_db), budget_range: str = Form(...)):
    plans = []
    
    for plan_name in ["Full Plan", "Hydration Plan", "Minimalist Plan"]:
        routine = create_routine(
            db,
            data.user_id,
            plan_name,
            data.skin_type,
            data.concerns,
            data.preferences,
            data.budget_range
        )

        steps_out = [
            schemas.RoutineStepOut(
                step_name=step.description,
                product_name=step.product_name
            )
            for step in routine.steps
        ]

        plan_out = schemas.RoutinePlanOut(
            id=routine.id,
            user_id=routine.user_id,
            plan_name=routine.plan_name,
            created_at=routine.created_at,
            steps=steps_out
        )
        plans.append(plan_out)

    return plans




# @app.post('/quiz/selfie', tags=['Quiz'])
# async def selfie_analyze(file: UploadFile= File(...), db: Session = Depends(get_db)):
#     files = {"image":(file.filename, await file.read(), file.content_type)}

#     headers = {'X-API-KEY':  AILAB_API_KEY}

#     response = requests.post(AILAB_URL, files = files, headers= headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {'error': response.text}

@app.post('/quiz/submit', tags=['Quiz'])
async def submitting_quiz(
                  q1: str = Form(...),
                  q2: str = Form(...),
                  q3: str = Form(...),
                  q4: str = Form(...),
                  q5: str = Form(...),
                  q6: str = Form(...),
                  q7: str = Form(...),
                  q8: str = Form(...),
                  q9: str = Form(...),
                  q10: str = Form(...),
                  budget: int = Form, db: Session = Depends(get_db), file: Optional[UploadFile] = File(None)):
    selfie_result = {}
    if file is not None:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Please enter appropriate file(image)")

        files = {"image": (file.filename, await file.read(), file.content_type)}
        headers = {"X-API-KEY": AILAB_API_KEY}
        response = requests.post(AILAB_URL, files=files, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        selfie_result = response.json()

    answers = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q9": q9,
        "q10": q10,
    }


    quiz_result = utils.analyze_quiz(answers)
    complete_database = {'user_id': user_in_code, 'password': '1', 'skin_type': quiz_result['skin_type'], 'concerns': quiz_result['concerns'],
                         'preferences': quiz_result['preferences'], 'device_type': 'mobile'}
    print(complete_database)
    user_skin_property = models.Users(**complete_database)
    db.add(user_skin_property)
    db.commit()
    db.refresh(user_skin_property)
    if selfie_result:
        final_result_data = merge_results(selfie_result, quiz_result)
    else:
        final_result_data = quiz_result

    final = models.FinalResult(user_id=user_in_code,
                               selfie_result=selfie_result,
                               quiz_result=quiz_result,
                               final_result=final_result_data)

    db.add(final)
    db.commit()
    db.refresh(final)
    return {
        "final_result_id": final.id,
        "final_result": final_result_data,
        "message": "Conclusion has been successfully saved!"
    }