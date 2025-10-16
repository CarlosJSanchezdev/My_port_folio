from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
import re
import logging


#inicializar extensiones

db = SQLAlchemy()
migrate = Migrate()


#Configuracion del logger para seguridad 
security_logger = logging.getLogger('security')

def create_app():
    """Factory function para crear la aplicacion Flask"""

    #crear la instancia de Flask
    app = Flask(__name__)

    #Cargar la configuracion 
    app.config.from_object(Config)

    #Middleware de seguridad 
    @app.before_request
    def security_checks():
        #log de requests para analisis
        security_logger.info(f"Request: {request.method} {request.path} - From: {request.remote_addr} -User-Agent: {request.user_agent}")

        #Detectar y bloquear requests SSL/https mal formados
        if request.environ.get('SERVER_PROTOCOL', '').startswith('HTTP/') and any(char in request.data.decode('latin-1') for char in ['\x16', '\x03', '\x01']):
            security_logger.warning(f"SSl malformed request blocked from {request.remote_addr}")
            return jsonify({
                 "error": "Bad Request",
                 "message": "Invalid request protocol"
            }), 400
    
        #Validate User-Agent
        user_agent = str(request.user_agent)
        suspicious_agents = [
            'nikto','sqlmap','nmap','metasploit','acunetis','nessus','openvas','w3af','zap','burp','fiddler',
            'httprecon','whatweb','dirbuster','dirb','gobuster','wfuzz','hydra','medusa','john the ripper'
        ]
        if not user_agent or user_agent == 'Python-urllib':
            security_logger.warning(f"Request without User-Agent from {request.remote_addr}")
            return jsonify({
                "error": "Bad Request",
                "message": "User-Agent header required"
            }),400
        if any(bot in user_agent.lower() for bot in suspicious_agents):
            security_logger.warning(f"Suspicious User-Agent blocked: {user_agent} from {request.remote_addr}")
            return jsonify({
                "error": "Forbidden",
                "message": "Suspicious activity detected"
            }),403
        
        #Validar metodos http permitidos Solo permitir GET, POST, PUT, DELETE, OPTIONS 
        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
        if request.method not in allowed_methods:
            security_logger.warning(f"Invalid HTTP method: {request.method} from {request.remote_addr}")
            return jsonify({
                "error": "Method Not Allowed",
                "message": f"Method  {request.method} not suported"
            }), 405
        
        #Validar  contenido de para requests post/put
        if request.method in ['POST', 'PUT']:
            if  not request.is_json and request.content_type != 'application/json':
                security_logger.warning(f"Invalid content type {request.content_type} from {request.remote_addr}")
                return jsonify({
                    "error": "Unsupported Media Type",
                    "message": "Content-Type must be application/json"
                }), 415     


    #inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)

    #Configracion desde CORS de manera obusta y segura
    CORS(app, resources={
        r"/api/*":{
            "origins":[
                "http://localhost:4200",
                "http://127.0.0.1:4200",
                "https://localhost:4200",
                "https://127.0.0.1:4200"
            ],
            "methods":["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers":["Content-Type", "Authorization", "Accept"],
            "expose_headers":["Content-Range", "X-Total-Count"],
            "supports_credentials":False,
            "max_age":3600
        }
    })

    # Header de seguridad Globales

    @app.after_request
    def security_headers(response):
        "Agregar heders de seguridad a todas las responses"

        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "'default-src 'self'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        #Headers  CORS especificos
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
        response.headers['Access-Control-Allow-Credentials'] = 'false'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization,'

        return response

        # Rate limiting basico
        from colections import defaultdict
        from datetime import datetime, timedelta
        request_log = defaultdict(list)

        @app.before_request
        def rate_limiting():
            "Rate limitng basico para prevenir abusos"
            if request.path.startswith('/api/'):
                cliente_ip = request.remote_addr
                now = datetime.now()

                #Limpiar requests antiguos(Ultimos 5 minutos)
                request_log[client_ip] = [req_time for req_time in request_log[client_ip] if now - req_time < timedelta(minutes=5)]

                #Limitar a 100 requests cada 5 minutos
                if len(request_log[client_ip]) >= 100:
                    security_logger.warning(f"Rate limit exceeded for {client_ip}")
                    return jsonify({
                        "error": "Too Many Requests",
                        "message": "Rate limit exceeded. Try again later."
                    }), 429
                request_log[client_ip].append(now)
      
  

    #Importar y registrar blueprints
    register_blueprints(app)

    #Manejo de errores globales
    @app.errorhandler(404)
    def not_found_error(error):
        security_logger.info(f"404 Not Found: {request.path} from {request.remote_addr}")
        return jsonify({
            "error": "Endpoint Not Found",
            "message": "The requested URL was not found on the server.",
            "path": request.path,
            "status": 404
        }),404

    @app.errorhandler(500)
    def internal_error(error):
        security_logger.error(f"500 Internal Server Error: {request.path} from {request.remote_addr} - Error: {str(error)}")
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "status": 500
        }),500

    @app.errorhandler(405)
    def method_not_allowed(error):
        security_logger.warning(f"405 Method Not Allowed: {request.method} {request.path}")
        return jsonify({
            "error": "Method Not Allowed",
            "message": f"The method {request.method} is not allowed for the requested URL.",
            "status": 405
        }),405

    #Endopoint especifico para manejar favicon.ico
    @app.route('/favicon.ico')
    def favicon():
        return '', 204
    
    #endopornt para robots.txt
    @app.route('/robots.txt')
    def robots_txt():
        return "User-agent: *\nDisallow: /api/\n", 200, {'Content-Type': 'text/plain'}

    #crear tablas en la bd
    with app.app_context():
        db.create_all()
    return app


def register_blueprints(app):
    from app.routes.projects import bp as projects_bp
    from app.routes.blog import bp as blog_bp
    from app.routes.contact import bp as contact_bp

    #Registrar blueprints con prefijo /api
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(blog_bp, url_prefix='/api/blog')
    app.register_blueprint(contact_bp, url_prefix='/api/contact')