def search_in_database(user_in_code, products, searched_item, purchase, browsed):
    products_scores = {}    
    parameters_score = {'concers': 85, 'category': 75, 'views':63,'searched_box': 120,
                        'rating': 51, 'name': 110, 'brand': 105, 
                        'purchase': 41,'searched': 11, 'close': 31,
                        'most_view': 53}
    
    concers_labels = {'acne': 10,'combination': 12 ,'dullness': 14}
    category = {'cleanser': 10, 'moisturizer': 12, 'serum': 20}
    skin_types = {'oily': 10, 'dry': 40, 'sensitive': 70, 'combination': 25}
    reasons_of_parameters = {
        parameters_score['searched']: 'This product has been viewed frequently.',
        parameters_score['name']: 'Your search exactly matched the product name.',
        parameters_score['brand']: 'You searched for this brand.',
        parameters_score['category']: 'You searched for this product category.',
        parameters_score['concers']: 'You searched for this product concern (like acne, dullness, etc).',
        parameters_score['rating']: 'This product has a high average user rating.',
        parameters_score['purchase']: 'You have purchased this product before.',
        parameters_score['close']: 'This product is similar to what you searched for.',
        parameters_score['most_view']: 'This is one of the most viewed products.',
        parameters_score['searched_box']: 'you exactly searched this.',
        parameters_score['views']: 'it because ite view.'
    }

    results = []
    views = {}
    exist = False
    id_exist = False
    for i in products:
        products_scores[i['product_id']] = []
    for i in browsed:
        if i['product_id'] in views:
            views[i['product_id']] += 1
        else:
            views[i['product_id']] = 1
    views = sorted(views.items(), key=lambda item: item[1], reverse=True)
    for i in products:
        try:
            if i['product_id'] == int(searched_item):
                id_exist = True
                products_scores[i['product_id']].append(parameters_score['searched_box'])
                for j in purchase:
                    if j['user_id'] == user_in_code:
                        products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])
                    break
        except:
            pass


        if i['name'] == searched_item:
            products_scores[i['product_id']].append(parameters_score['searched_box'])
            exist = True
            for j, k in concers_labels.items():
                if i['concerns_targeted'][0] in concers_labels.keys():
                    if abs(concers_labels[i['concerns_targeted'][0]] - k) < 3:
                        for l in products:
                            if l['concerns_targeted'] == j:
                                products_scores[i['product_id']].append(parameters_score['close'])
            
            
            for j, k in category.items():
                if i['category'][0] in category.keys():
                    if abs(category[i['category'][0]] - k) < 3:
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

        elif i['category'][0] == searched_item:
            exist = True
            for item in products:
                if item['category'] == searched_item:
                    products_scores[item['product_id']].append(parameters_score['searched_box'])
            for j, k in category.items():
                if i['category'][0] in category.keys():
                    if abs(category[i['category'][0]] - k) < 3:
                        for l in products:
                            if l['category'] == j:
                                products_scores[i['product_id']].append(parameters_score['close'])

            for j in purchase:
                if j['user_id'] == user_in_code:
                    products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])

        elif i['skin_type'][0] == searched_item:
            # add skin type from username
            exist = True
            for j, k in concers_labels.items():
                if i['concerns_targeted'][0] in concers_labels.keys():
                    if abs(concers_labels[i['concerns_targeted'][0]] - k) < 3:
                        for l in products:
                            if l['concerns_targeted'] == j:
                                products_scores[i['product_id']].append(parameters_score['close'])

            for j, k in skin_types.items():
                if i['concerns_targeted'][0] in skin_types.keys():
                    if abs(skin_types[i['skin_type'][0]] - k) < 30:
                        for l in products:
                            if l['skin_type'] == j:
                                products_scores[i['product_id']].append(parameters_score['close'])
            for j in purchase:
                if j['user_id'] == user_in_code:
                    products_scores[j['product_id']].append(j['quantity'] * parameters_score['purchase'])

        if id_exist or exist:
            for id, scores_list in products_scores.items():
                for item_id, view in views:
                    if item_id == id:
                        scores_list.append(parameters_score['searched'] * view)

            products_scores[views[0][0]].append(parameters_score['most_view'])

            for id, scores_list in products_scores.items():
                for item in products:
                    if item['product_id'] == id:
                        products_scores[item['product_id']].append(parameters_score['rating'])

            list_of_products = []
            for id, scores_list in products_scores.items():
                list_of_products.append([id, sum(scores_list)])

            list_of_products.sort(key=lambda item: item[1])
            if len(list_of_products) > 1:
                for item in range(len(list_of_products) - 1):
                    first_item = None
                    second_item = None
                    for j in products:
                        if j['product_id'] == list_of_products[item][0]:
                            first_item = j['product_id']
                        if j['product_id'] == list_of_products[item + 1][0]:
                            second_item = j['product_id']

                    for j in products_scores[first_item]:
                        if j not  in products_scores[second_item]:
                            if j % parameters_score['name'] == 0:
                                list_of_products[item].append(reasons_of_parameters[j])
                            elif j % parameters_score['brand'] == 0:
                                list_of_products[item].append(reasons_of_parameters[j])
                            elif j % parameters_score['category'] == 0:
                                list_of_products[item].append(reasons_of_parameters[j])
                            elif j % parameters_score['most_view'] == 0:
                                list_of_products[item].append(reasons_of_parameters[j])
                            elif j % parameters_score['rating'] == 0:
                                list_of_products[item].append(reasons_of_parameters[j])
                            elif j % parameters_score['purchase'] == 0:
                                list_of_products[item].append(reasons_of_parameters[j])
                            else:
                                list_of_products[item].append(reasons_of_parameters[j])

                        for parameter, value in parameters_score.items():
                            if value == max(products_scores[list_of_products[-1][0]]) or max(products_scores[list_of_products[-1][0]]) % value == 0:
                                list_of_products[-1].append(reasons_of_parameters[value])
            else:
                for parameter, value in parameters_score.items():
                    if value == max(products_scores[list_of_products[-1][0]]) or max(products_scores[list_of_products[-1][0]]) % value == 0:
                        list_of_products[-1].append(reasons_of_parameters[value])
            for item in list_of_products:
                for item_list_search in products:
                    if item_list_search['product_id'] == item[0]:
                        item_of_product = {
                            'product_id': item_list_search['product_id'],
                            'name': item_list_search['name'],
                            'brand': item_list_search['brand'],
                            'category': item_list_search['category'],
                            'skin_type': item_list_search['skin_type'],
                            'concerns_targeted': item_list_search['concerns_targeted'],
                            'ingredients': item_list_search['ingredients'],
                            'price': item_list_search['price'],
                            'rating': item_list_search['rating'],
                            'response': item[2]
                        }
                        results.append(item_of_product)
                        break
            return {'items': results}
        # add view to products
        else:
            return {'items': [{'product_id': user_in_code,
                               'name': 'None',
                               'brand': 'None',
                               'category': ['None'],
                               'skin_types': ['None'],
                               'concerns_targeted': ['None'],
                               'ingredients': ['None'],
                               'price': 0,
                               'rating': 0.0,
                               'response': 'we dont have product for your search.'}]}


