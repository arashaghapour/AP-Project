from fastapi import FastAPI, Depends, HTTPException, Response, File, UploadFile, Form
from sqlalchemy.orm import Session
from . import schemas, models, utils, questions
from .database import Base, engine, get_db
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from .token_utils import create_access_token
from typing import List, Optional
from .search import search_in_database
from .schemas import ProductCreate, Product_out1, QuizInput
from .models import Products
import requests
from .add_product_to_routin import add_product
import sqlite3
import random
############################
Base.metadata.create_all(bind=engine)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
AILAB_API_KEY = "cmea2907w0001jo041hntvzpp"
AILAB_URL = "https://api.ailabtools.com/skin/analyze"
user_in_code = None
@app.post('/generate random database', tags=['fill database'])
def add_product_to_database(db: Session = Depends(get_db)):
    Products = []
    for i in range(1000):
        len_of_skintype = random.randint(1, 5)
        len_of_concens = random.randint(1, 4)
        product = models.Products(
            name=f'product {i}',
            brand=random.choice(['iran', 'turkey', 'america', 'german', 'france']), 
            category=random.choice(['cleanser', 'serum',  'moisturizer']),            
            skin_types= list(set([random.choice(['oily', 'dry', 'sensitive', 'combination']) for i in range(len_of_skintype)])),
            concerns_targeted=list(set([random.choice(['acne', 'combination', 'dullness']) for i in range(len_of_concens)])),
            ingredients = ['string'],
            price=random.randrange(1000, 10000),
            rating = round(random.uniform(3.6, 5), 2),
            image_url = 'string',
            tags = ['string'],
            count = random.randint(10, 10000)
        )
        Products.append(product)
    db.bulk_save_objects(Products)
    db.commit()
############################

def read_database():
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    return conn, cursor


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
    global user_in_code
    conn, cursor = read_database()
    user_id = find_user_id(cursor, user.user_name)
    user_in_code = user_id
    token_data = {"sub": str(user_in_code), "role": 'normal user'} 
    token = create_access_token(token_data)
    return {"message": "user created", "access_token": token, "token_type": "bearer"}


@app.post("/Account/login", tags=['Account'] , response_model=schemas.Token)
def review_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    global user_in_code
    
    conn, cursor = read_database()
    user_id = find_user_id(cursor, user.user_name)
    user_review = db.query(models.Users_for_sign_up).filter(models.Users_for_sign_up.user_name == user.user_name).first()
    admin_review = db.query(models.Admins).filter(models.Admins.user_name == user.user_name).first()
    if user_review and pwd_context.verify(user.password, user_review.password):
        user_in_code = user_review.user_id
        token = create_access_token({"sub": str(user_in_code), "role": "user"})
        return {"access_token": token, "token_type": "bearer"}

    if admin_review and pwd_context.verify(user.password, admin_review.password):
        token = create_access_token({"sub": str(user.user_id), "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post("/product/add_product", response_model=schemas.ProductCreate, tags=['Product'])
def Product_Create(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    product_data = product.dict()
    new_product = models.Products(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return Response(content='product created', status_code=201)

@app.delete("/product/delete_product/{product_id}", response_model=List[schemas.ProductCreate], tags=['Product'])
def deleting_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return Response(content="Product deleted successfully", status_code=200)


@app.get("/product/all_products", response_model=List[schemas.ProductCreate], tags=['Product'])
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


@app.post('/shop/add_to_cart', tags=['Shop'])
def add_to_cart(product: schemas.Purchase_input, db: Session = Depends(get_db)):
    global user_in_code
    db_product = db.query(models.Products).filter(models.Products.product_id == product.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if db_product.stock < product.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    cart_item = models.Cart(user_id=user_in_code, product_id=product.product_id, quantity=product.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"message": "Product added to cart successfully :)"}


@app.post('/shop/checkout', tags=['Shop'])
def checkout(db: Session = Depends(get_db)):
    global user_in_code
    cart_items = db.query(models.Cart).filter(models.Cart.user_id == user_in_code).all()  
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    for item in cart_items:
        db_product = db.query(models.Products).filter(models.Products.product_id == item.product_id).first()
        if not db_product or db_product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} is out of stock or insufficient")
        
        db_product.stock -= item.quantity

        if db_product.stock == 0:
            db_product.Status = False
        # status_text = 'available' if db_product.Status else 'Out of stock'

        purchase = models.Purchase_History(
            user_id=user_in_code,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(purchase)

    db.query(models.Cart).filter(models.Cart.user_id == user_in_code).delete()
    db.commit()
    return {"message": "Checkout successful. Purchase completed."}

# @app.post("/shopping", response_model=schemas.PurchaseHistoryCreate, tags=['Shop'])
# def Shopping(product: schemas.Purchase_input, db: Session = Depends(get_db)):
#     global user_in_code
#     new_product_data = {'user_id': user_in_code, 'product_id': product.product_id, 'quantity': product.quantity}
#     new_product = models.Purchase_History(**new_product_data)
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     browse_create = {}
#     browse_create['user_id'] = user_in_code
#     browse_create['product_id'] = product.product_id
#     browse_create['interaction_type'] = 'view'
#     new_browse = models.Browsing_History(**browse_create)
#     db.add(new_browse)
#     db.commit()
#     db.refresh(new_browse)
#     return Response(content='You will be happy you choose us', status_code=201)


@app.post("/search", response_model=schemas.Product_out2, tags=['Search'])
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



from . import models

@app.post("/generate_routine", response_model=List[schemas.RoutineOut], tags=['Routine'])
def generate_routine():
    return add_product(user_in_code)





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
    # complete_database = {'user_id': user_in_code, 'password': '1', 'skin_type': quiz_result['skin_type'], 'concerns': quiz_result['concerns'],
    #                      'preferences': quiz_result['preferences'], 'device_type': 'mobile'}
    # print(complete_database)
    # user_skin_property = models.Users(**complete_database)
    # db.add(user_skin_property)
    # db.commit()
    # db.refresh(user_skin_property)
    if selfie_result:
        final_result_data = merge_results(selfie_result, quiz_result)
        # final = models.FinalResult(user_id = user_in_code, 
        #                        skin_type = final_result_data['skin_type'],
        #                        concerns = final_result_data['concerns'],
        #                        preferences = final_result_data['preferences'])
    else:
        final_result_data = quiz_result
        
    conn, cursor = read_database()
    cursor.execute('delete from Users where user_id = ?', (user_in_code, ))
    conn.commit()
    

    

    
    # final = models.FinalResult(user_id=user_in_code,
    #                            selfie_result=selfie_result,
    #                            quiz_result=quiz_result,
    #                            final_result=final_result_data)
    
    final = models.FinalResult(user_id = user_in_code, 
                               skin_type = final_result_data['skin_type'],
                               concerns = final_result_data['concerns'],
                               preferences = final_result_data['preferences'])
    db.add(final)
    db.commit()
    db.refresh(final)
    complete_database = {'user_id': user_in_code, 'password': '1', 'skin_type': final_result_data['skin_type'], 'concerns': final_result_data['concerns'],
                         'preferences': final_result_data['preferences'], 'device_type': 'mobile', 'budget_range': budget}
    user_skin_property = models.Users(**complete_database)
    db.add(user_skin_property)
    db.commit()
    db.refresh(user_skin_property)
    return {
        "final_result_id": final.id,
        "final_result": final_result_data,
        "message": "Conclusion has been successfully saved!"
    }