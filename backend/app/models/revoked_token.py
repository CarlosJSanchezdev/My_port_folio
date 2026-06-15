from app import db
from datetime import datetime, timedelta

class RevokedToken(db.Model):
    """Modelo para tokens revocados (blacklist)"""
    
    __tablename__ = 'revoked_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False, index=True)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<RevokedToken {self.jti}>'
    
    @staticmethod
    def is_revoked(jti: str) -> bool:
        """Verifica si un token está en la blacklist"""
        return db.session.query(
            db.exists().where(RevokedToken.jti == jti)
        ).scalar()
    
    @staticmethod
    def add(jti: str, expires_at: datetime):
        """Agrega un token a la blacklist"""
        revoked = RevokedToken(jti=jti, expires_at=expires_at)
        db.session.add(revoked)
        db.session.commit()
    
    @staticmethod
    def cleanup():
        """Limpia tokens expirados de la blacklist"""
        RevokedToken.query.filter(RevokedToken.expires_at < datetime.utcnow()).delete()
        db.session.commit()
