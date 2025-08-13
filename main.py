from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from . import schemas, models
from .database import Base, engine, get_db
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from .token_utils import create_access_token
from typing import List
from .search import search_in_database
from routine import create_product, create_routine
from schemas import ProductCreate, ProductOut, QuizInput, RoutinePlanOut
from utils import csv_to_list
from models import Product

Base.metadata.create_all(bind=engine)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

user_in_code = None

@app.post("/Account/sign_up", tags=['Account'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["password"] = pwd_context.hash(user.password)
    new_user = models.Users(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token_data = {"sub": str(user.user_id), "role": 'normal user'} 
    token = create_access_token(token_data)
    global user_in_code
    user_in_code = user_data['user_id']
    return {"message": "user created", "access_token": token, "token_type": "bearer"}


@app.post("/Account/login", tags=['Account'] , response_model=schemas.Token)
def review_user(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    global user_in_code
    user_review = db.query(models.Users).filter(models.Users.user_id == user.user_id).first()
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
        db.refresh(new_browse)
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
    products = db.query(models.Products).all()
    product_list = []
    purchase_list = []
    browsed = []
    for product in products:
        product_dict = {
            "product_id": product.product_id,
            "name": product.name,
            'brand': product.brand,
            'category': product.category,
            'skin_type': product.skin_types,
            'concerns_targeted': product.concerns_targeted,
            'ingredients': product.ingredients,
            "price": product.price,
            'rating': product.rating
        }
        product_list.append(product_dict)
    purchase = db.query(models.Purchase_History).all()
    for items in purchase:
        purchase_dict = {
            "user_id": items.user_id,
            "product_id": items.product_id,
            "quantity": items.quantity,
            'timestamp': items.timestamp            
        }
        purchase_list.append(purchase_dict)
    searches = db.query(models.Browsing_History).all()
    for items in searches:
        search_dict = {
            "user_id": items.user_id,
            "product_id": items.product_id,
            'timestamp': items.timestamp            
        }
        browsed.append(search_dict)
    users_dict = {}
    all_users = []
    users = db.query(models.Users).all()
    for user in users:
        users_dict = {
            'user_id': user.user_id,
            'skin_type': user.skin_type,
            'consers': user.concers
        }
        all_users.append(users_dict)

    search_result = search_in_database(user_in_code, product_list, search.search, purchase_list, browsed, all_users)
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
        db.commit()
        db.refresh(new_browse)
        count1 += 1
        if count1 == 3:
            break
    for items in search_result['items']:
        submit_list.append(items)
        count2 += 1
        if count2 == 3:
            break
    return {'items': submit_list}


@app.post("/add_admin", response_model=schemas.Admin)
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

@app.post('/quiz/submit',  tags=['Quiz'])
def submitting_quiz(data: schemas.QuizQuestions, db: Session = Depends(get_db)):
    answers = {
        "q1": data.q1.value,
        "q2": data.q2.value,
        "q3": data.q3.value,
        "q4": data.q4.value,
        "q5": data.q5.value,
        "q6": data.q6.value,
        "q7": data.q7.value,
        "q8": data.q8.value,
        "q9": data.q9.value,
        "q10": data.q10.value,
    }
    result = utils.analyze_quiz(answers)
    quiz = models.Quiz_result(
        user_id=data.user_id,
        skin_type=result["skin_type"],
        concerns=result["concerns"],
        preferences=result["preferences"]
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return {"quiz_id": quiz.quiz_id, "message": "Quiz submitted"}

@app.post("/products", response_model=ProductOut)
def add_product(data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, data)

@app.post("/generate_routine", response_model=list[RoutinePlanOut])
def generate_routine(data: QuizInput, db: Session = Depends(get_db)):
    plans = []
    for plan_name in ["Full Plan", "Hydration Plan", "Minimalist Plan"]:
        routine = create_routine(db, data.user_id, plan_name, data.skin_type, data.concerns, data.preferences, data.budget_range)
        plans.append(routine)
    return plans
