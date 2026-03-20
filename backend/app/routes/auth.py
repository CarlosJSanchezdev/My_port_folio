from flask import Blueprint, request, jsonify, session, current_app
from app.models.email_verification import EmailVerification
from app.models.owner_info import OwnerInfo
from app.models.user import User
from app import db
from app.services.email_service import send_verification_email
from datetime import datetime, timedelta
import re

bp = Blueprint('auth', __name__)

# Rate limiting simple en memoria (para producción usar Redis)
email_request_cache = {}
RATE_LIMIT_WINDOW = 3600  # 1 hora
MAX_EMAIL_REQUESTS = 5  # 5 solicitudes por hora


@bp.route('/request-verification', methods=['POST'])
def request_verification():
    """Solicita código de verificación por email"""
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name', 'Usuario')

        # Validar email
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({
                'success': False,
                'error': 'Email inválido'
            }), 400

        # Rate limiting simple
        now = datetime.utcnow()
        if email in email_request_cache:
            # Limpiar solicitudes antiguas
            email_request_cache[email] = [
                ts for ts in email_request_cache[email]
                if (now - ts).total_seconds() < RATE_LIMIT_WINDOW
            ]
            
            if len(email_request_cache[email]) >= MAX_EMAIL_REQUESTS:
                oldest = email_request_cache[email][0]
                retry_after = int(RATE_LIMIT_WINDOW - (now - oldest).total_seconds())
                return jsonify({
                    'success': False,
                    'error': f'Demasiados intentos. Intenta en {retry_after // 60} minutos.'
                }), 429
        else:
            email_request_cache[email] = []

        # Registrar esta solicitud
        email_request_cache[email].append(now)

        # Crear nueva verificación
        verification = EmailVerification(email=email)
        db.session.add(verification)
        db.session.commit()

        # Enviar email con Resend
        try:
            send_verification_email(email, name, verification.verification_code)
        except Exception as e:
            current_app.logger.error(f"Email send failed: {str(e)}")
            # No fallamos la request, pero informamos
            return jsonify({
                'success': True,
                'message': 'Código generado. Si no llega en 1 minuto, revisa spam o solicita otro.',
                'warning': 'Posible retraso en envío de email.'
            }), 202

        return jsonify({
            'success': True,
            'message': 'Código enviado a tu email',
            'expires_in': 600  # 10 minutos
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in request_verification: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al procesar la solicitud. Intenta más tarde.'
        }), 500

@bp.route('/verify-code', methods=['POST'])
def verify_code():
    """Verifica el código ingresado"""
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')
        name = data.get('name', 'Usuario')
        
        if not email or not code:
            return jsonify({
                'success': False,
                'error': 'Email y código son requeridos'
            }), 400
        
        # Buscar verificación más reciente no verificada
        verification = EmailVerification.query.filter_by(
            email=email,
            verification_code=code,
            verified=False
        ).order_by(EmailVerification.created_at.desc()).first()
        
        if not verification:
            current_app.logger.warning(f"Invalid verification code attempt for email: {email}")
            return jsonify({
                'success': False,
                'error': 'Código inválido'
            }), 400
        
        # Verificar expiración
        if verification.is_expired():
            current_app.logger.info(f"Expired verification code for email: {email}")
            return jsonify({
                'success': False,
                'error': 'Código expirado. Solicita uno nuevo.'
            }), 400
        
        # Incrementar intentos
        verification.attempts += 1
        
        if verification.attempts > 5:
            db.session.commit()
            current_app.logger.warning(f"Too many verification attempts for email: {email}")
            return jsonify({
                'success': False,
                'error': 'Demasiados intentos. Solicita un nuevo código.'
            }), 429
        
        # Marcar como verificado
        verification.verified = True
        
        # Crear o actualizar usuario
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User()
                user.email = email
                user.name = name
                user.access_level = 3  # Nivel 3 = Premium (acceso completo)
                user.last_login = datetime.utcnow()
                db.session.add(user)
                current_app.logger.info(f"New user created: {email}")
            else:
                user.last_login = datetime.utcnow()
                if name and not user.name:
                    user.name = name
                current_app.logger.info(f"User updated: {email}")
            
            db.session.commit()
            
            # Guardar en sesión
            session['user_id'] = user.id
            session['access_level'] = user.access_level
            session['email'] = user.email
            
            return jsonify({
                'success': True,
                'message': 'Email verificado correctamente',
                'user': user.to_dict()
            }), 200
            
        except Exception as db_error:
            db.session.rollback()
            current_app.logger.error(f"Database error in verify_code: {str(db_error)}")
            return jsonify({
                'success': False,
                'error': 'Error al procesar la verificación. Intenta de nuevo más tarde.'
            }), 500
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in verify_code: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error inesperado. Por favor intenta de nuevo.'
        }), 500

@bp.route('/owner-info', methods=['GET'])
def get_owner_info():
    """Retorna información del propietario según nivel de acceso"""
    try:
        # Obtener nivel de acceso del usuario
        access_level = session.get('access_level', 1)
        
        # Obtener información según nivel
        info_items = OwnerInfo.query.filter(
            OwnerInfo.required_level <= access_level
        ).order_by(OwnerInfo.order, OwnerInfo.id).all()
        
        return jsonify({
            'success': True,
            'access_level': access_level,
            'data': [item.to_dict() for item in info_items]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/status', methods=['GET'])
def get_auth_status():
    """Verifica el estado de autenticación actual"""
    user_id = session.get('user_id')
    access_level = session.get('access_level', 1)
    
    if user_id:
        user = User.query.get(user_id)
        return jsonify({
            'authenticated': True,
            'access_level': access_level,
            'user': user.to_dict() if user else None
        }), 200
    
    return jsonify({
        'authenticated': False,
        'access_level': 1
    }), 200

@bp.route('/logout', methods=['POST'])
def logout():
    """Cierra la sesión del usuario"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Sesión cerrada correctamente'
    }), 200
