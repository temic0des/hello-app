import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I-cannot-guess-this-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')