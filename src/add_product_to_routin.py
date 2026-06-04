from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Products
from .search import search_in_database

def add_product(user_in_code):
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
        step1 = []
        for idx, step in enumerate(base_routine, start=1):
            pro = search_in_database(user_in_code, step)
            if not pro:
                continue
            products = pro['items'][:5]
            p_id = ''
            p_name = ''
            for prod in products:
                p_id += str(prod['product_id'])
                p_name += prod['name']
                p_id += ', '
                p_name += ', '
            per_steps = {'step_name': step, 'product_id': p_id, 'product_name': p_name, 'instructions': instructions[step]}
            step1.append(per_steps)
        routine['step'] = step1
        step1 = []
        routine_steps.append(routine)
    
    return routine_steps


