from os import environ
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = environ.get('MAIL_SERVER')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=int(environ.get('TIME')))
    MAIL_PORT = environ.get("PORT")
    MAIL_USERNAME = environ.get("USER_MAIL") 
    MAIL_PASSWORD =environ.get("USER_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
