from sqlalchemy import Column, Integer, DateTime, JSON, String, Enum as SqllEnum, Float, Numeric, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from .database import Base
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime


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
    wishlist = 'wishlist'
    cart = 'cart'


class Users_for_sign_up(Base):
    __tablename__ = "Users_sign_up"
    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Users(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    password = Column(String)
    skin_type = Column(SqllEnum(skin_type_allowed), nullable=False)
    concerns = Column(JSON)
    preferences = Column(JSON)
    device_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    budget_range = Column(Integer)
    browsing = relationship('Browsing_History', back_populates='user')
    quiz = relationship('final_result', back_populates='user2')
    purchasing = relationship('Purchase_History', back_populates='user2')  

    cart_items = relationship("Cart", back_populates="user")


class Admins(Base):
    __tablename__ = "Admins"
    user_id = Column(Integer, primary_key=True, index=True)
    password = Column(String, primary_key=True, index=True)


class Products(Base):
    __tablename__ = "Products"
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    category = Column(JSON, nullable=False)    
    skin_types = Column(JSON, nullable=False)        
    concerns_targeted = Column(JSON, nullable=False) 
    ingredients = Column(JSON, nullable=True) 
    price = Column(Numeric(10, 2), index=True)
    rating = Column(Float, index=True)
    image_url = Column(String, nullable=True, index=True)
    tags = Column(JSON, index=True)
    stock = Column(Integer, default=0, nullable=False)
    Status = Column(Boolean, default=True)

    purchases = relationship("Purchase_History", back_populates="product")
    cart_items = relationship("Cart", back_populates="product")

class Cart(Base):
    __tablename__ = "Cart"
    id = Column(Integer, primary_key=True, index= True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    product_id = Column(Integer, ForeignKey("Products.product_id"))
    quantity = Column(Integer, nullable=False)

    user = relationship("Users", back_populates="cart_items")
    product = relationship("Products", back_populates="cart_items")

class Quiz_result(Base):
    __tablename__ = "Quiz_result"
    quiz_id = Column(Integer, primary_key=True, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), index=True)
    skin_type = Column(SqllEnum(skin_type_allowed), nullable=False)
    concerns = Column(JSON)
    preferences = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # user2 = relationship('Users', back_populates='quiz')


class QuizQuestions(Base):
    __tablename__ = "Quiz_questions"
    user_id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, index=True)
    q1 = Column(String, index=True)
    q2 = Column(String, index=True)
    q3 = Column(String, index=True)
    q4 = Column(String, index=True)
    q5 = Column(String, index=True)
    q6 = Column(String, index=True)
    q7 = Column(String, index=True)
    q8 = Column(String, index=True)
    q9 = Column(String, index=True)
    q10 = Column(String, index=True)


# class Routine_Plans(Base):
#     __tablename__ = "Routine_Plans"
#     routine_id = Column(Integer, primary_key=True, unique=True, index=True)
#     user_id = Column(Integer, index=True)
#     plan_name = Column(String, index=True)
#     steps = Column(JSON, index=True)
#     created_at = Column(DateTime, default=datetime.utcnow, index=True)


class Browsing_History(Base):
    __tablename__ = "Browsing_History"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), index=True)
    product_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    interaction_type = Column(SqllEnum(interaction_type_allowed), nullable=False, index=True)

    user = relationship('Users', back_populates='browsing')
    # purchasing2 = relationship('Purchase_History', back_populates='browsing2')  


class Purchase_History(Base):
    __tablename__ = 'Purchase_History'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), index=True)
    product_id = Column(Integer, ForeignKey('Products.product_id'), index=True)
    quantity = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    user2 = relationship('Users', back_populates='purchasing')
    # browsing2 = relationship('Browsing_History', back_populates='purchasing2')
    product = relationship('Products', back_populates='purchases')


class Contextual_Signals(Base):
    __tablename__ = 'Contextual_Signals'
    user_id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    device_type = Column(String, index=True)
    season = Column(String, index=True)

class RoutinePlan(Base):
    __tablename__ = "routine_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    plan_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    steps = relationship("RoutineStep", back_populates="routine", cascade="all, delete-orphan")

class RoutineStep(Base):
    __tablename__ = "routine_steps"
    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routine_plans.id"))
    step_number = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=True)
    product_name = Column(String)
    price = Column(Float, nullable=True)
    routine = relationship("RoutinePlan", back_populates="steps")

class FinalResult(Base):
    __tablename__ = 'final_result'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    # selfie_result = Column(JSON, nullable=True)
    # quiz_result = Column(JSON, nullable=False)
    # final_result = Column(JSON, nullable=False)
    skin_type = Column(SqllEnum(skin_type_allowed), nullable=False)
    concerns = Column(JSON)
    preferences = Column(JSON)

    user2 = relationship('Users', back_populates='quiz')