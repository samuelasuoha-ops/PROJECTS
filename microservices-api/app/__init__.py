from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://mongo:27017/microservicesdb"
    
    mongo.init_app(app)

    from .routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
