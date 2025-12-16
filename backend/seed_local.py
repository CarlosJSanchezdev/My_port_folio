"""
Script para poblar la base de datos LOCAL con datos de prueba
Usa .env.local para conectarse a SQLite
"""
import os
from dotenv import load_dotenv

# Cargar SOLO .env.local (ignorar .env)
load_dotenv('.env.local', override=True)

from app import create_app, db
from app.models.projects import Project
from app.models.blog import BlogPost

def seed_local_db():
    app = create_app()
    
    with app.app_context():
        # Limpiar datos existentes
        print("🗑️  Limpiando base de datos local...")
        db.drop_all()
        db.create_all()
        
        # Crear proyectos de prueba
        print("📦 Creando proyectos...")
        projects = [
            Project(
                title="My Portfolio",
                description="Portafolio profesional con Angular 19 y diseño moderno",
                technologies="Angular 19,TypeScript,CSS,SSR",
                github_url="https://github.com/CarlosJSanchezdev/My_port_folio",
                live_demo_url="https://my-port-folio-8510.vercel.app",
                featured_image="/assets/projects/portfolio.png",
                category="Web",
                is_featured=True
            ),
            Project(
                title="Comai",
                description="Aplicación móvil de recetas inteligentes con IA (En Desarrollo)",
                technologies="React Native,TypeScript,Supabase,OpenAI GPT-4",
                github_url="https://github.com/CarlosJSanchezdev/Comai",
                live_demo_url="",
                featured_image="/assets/projects/comai.png",
                category="Mobile",
                is_featured=True
            ),
            Project(
                title="App Message",
                description="Sistema de mensajería con FastAPI (En Desarrollo)",
                technologies="Python,FastAPI,SQLAlchemy,WebSockets",
                github_url="https://github.com/CarlosJSanchezdev/app_message",
                live_demo_url="",
                featured_image="/assets/projects/app-message.png",
                category="Backend",
                is_featured=True
            ),
        ]
        
        for project in projects:
            db.session.add(project)
        
        # Crear posts de blog de prueba
        print("📝 Creando posts de blog...")
        blog_posts = [
            BlogPost(
                title="El Futuro del Desarrollo Web con Angular 19",
                slug="angular-19-futuro-desarrollo-web",
                content="Angular 19 marca un hito importante en la evolución del framework...",
                excerpt="Descubre las nuevas características de Angular 19",
                tags="Angular,Frontend,Web Development",
                read_time=5,
                published=True
            ),
            BlogPost(
                title="React Native vs Flutter en 2025",
                slug="react-native-vs-flutter-2025",
                content="La batalla por el desarrollo móvil multiplataforma continúa...",
                excerpt="Comparativa detallada para tu próximo proyecto móvil",
                tags="React Native,Flutter,Mobile",
                read_time=7,
                published=True
            ),
            BlogPost(
                title="Microservicios con FastAPI y Python",
                slug="microservicios-fastapi-python",
                content="FastAPI se ha convertido en el estándar de facto para APIs en Python...",
                excerpt="Aprende a construir APIs de alto rendimiento",
                tags="Python,FastAPI,Backend",
                read_time=6,
                published=True
            ),
        ]
        
        for post in blog_posts:
            db.session.add(post)
        
        # Guardar cambios
        db.session.commit()
        
        print("✅ Base de datos local poblada exitosamente!")
        print(f"   - {len(projects)} proyectos creados")
        print(f"   - {len(blog_posts)} posts de blog creados")
        print("\n🚀 Tu backend local está listo para usar!")

if __name__ == '__main__':
    seed_local_db()
