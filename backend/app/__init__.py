from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config


#inicializar extensiones

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Factory function para crear la aplicacion Flask"""

    #crear la instancia de Flask
    app = Flask(__name__)

    #Cargar la configuracion 
    app.config.from_object(Config)

    #inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)

    #Configracion desde CORS para permitir solicitudes desde el frontend
    CORS(app, resources={
        r"/api/*":{
            "origins":["http://localhost:4200", "http://127.0.0.1:4200"],
            "methods":["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Autorization"]
        }
    })

    #Importar y registrar blueprints
    register_blueprints(app)

    #crear talas en la bd
    with app.app_context():
        db.create_all()
    return app


def register_blueprints(app):

    from app.projects import bp as projects_bp
    from app.routes.blog import bp as blog_bp
    from app.routes.contact import bp as contact_bp

    #Registrar blueprints con prefijo /api
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(blog_bp, url_prefix='/api/blog')
    app.register_blueprint(contact_bp, url_prefix='/api/contact')
