from flask import Blueprint, jsonify

bp = Blueprint('contact', __name__)

@bp.route('/', methods=['GET'])
def get_contacts():
    # Ejemplo de respuesta, puedes conectar con tu modelo ContactMessage
    return jsonify({'contacts': []})
