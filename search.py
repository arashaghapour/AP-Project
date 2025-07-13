from typing import List
def serch_in_database(products, searched_item):
    products_scores = {}
    parameters_score = {'seaeched': 100, 'concers': 85, 'category': 75, 'views':65, 'rating': 55}
    concers_labels = {'acne': 10, 'dullness': 12}
    category = {'cleanser': 10, 'moisturizer': 12, 'serum': 20}
    for i in products:
        i = i.__dict__
        products_scores[i['product_id']] = 0
    for i in products:
        i = i.__dict__
        try:
            if(i['product_id'] == int(searched_item)):
                pass
        except:
            pass
    