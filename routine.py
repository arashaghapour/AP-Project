from sqlalchemy.orm import Session
from models import Product, RoutinePlan, RoutineStep
from utils import csv_to_list, list_to_csv
from schemas import ProductCreate
from typing import List, Optional, Tuple

ROUTINE_TEMPLATES = {
    "Full Plan": ["Cleanser", "Toner", "Serum", "Moisturizer", "Sunscreen"],
    "Hydration Plan": ["Cleanser", "Serum", "Moisturizer"],
    "Minimalist Plan": ["Cleanser", "Moisturizer", "Sunscreen"],
}

def create_product(db: Session, payload: ProductCreate) -> Product:
    product = Product(
        name=payload.name,
        brand=payload.brand,
        category=payload.category,
        price=payload.price,
        skin_types_csv=list_to_csv(payload.skin_types) or "all",
        concerns_targeted_csv=list_to_csv(payload.concerns_targeted),
        preferences_csv=list_to_csv(payload.preferences),
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def list_products(
    db: Session,
    category: Optional[str] = None,
    price_range: Optional[Tuple[float, float]] = None
) -> List[Product]:
    query = db.query(Product)
    if category:
        query = query.filter(Product.category.ilike(category))
    if price_range:
        lo, hi = price_range
        query = query.filter(Product.price >= lo, Product.price <= hi)
    return query.all()

def score_product(p: Product, skin_type: str, concerns: List[str], preferences: List[str]) -> float:
    score = 0
    if "all" in csv_to_list(p.skin_types_csv) or skin_type.lower() in csv_to_list(p.skin_types_csv):
        score += 2
    if set(concerns) & set(csv_to_list(p.concerns_targeted_csv)):
        score += 1
    if set(preferences) & set(csv_to_list(p.preferences_csv)):
        score += 0.5
    return score

def select_best_product(db: Session, category: str, skin_type: str, concerns: List[str], preferences: List[str], budget: List[float]) -> Optional[Product]:
    lo, hi = budget
    products = list_products(db, category=category, price_range=(lo, hi))
    if not products:
        return None
    products.sort(key=lambda p: score_product(p, skin_type, concerns, preferences), reverse=True)
    return products[0]

def create_routine(db: Session, user_id: Optional[int], plan_name: str, skin_type: str, concerns: List[str], preferences: List[str], budget: List[float]) -> RoutinePlan:
    routine = RoutinePlan(user_id=user_id, plan_name=plan_name)
    db.add(routine)
    db.flush()

    for step in ROUTINE_TEMPLATES[plan_name]:
        product = select_best_product(db, step, skin_type, concerns, preferences, budget)
        db.add(RoutineStep(
            routine_id=routine.id,
            step_name=step,
            product_id=product.id if product else None,
            product_name=product.name if product else None
        ))
    db.commit()
    db.refresh(routine)
    return routine
