from sqlalchemy import Column, Integer,DateTime, JSON, String, Enum as SqllEnum, Float, func
from sqlalchemy.ext.declarative import declarative_base
import database
from datetime import datetime
Base = database.Base
from enum import Enum
class skin_type_allowed(str, Enum):
    oily = 'oily'
    dry = 'dry'
    sensitive = 'sensitive'
    combination = 'combination'
class category_allowed(str, Enum):
    cleanser = 'cleanser'
    serum = 'serum'
    moisturizer = 'moisturizer'
class interaction_type_allowed(str, Enum):
    view = 'view'
    like = 'like'
    wishlist =  'wishlist'
    cart = 'cart'
class Users(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    password = Column(String, primary_key=True)
    skin_type = Column(SqllEnum(skin_type_allowed), nullable=False)
    concers = Column(JSON)
    preferences = Column(JSON)
    devise = Column(String)
    created_at = Column(DateTime)

class Admins(Base):
    __tablename__ = "Admins"
    user_id = Column(Integer, primary_key=True)
    password = Column(String, primary_key=True)
class Products(Base):
    __tablename__ = "Products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    category = Column(SqllEnum(category_allowed), nullable=False)
    skin_types = Column(JSON)
    concerns_targeted = Column(JSON)
    ingredients = Column(JSON)
    price = Column(Integer)
    rating = Column(Float)



class Browsing_History(Base):
    __tablename__ = "Browsing_History"
    user_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    timestamp = Column(DateTime)
    interaction_type = Column(SqllEnum(interaction_type_allowed), nullable=False)
class Purchase_History(Base):
    __tablename__ = 'Purchase_History'
    user_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
class Contextual_Signals(Base):
    __tablename__ = 'Contextual_Signals'
    user_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    device_type = Column(String)
    season = Column(String)
    