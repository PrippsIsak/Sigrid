from flask import jsonify
from pymongo import ReturnDocument
from pymongo.mongo_client import MongoClient
import os 
from dotenv import load_dotenv, dotenv_values

load_dotenv()


connectionString = os.getenv("MONGO_STRING") 
client = MongoClient('mongodb+srv://isakolofaxelsson:LN5obMliukgWgUd1@smarthome.4dvbmcv.mongodb.net/?retryWrites=true&w=majority&appName=SmartHome')

DATABASE_NAME = 'SmartHome'
COLLECTION_SHOPPINGITEMS = 'ShoppingItems'
COLLECTION_ALARM = 'Alarms'
COLLECTION_USER = 'User'

def login(username, password):
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_USER)
        user = collection.find_one({'Username' : username})
        if user['password'] == password:
            return 'OK'
     
    except Exception as e:
        return e
    
    return jsonify({"Bad request": "Failed login"})  
    
def getAllAlarm():
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_ALARM)
        alarms = collection.find({}, {'_id': 0})
        return list(alarms)
    except Exception as e:
        return 'NOT OK'

def createAlarm(hour, minute):
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_ALARM)
        collection.insert_one({'hour': hour, 'minute': minute, 'active': True})
        return "OK"
    except Exception as e:
        return e

def findAlarm(hour, minute, state):
    try:
        print(type(hour), type(minute), type(state))
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_ALARM)
        update = {'$set': {'active':state }}
        alarm = collection.find_one_and_update(
            {'hour': hour, 'minute': minute},
              update=update,
              projection={'_id':0, 'active':0},
              return_document=ReturnDocument.AFTER)
              
        #check if alarm exist
        if alarm == None:
            return 'NOT OK'
        
    except Exception as e:
        return 'NOT OK'
    
    return 'OK'

def getActiveAlarms():
    try:    
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_ALARM)
        alarm = collection.find_one({'active': True})
        print(alarm['active'])
        if alarm == None:
            return 'NOT OK'

        return alarm.get('active')
    except Exception as e:
        return 'NOT OK'

def fetchShoppingItems():
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_SHOPPINGITEMS)
        shoppinglist = collection.find({}, {'_id': 0})
        return list(shoppinglist)
    
    except Exception as e:
        return 'NOT OK'

def createShoppingItem(itemName):
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_SHOPPINGITEMS)
        _ = collection.insert_one({'shoppingItem': itemName, 'checked': False})
        return 'OK'
    
    except Exception as e:
        return 'NOT OK'
    
def deleteShoppingItem(itemName):
    try:
        collection = client.get_database(DATABASE_NAME).get_collection(COLLECTION_SHOPPINGITEMS)
        result = collection.delete_one({'shoppingItem': itemName})
        if result.deleted_count == 1:
            return 'OK'
        else: 
            return 'NOT OK'
    except Exception as e:
        return 'NOT OK'
def