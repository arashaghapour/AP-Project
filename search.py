from typing import List
def serch_in_database(items_Cosmetics, items_skin_care, item, everything_item):
    if(everything_item):
        list_of_products_cosmetics = []
        list_of_products_skin_care = []
        for i in items_Cosmetics:
            i = i.__dict__
            for j, k in i.items():
                if(k == everything_item):
                    list_of_products_cosmetics.append(i)
        for i in items_skin_care:
            i = i.__dict__
            for j, k in i.items():
                if(k == everything_item):
                    list_of_products_skin_care.append(i)
        if(list_of_products_cosmetics or list_of_products_skin_care):
            return {"cosmetics": list_of_products_cosmetics, "skin_care": list_of_products_skin_care}
        else:
            return 0
    else:
        list_of_products_cosmetics = []
        list_of_products_skin_care = []
        for i in item:
            if(i):
                try:
                    i = int(i)
                    for j in items_Cosmetics:
                        if(j['id'] == i):
                            return {"cosmetics": List[j], "skin_care": list_of_products_skin_care}
                    for j in items_skin_care:
                        if(j['id'] == i):
                            return {"cosmetics": list_of_products_cosmetics, "skin_care": List[j]}
                except:
                    
                    for j in items_Cosmetics:
                        j = j.__dict__
                        for k, l in j.items():
                            if(l == i):
                                list_of_products_cosmetics.append(j)
                    for j in items_skin_care:
                        j = j.__dict__
                        for k, l in j.items():
                            if(l == i):
                                list_of_products_skin_care.append(j)
        if(list_of_products_cosmetics or list_of_products_skin_care):
            return {"cosmetics": list_of_products_cosmetics, "skin_care": list_of_products_skin_care}
        else:
            return 0