from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date
from enum import Enum
from datetime import datetime


class SkinTypeAllowed(str, Enum):
    oily = 'oily'
    dry = 'dry'
    sensitive = 'sensitive'
    combination = 'combination'


class concersAllowed(str, Enum):
    acne = 'acne'
    dullness = 'dullness'
    
class CategoryAllowed(str, Enum):
    cleanser = 'cleanser'
    serum = 'serum'
    moisturizer = 'moisturizer'


class InteractionTypeAllowed(str, Enum):
    view = 'view'
    like = 'like'
    wishlist = 'wishlist'
    cart = 'cart'


class UserCreate(BaseModel):
    user_id: int
    password: str
    skin_type: SkinTypeAllowed
    concers: dict
    preferences: dict
    devise: str
    created_at: datetime


class ProductCreate(BaseModel):
    product_id: int
    name: str
    brand: str
    category: List[CategoryAllowed]
    skin_types: List[SkinTypeAllowed]
    concerns_targeted: List[str]
    ingredients: List[str]
    price: int
    rating: float

class Product_out1(BaseModel):
    product_id: int
    name: str
    brand: str
    category: List[str]
    skin_type: List[str]
    concerns_targeted: List[str]
    ingredients: List[str]
    price: int
    rating: float
    response: str


class Product_out2(BaseModel):
    items: List[Product_out1]


class BrowsingHistoryCreate(BaseModel):
    user_id: int
    product_id: int
    timestamp: datetime
    interaction_type: InteractionTypeAllowed


class PurchaseHistoryCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Purchase_input(BaseModel):
    product_id: int
    quantity: int
class ContextualSignalCreate(BaseModel):
    user_id: int
    timestamp: datetime
    device_type: str
    season: str
    
    
class LoginRequest(BaseModel):
    user_id: int
    password: str


class Admin(BaseModel):
    user_id: int
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class Search(BaseModel):
    search: str