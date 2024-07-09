import datetime
from flask import request, Flask, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import threadManager
import database as db
import util.coffeeMachine

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
thread_pool_manager = threadManager.ThreadManager()


@app.route("/toggleAlarm", methods=["POST"])
def toggle_alarm():
    """REST-API - sets a alarm to active or inactive."""
    data = request.get_json()
    if not data:
        return jsonify({"Error": "Invalid input"}), 400
    try:
        hour = int(data.get("hour"))
        minute = int(data.get("minute"))
        state = bool(data.get("active"))
    except (KeyError, ValueError):
        return jsonify({"Error": "Invalid input"}), 400

    status = db.findAlarm(hour, minute, state)
    if status == "NOT OK":
        return jsonify({"Error": "Invalid input"})

    time = datetime.time(hour=hour, minute=minute)

    if state:
        thread_pool_manager.submit_task(time)
        return jsonify({"Succes": "Alarm has been turned on"}), 200

    thread_pool_manager.close_task(time)
    return jsonify({"Succes": "Alarm has been turned off"}), 200


@app.route("/toggleCoffee", methods=["POST"])
def toggle_coffe():
    """Toogle on and off the coffe machine by sending a string with websocket to a micro controller."""
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"Error": "Invalid input"}), 400
    try:
        state = str(data.get("state"))
        if state != ('On' or 'Off'):
            return jsonify({'Error:' 'Invalid input'}), 400
    except (KeyError, ValueError):
        return jsonify({"Error": "Inavlid input"}), 400

    result = util.coffeeMachine.setCoffe(state)
    if not result:
        return jsonify({"Error": "Internal server error"}), 500
    return jsonify({"Succes": "Message sent to arduino"}), 200


@app.route("/createAlarm", methods=["POST"])
def create_alarm():
    """Creates a alarm in the server and sets it to active"""
    data = request.get_json()
    if not data:
        return jsonify({"Error": "Invalid input"}), 400

    try:
        hour = int(data.get("hour"))
        minute = int(data.get("minute"))
    except (KeyError, ValueError):
        return jsonify({"Error": "Invalid input"}), 400

    status = db.create_alarm(hour, minute)
    if status != "OK":
        return jsonify({"Error": status}), 500

    # should be a try catch here
    time = datetime.time(hour=hour, minute=minute)
    thread_pool_manager.submit_task(time)

    return jsonify({"Succes": "Alarm has been created"}), 200


@app.route("/login", methods=["POST"])
def login():
    """Login infunction, checks if the correct type of data is sent or not"""
    data = request.get_json()
    if not data:
        return jsonify({"Error": "Invalid input"})

    try:
        username = str(data.get("username", 0))
        password = str(data.get("password", 0))
    except (KeyError, ValueError):
        return jsonify({"Error": "Invalid data"}), 400

    status = db.login(username, password)
    if status != "OK":
        return jsonify({"Error": "Wrong password or username"}), 500

    return jsonify({"Succes": "Login succesful"}), 200

@app.route("/getAllAlarms", methods=["GET"])
def get_all_alarms():
    """Fetches all alarms in database"""
    alarms = db.get_all_alarm()
    if alarms == "NOT OK":
        return jsonify({"Error": "Invalid Input"}), 500

    return jsonify({"Alarms": alarms}), 200


@app.route("/checkActive", methods=["GET"])
def check_active():
    """Function checks if any coffe_alarms exist"""
    active = db.get_active_alarms()
    if active == "NOT OK":
        return jsonify({"Error": "Invalid input"}), 500
    return jsonify({"active": active}), 200

@app.route("/getShoppingItems", methods=["GET"])
def get_shopping_list():
    """Function - gets all of the shopping items"""
    shopping_list = db.fetch_shopping_items()
    if shopping_list == "NOT OK":
        return jsonify({"Error": "Internal server error"}), 500
    return jsonify({"Shopping items": shopping_list})


@app.route("/createShoppingItems", methods=["POST"])
def create_shopping_item():
    """Function creates """
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"Error": "Invalid input"}), 400

    try:
        item = str(data["shoppingItem"])
        item = item.capitalize()
        status = db.create_shopping_item(item)
        if status == "NOT OK":
            return jsonify({"Error": "Invalid input"}), 500
        return jsonify({"Succes": "Item added"}), 200
    
    except (KeyError, ValueError):
        return jsonify({"Error": "Invalid input"}), 400

@app.route("/deteShoppingItems", methods=["DELETE"])
def delete_shopping_items():
    """Function finds the shopping item and deletes it from data base"""
    data = request.get_json()
    print(data)
    for item in data:
        status = db.delete_shopping_item(item["shoppingItem"])
        if status == "NOT OK":
            return jsonify({"Error": "Internal server error"}), 500
    socketio.emit("shopping")
    return jsonify({"Succes": "items has been deleted"}), 200

def run_flask():
    """Function runs app"""
    Flask.run(app, host="0.0.0.0", port=5001)

if __name__ == "__main__":
    run_flask()
