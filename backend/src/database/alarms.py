from main import DATABASE
from pymongo import ReturnDocument
COLLECTION_ALARM = 'Alarms'

def get_all_alarm():
    try:
        collection = DATABASE.get_collection(COLLECTION_ALARM)
        alarms = collection.find({}, {'_id': 0})
        return list(alarms)
    except Exception as e:
        return 'NOT OK'
    
def create_alarm(hour, minute):
    try:
        collection = DATABASE.get_collection(COLLECTION_ALARM)
        collection.insert_one({'hour': hour, 'minute': minute, 'active': True})
        return "OK"
    except Exception as e:
        return e


def find_alarm(hour, minute, state):
    try:
        print(type(hour), type(minute), type(state))
        collection = DATABASE.get_collection(COLLECTION_ALARM)
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

def get_active_alarms():
    try:    
        collection = DATABASE.get_collection(COLLECTION_ALARM)
        alarm = collection.find_one({'active': True})
        print(alarm['active'])
        if alarm == None:
            return 'NOT OK'

        return alarm.get('active')
    except Exception as e:
        return 'NOT OK'