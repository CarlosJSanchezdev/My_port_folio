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
