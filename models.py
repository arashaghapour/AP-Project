from sqlalchemy import Column, Date, Integer, JSON, String, Enum as SqllEnum
from sqlalchemy.ext.declarative import declarative_base
import database
from sqlalchemy import Date as SQLDate
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
    user_id = Column(int)
    skin_type = Column(SqllEnum(skin_type_allowed), nullable=False)
    concers = Column(JSON)
    preferences = Column(JSON)
    devise = Column(String)
    created_at = Column(SQLDate)
class products(Base):
    __tablename__ = "Products"
    product_id = Column(int)
    name = Column(String)
    brand = Column(String)
    category = Column(SqllEnum(category_allowed), nullable=False)
    skin_types = Column(JSON)
    concerns_targeted = Column(JSON)
    ingredients = Column(JSON)
    price = Column(int)
    rating = Column(float)

class Browsing_History(Base):
    __tablename__ = "Browsing_History"
    user_id = Column(int)
    product_id = Column(int)
    timestamp = Column(SQLDate)
    interaction_type = Column(SqllEnum(interaction_type_allowed), nullable=False)
class Purchase_History(Base):
    __tablename__ = 'Purchase_History'
    user_id = Column(int)
    product_id = Column(int)
    quantity = Column(int)
    timestamp = Column(SQLDate)
class Contextual_Signals(Base):
    __tablename__ = 'Contextual_Signals'
    user_id = Column(int)
    timestamp = Column(SQLDate)
    device_type = Column(str)
    season = Column(str)
    