from main import DATABASE

COLLECTION_SHOPPINGITEMS = 'ShoppingItems'

def fetch_shopping_items():
    try:
        collection = DATABASE.get_collection(COLLECTION_SHOPPINGITEMS)
        shoppinglist = collection.find({}, {'_id': 0})
        return list(shoppinglist)
    
    except Exception as e:
        return 'NOT OK'

def create_shopping_item(itemName):
    try:
        collection = DATABASE.get_collection(COLLECTION_SHOPPINGITEMS)
        _ = collection.insert_one({'shoppingItem': itemName, 'checked': False})
        return 'OK'
    
    except Exception as e:
        return 'NOT OK'
    
def delete_shopping_item(itemName):
    try:
        collection = DATABASE.get_collection(COLLECTION_SHOPPINGITEMS)
        result = collection.delete_one({'shoppingItem': itemName})
        if result.deleted_count == 1:
            return 'OK'
        else: 
            return 'NOT OK'
    except Exception as e:
        return 'NOT OK'