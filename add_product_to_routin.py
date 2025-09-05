from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Products
from .search import search_in_database

def choose_products(
    db: Session,
    skin_types: list,
    concerns: list,
    preferences: list,
    plan_name: str,
    budget_range: list
):
    routine_steps = []

    if plan_name == "Full Plan":
        base_routine = ["cleanser", "toner", "serum", "moisturizer", "sunscreen"]
    elif plan_name == "Hydration Plan":
        base_routine = ["cleanser", "serum", "moisturizer", "mask/sunscreen"]
    else: 
        base_routine = ["cleanser", "moisturizer", "sunscreen"]

    for idx, step in enumerate(base_routine, start=1):
        query = db.query(Products).filter(
            Products.price >= budget_range[0],
            Products.price <= budget_range[1]
        )
        query = query.filter(Products.category.contains([step]))

        if skin_types:
            skin_filters = [Products.skin_types.contains([st]) for st in skin_types]
            query = query.filter(or_(*skin_filters))

        if concerns:
            concern_filters = [Products.concerns_targeted.contains([c]) for c in concerns]
            query = query.filter(or_(*concern_filters))

        products = query.all()

        if products:
            for prod_idx, prod in enumerate(products, start=1):
                routine_steps.append({
                    "step_number": idx,
                    "step_name": f"Option {prod_idx}: Use {prod.name} for {step}",
                    "description": f"A {', '.join(prod.category)} suitable for {', '.join(prod.skin_types)} skin targeting {', '.join(prod.concerns_targeted)}.",
                    "product_id": prod.product_id,
                    "product_name": prod.name,
                    "price": float(prod.price)
                })
        else:
    
            routine_steps.append({
                "step_number": idx,
                "step_name": f"No suitable product found in budget {budget_range} for skin {', '.join(skin_types)} targeting {', '.join(concerns)}.",
                "description": "No product available",
                "product_id": None,
                "product_name": None,
                "price": None
            })

    # return routine_steps
def add_product(user_in_code, plan_name: str):
    routine_steps = []
    plans = ["Full Plan", "Hydration Plan", 'Minimalist Plan']
    instructions = {
        "cleanser": "Apply to wet face, massage gently, then rinse thoroughly.",
        "toner": "Apply to clean skin with a cotton pad or hands, let absorb.",
        "serum": "Apply a few drops to face and neck, gently pat until absorbed.",
        "moisturizer": "Apply evenly to face and neck to lock in hydration.",
        "sunscreen": "Apply generously on exposed skin 15 minutes before sun.",
        "mask/sunscreen": "Apply as a mask or thin layer for sun protection."
    }

    for plan_name in plans:
        if plan_name == "Full Plan":
            base_routine = ["cleanser", "toner", "serum", "moisturizer", "sunscreen"]
        elif plan_name == "Hydration Plan":
            base_routine = ["cleanser", "serum", "moisturizer", "mask/sunscreen"]
        else:
            base_routine = ["cleanser", "moisturizer", "sunscreen"]
        routine = {}
        routine = {'Plan_name': plan_name}
        step = []
        for idx, step in enumerate(base_routine, start=1):
            products = search_in_database(user_in_code, step)[:5]
            p_id = ''
            p_name = ''
            for prod in products:
                p_id += prod.product_id
                p_name += prod.name
                p_id += ', '
                p_name += ', '
            per_steps = {'step_name': step, 'product_id': p_id, 'product_name': p_name, 'instructions': instructions[step]}
            step.append(per_steps)
        routine['step'] = step
        step = []
        routine_steps.append(routine)


