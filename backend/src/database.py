from flask import jsonify
from flask_socketio import SocketIO
from pymongo import ReturnDocument
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv("/home/isak/projects/Sigrid/backend/src/variable.env")
connectionString = os.getenv("MONGO_STRING")
client = MongoClient(connectionString)

DATABASE_NAME = "SmartHome"
COLLECTION_SHOPPINGITEMS = "ShoppingItems"
COLLECTION_ALARM = "Alarms"
COLLECTION_USER = "User"


def login(username, password):
    """Function checks if user exist or not and if password matches"""
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_USER)
        user = collection.find_one({"Username": username})
        if user["password"] == password:
            return "OK"

    except Exception as e:
        return e

    return jsonify({"Bad request": "Failed login"})


def get_all_alarm():
    """Function gets all alarms from database"""
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_ALARM)
        alarms = collection.find({}, {"_id": 0})
        return list(alarms)
    except Exception as e:
        return "NOT OK"


def create_alarm(hour, minute):
    """Create a alarm in database"""
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_ALARM)
        collection.insert_one({"hour": hour, "minute": minute, "active": True})
        return "OK"
    except Exception as e:
        return e


def find_alarm(hour, minute, state):
    """Find the requested alarm"""
    try:
        print(type(hour), type(minute), type(state))
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_ALARM)
        update = {"$set": {"active": state}}
        alarm = collection.find_one_and_update(
            {"hour": hour, "minute": minute},
            update=update,
            projection={"_id": 0, "active": 0},
            return_document=ReturnDocument.AFTER,
        )

        # check if alarm exist
        if alarm is None:
            return "NOT OK"

    except Exception as e:
        return "NOT OK"

    return "OK"


def get_active_alarms():
    """Get all alarm items from database and sends it back"""
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_ALARM)
        alarm = collection.find_one({"active": True})
        print(alarm["active"])
        if alarm == None:
            return "NOT OK"

        return alarm.get("active")
    except Exception as e:
        return "NOT OK"


def fetch_shopping_items():
    """Gets all the shopping items and sends it back"""
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(
            COLLECTION_SHOPPINGITEMS
        )
        shoppinglist = collection.find({}, {"_id": 0})
        return list(shoppinglist)

    except Exception as e:
        return "NOT OK"


def create_shopping_item(itemName):
    """Creates a shopping item and sends it to the database"""
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(
            COLLECTION_SHOPPINGITEMS
        )
        _ = collection.insert_one({"shoppingItem": itemName, "checked": False})
        return "OK"

    except Exception as e:
        return "NOT OK"


def delete_shopping_item(itemName):
    """Deletes a specific shopping item"""
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(
            COLLECTION_SHOPPINGITEMS
        )
        result = collection.delete_one({"shoppingItem": itemName})
        if result.deleted_count == 1:
            return "OK"
        else:
            return "NOT OK"
    except Exception as e:
        return "NOT OK"
