import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    "Configuracion de la aplicacion Flask"
    #Clave secreta para sessiones y seguridad 
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-change-in-production'

    #Configuracion de la base de datos 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///portfolio.db'

    #Desactivar track modifications para el mejor performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #configuracion para Flask-migrate
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    
