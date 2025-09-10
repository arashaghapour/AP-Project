from fastapi import FastAPI, Depends, HTTPException, Response, File, UploadFile, Form, Request, Body
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
from .redis_client import redis_client
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates



Base.metadata.create_all(bind=engine)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
AILAB_API_KEY = "cmea2907w0001jo041hntvzpp"
AILAB_URL = "https://api.ailabtools.com/skin/analyze"
user_in_code = None
templates = Jinja2Templates(directory="./AP-Project/templates")
app.mount("/static", StaticFiles(directory="./AP-Project/static"), name="static")
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

@app.get("/signup", response_class=HTMLResponse)
def signup(request: Request):
    return templates.TemplateResponse("Sign-up.html", {"request": request})
@app.post("/Account/sign_up", tags=['Account'])
def create_user(db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
    user_data = {'user_name':username, 'password':password}
    user_data["password"] = pwd_context.hash(password)
    new_user = models.Users_for_sign_up(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    global user_in_code
    conn, cursor = read_database()
    user_id = find_user_id(cursor, username)
    user_in_code = user_id
    token_data = {"sub": str(user_in_code), "role": 'normal user'} 
    token = create_access_token(token_data)
    response = RedirectResponse(url="/shop", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.post("/Account/login", tags=['Account'])
def review_user(request: Request, db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
    global user_in_code
    
    conn, cursor = read_database()
    user_id = find_user_id(cursor, username)
    user_review = db.query(models.Users_for_sign_up).filter(models.Users_for_sign_up.user_name == username).first()
    admin_review = db.query(models.Admins).filter(models.Admins.user_name == username).first()
    if user_review and pwd_context.verify(password, user_review.password):
        user_in_code = user_review.user_id
        token = create_access_token({"sub": str(user_in_code), "role": "user"})
        response = RedirectResponse(url="/shop", status_code=302)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    else:
        return templates.TemplateResponse('login.html', {"request": request})
    if admin_review and pwd_context.verify(password, admin_review.password):
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

@app.get("/shop", response_class=HTMLResponse)
def shop(request: Request):
    return templates.TemplateResponse("shop.html", {"request": request})
@app.get("/product/all_products", tags=['Product'])
def get_all_products(db: Session = Depends(get_db)):

    # cache_key = 'all_products'
    # cached_products = redis_client.get(cache_key)
    # if cached_products:
    #     return json.loads(cached_products)
    
    # products = db.query(models.Products).all()
    # result = [schemas.ProductCreate.from_orm(p).dict() for p in products]

    # redis_client.set(cache_key, json.dumps(result), ex=600)
    # return result

    products = db.query(models.Products).all()
    return products


@app.post('/shop/add_to_cart', tags=['Shop'])
def add_to_cart(product: schemas.Purchase_input, db: Session = Depends(get_db)):
    global user_in_code
    print("Received body:", product.dict())
    db_product = db.query(models.Products).filter(models.Products.product_id == product.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if db_product.count < product.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    cart_item = models.Cart(user_id=user_in_code, product_id=product.product_id, quantity=product.quantity, name=db_product.name, brand=db_product.brand, category=db_product.category, price=db_product.price)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"message": "Product added to cart successfully :)"}


@app.post('/shop/checkout', tags=['Shop'])
def checkout(purchases: List[schemas.purchases_json] = Body(...), db: Session = Depends(get_db)):
    global user_in_code
    print('hello_world')

    for i in purchases:
        prod = db.query(models.Products).filter(models.Products.product_id == i.id).first()
        if prod and prod.count >= i.quantity:
            prod.count -= i.quantity
            new_pur = models.Purchase_History(
                user_id=user_in_code,
                product_id=i.id,
                quantity=i.quantity
            )
            db.add(new_pur)
        else:
           
            print(f"Product {i.id} not enough stock")

    db.commit()
    print('checkout done')
    return {"message": "Checkout successful. Purchase completed."}


    
@app.post("/search", response_model=schemas.Product_out2, tags=['Search'])
def search_input(search: schemas.Search, db: Session = Depends(get_db)):

    # cached_result = redis_client.get(cache_key)
    # if cached_result:
    #     return {'items': json.loads(cached_result)}
    

    # search_result = search_in_database(user_in_code, search.search)
    # browse_create = {}
    # submit_list = search_result['items'][:3]
    
    # for items in submit_list:
    #     browse_create['user_id'] = user_in_code
    #     browse_create['product_id'] = items['product_id']
    #     browse_create['interaction_type'] = 'view'
    #     new_browse = models.Browsing_History(**browse_create)
    #     db.add(new_browse)

    # db.commit()
    
    # result = [schemas.ProductCreate(**item).dict() for item in submit_list]

    # redis_client.set(cache_key, json.dumps(result), ex=300)

    # return {'items': result}


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




from . import models

@app.get("/routine", response_class=HTMLResponse)
def routine(request: Request):
    return templates.TemplateResponse("routine.html", {"request": request})

@app.post("/generate_routine", tags=['Routine'])
def generate_routine():
    return add_product(user_in_code)


@app.get('/quiz', response_class=HTMLResponse)
def quiz(request: Request):
    return templates.TemplateResponse('Quiz.html', {'request': request})
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
                  budget: int = Form(...), db: Session = Depends(get_db), file: Optional[UploadFile] = File(None)):
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
    if selfie_result:
        final_result_data = merge_results(selfie_result, quiz_result)
    else:
        final_result_data = quiz_result
        
    conn, cursor = read_database()
    cursor.execute('delete from Users where user_id = ?', (user_in_code, ))
    conn.commit()
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

@app.get("/detail", response_class=HTMLResponse)
def product_page(request: Request, id: int):
    return templates.TemplateResponse("product.html", {"request": request, "id": id})


@app.get("/product/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.product_id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
@app.get('/api/cart', response_class=HTMLResponse)
def cart_prod(request: Request):
    return templates.TemplateResponse("Cart.html", {"request": request})
@app.get('/get/cart', response_model=list[schemas.CartProduct1])
def get_cart_product(db: Session = Depends(get_db)):
    carts = db.query(models.Cart).all()
    result = []
    for c in carts:
        result.append(
            schemas.CartProduct1(
                product_id=c.product.product_id,
                name=c.product.name,
                brand=c.product.brand,
                category=c.product.category,
                price=float(c.product.price),
                quantity=c.quantity
            )
        )
    print(result)
    return result
