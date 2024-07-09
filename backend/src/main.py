from flask import Flask
from flask_cors import CORS
import backend.src.services.threadManager as threadManager
from flask_bcrypt import Bcrypt
from pymongo.mongo_client import MongoClient
import os 
from dotenv import load_dotenv

load_dotenv('/home/isak/projects/Sigrid/backend/src/variable.env')
connectionString = os.getenv("MONGO_STRING")
database_name = 'SmartHome'
DATABASE = MongoClient(connectionString).get_database(database_name)
THREAD_POOL_MANAGER = threadManager.ThreadManager()
BCRYPT = Bcrypt()

def create_app():
    app = Flask(__name__)
    CORS(app)

    from restapi.user import user_bp
    from restapi.alarm import alarm_bp
    from restapi.coffee_machine import coffee_machine_bp
    from restapi.shopping_items import shopping_item_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(alarm_bp)
    app.register_blueprint(coffee_machine_bp)
    app.register_blueprint(shopping_item_bp)

    return app

def run_flask():
    app = create_app()
    app.run(app, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    run_flask()
