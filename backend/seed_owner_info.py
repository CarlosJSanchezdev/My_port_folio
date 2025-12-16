# Seed data for owner_info table
# Run this script to populate the owner_info table with initial data

import os
from dotenv import load_dotenv

# Load .env.local configuration
load_dotenv('.env.local', override=True)

from app import create_app, db
from app.models.owner_info import OwnerInfo

def seed_owner_info():
    """Seed owner information with different access levels"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        OwnerInfo.query.delete()
        
        # Level 1: Public information (None currently)
        public_info = []
        
        # Level 2: Verified email users (None currently)
        verified_info = []
        
        # Level 3: Premium users (Full Access)
        premium_info = [
            OwnerInfo(
                info_key='email',
                info_value='cjsatlas@hotmail.com',
                info_type='email',
                required_level=3,
                display_label='Email',
                icon='📧',
                order=1
            ),
            OwnerInfo(
                info_key='location',
                info_value='Santiago de Cali, Colombia',
                info_type='location',
                required_level=3,
                display_label='Ubicación',
                icon='📍',
                order=2
            ),
            OwnerInfo(
                info_key='phone',
                info_value='+573176913321',
                info_type='phone',
                required_level=3,
                display_label='Teléfono',
                icon='📱',
                order=3
            ),
            OwnerInfo(
                info_key='whatsapp',
                info_value='573176913321',
                info_type='whatsapp',
                required_level=3,
                display_label='WhatsApp',
                icon='💬',
                order=4
            ),
            OwnerInfo(
                info_key='hours',
                info_value='Lun - Vie: 9:00 AM - 6:00 PM',
                info_type='hours',
                required_level=3,
                display_label='Horario',
                icon='⏰',
                order=5
            ),
            OwnerInfo(
                info_key='cv_download',
                info_value='/assets/cv/carlos_sanchez_cv.pdf',
                info_type='file',
                required_level=3,
                display_label='CV Descargable',
                icon='📄',
                order=6
            ),
            OwnerInfo(
                info_key='portfolio_private',
                info_value='/portfolio/private',
                info_type='link',
                required_level=3,
                display_label='Portafolio Privado',
                icon='🔐',
                order=7
            ),
        ]
        
        # Add all info to database
        for info in public_info + verified_info + premium_info:
            db.session.add(info)
        
        db.session.commit()
        
        print("✅ Owner info seeded successfully!")
        print(f"   - {len(public_info)} public items (Level 1)")
        print(f"   - {len(verified_info)} verified items (Level 2)")
        print(f"   - {len(premium_info)} premium items (Level 3)")

if __name__ == '__main__':
    seed_owner_info()
