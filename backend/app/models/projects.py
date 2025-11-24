from app import db 
from datetime import datetime

class Project(db.Model): # Modelo para los projectos del portafolio

    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_url = db.Column(db.String(200), nullable=True)
    live_demo_url = db.Column(db.String(200), nullable=True)
    technologies = db.Column(db.String(200), nullable=True)
    featured_image = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=True, default='Web')  # Web, Mobile, Backend
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'

    def to_dict(self): #convertir el modelo a diccionario par JSON
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'github_url': self.github_url,
            'live_demo_url': self.live_demo_url,
            'technologies': self.technologies.split(',') if self.technologies else [],
            'featured_image': self.featured_image,
            'category': self.category,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

