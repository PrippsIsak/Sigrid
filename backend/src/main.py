import datetime
from flask import request, Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import threadManager
import database as db

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)
state = "Off"
thread_pool_manager = threadManager.ThreadManager()

@app.route('/toggleAlarm', methods=['POST'])
def onOff():
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

    if state:
        thread_pool_manager.submit_task(time)
        return jsonify({"Succes": 'Alarm has been turned on'}),200
    
    #If a active alarm is set to be deactived
    thread_pool_manager.close_task(time)
    return jsonify({"Succes": "Alarm has been turned off"}),200


@app.route('/createAlarm', methods=['POST'])
def createAlarm():
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid input'}), 400
    
    try:
        hour = int(data.get('hour'))
        minute = int(data.get('minute')) 
    except(KeyError, ValueError):
        return jsonify({'Error': 'Invalid input'}), 400
    
    status = db.createAlarm(hour, minute)
    if status != "OK":
        return jsonify({'Error': status}),400
    
    time = datetime.time(hour=hour, minute=minute)
    thread_pool_manager.submit_task(time)
    
    return jsonify({"Succes": "Alarm has been created"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid input'})
    
    try:
        username = str(data.get('username', 0))
        password = str(data.get('password', 0))
    except(KeyError, ValueError):
        return jsonify({'Error': 'Invalid data'})
    
    status = db.login(username, password)
    if status !='OK':
        return jsonify({'Error': 'Wrong password or username'}), 400

    return jsonify({'Succes': 'Login succesful'}), 200

@app.route('/getAllAlarms', methods=['GET'])
def getAllAlarms():
    alarms = db.getAllAlarm()
    if alarms == 'NOT OK':
        return jsonify({"Error": "Invalid Input"}), 400
    
    return jsonify({"Alarms": alarms}), 200

@app.route('/checkActive', methods=['GET'])
def checkActive():
    active = db.getActiveAlarms()   
    if active == 'NOT OK':
        return jsonify({'Error': 'Invalid input'}), 400
    
    return jsonify({'active': active}), 200

@app.route('/getShoppingItems', methods=['GET'])
def getShoppingList():
    shoppingList = db.fetchShoppingItems()
    if shoppingList == 'NOT OK':
        return jsonify({'Error': 'Internal server error'}), 500
    
    return jsonify({'Shopping items': shoppingList})

@app.route('/createShoppingItems', methods=['POST'])
def createShoppingItem():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'Error': 'Invalid input'}), 400
    
    try:
        item = str(data['shoppingItem'])
        item.capitalize()
        status = db.createShoppingItem(item)
        if status == 'NOT OK':
            return jsonify({'Error': 'Invalid input'}), 400
        return jsonify({'Succes': 'Item added'}), 200
    
    except(KeyError, ValueError):
        return jsonify({'Error': 'Invalid input'}), 400
    
@app.route('/deleteShoppingItems', methods=['post'])
def deleteShoppingItems():
    data = request.get_json()
    print(data)
    for item in data:
        status = db.deleteShoppingItem(item['shoppingItem'])
        if status == 'NOT OK':
            return jsonify({'Error': 'Internal server error'}), 500
    return jsonify({'Succes': 'items has been deleted'}), 200

    
def run_flask():
    app.run(debug=False, host='0.0.0.0' ,port=5001)

if __name__ == '__main__':
    run_flask()

