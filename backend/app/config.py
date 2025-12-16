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
    
    # Email configuration (Gmail SMTP)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'Cafefincasanrafael@gmail.com')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_DOMAIN = None  # Allow cookies on localhost
    SESSION_COOKIE_NAME = 'portfolio_session'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora

