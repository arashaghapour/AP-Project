import sqlite3 as lite
import json
from datetime import datetime

season_weights = {
    "summer": {"sunscreen": 3, "moisturizer": 1, "serum": 1},
    "winter": {"moisturizer": 3, "lip_balm": 2, "sunscreen": 0.5},
    "spring": {"serum": 2, "cleanser": 1.5},
    "autumn": {"moisturizer": 2, "cleanser": 1}
}

def get_season():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'autumn'
    

def search_in_database(user_in_code, searched_item):
    products_scores = {}
    parameters_score = {'concerns': 85, 'category': 75, 'views':63,'searched_box': 301,
                        'rating': 22, 'name': 283, 'brand': 281,
                        'purchase': 41,'searched': 13, 'close': 31,
                        'most_view': 53, 'skin_type': 90, 'user_skin_type': 43, 'user_concerns': 47,
                        'searched_skin_type': 297, 'searched_concerns': 294, 'searched_category': 292, 'budget_range': 51}
    
    parameters_score['season'] = 77

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
        parameters_score['skin_type']: 'it because you have same skin types.',
        parameters_score['user_skin_type']: 'it because you have same skin types.',
        parameters_score['user_concerns']: 'it because you have same concerns.',
        parameters_score['searched_skin_type']: 'it because you have searched this skin types.',
        parameters_score['searched_concerns']: 'it because you have searched this concerns.',
        parameters_score['searched_category']: 'it because you have searched this category.',
        parameters_score['budget_range']: 'it because you have budge range.',
        parameters_score['season']: 'This product is more suitable for the current season.'
    }

    conn = lite.connect('./database.db')
    cursor = conn.cursor()
    results = []
    output = []
    views = {}
    exist = False
    id_exist = False
    for i in get_column(cursor):
        products_scores[i] = []
    views = users_views(cursor)
    views = dict(sorted(views.items(), key=lambda item: item[1], reverse=True))
    search_value = searched_item
    results = None

    if search_value.isdigit():
        cursor.execute("SELECT product_id FROM Products WHERE product_id = ?", (int(search_value),))
        results = cursor.fetchall()
        for i in results:
            products_scores[i[0]].append(parameters_score['searched_box'])
    if not results:
        cursor.execute("SELECT product_id FROM Products WHERE name = ?", (search_value,))
        results = cursor.fetchall()
        for i in results:
            products_scores[i[0]].append(parameters_score['name'])
    if not results:
        cursor.execute("SELECT product_id FROM Products WHERE brand = ?", (search_value,))
        results = cursor.fetchall()
        for i in results:
            products_scores[i[0]].append(parameters_score['brand'])
    if not results:
        cursor.execute("""
                       SELECT product_id
                       FROM Products
                       WHERE json_extract(concerns_targeted, '$[0]') = ?
                       """, (search_value,))
        results = cursor.fetchall()
        for i in results:
            products_scores[i[0]].append(parameters_score['searched_concerns'])

    if not results:
        cursor.execute('select product_id from Products where category = ?', (search_value, ))
        results = cursor.fetchall()
        for i in results:
            products_scores[i[0]].append(parameters_score['searched_category'])

    if not results:
        cursor.execute("""
                       SELECT product_id
                       FROM Products
                       WHERE json_extract(skin_types, '$[0]') = ?
                       """, (search_value,))
        results = cursor.fetchall()
        for i in results:
            products_scores[i[0]].append(parameters_score['searched_skin_type'])
    cursor = conn.cursor()
    user_row_in_database = user_information(cursor, user_in_code)
    try:
        skin_product = s_product(cursor, user_row_in_database[2])
    except:
        skin_product = None
    try:
        purchase_in_database = purchase_da(cursor, user_in_code)
    except:
        purchase_in_database = None
    try:
        user_concern = concerns_targeted(cursor, user_row_in_database[3][0])
    except:
        user_concern = None

    if skin_product:
        for i in skin_product:
            products_scores[i].append(parameters_score['user_skin_type'])

    if user_concern:
        for i in user_concern:
            products_scores[i].append(parameters_score['user_concerns'])

    if purchase_in_database:
        for i in purchase_in_database:
            products_scores[i[2]].append(i[3] * parameters_score['purchase'])
    list_of_products = []
    for id, scores_list in products_scores.items():
        list_of_products.append([id, sum(scores_list)])
    list_of_products.sort(key=lambda item: item[1], reverse=True)
    if results or products_scores:
        for id, scores_list in products_scores.items():
            if id in views:
                scores_list.append(views[id] * parameters_score['searched'])

        for i, j in views.items():
            products_scores[i].append(parameters_score['most_view'])
            break
        user_budget = user_budget_range(cursor, user_in_code)
        for id, scores_list in products_scores.items():
            products_scores[id].append(round(product_rating(cursor, id) * parameters_score['rating'], 2))
            if user_budget:
                user_budget = user_budget[0][0]
                print(user_budget)
                if user_budget - 2000 < product_price(cursor, id) < user_budget + 2000:
                    products_scores[id].append(parameters_score['budget_range'])
                   


        list_of_products = []
        for id, scores_list in products_scores.items():
            list_of_products.append([id, sum(scores_list)])
        list_of_products.sort(key=lambda item: item[1], reverse=True)

        first_product = product_information(cursor, list_of_products[0][0])
        if user_budget:
            near_skin_type = 30
            for skin_type, score in skin_types.items():
                if abs(score - skin_types[first_product[4][0]]) < near_skin_type:
                    near_products = s_product(cursor, skin_type)
                    for i in near_products:
                        products_scores[i].append(parameters_score['close'])

            near_concern = 3
            for concern, score in concerns_labels.items():
                if abs(score - concerns_labels[first_product[5][0]]) < near_concern:
                    product = concerns_targeted(cursor, concern)
                    for i in product:
                        products_scores[i].append(parameters_score['close'])
        list_of_products.sort(key=lambda item: item[1], reverse=True)
        list_of_products = list_of_products[:10]
        
        season = get_season()
        for id, scores_list in products_scores.items():
            product_info = product_information(cursor, id)
            product_category = product_info[3][0]  
            if product_category in season_weights[season]:
                weight = season_weights[season][product_category]
                products_scores[id].append(weight * 50)

        if len(list_of_products) > 1:
            for item in range(len(list_of_products) - 1):
                first_item = list_of_products[item][0]
                second_item = list_of_products[item + 1][0]
                for score in products_scores[first_item]:
                    if score not in products_scores[second_item]:
                        for i in reasons_of_parameters:
                            if score % i == 0:
                                list_of_products[item].append(reasons_of_parameters[i])
                                break
                        break
                if len(list_of_products[item]) != 3:
                    maximum_score = max(products_scores[list_of_products[item][0]])
                    for values, descriptions in reasons_of_parameters.items():
                        if maximum_score % values == 0:
                            list_of_products[item].append(descriptions)
                            break
                if len(list_of_products[item]) != 3:
                    list_of_products[item].append(reasons_of_parameters[parameters_score['rating']])
            maximum_last_product_score = max(products_scores[list_of_products[-1][0]])
            for values, descriptions in reasons_of_parameters.items():
                if maximum_last_product_score % values == 0:
                    list_of_products[-1].append(descriptions)
                    break
            if len(list_of_products[-1]) != 3:
                    list_of_products[-1].append(reasons_of_parameters[parameters_score['rating']])
        else:
            for values, descriptions in reasons_of_parameters.items():
                if max(products_scores[list_of_products[-1][0]]) % values == 0:
                    list_of_products[-1].append(reasons_of_parameters[values])
                    break
            if len(list_of_products[-1]) != 3:
                    list_of_products[-1].append(reasons_of_parameters[parameters_score['rating']])
        for item in list_of_products:
            if item[1] == 0:
                continue
            item_list_search = product_information(cursor, item[0])
            item_of_product = {
                'product_id': item_list_search[0],
                'name': item_list_search[1],
                'brand': item_list_search[2],
                'category': item_list_search[3],
                'skin_type': item_list_search[4],
                'concerns_targeted': item_list_search[5],
                'ingredients': item_list_search[6],
                'price': item_list_search[7],
                'rating': item_list_search[8],
                'image_url': 'string',
                'tags': ['string'],
                'count': item_list_search[11],
                'response': item[2]
            }
            output.append(item_of_product)
        return {'items': output}
    else:
        return {'items': [{'product_id': user_in_code,
                           'name': 'None',
                           'brand': 'None',
                           'category': ['None'],
                           'skin_type': ['None'],
                           'concerns_targeted': ['None'],
                           'ingredients': ['None'],
                           'price': 0,
                           'rating': 0.0,
                           'response': 'we dont have product for your search.'}]}
def users_views(cursor):
    cursor.execute("""
                   SELECT product_id, COUNT(*) AS views_count
                   FROM Browsing_History
                   GROUP BY product_id
                   """)
    return dict(cursor.fetchall())
def user_information(cursor, user_id):
    cursor.execute("select * from Users where user_id = ?", (user_id, ))
    row = cursor.fetchone()
    if row:
        row = list(row)
        row[3] = json.loads(row[3])
        row[4] = json.loads(row[4])
        return list(row)
    else:
        return None

def product_information(cursor, product_id):
    cursor.execute("select * from Products where product_id = ?", (product_id, ))
    row = cursor.fetchone()
    if not row:
        return None
    row = list(row)
    row[4] = json.loads(row[4])
    row[5] = json.loads(row[5])
    row[6] = json.loads(row[6])
    row[10] = json.loads(row[10])
    return row

def product_price(cursor, product_id):
    cursor.execute("select price from Products where product_id = ?", (product_id, ))
    return cursor.fetchone()[0]

def product_rating(cursor, product_id):
    cursor.execute("select rating from Products where product_id = ?", (product_id, ))
    return cursor.fetchone()[0]

def s_product(cursor, product_type):
    cursor.execute("select p.* from Products p, json_each(p.skin_types) where json_each.value = ?", (product_type, ))
    row = cursor.fetchall()
    row = [i[0] for i in row]
    return row

def purchase_da(cursor, user_in_code):
    cursor.execute("select * from Purchase_History where user_id = ?", (user_in_code, ))
    return cursor.fetchall()

def concerns_targeted(cursor, concern):
    cursor.execute("select p.* from Products p, json_each(p.concerns_targeted) where json_each.value = ?", (concern, ))
    row = cursor.fetchall()
    row = [i[0] for i in row]
    return row

def get_column(cursor):
    cursor.execute("SELECT product_id FROM Products")
    columns = [i[0] for i in cursor.fetchall()]
    return columns

def user_budget_range(cursor, user_in_code):
    cursor.execute("select budget_range from Users where user_id = ?", (user_in_code, ))
    return cursor.fetchall()

