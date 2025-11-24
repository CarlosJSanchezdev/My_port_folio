from app import db 
from datetime import datetime

class BlogPost(db.Model): # Modelo para los blogposts del portafolio

    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(200), nullable=True)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    featured_image = db.Column(db.String(200), nullable=True)
    published = db.Column(db.Boolean, default=False)    
    published_at = db.Column(db.DateTime, nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    read_time = db.Column(db.Integer, default=5)  # Tiempo de lectura en minutos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

    def to_dict(self): #convertir el modelo a diccionario par JSON
         return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'excerpt': self.excerpt,
            'slug': self.slug,
            'featured_image': self.featured_image,
            'published': self.published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'tags': self.tags.split(',') if self.tags else [],
            'read_time': self.read_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
