from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import schemas, models
from database import Base, engine, SessionLocal, get_db
from typing import List, Optional
from search import serch_in_database
from passlib.context import CryptContext
from jose import jwt
from token_utils import create_access_token
from dependencies import get_current_user, admin_required


Base.metadata.create_all(bind=engine)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/sign up", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["password"] = pwd_context.hash(user.password)
    new_user = models.Users(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token_data = {"sub": user.user_id, "role": 'normal user'}  # فرض کن user.role مثل "admin" یا "user"
    token = create_access_token(token_data)

    return {"message": "user created", "access_token": token, "token_type": "bearer"}


@app.post("/login", response_model=schemas.Token)
def Review_user(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    admin = False
    user_review = db.query(models.Users).filter(models.Users.user_id == user.user_id).first()
    admin_review = db.query(models.Admins).filter(models.Admins.user_id == user.user_id).first()
    if user_review:
        if pwd_context.verify(user.password, user_review.password):
            token_data = {"sub": user.user_id, "role": 'normal user'}  
            token = create_access_token(token_data)
            return {"message": "welcome user", "access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        if pwd_context.verify(user.password, admin_review.password):
            token_data = {"sub": user.user_id, "role": 'admin'}  
            token = create_access_token(token_data)
            return {"message": "welcome admin", "access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    
@app.post("/add_product", response_model=schemas.ProductCreate)
def Product_Create(product: schemas.ProductCreate, db: Session = Depends(get_db), create_user: models.Products = Depends(admin_required)):
    product_data = product.dict()
    new_product = models.Products(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return Response(content='product created', status_code=201)

# @app.post("/add_admin", response_model=schemas.Admin)
# def create_user(user: schemas.Admin, db: Session = Depends(get_db)):
#     user_data = user.dict()
#     user_data["password"] = pwd_context.hash(user.password)
#     new_user = models.Admins(**user_data)
#     db.add(new_user)
#     db.commit()string
#     db.refresh(new_user)
#     return Response(content='admin created', status_code=201)