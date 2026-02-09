from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from flask_session import Session
from app.config import Config
import logging
from collections import defaultdict
from datetime import datetime, timedelta

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
sess = Session()

# Configuración del logger para seguridad 
security_logger = logging.getLogger('security')

# Rate limiter en memoria - caché para evitar queries a BD
email_request_cache = {}  # {email: [timestamp1, timestamp2, ...]}
def create_app(config_class=Config):
    """Factory function para crear la aplicación Flask"""

    # Crear la instancia de Flask
    app = Flask(__name__)

    # Cargar la configuración 
    app.config.from_object(config_class)

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    sess.init_app(app)

    # Configuración de CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:4200",
                "http://127.0.0.1:4200",
                "https://localhost:4200", 
                "https://127.0.0.1:4200",
                "http://localhost:4000",
                "http://127.0.0.1:4000",
                "https://carlosjsanchezdev.vercel.app",
                "https://my-port-folio-n6vb.onrender.com"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "supports_credentials": True  # Necesario para sesiones
        }
    })

    # Headers de seguridad Globales
    @app.after_request
    def security_headers(response):
        """Agregar headers de seguridad a todas las responses"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    # Rate limiting básico
    request_log = defaultdict(list)

    @app.before_request
    def rate_limiting():
        """Rate limiting básico para prevenir abusos"""
        if request.path.startswith('/api/'):
            client_ip = request.remote_addr
            now = datetime.now()

            # Limpiar requests antiguos (Últimos 5 minutos)
            request_log[client_ip] = [req_time for req_time in request_log[client_ip] 
                                    if now - req_time < timedelta(minutes=5)]

            # Limitar a 100 requests cada 5 minutos
            if len(request_log[client_ip]) >= 100:
                security_logger.warning(f"Rate limit exceeded for {client_ip}")
                return jsonify({
                    "error": "Too Many Requests",
                    "message": "Rate limit exceeded. Try again later."
                }), 429
            request_log[client_ip].append(now)

    # Middleware de seguridad simplificado
    @app.before_request
    def security_checks():
        """Middleware para filtrado básico de requests"""
        
        # Solo log, sin bloquear (para desarrollo)
        security_logger.info(f"Request: {request.method} {request.path} - From: {request.remote_addr}")

    # ✅ RUTAS PRINCIPALES - Solo definidas aquí
    @app.route('/')
    def home():
        return jsonify({
            "message": "¡Backend del Portfolio funcionando correctamente!",
            "status": "success",
            "endpoints": {
                "projects": "/api/projects",
                "blog": "/api/blog", 
                "contact": "/api/contact"
            }
        })

    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "portfolio-backend",
            "timestamp": datetime.utcnow().isoformat()
        })

    @app.route('/favicon.ico')
    def favicon():
        return '', 204

    @app.route('/robots.txt')
    def robots_txt():
        return """User-agent: *
Disallow: /api/
Disallow: /admin/
Allow: /$
""", 200, {'Content-Type': 'text/plain'}

    # Registrar blueprints
    register_blueprints(app)

    # Manejo de errores globales
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "error": "Endpoint Not Found",
            "message": "The requested URL was not found on the server.",
            "path": request.path,
            "status": 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal Server Error", 
            "message": "An unexpected error occurred. Please try again later.",
            "status": 500
        }), 500

    # Crear tablas en la BD
    with app.app_context():
        db.create_all()
        
    return app

def register_blueprints(app):
    """Registrar todos los blueprints"""
    from app.routes.projects import bp as projects_bp
    from app.routes.blog import bp as blog_bp
    from app.routes.contact import bp as contact_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.protected import bp as protected_bp

    # Registrar blueprints
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(blog_bp, url_prefix='/api/blog')
    app.register_blueprint(contact_bp, url_prefix='/api/contact')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(protected_bp, url_prefix='/api/protected')