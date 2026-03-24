"""
Servicio de JWT para autenticación sin sesiones
"""
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app, g

SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.getenv('SECRET_KEY', 'dev-secret-key'))
ALGORITHM = 'HS256'
TOKEN_EXPIRY_HOURS = 720  # 30 días

def generate_token(user_id: int, email: str, access_level: int) -> str:
    """Genera un token JWT para el usuario"""
    payload = {
        'user_id': user_id,
        'email': email,
        'access_level': access_level,
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """Decodifica y valida un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Buscar token en header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'success': False, 'error': 'Token requerido'}), 401
        
        payload = decode_token(token)
        if not payload:
            return jsonify({'success': False, 'error': 'Token inválido o expirado'}), 401
        
        # Guardar info del usuario en g para usar en la ruta
        g.user_id = payload['user_id']
        g.email = payload['email']
        g.access_level = payload['access_level']
        
        return f(*args, **kwargs)
    
    return decorated
