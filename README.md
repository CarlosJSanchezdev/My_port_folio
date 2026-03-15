MyPortFolio - Portfolio Personal

Aplicación web full-stack para portfolio personal desarrollada con **Angular 19** (frontend) y **Flask** (backend).
	
## 📋 Tabla de Contenidos
	
- [Tecnologías](#-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Ejecución en Desarrollo Local](#-ejecución-en-desarrollo-local)
- [Comandos Útiles](#-comandos-útiles)
- [Documentación Adicional](#-documentación-adicional)
	
## 🛠 Tecnologías
	
### Frontend
- Angular 19.2.12
- Angular CLI
- SSR (Server-Side Rendering)
	
### Backend
- Python 3.10+
- Flask
- SQLAlchemy
- SMTP (Gmail) para envío de emails
- Alembic (migraciones de base de datos)
	
## 📁 Estructura del Proyecto
	

"""My_port_folio/
├── backend/                 # Backend Flask
│   ├── .env                # Variables de entorno (NO commit)
│   ├── .env.example        # Ejemplo de variables de entorno
│   └── .venv/              # Entorno virtual Python
├── src/                    # Código fuente Angular
├── angular.json            # Configuración de Angular
├── README.md               # Este archivo
└── .gitignore              # Archivos ignorados por Git
"""
	
## 📦 Requisitos Previos
	
### Para el Frontend
- Node.js (versión recomendada: 18.x o superior)
- npm
- Angular CLI 19.x
	
bash
npm install -g @angular/cli@19
	
### Para el Backend
- Python 3.10+
- pip
	
## ⚙️ Instalación y Configuración
	
### 1. Clonar el Repositorio
	
bash
git clone <URL_DEL_REPOSITORIO>
cd My_port_folio


## 2. Configurar el Backend
 
 bash
 cd backend
 	
 # Crear entorno virtual
 	python3 -m venv .venv
 
 # Activar entorno virtual
 # En Linux/Mac:
 source .venv/bin/activate
 # En Windows:
 .venv\Scripts\activate
 	
 # Instalar dependencias
 pip install flask sqlalchemy python-dotenv flask-mail alembic
 	
 # Copiar archivo de ejemplo de variables de entorno
 cp .env.example .env
 	
 # Editar .env con tus credenciales
 nano .env  # O usa tu editor preferido
 
 	
 #### Configurar Variables de Entorno (.env)
 	
 **Importante**: Para usar Gmail, necesitas:
 	
 1. Habilitar 2FA en tu cuenta de Google
 2. Generar una App Password en [Google App Passwords](https://myaccount.google.com/apppasswords)
 3. Usar esa contraseña (NO tu contraseña normal de Gmail)
 
 env
 # Flask Configuration
 SECRET_KEY=tu-clave-secreta-fuerte
 FLASK_ENV=development
 FLASK_DEBUG=True
 	
 # Database Configuration
 DATABASE_URL=sqlite:///portfolio.db
 
 # Email Configuration (Gmail SMTP)
 MAIL_SERVER=smtp.gmail.com
 MAIL_PORT=587
 MAIL_USE_TLS=true
 MAIL_USERNAME=tu-email@gmail.com
 MAIL_PASSWORD=tu-app-password-de-16-caracteres
 MAIL_DEFAULT_SENDER=tu-email@gmail.com
 
 	
 ### 3. Configurar el Frontend
 	
 bash
 # Volver a la raíz del proyecto
 cd ..
 
 # Instalar dependencias de Angular
 	npm install
 
 	
 ## 🚀 Ejecución en Desarrollo Local
 	
 ### Iniciar el Backend
 	
 	Abre una terminal:
 	
 bash
 cd backend
 source .venv/bin/activate  # Activar entorno virtual si no está activo
 flask run
 
 	
 El servidor backend se ejecutará en `http://localhost:5000`
 	
 ### Iniciar el Frontend
 	
 Abre **otra terminal**:
 	
 bash
 ng serve
 
 	
 El frontend se ejecutará en `http://localhost:4200`
 	
 Accede a la aplicación desde tu navegador en `http://localhost:4200`
 	
  💻 Comandos Útiles
 	
 ### Frontend (Angular)
 	
 bash
 # Iniciar servidor de desarrollo
 ng serve
 	
 # Generar nuevo componente
 ng generate component nombre-componente
 	
 # Generar servicio
 ng generate service nombre-servicio
 	
 # Build de producción
 ng build --configuration production
 	
 # Ejecutar tests
 	ng test
 
 	
 ### Backend (Flask)
 	
 bash
 # Activar entorno virtual
 source .venv/bin/activate
 	
 # Ejecutar servidor local
 flask run
 	
 # Ejecutar con host accesible externamente
 flask run --host=0.0.0.0
 	
 # Ver logs en tiempo real
 tail -f *.log
 
 	
 ### Git
 	
 bash
 # Ver estado del repositorio
 	git status
 
 # Añadir cambios
 git add .
 	
 # Commit
 git commit -m "mensaje descriptivo"
 	
 # Push a GitHub
 git push origin master
  
	
## 📚 Documentación Adicional
	
- **[GUIA_IMPLEMENTACION.md](GUIA_IMPLEMENTACION.md)**: Guía detallada paso a paso para configuración y testing
- **[Angular CLI Documentation](https://angular.dev/tools/cli)**: Referencia completa de comandos de Angular
- **[Flask Documentation](https://flask.palletsprojects.com/)**: Documentación oficial de Flask
- **[Google App Passwords](https://myaccount.google.com/apppasswords)**: Generar contraseñas de aplicación para Gmail
	
## 🔒 Seguridad
	
- **NUNCA** hagas commit del archivo `.env` con credenciales reales
- Usa variables de entorno para todas las credenciales sensibles
- La contraseña de Gmail debe ser una **App Password**, no tu contraseña normal
- El archivo `.env` ya está incluido en `.gitignore`
	

	
**Fecha de última actualización**: Marzo 2025  
**Versión**: 1.0  
   224	**Estado**: ✅ Listo para Desarrollo Local
   225	
Review the changes and make sure they are as expected. Edit the file again if necessary.
