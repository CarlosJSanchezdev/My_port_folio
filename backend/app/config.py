import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuracion de la aplicacion Flask"""
    # Clave secreta para sessiones y seguridad 
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Configuracion de la base de datos 
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Fix for Supabase/Heroku postgres:// vs postgresql://
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///portfolio.db'

    # Desactivar track modifications para el mejor performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SSL configuration for Supabase
    if DATABASE_URL and 'supabase' in DATABASE_URL:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }
    
