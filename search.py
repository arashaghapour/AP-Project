from typing import List
def serch_in_database(items_Cosmetics, items_skin_care, dict_searched_item):
    cosmetics_results = []
    skin_care_results = []
    if(dict_searched_item['id']):
        for i in items_Cosmetics:
            i = i.__dict__
            if i['id'] == dict_searched_item['id']:
                cosmetics_results.append(i)
        for i in items_skin_care:
            i = i.__dict__
            if i['id'] == dict_searched_item['id']:
                skin_care_results.append(i)
    
        