import datetime
from flask import request, jsonify, Blueprint
from main import THREAD_POOL_MANAGER
import database as db
alarm_bp = Blueprint('alarm', __name__)

@alarm_bp.route('/toggleAlarm', methods=['POST'])
def toggle_alarm():
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
    

@alarm_bp.route('/createAlarm', methods=['POST'])
def create_alarm():
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
    THREAD_POOL_MANAGER.submit_task(time)
    
    return jsonify({"Succes": "Alarm has been created"}), 200

@alarm_bp.route('/getAllAlarms', methods=['GET'])
def get_all_alarms():
    alarms = db.get_all_alarm()
    if alarms == 'NOT OK':
        return jsonify({"Error": "Invalid Input"}), 500
    return jsonify({"Alarms": alarms}), 200

@alarm_bp.route('/checkActive', methods=['GET'])
def check_active():
    active = db.get_active_alarms()   
    if active == 'NOT OK':
        return jsonify({'Error': 'Invalid input'}), 500
    return jsonify({'active': active}), 200 
