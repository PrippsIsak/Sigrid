import datetime
from flask import request, jsonify, Blueprint
import backend.src.services.coffee_machine as coffee
import database as db
alarm_bp = Blueprint('alarm', __name__)

@alarm_bp.route('/toggleAlarm', methods=['POST'])
def toggle_alarm():
    """Function gets the body then calls the database api"""
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid input'}), 400
    try:
        hour = int(data.get('hour'))
        minute = int(data.get('minute'))
        state = bool(data.get('active'))
    except (KeyError, ValueError):
        return jsonify({'Error': 'Invalid input'}), 400
    
    status = db.findAlarm(hour, minute, state)
    if status == 'NOT OK':
        return jsonify({'Error': 'Invalid input'})
    
    time = datetime.time(hour=hour, minute=minute)
    result, err = coffee.set_coffee_timer(time)
    if err != None:
        return jsonify({'Error', 'Internal server error'}), 500
    return jsonify({'Succes': f'Coffe machine was set to {result}'})

@alarm_bp.route('/createAlarm', methods=['POST'])
def create_alarm():
    """Gets the body, checks for type and then call the database api"""
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid input'}), 400
    
    try:
        hour = int(data.get('hour'))
        minute = int(data.get('minute')) 
    except(KeyError, ValueError):
        return jsonify({'Error': 'Invalid input'}), 400
    
    if hour > 23 or hour < 0:
        return jsonify({'Error': 'Invalid input'}), 400
    
    if minute > 59 or minute < 0:
        return jsonify({'Error': 'Invalid input'}), 400
    
    status = db.create_alarm(hour, minute)
    if status != "OK":
        return jsonify({'Error': status}), 500

    time = datetime.time(hour=hour, minute=minute)
    result, err = coffee.set_coffee_timer(time)
    if err != None:
        return jsonify({'Error', 'Internal server error'}), 500
    return jsonify({'Succes': f'Coffe machine was set to {result}'})

@alarm_bp.route('/getAllAlarms', methods=['GET'])
def get_all_alarms():
    """Calls the database api and return all alarms"""
    alarms = db.get_all_alarm()
    if alarms == 'NOT OK':
        return jsonify({"Error": "Invalid Input"}), 500
    return jsonify({"Alarms": alarms}), 200

@alarm_bp.route('/checkActive', methods=['GET'])
def check_active():
    """Calls database api and return there is any active alarms"""
    active = db.get_active_alarms()   
    if active == 'NOT OK':
        return jsonify({'Error': 'Invalid input'}), 500
    return jsonify({'active': active}), 200
