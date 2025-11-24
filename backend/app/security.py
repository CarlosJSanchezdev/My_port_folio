import re
from flask import request, jsonify
import logging

security_logger = logging.getLogger('security')

class SecurityMiddleware:
    """Middleware de seguridad para la aplicacion Flask"""
    @staticmethod
    def malicius_path(path):
        malicius_patterns = [
            r'\.\./',  # Path traversal
            r'\.env',  # Archivos de configuración
            r'wp-admin',  # WordPress
            r'phpmyadmin',  # PHPMyAdmin
            r'\.git',  # Git
            r'\.sql',  # Bases de datos
            r'admin',  # Paneles de admin
            r'config',  # Configuración
            r'backup',  # Backups
        ]
        return (any(re.search(pattern, path.lower()))for pattern in malicius_patterns)
    
    @staticmethod
    def is_suspicius_payload(data):
        """Detectar payloads sospechosos en datos"""
        if not data:
            return False
        
        suspicius_patterns = [
            r'<script', #XSS
            r'union.*select', #SQL injection
            r'exec\(', #Ejecucion de comandos
            r'base64_decode', #Codificacion sospechosa
            r'eval\(', #Javascript eval
        ]
        data_str = str(data).lower()
        return any(re.search(pattern, data_str) for pattern in suspicius_patterns)
    
    @staticmethod
    def check_request():
        """verificacion completa de seguridad en cada request"""
        client_ip = request.remote_addr
        #veriificar path malicioso
        if SecurityMiddleware.malicius_path(request.path):
            security_logger.warning(f"Request bloqueada por path malicioso desde {client_ip}: {request.path}")
            return jsonify({"error": "Request bloqueada por path malicioso"}), 403
        #verificar en post/put
        if request.method in ['POST','PUT']:
            if request.is_json and SecurityMiddleware.is_suspicius_payload(request.get_json()):
                security_logger.warning(f"Request bloqueada por payload sospechoso desde {client_ip}: {request.get_json()}")
                return jsonify({"error": "Request bloqueada por payload sospechoso"}), 403
            
            if request.form and SecurityMiddleware.is_suspicius_payload(request.form):
                security_logger.warning(f"Request bloqueada por payload sospechoso desde {client_ip}: {request.form}")
                return jsonify({"error": "Request bloqueada por payload sospechoso"}), 403
        return "OK"
# Funcion para  uso del middleware en Flask
def security_check():
    """funcion para integracion con before_request"""
    is_safe, mesage = SecurityMiddleware.check_request()
    if not is_safe:
        return jsonify({
            "error": "Security Violation",
            "message": message
        }),403
    return None
