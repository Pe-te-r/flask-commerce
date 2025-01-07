from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.routes import register_routes
from app.database import db,bcypt
from config import Config
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    bcypt.init_app(app)
    db.init_app(app)
    Migrate(app,db)
    JWTManager(app)
    
    register_routes(app)
    
    return app