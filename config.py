import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    DEBUG = True