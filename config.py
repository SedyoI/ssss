import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://hayd:agro123*&back12@localhost/agrotracker")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    JWT_SECRET = os.getenv("JWT_SECRET", "VerySecretKey")
    JWT_TOKEN_LOCATION = ["headers"] 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
