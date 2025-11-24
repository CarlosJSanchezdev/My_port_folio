from flask import Blueprint, request, jsonify
from app.models.blog import BlogPost
from app import db
from datetime import datetime

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET'])
def get_blog_posts():
    try:
        # Filtros
        published_only = request.args.get('published', 'true').lower() == 'true'
        tag = request.args.get('tag')
        
        query = BlogPost.query
        
        if published_only:
            query = query.filter_by(published=True)
            
        if tag:
            query = query.filter(BlogPost.tags.contains(tag))
            
        posts = query.order_by(BlogPost.published_at.desc()).all()
        
        return jsonify({
            "success": True,
            "data": [post.to_dict() for post in posts],
            "count": len(posts)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/', methods=['POST'])
def create_blog_post():
    try:
        data = request.get_json()
        
        if not data.get('title') or not data.get('content'):
            return jsonify({
                "success": False,
                "error": "Title and content are required"
            }), 400
        
        # Generar slug automáticamente si no se proporciona
        slug = data.get('slug')
        if not slug:
            slug = data['title'].lower().replace(' ', '-')
        
        post = BlogPost(
            title=data['title'],
            content=data['content'],
            excerpt=data.get('excerpt', data['content'][:297] + '...'),
            slug=slug,
            featured_image=data.get('featured_image'),
            published=data.get('published', False),
            tags=','.join(data.get('tags', [])),
            read_time=data.get('read_time', 5)
        )
        
        if post.published and not post.published_at:
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": post.to_dict(),
            "message": "Blog post created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/<slug>', methods=['GET'])
def get_blog_post(slug):
    try:
        post = BlogPost.query.filter_by(slug=slug).first_or_404()
        return jsonify({
            "success": True,
            "data": post.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Post not found"
        }), 404