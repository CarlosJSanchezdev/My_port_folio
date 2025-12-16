"""
Script para correr el backend localmente con SQLite
Usa .env.local en lugar de .env
"""
import os
from dotenv import load_dotenv

# Cargar SOLO .env.local (ignorar .env)
load_dotenv('.env.local', override=True)

from app import create_app

# Crear la aplicación Flask
app = create_app()

if __name__ == '__main__':
    # Obtener puerto de environment variable o usar 5001 por defecto 
    port = int(os.environ.get('PORT', 5001))
    print(f"\n🚀 Backend corriendo en modo LOCAL con SQLite")
    print(f"📍 URL: http://localhost:{port}")
    print(f"💾 Base de datos: SQLite (instance/portfolio_local.db)\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
