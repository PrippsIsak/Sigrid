from flask import request, jsonify, Blueprint
import util.coffeeMachine

coffee_machine_bp = Blueprint('coffe_machine', __name__)

@coffee_machine_bp('/toggleCoffee', methods=['POST'])
def toggle_coffe():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'Error': 'Invalid input'}), 400
    try:
        state = str(data.get('state'))
    except (KeyError, ValueError):
        return jsonify({'Error': 'Inavlid input'}), 400
    
    result = util.coffeeMachine.setCoffe(state)
    if not result:
        return jsonify({'Error': 'Internal server error'}), 500
    return jsonify({'Succes': 'Message sent to arduino'}), 200