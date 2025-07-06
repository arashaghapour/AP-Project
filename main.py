from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas, models
from database import Base, engine, SessionLocal
app = FastAPI()
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/Cosmetics", response_model=schemas.Cosmetics_input)
def create_Cosmetics_rows(user: schemas.Cosmetics_input, db: Session = Depends(get_db)):
    new_user = models.Cosmetics(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@app.post("/skin_care", response_model=schemas.skin_care_input)
def create_skin_care_rows(user: schemas.skin_care_input, db: Session = Depends(get_db)):
    new_user = models.skin_care(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user