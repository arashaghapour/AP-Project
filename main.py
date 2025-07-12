from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
import schemas, models
from database import Base, engine, get_db
from passlib.context import CryptContext
from token_utils import create_access_token
from dependencies import get_current_user, admin_required
from fastapi.security import HTTPBearer
from token_utils import create_access_token


Base.metadata.create_all(bind=engine)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

user_in_code = None

@app.post("/sign up", response_model=schemas.UserCreate)
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


@app.post("/login", response_model=schemas.Token)
def Review_user(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    global user_in_code
    user_review = db.query(models.Users).filter(models.Users.user_id == user.user_id).first()
    admin_review = db.query(models.Admins).filter(models.Admins.user_id == user.user_id).first()
    if user_review and pwd_context.verify(user.password, user_review.password):
        user_in_code = user_review['user_id']
        token = create_access_token({"sub": str(user.user_id), "role": "user"})
        return {"access_token": token, "token_type": "bearer"}

    if admin_review and pwd_context.verify(user.password, admin_review.password):
        token = create_access_token({"sub": str(user.user_id), "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post("/add_product", response_model=schemas.ProductCreate)
def Product_Create(product: schemas.ProductCreate, db: Session = Depends(get_db), admin=Depends(admin_required)):
    product_data = product.dict()
    new_product = models.Products(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return Response(content='product created', status_code=201)

@app.get("/all_products", response_model=schemas.ProductCreate)
def get_all_products(user=Depends(get_current_user), db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products

@app.post("/shopping", response_model=schemas.PurchaseHistoryCreate)
def Product_Create(product: schemas.Purchase_input, db: Session = Depends(get_db), user=Depends(get_current_user)):
    global user_in_code
    product_data = product.dict()
    new_product_data = {'user_id': user_in_code, 'product_id': product_data['product_id'], 'quantity': product_data['quantity']}
    new_product = models.Purchase_History(**new_product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return Response(content='You will be happy you chose us', status_code=201)


# @app.post("/add_admin", response_model=schemas.Admin)
# def create_user(user: schemas.Admin, db: Session = Depends(get_db)):
#     user_data = user.dict()
#     user_data["password"] = pwd_context.hash(user.password)
#     new_user = models.Admins(**user_data)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return Response(content='admin created', status_code=201)