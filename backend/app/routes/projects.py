from flask import Blueprint, request, jsonify
from app.models.projects import Project
from app import db

bp = Blueprint('projects', __name__)

@bp.route('/', methods=['GET'])
def get_projects():
    try:
        # Filtros opcionales
        category = request.args.get('category')
        featured = request.args.get('featured')
        
        query = Project.query
        
        if category:
            query = query.filter_by(category=category)
        if featured:
            query = query.filter_by(is_featured=True)
            
        projects = query.order_by(Project.created_at.desc()).all()
        
        return jsonify({
            "success": True,
            "data": [project.to_dict() for project in projects],
            "count": len(projects)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/', methods=['POST'])
def create_project():
    try:
        data = request.get_json()
        
        # Validación básica
        if not data.get('title') or not data.get('description'):
            return jsonify({
                "success": False,
                "error": "Title and description are required"
            }), 400
        
        project = Project(
            title=data['title'],
            description=data['description'],
            github_url=data.get('github_url'),
            live_demo_url=data.get('live_demo_url'),
            technologies=','.join(data.get('technologies', [])),
            featured_image=data.get('featured_image'),
            category=data.get('category', 'web'),
            is_featured=data.get('is_featured', False)
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": project.to_dict(),
            "message": "Project created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        return jsonify({
            "success": True,
            "data": project.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404

@bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        data = request.get_json()
        
        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        project.github_url = data.get('github_url', project.github_url)
        project.live_demo_url = data.get('live_demo_url', project.live_demo_url)
        project.featured_image = data.get('featured_image', project.featured_image)
        project.category = data.get('category', project.category)
        project.is_featured = data.get('is_featured', project.is_featured)
        
        if 'technologies' in data:
            project.technologies = ','.join(data['technologies'])
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": project.to_dict(),
            "message": "Project updated successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Project deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500