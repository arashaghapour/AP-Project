from typing import List

from pydantic_core.core_schema import none_schema


def search_in_database(user_in_code, products, searched_item, purchase, browsed):
    products_scores = {}    
    parameters_score = {'concers': 85, 'category': 75, 'views':63,'searched_box': 120,
                        'rating': 51, 'name': 110, 'brand': 105, 
                        'purchase': 41,'searched': 11, 'close': 31,
                        'most_view': 53}
    
    concers_labels = {'acne': 10,'combination': 12 ,'dullness': 14}
    category = {'cleanser': 10, 'moisturizer': 12, 'serum': 20}
    reasons_of_paramemters = {
        parameters_score['searched']: 'Your input matched a product\'s feature (like brand, category, or concern).',
        parameters_score['name']: 'Your search exactly matched the product name.',
        parameters_score['brand']: 'You searched for this brand.',
        parameters_score['category']: 'You searched for this product category.',
        parameters_score['concers']: 'You searched for this product concern (like acne, dullness, etc).',
        parameters_score['rating']: 'This product has a high average user rating.',
        parameters_score['views']: 'This product has been viewed frequently.',
        parameters_score['purchase']: 'You have purchased this product before.',
        parameters_score['close']: 'This product is similar to what you searched for.',
        parameters_score['browsed_befor']: 'You have browsed this product before.',
        parameters_score['most_view']: 'This is one of the most viewed products.',
        parameters_score['searched_box']: 'You typed this directly into the search box.'
    }

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
            exist = True
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

            for j in purchase:
                if j['user_id'] == user_in_code:
                    products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])
            

        elif i['brand'] == searched_item:
            exist = True
            for j in products:
                if j['brand'] == searched_item:
                    products_scores[j['product_id']].append(parameters_score['brand'])
        
        elif i['category'] == searched_item:
            exist = True
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
            exist = True
            for j, k in concers_labels.items():
                if abs(concers_labels[i['concers_targeted']] - k) < 3:
                    for l in products:
                        if l['concerns_targeted'] == j:
                            products_scores[i['product_id']].append(parameters_score['close'])

            for j in purchase:
                if j['user_id'] == user_in_code:
                    products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])

        else:
            pass
        if id_exist or exist:
            for id, scores_list in products_scores.items():
                if id in views:
                    scores_list.append(parameters_score['searched'] * views[id])
            parameters_score[views[0][0]].append(parameters_score['most_viewed'])

            for id, scores_list in products_scores.items():
                for item in products:
                    if item['product_id'] == id:
                        products_scores[item['product_id']].append(parameters_score['rating'])

            list_of_producs = []
            for id, scores_list in products_scores.items():
                list_of_producs.append([id, sum(scores_list)])

            list_of_producs.sort(key=lambda item: item[1])

            for item in range(len(list_of_producs)):
                first_item = None
                second_item = None
                for j in products:
                    if j['product_id'] == list_of_producs[item][0]:
                        first_item = j['product_id']
                    if j['product_id'] == list_of_producs[item + 1][0]:
                        second_item = j['product_id']

                for j in products_scores[first_item]:
                    if j not products_scores[second_item]:

                        list_of_producs[first_item].append()




