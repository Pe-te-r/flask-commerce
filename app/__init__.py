from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from app.routes import register_routes
from app.database import db,bcypt
from config import Config
from app.helper.mails import mail
# from flask_mail import Mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    bcypt.init_app(app)
    db.init_app(app)
    Migrate(app,db)
    JWTManager(app)
    mail.init_app(app)
    CORS(app)
    register_routes(app)
    
    return app