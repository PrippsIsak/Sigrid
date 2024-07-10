from flask import request, jsonify, Blueprint
import database as db

shopping_item_bp = Blueprint('shopping_items', __name__)
@shopping_item_bp.route('/getShoppingItems', methods=['GET'])
def get_shopping_list():
    shoppingList = db.fetch_shopping_items()
    if shoppingList == 'NOT OK':
        return jsonify({'Error': 'Internal server error'}), 500
    
    return jsonify({'Shopping items': shoppingList})

@shopping_item_bp.route('/createShoppingItems', methods=['POST'])
def create_shopping_item():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'Error': 'Invalid input'}), 400
    
    try:
        item = str(data['shoppingItem'])
        item = item.capitalize()
        status = db.create_shopping_item(item)
        if status == 'NOT OK':
            return jsonify({'Error': 'Invalid input'}), 500
        return jsonify({'Succes': 'Item added'}), 200
    
    except(KeyError, ValueError):
        return jsonify({'Error': 'Invalid input'}), 400
    
@shopping_item_bp.route('/deteShoppingItems', methods=['delete'])
def delete_shopping_items():
    data = request.get_json()
    print(data)
    try:
        for item in data:
            status = db.delete_shopping_item(item['shoppingItem'])
            if status == 'NOT OK':
                return jsonify({'Error': 'Internal server error'}), 500
    except(KeyError, ValueError):
        return jsonify({'Error': 'Invalid data'}), 400
    return jsonify({'Succes': 'items has been deleted'}), 200