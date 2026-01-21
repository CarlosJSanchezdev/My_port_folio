from flask import Blueprint, request, jsonify, session, current_app
from app.models.email_verification import EmailVerification
from app.models.owner_info import OwnerInfo
from app.models.user import User
from app import db
from app.utils import send_verification_email
from datetime import datetime, timedelta
import re

bp = Blueprint('auth', __name__)

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
        
        # Verificar rate limiting (máximo 3 intentos por hora)
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_attempts = EmailVerification.query.filter(
            EmailVerification.email == email,
            EmailVerification.created_at > one_hour_ago
        ).count()
        
        if recent_attempts >= 3:
            return jsonify({
                'success': False,
                'error': 'Demasiados intentos. Intenta de nuevo en 1 hora.'
            }), 429
        
        # Crear nueva verificación
        verification = EmailVerification(email=email)
        db.session.add(verification)
        db.session.commit()
        
        # Enviar email de forma asíncrona (sin bloquear)
        try:
            send_verification_email(email, name, verification.verification_code)
            # No esperamos a que se complete el envío para responder
        except Exception as e:
            # Logueamos el error pero no hacemos rollback ya que el email es asíncrono
            from flask import current_app
            current_app.logger.error(f"Email preparation failed: {str(e)}")
            # Devolvemos éxito pero advertimos posible retraso
            return jsonify({
                'success': True,
                'message': 'Solicitud procesada. El código puede tardar unos minutos en llegar.',
                'warning': 'El envío de email puede estar experimentando retrasos.',
                'expires_in': 900  # 15 minutos en segundos
            }), 202  # Accepted - procesamiento en segundo plano
        
        return jsonify({
            'success': True,
            'message': 'Código enviado a tu email',
            'expires_in': 900  # 15 minutos en segundos
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
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
            return jsonify({
                'success': False,
                'error': 'Código inválido'
            }), 400
        
        # Verificar expiración
        if verification.is_expired():
            return jsonify({
                'success': False,
                'error': 'Código expirado. Solicita uno nuevo.'
            }), 400
        
        # Incrementar intentos
        verification.attempts += 1
        
        if verification.attempts > 5:
            return jsonify({
                'success': False,
                'error': 'Demasiados intentos. Solicita un nuevo código.'
            }), 400
        
        # Marcar como verificado
        verification.verified = True
        
        # Crear o actualizar usuario
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User()
            user.email = email
            user.name = name
            user.access_level = 3  # Nivel 3 = Premium (acceso completo)
            user.last_login = datetime.utcnow()
            db.session.add(user)
        else:
            user.last_login = datetime.utcnow()
            if name and not user.name:
                user.name = name
        
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
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
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
