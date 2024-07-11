from flask import Flask
from flask_cors import CORS
from extensions import CRYPT

from restapi.user import user_bp
from restapi.alarm import alarm_bp
from restapi.coffee_machine import coffee_machine_bp
from restapi.shopping_items import shopping_item_bp



def create_app():
    """configues the app and routes"""
    app = Flask(__name__)
    CRYPT.init_app(app)
    CORS(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(alarm_bp)
    app.register_blueprint(coffee_machine_bp)
    app.register_blueprint(shopping_item_bp)

    return app

def run_flask():
    app = create_app()
    app.run(host='0.0.0.0', port=5001)

if __name__ == "__main__":
    run_flask()
