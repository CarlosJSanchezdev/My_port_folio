from flask import Blueprint, request, jsonify
from app.models.contact import ContactMessage
from app import db
import re

bp = Blueprint('contact', __name__)

@bp.route('/', methods=['POST'])
def create_contact_message():
    try:
        data = request.get_json()
        
        # Validaciones
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({
                "success": False,
                "error": "Name, email and message are required"
            }), 400
        
        # Validar email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, data['email']):
            return jsonify({
                "success": False,
                "error": "Invalid email format"
            }), 400
        
        message = ContactMessage(
            name=data['name'],
            email=data['email'],
            subject=data.get('subject', ''),
            message=data['message']
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Aquí podrías agregar envío de email de notificación
        
        return jsonify({
            "success": True,
            "data": message.to_dict(),
            "message": "Message sent successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/', methods=['GET'])
def get_contact_messages():
    try:
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        return jsonify({
            "success": True,
            "data": [message.to_dict() for message in messages],
            "count": len(messages)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/<int:message_id>/read', methods=['PUT'])
def mark_as_read(message_id):
    try:
        message = ContactMessage.query.get_or_404(message_id)
        message.read = True
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": message.to_dict(),
            "message": "Message marked as read"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500