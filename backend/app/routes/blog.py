from flask import Blueprint, jsonify

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET'])
def get_blog_posts():
    # Ejemplo de respuesta, puedes conectar con tu modelo BlogPost
    return jsonify({'blog_posts': []})
