from sqlalchemy import Column, Integer,DateTime, JSON, String, Enum as SqllEnum, Float, func, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .database import Base
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import relationship

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
    name = Column(String)
    email = Column(String)
    password = Column(String)
    skin_type = Column(SqllEnum(skin_type_allowed), nullable=False)
    concers = Column(JSON)
    preferences = Column(JSON)
    device_type = Column(String)
    created_at = Column(DateTime)

    browsing = relationship('Browsing_History', back_populates='user')
    quiz = relationship('Quiz_result', back_populates= 'user2')
    # purchasing = relationship('Purchase_History', 'user2')


class Admins(Base):
    __tablename__  = "Admins"
    user_id = Column(Integer, primary_key=True)
    password = Column(String, primary_key=True)
    

class Products(Base):
    __tablename__ = "Products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    category = Column(JSON)
    skin_types = Column(JSON)
    concerns_targeted = Column(JSON)
    ingredients = Column(JSON)
    price = Column(Numeric)
    rating = Column(Float)
    image_url = Column(String, nullable= True)
    tags = Column(JSON)



class Quiz_result(Base):
    __tablename__ = "Quiz_result"
    quiz_id = Column(Integer, primary_key= True, unique= True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    skin_type = Column(SqllEnum(skin_type_allowed), nullable=False)
    concerns = Column(JSON)
    preferences = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)


    user2 = relationship('Users', back_populates= 'quiz')

# class QuizQuestions(Base):
#     __tablename__ = "Quiz_questions"
#     user_id = Column(Integer, primary_key=True, unique= True)
#     name= Column(String)
#     q1 =Column(String)
#     q2 =Column(String)
#     q3 =Column(String)
#     q4 =Column(String)
#     q5 =Column(String)
#     q6 =Column(String)
#     q7 =Column(String)
#     q8 =Column(String)
#     q9 =Column(String)
#     q10 =Column(String)

class Routine_Plans(Base):
    __tablename__ = "Routine_Plans"
    routine_id = Column(Integer, primary_key=True, unique= True)
    user_id = Column(Integer)
    plan_name = Column(String)
    steps = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Browsing_History(Base):
    __tablename__ = "Browsing_History"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    product_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    interaction_type = Column(SqllEnum(interaction_type_allowed), nullable=False)

    user = relationship('Users', back_populates= 'browsing')
    # purchasing2 = relationship('Purchase_History', 'browsing2')

class Purchase_History(Base):
    __tablename__ = 'Purchase_History'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # user_id = Column(Integer, ForeignKey('Users.user_id'))
    # product_id = Column(Integer, ForeignKey('Browsing_History.product_id'))
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # user2 = relationship('User', back_populates= 'purchasing')
    # browsing2 = relationship('Browsing_History', 'purchasing2')
    
    
class Contextual_Signals(Base):
    __tablename__ = 'Contextual_Signals'
    user_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    device_type = Column(String)
    season = Column(String)

