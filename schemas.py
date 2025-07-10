from pydantic import BaseModel
from typing import Optional, List
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
    category: CategoryAllowed
    skin_types: dict
    concerns_targeted: dict
    ingredients: dict
    price: int
    rating: float

class BrowsingHistoryCreate(BaseModel):
    user_id: int
    product_id: int
    timestamp: datetime
    interaction_type: InteractionTypeAllowed

class PurchaseHistoryCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    timestamp: datetime

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