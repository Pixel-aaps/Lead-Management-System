import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # JWT configuration
    JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwt")
    JWT_ALGORITHM = "HS256"
    JWT_EXP_DELTA_SECONDS = 3600  # 1 hour expiration
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///leads.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
