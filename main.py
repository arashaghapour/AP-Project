from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
import schemas, models
from database import Base, engine, SessionLocal, get_db
from typing import List, Optional
from search import serch_in_database
Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.post("/sign up", response_model=schemas.Cosmetics_input)
def create_user(user: schemas.Cosmetics_input, db: Session = Depends(get_db)):
    new_user = models.Cosmetics(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return Response(content='user created', status_code=201)
@app.post("/login")
def Review_user(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    user_review = db.query(models.Users).filter(
        models.Users.user_id == user.user_id,
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )
    else:
        return Response(content='you loged in soccesfully', status_code=200)

@app.post("/skin_care", response_model=schemas.UserCreate)
def create_skin_care_rows(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return 
@app.get("/search", response_model=schemas.SearchResponse)
def read_all_items(id: Optional[int] = None, 
    product_type: Optional[str] = None, skin_type: Optional[str] = None, sun_protection_factor: Optional[str] = None,
    country_of_origin: Optional[str] = None, volume: Optional[str] = None, finished: Optional[str] = None, search: Optional[str] = None,db: Session = Depends(get_db)):
    items_Cosmetics = db.query(models.Cosmetics).all()
    items_Skin_care = db.query(models.skin_care).all()
    dict_item = {'id': id,'product_type': product_type, 'skin_type': skin_type,
                 'sun_protection_factor': sun_protection_factor, 'country_of_origin': country_of_origin, 
                 'volume': volume, 'finished': finished, 'search': search}
    result_of_search = serch_in_database(items_Cosmetics, items_Skin_care, dict_item)
    if(result_of_search == 0):
        raise HTTPException(status_code=404, detail="The product you are looking for was not found.")
    else:
        return result_of_search