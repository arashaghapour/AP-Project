from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import schemas, models
from database import Base, engine, SessionLocal, get_db
from typing import List, Optional
from search import serch_in_database
from passlib.context import CryptContext
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
    return Response(content='user created', status_code=201)
@app.post("/login", response_model=schemas.LoginRequest)
def Review_user(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    admin = False
    user_review = db.query(models.Users).filter(models.Users.user_id == user.user_id).first()
    admin_review = db.query(models.Admins).filter(models.Admins.user_id == user.user_id).first()
    if user_review:
        if pwd_context.verify(user.password, user_review.password):
            return Response(content='welcome to our site')
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        if pwd_context.verify(user.password, admin_review.password):
            return Response(content='welcome admin')
        else:
            raise HTTPException(status_code=404, detail="User not found")
    

    
@app.post("/add_admin", response_model=schemas.Admin)
def create_user(user: schemas.Admin, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["password"] = pwd_context.hash(user.password)
    new_user = models.Admins(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return Response(content='admin created', status_code=201)