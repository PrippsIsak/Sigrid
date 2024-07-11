from backend.src.database.global_database import DATABASE

COLLECTION_SHOPPINGITEMS = 'ShoppingItems'

def fetch_shopping_items():
    """Function finds and return all shopping_items"""
    try:
        collection = DATABASE.get_collection(COLLECTION_SHOPPINGITEMS)
        shoppinglist = collection.find({}, {'_id': 0})
        return list(shoppinglist)
    
    except Exception as e:
        return 'NOT OK'

def create_shopping_item(itemName):
    """Creates a shopping_item in database"""
    try:
        collection = DATABASE.get_collection(COLLECTION_SHOPPINGITEMS)
        _ = collection.insert_one({'shoppingItem': itemName, 'checked': False})
        return 'OK'
    
    except Exception as e:
        return 'NOT OK'
    
def delete_shopping_item(itemName):
    """Function find a specific shopping_items and deletes it"""
    try:
        collection = DATABASE.get_collection(COLLECTION_SHOPPINGITEMS)
        result = collection.delete_one({'shoppingItem': itemName})
        if result.deleted_count == 1:
            return 'OK'
        else: 
            return 'NOT OK'
    except Exception as e:
        return 'NOT OK'