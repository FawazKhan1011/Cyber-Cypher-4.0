from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    mongo.init_app(app)

    from .auth.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app