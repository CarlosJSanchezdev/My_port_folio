# app/seed.py
from app import create_app, db
from app.models.projects import Project
from app.models.blog import BlogPost
from datetime import datetime

def seed_database():
    """Seed database with real portfolio data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing tables
        print("🗑️  Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Real Projects from portfolio.config.ts
        projects = [
            Project(
                title="My Portfolio",
                description="Portafolio profesional con Angular 19 y diseño moderno",
                github_url="https://github.com/CarlosJSanchezdev/My_port_folio",
                live_demo_url="",
                technologies="Angular 19,TypeScript,CSS,SSR",
                featured_image="/assets/projects/portfolio.png",
                category="Web",
                is_featured=True
            ),
            Project(
                title="Comai",
                description="Aplicación móvil de recetas inteligentes con IA y delivery multi-proveedor (En Desarrollo)",
                github_url="https://github.com/CarlosJSanchezdev/Comai",
                live_demo_url="",
                technologies="React Native,TypeScript,Supabase,OpenAI GPT-4,PostgreSQL,Expo",
                featured_image="/assets/projects/comai.png",
                category="Mobile",
                is_featured=True
            ),
            Project(
                title="App Message",
                description="Sistema de mensajería con FastAPI y arquitectura moderna (En Desarrollo)",
                github_url="https://github.com/CarlosJSanchezdev/app_message",
                live_demo_url="",
                technologies="Python,FastAPI,SQLAlchemy,SQLite,WebSockets",
                featured_image="/assets/projects/app-message.png",
                category="Backend",
                is_featured=True
            ),
            Project(
                title="Salon Scheduler",
                description="Sistema de gestión de citas para salones de belleza (En Desarrollo)",
                github_url="https://github.com/CarlosJSanchezdev/salon_scheduler",
                live_demo_url="",
                technologies="Python,Flask,SQLite,HTML,CSS,JavaScript",
                featured_image="/assets/projects/salon-scheduler.png",
                category="Web",
                is_featured=False
            ),
            Project(
                title="URL Shortener",
                description="Acortador de URLs con análisis de estadísticas (En Desarrollo)",
                github_url="https://github.com/CarlosJSanchezdev/url_shortener",
                live_demo_url="",
                technologies="Python,Flask,SQLite,REST API",
                featured_image="/assets/projects/url-shortener.png",
                category="Backend",
                is_featured=False
            ),
            Project(
                title="WorkList",
                description="Aplicación de gestión de tareas y productividad (En Desarrollo)",
                github_url="https://github.com/CarlosJSanchezdev/workList",
                live_demo_url="",
                technologies="JavaScript,Node.js,Express,MongoDB",
                featured_image="/assets/projects/worklist.png",
                category="Web",
                is_featured=False
            ),
            Project(
                title="San Rafael Desarrollo",
                description="Plataforma web corporativa con múltiples servicios (En Desarrollo)",
                github_url="https://github.com/CarlosJSanchezdev/San_Rafael_desarrollo",
                live_demo_url="",
                technologies="Python,Flask,PostgreSQL,HTML,CSS",
                featured_image="/assets/projects/san-rafael.png",
                category="Web",
                is_featured=False
            ),
            Project(
                title="Frontend COMS",
                description="Frontend para sistema de comunicaciones (En Desarrollo)",
                github_url="https://github.com/CarlosJSanchezdev/frontend-coms",
                live_demo_url="",
                technologies="React,TypeScript,Tailwind CSS",
                featured_image="/assets/projects/frontend-coms.png",
                category="Web",
                is_featured=False
            )
        ]
        
        # Blog posts
        blog_posts = [
            BlogPost(
                title="Construyendo Aplicaciones Modernas con Angular 19",
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
                slug="angular-19-aplicaciones-modernas",
                featured_image="/assets/blog/angular-19.png",
                published=True,
                tags="Angular,TypeScript,Web Development",
                read_time=5,
                published_at=datetime(2025, 1, 15)
            ),
            BlogPost(
                title="React Native vs Flutter: ¿Cuál Elegir en 2025?",
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
                slug="react-native-vs-flutter-2025",
                featured_image="/assets/blog/react-native-flutter.png",
                published=True,
                tags="React Native,Flutter,Mobile Development",
                read_time=7,
                published_at=datetime(2025, 1, 10)
            ),
            BlogPost(
                title="FastAPI: El Framework Python para APIs Modernas",
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
                slug="fastapi-framework-python-moderno",
                featured_image="/assets/blog/fastapi.png",
                published=True,
                tags="Python,FastAPI,API Development",
                read_time=6,
                published_at=datetime(2025, 1, 5)
            )
        ]
        
        # Add to database
        db.session.add_all(projects)
        db.session.add_all(blog_posts)
        db.session.commit()
        
        print("✅ Base de datos sembrada exitosamente!")
        print(f"📁 Proyectos creados: {len(projects)}")
        print(f"📝 Posts de blog creados: {len(blog_posts)}")
        print("\n🎯 Próximos pasos:")
        print("1. Inicia el backend: cd backend && python run.py")
        print("2. Inicia el frontend: ng serve")
        print("3. Visita: http://localhost:4200")

if __name__ == '__main__':
    seed_database()