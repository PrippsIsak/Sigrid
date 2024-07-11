from pymongo.mongo_client import MongoClient
import os 
from dotenv import load_dotenv

load_dotenv('/home/isak/projects/Sigrid/backend/src/variable.env')
connectionString = os.getenv("MONGO_STRING")
database_name = 'SmartHome'
DATABASE = MongoClient(connectionString).get_database(database_name)