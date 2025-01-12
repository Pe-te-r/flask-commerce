from os import environ
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "sandbox.smtp.mailtrap.io"
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
    MAIL_PORT = 2525
    MAIL_USERNAME = "a040f4f871f7b5"
    MAIL_PASSWORD = "634e1d8d2d465e"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
