from flask import Blueprint, jsonify, request
from app.models.projects import Project
from app import db

bp = Blueprint('projects', __name__)

@bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify({'projects': [p.to_dict() for p in projects]})

@bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()
    required_fields = ['title', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    project = Project(
        title=data['title'],
        description=data['description'],
        github_url=data.get('github_url'),
        live_demo_url=data.get('live_demo_url'),
        technologies=','.join(data.get('technologies', [])),
        featured_image=data.get('featured_image')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({'project': project.to_dict()}), 201
