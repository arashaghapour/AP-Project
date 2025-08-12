import sqlite3 as lite
def search_in_database(user_in_code, products, searched_item, purchase, browsed, users):
    products_scores = {}
    parameters_score = {'concerns': 85, 'category': 75, 'views':63,'searched_box': 120,
                        'rating': 51, 'name': 110, 'brand': 105, 
                        'purchase': 41,'searched': 13, 'close': 31,
                        'most_view': 53, 'skin_type': 90}
    
    concerns_labels = {'acne': 10,'combination': 12 ,'dullness': 14}
    category = {'cleanser': 10, 'moisturizer': 12, 'serum': 20}
    skin_types = {'oily': 10, 'dry': 40, 'sensitive': 70, 'combination': 25}
    reasons_of_parameters = {
        parameters_score['searched']: 'This product has been viewed frequently.',
        parameters_score['name']: 'Your search exactly matched the product name.',
        parameters_score['brand']: 'You searched for this brand.',
        parameters_score['category']: 'You searched for this product category.',
        parameters_score['concerns']: 'You searched for this product concern (like acne, dullness, etc).',
        parameters_score['rating']: 'This product has a high average user rating.',
        parameters_score['purchase']: 'You have purchased this product before.',
        parameters_score['close']: 'This product is similar to what you searched for.',
        parameters_score['most_view']: 'This is one of the most viewed products.',
        parameters_score['searched_box']: 'you exactly searched this.',
        parameters_score['views']: 'it because ite view.',
        parameters_score['skin_type']: 'it because you have same skin types.'
    }

    conn = lite.connect('./AP-Project/database.db')
    cursor = conn.cursor()
    results = []
    views = {}
    exist = False
    id_exist = False
    for i in products:
        products_scores[i['product_id']] = []
    views = users_views(cursor)
    views = sorted(views.items(), key=lambda item: item[1], reverse=True)
    for i in products:
        try:
            if i['product_id'] == int(searched_item):
                id_exist = True
                products_scores[i['product_id']].append(parameters_score['searched_box'])
        except:
            pass
        if i['name'] == searched_item:
            products_scores[i['product_id']].append(parameters_score['searched_box'])
            exist = True

        elif i['brand'] == searched_item:
            exist = True
            products_scores[i['product_id']].append(parameters_score['brand'])

        elif i['concerns_targeted'][0] == searched_item:
            exist = True
            products_scores[i['product_id']].append(parameters_score['concerns'])

        elif i['category'][0] == searched_item:
            exist = True
            products_scores[i['product_id']].append(parameters_score['searched_box'])

        elif i['skin_type'][0] == searched_item:
            exist = True
            products_scores[i['product_id']].append(parameters_score['searched_box'])
    user_row_in_database = user_information(cursor, user_in_code)
    skin_product = s_product(cursor, user_row_in_database[2])
    purchase_in_database = purchase_da(cursor, user_in_code)
    if skin_product:
        for i in skin_product:
            products_scores[i[0]].append(parameters_score['skin_type'])
    if purchase_in_database:
        for i in purchase_in_database:
            products_scores[i[2]].append(i[3] * parameters_score['purchase'])
    list_of_products = []
    for id, scores_list in products_scores.items():
        list_of_products.append([id, sum(scores_list)])
    list_of_products.sort(key=lambda item: item[1], reverse=True)

    if id_exist or exist:
        for id, scores_list in products_scores.items():
            if id in views:
                scores_list.append(views[id] * parameters_score['searched'])

        for i, j in views.items():
            products_scores[i].append(parameters_score['most_view'])
            break

        for id, scores_list in products_scores.items():
            for item in products:
                if item['product_id'] == id:
                    products_scores[item['product_id']].append(parameters_score['rating'])
                    break
        list_of_products = []
        for id, scores_list in products_scores.items():
            list_of_products.append([id, sum(scores_list)])
        list_of_products.sort(key=lambda item: item[1], reverse=True)


    # first_product = product_information(cursor, list_of_products[0][0])
    # for product in products:
    #     if product['product_id'] == first_product:
    #         for parameters, values in skin_types.items():
    #             if abs(values - skin_types[product['skin_type'][0]]) < 30:
    #                 for l in products:
    #                     if l['skin_type'] == parameters:
    #                         products_scores[l['product_id']].append(parameters_score['close'])
    #
    #         for parameters, values in category.items():
    #             if abs(values - category[product['category'][0]]) < 3:
    #                 for l in products:
    #                     if l['category'] == parameters:
    #                         products_scores[l['product_id']].append(parameters_score['close'])
    #         break
    # nearest products to most score product with date


    #     if len(list_of_products) > 1:
    #         for item in range(len(list_of_products) - 1):
    #             first_item = list_of_products[item][0]
    #             second_item = list_of_products[item + 1][0]
    #             for score in products_scores[first_item]:
    #                 if score not in products_scores[second_item]:
    #                     list_of_products[item].append(reasons_of_parameters[score])
    #                     break
    #             if len(list_of_products[item]) == 2:
    #                 for values, descriptions in reasons_of_parameters.items():
    #                     if max(products_scores[first_item]) % values == 0:
    #                         list_of_products[item].append(reasons_of_parameters[values])
    #         for values, descriptions in reasons_of_parameters.items():
    #             if max(products_scores[list_of_products[-1][0]]) % values == 0:
    #                 list_of_products[-1].append(reasons_of_parameters[values])
    #     else:
    #         list_of_products[-1].append(reasons_of_parameters[max(products_scores[list_of_products[-1][0]])])
    #     list_of_products.sort(key=lambda j: j[1], reverse=True)
    #     print(products_scores)
    #     print(list_of_products)
    #     for item in list_of_products:
    #         if item[1] == 0:
    #             continue
    #         for item_list_search in products:
    #             if item_list_search['product_id'] == item[0]:
    #                 item_of_product = {
    #                     'product_id': item_list_search['product_id'],
    #                     'name': item_list_search['name'],
    #                     'brand': item_list_search['brand'],
    #                     'category': item_list_search['category'],
    #                     'skin_type': item_list_search['skin_type'],
    #                     'concerns_targeted': item_list_search['concerns_targeted'],
    #                     'ingredients': item_list_search['ingredients'],
    #                     'price': item_list_search['price'],
    #                     'rating': item_list_search['rating'],
    #                     'response': item[2]
    #                 }
    #                 results.append(item_of_product)
    #                 break
    #     return {'items': results}
    # else:
    #     return {'items': [{'product_id': user_in_code,
    #                        'name': 'None',
    #                        'brand': 'None',
    #                        'category': ['None'],
    #                        'skin_type': ['None'],
    #                        'concerns_targeted': ['None'],
    #                        'ingredients': ['None'],
    #                        'price': 0,
    #                        'rating': 0.0,
    #                        'response': 'we dont have product for your search.'}]}
def users_views(cursor):
    cursor.execute("""
                   SELECT product_id, COUNT(*) AS views_count
                   FROM Browsing_History
                   GROUP BY product_id
                   """)
    return dict(cursor.fetchall())
def user_information(cursor, user_id):
    cursor.execute("select * from Users where user_id = ?", (user_id, ))
    return cursor.fetchone()

def product_information(cursor, product_id):
    cursor.execute("select * from Products where product_id = ?", (product_id, ))
    return cursor.fetchone()

def s_product(cursor, product_type):
    cursor.execute("select p.* from Products p, json_each(p.skin_types) where json_each.value = ?", (product_type, ))
    return cursor.fetchall()

def purchase_da(cursor, user_in_code):
    cursor.execute("select * from Purchase_History where user_id = ?", (user_in_code, ))
    return cursor.fetchall()