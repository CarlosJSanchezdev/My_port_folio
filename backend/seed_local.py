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
                title="Construyendo Aplicaciones Modernas con Angular 19",
                slug="angular-19-aplicaciones-modernas",
                content="""Angular 19 trae consigo una serie de mejoras significativas que transforman la forma en que desarrollamos aplicaciones web. En este artículo, exploraremos las características más destacadas y cómo implementarlas en tus proyectos.

**Standalone Components**
Una de las mejoras más importantes es la consolidación de los componentes standalone, que simplifican la arquitectura de las aplicaciones eliminando la necesidad de módulos NgModule en muchos casos.

**Mejoras en el Rendimiento**
Angular 19 incluye optimizaciones en el change detection y mejoras en el compilador que resultan en aplicaciones más rápidas y eficientes.

**Server-Side Rendering (SSR)**
El SSR ha sido mejorado significativamente, ofreciendo mejor rendimiento y una experiencia de desarrollo más fluida.

**Conclusión**
Angular 19 representa un gran paso adelante en el ecosistema de desarrollo web, ofreciendo herramientas más potentes y una mejor experiencia para los desarrolladores.""",
                excerpt="Descubre las nuevas características de Angular 19 y cómo aprovecharlas para crear aplicaciones web más rápidas y eficientes.",
                tags="Angular,TypeScript,Web Development",
                read_time=5,
                published=True
            ),
            BlogPost(
                title="React Native vs Flutter: ¿Cuál Elegir en 2025?",
                slug="react-native-vs-flutter-2025",
                content="""El desarrollo móvil multiplataforma ha evolucionado significativamente. Tanto React Native como Flutter ofrecen ventajas únicas. Analicemos cada uno.

**React Native**
- Basado en JavaScript/TypeScript
- Gran ecosistema y comunidad
- Ideal si ya conoces React
- Excelente para aplicaciones con mucha lógica de negocio

**Flutter**
- Basado en Dart
- Rendimiento nativo superior
- Widgets personalizables
- Mejor para aplicaciones con UI compleja

**Mi Recomendación**
Para proyectos con equipos JavaScript existentes, React Native es ideal. Para aplicaciones que requieren UI altamente personalizada y rendimiento óptimo, Flutter es la mejor opción.""",
                excerpt="Comparativa detallada entre React Native y Flutter para ayudarte a decidir la mejor opción para tu próximo proyecto móvil.",
                tags="React Native,Flutter,Mobile Development",
                read_time=7,
                published=True
            ),
            BlogPost(
                title="FastAPI: El Framework Python para APIs Modernas",
                slug="fastapi-framework-python-moderno",
                content="""FastAPI ha revolucionado el desarrollo de APIs en Python. Su combinación de velocidad, facilidad de uso y características modernas lo hace ideal para proyectos de cualquier escala.

**Características Principales**
- Validación automática de datos con Pydantic
- Documentación automática con Swagger/OpenAPI
- Rendimiento comparable a NodeJS y Go
- Type hints nativos de Python

**Ventajas sobre Flask**
Aunque Flask es excelente, FastAPI ofrece:
- Mejor rendimiento
- Validación de datos integrada
- Async/await nativo
- Documentación automática

**Cuándo Usar FastAPI**
- APIs REST modernas
- Microservicios
- Aplicaciones que requieren alto rendimiento
- Proyectos que necesitan documentación automática

FastAPI es mi elección para nuevos proyectos backend en Python.""",
                excerpt="Aprende por qué FastAPI se ha convertido en la opción preferida para construir APIs REST de alto rendimiento con Python.",
                tags="Python,FastAPI,API Development",
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
