from flask import Flask
from app.routes import register_routes
from app.database import db
def create_app():
    app = Flask(__name__)
    
    db.init_app(app)
    register_routes(app)
    
    return app