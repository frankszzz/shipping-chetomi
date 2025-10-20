import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shipping.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    TIMEZONE = os.getenv('TIMEZONE', 'America/Santiago')
    ORS_API_KEY = os.getenv('ORS_API_KEY')
    ORS_BASE_URL = 'https://api.openrouteservice.org/v2'
    MAX_DELIVERY_DISTANCE_KM = 7
