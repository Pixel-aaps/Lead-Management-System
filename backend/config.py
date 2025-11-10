# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # JWT configuration
    JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwt")
    JWT_ALGORITHM = "HS256"
    JWT_EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", "3600"))

    # Cookie settings for JWT cookie if you want to use cookies
    COOKIE_SECURE = os.getenv("COOKIE_SECURE", "False").lower() in ("1", "true", "yes")
    COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")  # 'Lax' or 'Strict' or 'None'
    COOKIE_NAME = os.getenv("COOKIE_NAME", "token")

    # Frontend origin - IMPORTANT: set this in Render to your Vercel URL (e.g. https://yourapp.vercel.app)
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://lmsfro-2mlzxna2y-avaneesh6404-3847s-projects.vercel.app")

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///leads.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
