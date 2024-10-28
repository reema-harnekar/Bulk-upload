from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    DEBUG = os.getenv("DEBUG", False)
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
