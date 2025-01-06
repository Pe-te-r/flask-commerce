from flask import Flask
from flask_migrate import Migrate
from app.routes import register_routes
from app.database import db
from config import Config
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    Migrate(app,db)
    register_routes(app)
    
    return app