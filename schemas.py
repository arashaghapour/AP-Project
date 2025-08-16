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

class Q1Options(str, Enum):
    dry = "dry"
    smooth = "smooth"
    oily = "oily"
    combination = "combination"

class Q2Options(str, Enum):
    yes = "yes"
    sometimes = "sometimes"
    rarely = "rarely"
    t_zone_only = "T-zone only"

class Q3Options(str, Enum):
    very_sensitive = "very_sensitive"
    mildly = "mildly"
    not_sensitive = "not_sensitive"
    not_sure = "not_sure"

class Q4Options(str, Enum):
    yes = "yes"
    no = "no"

class Q5Options(str, Enum):
    yes = "yes"
    no = "no"

class Q6Options(str, Enum):
    yes = "yes"
    no = "no"

class Q7Options(str, Enum):
    under_5min = "under_5min"
    between_5_10 = "5-10min"
    over_15 = "15min_plus"

class Q8Options(str, Enum):
    minimal = "minimal"
    moderate = "moderate"
    full = "full"

class Q9Options(str, Enum):
    natural = "natural"
    clinical = "clinical"

class Q10Options(str, Enum):
    daily = "daily"
    weekly = "weekly"
    rarely = "rarely"
    never = "never"

class UserCreate(BaseModel):
    user_id: int
    password: str
    skin_type: str
    concers: List[str]
    preferences: List[str]
    device_type: str
    created_at: datetime


class ProductCreate(BaseModel):
    product_id: int
    name: str
    brand: str
    category: List[str]
    skin_types: List[str]
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

class QuizQuestions(BaseModel):
    # user_id: int
    # # name: str
    # answers: Dict[str, str]
    # # q1 :str
    # # q2 :str
    # # q3 :str
    # # q4 :str
    # # q5 :str
    # # q6 :str
    # # q7 :str
    # # q8 :str
    # # q9 :str
    # # q10 :str
    user_id: int
    q1: Q1Options
    q2: Q2Options
    q3: Q3Options
    q4: Q4Options
    q5: Q5Options
    q6: Q6Options
    q7: Q7Options
    q8: Q8Options
    q9: Q9Options
    q10: Q10Options
    
class QuizResult(BaseModel):
    # quiz_id :int
    user_id :int
    skin_type :SkinTypeAllowed
    concerns :List[str]
    preferences :List[str]
    timestamp :datetime

class QuizInput(BaseModel):
    user_id: Optional[int] = None
    skin_type: str
    concerns: List[str] = Field(default_factory=list)
    preferences: List[str] = Field(default_factory=list)
    budget_range: List[float] = Field(default_factory=lambda: [0, 999])

class RoutineStepOut(BaseModel):
    step_name: str
    product_id: Optional[int]
    product_name: Optional[str]

class RoutinePlanOut(BaseModel):
    id: int
    user_id: Optional[int]
    plan_name: str
    created_at: datetime
    steps: List[RoutineStepOut]

    class Config:
        from_attributes = True