def choose_products(db, skin_type: str, concerns: list, preferences: list):
    steps = []

    if skin_type == "oily":
        product = db.query(models.Products).filter(models.Products.category == "cleanser", models.Products.tags.contains(["oil_control"])).first()
        steps.append({"description": "Cleanse", "product_name": product.name if product else "Foaming Cleanser"})
    elif skin_type == "dry":
        product = db.query(models.Products).filter(models.Products.category == "cleanser", models.Products.tags.contains(["hydrating"])).first()
        steps.append({"description": "Cleanse", "product_name": product.name if product else "Cream Cleanser"})
    else:
        steps.append({"description": "Cleanse", "product_name": "Gentle Cleanser"})

    if "acne" in concerns:
        product = db.query(models.Products).filter(models.Products.category == "serum", models.Products.ingredients.contains(["salicylic acid"])).first()
        steps.append({"description": "Serum", "product_name": product.name if product else "Anti-Acne Serum"})
    elif "wrinkles" in concerns:
        product = db.query(models.Products).filter(models.Products.category == "serum", models.Products.ingredients.contains(["retinol"])).first()
        steps.append({"description": "Serum", "product_name": product.name if product else "Anti-Aging Serum"})

    if "dry" in skin_type or "hydration" in concerns:
        product = db.query(models.Products).filter(models.Products.category == "moisturizer", models.Products.tags.contains(["hydrating"])).first()
        steps.append({"description": "Moisturize", "product_name": product.name if product else "Hydrating Moisturizer"})
    else:
        steps.append({"description": "Moisturize", "product_name": "Lightweight Moisturizer"})

    product = db.query(models.Products).filter(models.Products.category == "sunscreen").first()
    steps.append({"description": "Sunscreen", "product_name": product.name if product else "SPF 50"})

    return steps
