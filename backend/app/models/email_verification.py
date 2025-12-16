from app import db
from datetime import datetime, timedelta
import random
import string

class EmailVerification(db.Model):
    """Modelo para gestionar verificaciones de email"""
    
    __tablename__ = 'email_verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, index=True)
    verification_code = db.Column(db.String(6), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    attempts = db.Column(db.Integer, default=0)
    
    def __init__(self, email):
        self.email = email
        self.verification_code = self.generate_code()
        self.expires_at = datetime.utcnow() + timedelta(minutes=15)
    
    @staticmethod
    def generate_code():
        """Genera código de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """Verifica si el código ha expirado"""
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f'<EmailVerification {self.email} - {"verified" if self.verified else "pending"}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'verified': self.verified,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'attempts': self.attempts
        }
