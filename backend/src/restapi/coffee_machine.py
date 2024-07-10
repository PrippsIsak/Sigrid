from flask import request, jsonify, Blueprint
import backend.src.services.coffee_machine as coffe

coffee_machine_bp = Blueprint('coffe_machine', __name__)

@coffee_machine_bp('/toggleCoffee', methods=['POST'])
def toggle_coffe():
    """Call util to turn on and of coffee machine"""
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'Error': 'Invalid input'}), 400
  
    state = str(data.get('state'))

    if state != ('On' or 'Off'):
        return jsonify({'Error': 'Invalid input'}, 400
                       )
    err = coffe.set_coffee(state)
    if err != None:
        return jsonify({'Error': 'Internal server error'}), 500
    return jsonify({'Succes': f'Coffee machine was turned {state}'}), 200