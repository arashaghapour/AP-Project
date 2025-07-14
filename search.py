from typing import List
def serch_in_database(user_in_code, products, searched_item, purchase, browsed):
    products_scores = {}    
    parameters_score = {'concers': 85, 'category': 75, 'views':63,
                        'rating': 51, 'name': 110, 'brand': 105, 
                        'purchase': 40,'searched':40, 'close': 30,
                        'browsed_befor': 30, 'purchase': 32}
    
    concers_labels = {'acne': 10,'combination': 12 ,'dullness': 14}
    category = {'cleanser': 10, 'moisturizer': 12, 'serum': 20}
    reasons_of_paramemters = {parameters_score['searched']: 'your input in properties of product',
                              parameters_score['name']: 'What you searched for was in the product category.', 
                              parameters_score['brand']: 'What you searched for was the product brand.', 
                              parameters_score['view']: 'What you searched for had a high number of views.', 
                              parameters_score['rating']: 'What you searched for had a high rating.'}
    
    results = []
    
    for i in products:
        products_scores[i['product_id']] = []
    for i in products:
        try:
            if i['product_id'] == int(searched_item):
                dict1 = i.copy()
                dict1['description'] = 'What you searched for was the id of product'
                return List[dict1]
        except:
            pass
        
        
        if i['name'] == searched_item:
            products_scores[i['product_id']].append(parameters_score['name'])
            for j, k in concers_labels.items():
                if abs(concers_labels[i['concers_targeted']] - k) < 3:
                    for l in products:
                        if l['concerns_targeted'] == j:
                            products_scores[i['product_id']].append(parameters_score['close'])
            
            
            for j, k in category.items():
                if abs(category[i['category']] - k) < 3:
                    for l in products:
                        if l['category'] == j:
                            products_scores[i['product_id']].append(parameters_score['close'])
            
            
            # for j in browsed:
            #     if j['user_id'] == user_in_code:
            #         products_scores[j['product_id']].append(parameters_score['browsed_befor'])
            
            
            for j in purchase:
                if j['user_id'] == user_in_code:
                    products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])
            
            
            
            
            
        elif i['brand'] == searched_item:
            for j in products:
                if j 
        
        elif i[''] == searched_item:
            products_scores[i['product_id']].append(parameters_score['brand'])
        