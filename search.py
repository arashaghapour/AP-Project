from typing import List
def serch_in_database(products, searched_item):
    products_scores = {}
    parameters_score = {'seaeched': 90, 'concers': 85, 'category': 75, 'views':65,
                        'rating': 55, 'name': 110, 'brand': 105, 'purchase': 40, 'close': 30}
    concers_labels = {'acne': 10, 'dullness': 12}
    category = {'cleanser': 10, 'moisturizer': 12, 'serum': 20}
    reasons_of_paramemters = {
                              parameters_score['searched']: 'your input in properties of product',
                              parameters_score['name']: 'What you searched for was in the product category.', 
                              parameters_score['brand']: 'What you searched for was the product brand.', 
                              parameters_score['view']: 'What you searched for had a high number of views.', 
                              parameters_score['rating']: 'What you searched for had a high rating.'}
    for i in products:
        i = i.__dict__
        products_scores[i['product_id']] = []
    for i in products:
        i = i.__dict__
        try:
            if i['product_id'] == int(searched_item):
                i['description'] = 'What you searched for was the id of product'
                return List[i]
        except:
            pass
        
        for j in i:
            if j == searched_item:
                products_scores[i['product_id']].append(parameters_score['seaeched'])
        if i['name'] == searched_item:
            products_scores[i['product_id']].append(parameters_score['name'])
            
    