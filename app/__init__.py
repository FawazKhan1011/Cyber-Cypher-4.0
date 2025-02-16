from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = Config.MONGO_URI  # Corrected line

    mongo.init_app(app)

    from .auth.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app