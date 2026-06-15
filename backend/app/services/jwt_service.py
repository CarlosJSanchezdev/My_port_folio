"""
Servicio de JWT para autenticación sin sesiones
"""
import os
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app, g

SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY o SECRET_KEY debe estar configurado en variables de entorno")

ALGORITHM = 'HS256'
TOKEN_EXPIRY_HOURS = 720  # 30 días

def generate_token(user_id: int, email: str, access_level: int) -> tuple:
    """Genera un token JWT para el usuario. Retorna (token, jti)"""
    jti = str(uuid.uuid4())
    exp = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    payload = {
        'user_id': user_id,
        'email': email,
        'access_level': access_level,
        'jti': jti,
        'exp': exp,
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, exp

def decode_token(token: str) -> dict:
    """Decodifica y valida un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verificar si el token está en la blacklist
        from app.models.revoked_token import RevokedToken
        if RevokedToken.is_revoked(payload.get('jti')):
            current_app.logger.warning(f"Token revocado: {payload.get('jti')}")
            return None
        
        return payload
    except jwt.ExpiredSignatureError:
        current_app.logger.warning("Token expirado")
        return None
    except jwt.InvalidTokenError as e:
        current_app.logger.warning(f"Token inválido: {str(e)}")
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
