from app import db

class OwnerInfo(db.Model):
    """Modelo para información del propietario con niveles de acceso"""
    
    __tablename__ = 'owner_info'
    
    id = db.Column(db.Integer, primary_key=True)
    info_key = db.Column(db.String(50), unique=True, nullable=False)
    info_value = db.Column(db.Text, nullable=False)
    info_type = db.Column(db.String(50))  # 'phone', 'whatsapp', 'calendar', 'text', etc.
    required_level = db.Column(db.Integer, default=1)  # 1=public, 2=verified, 3=premium
    display_label = db.Column(db.String(100))
    icon = db.Column(db.String(50))
    order = db.Column(db.Integer, default=0)  # Para ordenar la visualización
    
    def __repr__(self):
        return f'<OwnerInfo {self.info_key} - Level {self.required_level}>'
    
    def to_dict(self):
        return {
            'key': self.info_key,
            'value': self.info_value,
            'type': self.info_type,
            'required_level': self.required_level,
            'label': self.display_label,
            'icon': self.icon,
            'order': self.order
        }
