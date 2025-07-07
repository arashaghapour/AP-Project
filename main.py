from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models
from database import Base, engine, SessionLocal, get_db
from typing import List, Optional
from search import serch_in_database
Base.metadata.create_all(bind=engine)
app = FastAPI()
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
@app.get("/search", response_model=schemas.SearchResponse)
def read_all_items(id: Optional[int] = None, 
    brand: Optional[str] = None, spf: Optional[str] = None, skin_type: Optional[str] = None,
    country_of_origin: Optional[str] = None, everything_search: Optional[str] = None,db: Session = Depends(get_db)):
    items_Cosmetics = db.query(models.Cosmetics).all()
    items_Skin_care = db.query(models.skin_care).all()
    item = [id, brand, spf, skin_type, country_of_origin]
    everything_item = everything_search
    result_of_search = serch_in_database(items_Cosmetics, items_Skin_care, item, everything_item)
    if(result_of_search == 0):
        raise HTTPException(status_code=404, detail="The product you are looking for was not found.")
    else:
        return result_of_search