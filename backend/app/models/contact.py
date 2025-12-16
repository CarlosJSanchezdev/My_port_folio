from app import db 
from datetime import datetime

class ContactMessage(db.Model): # Modelo para los mensajes de contacto

    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Campos de verificación
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    verification_level = db.Column(db.Integer, default=1)  # 1=anonymous, 2=verified, 3=premium
    verified_email = db.Column(db.String(100))
    
    # Relación con User
    user = db.relationship('User', backref='contact_messages')

    def __repr__(self):
        return f'<ContactMessage from {self.name}>'

    def to_dict(self): #convertir el modelo a diccionario par JSON
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'verification_level': self.verification_level,
            'verified_email': self.verified_email,
            'user_id': self.user_id
        }