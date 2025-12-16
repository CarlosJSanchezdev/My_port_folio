from app import db
from datetime import datetime

class User(db.Model):
    """Modelo para usuarios verificados y premium"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100))
    
    # LinkedIn data (optional - for premium level 3)
    linkedin_id = db.Column(db.String(100), unique=True)
    linkedin_profile_url = db.Column(db.String(200))
    linkedin_picture_url = db.Column(db.String(200))
    
    # Access level: 2=verified (email), 3=premium (LinkedIn)
    access_level = db.Column(db.Integer, default=2)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email} - Level {self.access_level}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'access_level': self.access_level,
            'linkedin_connected': self.linkedin_id is not None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
