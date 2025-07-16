from typing import List
def serch_in_database(user_in_code, products, searched_item, purchase, browsed):
    products_scores = {}    
    parameters_score = {'concers': 85, 'category': 75, 'views':63,'searched_box': 120,
                        'rating': 51, 'name': 110, 'brand': 105, 
                        'purchase': 40,'searched':40, 'close': 30,
                        'browsed_befor': 30, 'purchase': 32, 'most_view': 53}
    
    concers_labels = {'acne': 10,'combination': 12 ,'dullness': 14}
    category = {'cleanser': 10, 'moisturizer': 12, 'serum': 20}
    reasons_of_paramemters = {parameters_score['searched']: 'your input in properties of product',
                              parameters_score['name']: 'What you searched for was in the product category.', 
                              parameters_score['brand']: 'What you searched for was the product brand.', 
                              parameters_score['view']: 'What you searched for had a high number of views.', 
                              parameters_score['rating']: 'What you searched for had a high rating.'}
    
    results = []
    views = {}
    exist = False
    id_exist = False
    for i in products:
        products_scores[i['product_id']] = []
    for i in browsed:
        if i['product_id'] in views:
            views['product_id'] += 1
        else:
            views['product_id'] = 1
    views = sorted(views.items(), key=lambda item: item[1])
    for i in products:
        try:
            if i['product_id'] == int(searched_item):
                id_exist = True
                
                
                for j in purchase:
                    if j['user_id'] == user_in_code:
                        products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])
            
        except:
            pass
        
        
        if i['name'] == searched_item:
            products_scores[i['product_id']].append(parameters_score['searched_box'])
            exit = True
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
            exit = True
            for j in products:
                if j['brand'] == searched_item:
                    products_scores[j['product_id']].append(parameters_score['brand'])
        
        elif i['category'] == searched_item:
            exit = True
            for item in products:
                if item['category'] == searched_item:
                    products_scores[item['product_id']].append(parameters_score['searched_box'])
            for j, k in category.items():
                if abs(category[i['category']] - k) < 3:
                    for l in products:
                        if l['category'] == j:
                            products_scores[i['product_id']].append(parameters_score['close'])
            

            for j in purchase:
                if j['user_id'] == user_in_code:
                    products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])
        
        
        elif i['skin_type'] == searched_item:
            exit = True
            for j, k in concers_labels.items():
                if abs(concers_labels[i['concers_targeted']] - k) < 3:
                    for l in products:
                        if l['concerns_targeted'] == j:
                            products_scores[i['product_id']].append(parameters_score['close'])
            

            for j in purchase:
                if j['user_id'] == user_in_code:
                    products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])
                    
                    
        else:
            return None
        if id_exist:
            for id, list_scores in products_scores:
                if id in views:
                    list_scores.append(parameters_score['browsed_befor'] * views['id'])
