from app import create_app
import os

#Crear la aplicacion Flask

app = create_app()

@app.route('/')
def hello():
    return {
        'message': '¡Backend del Portafolio funcionando correctamente!',
        'status': 'success',
        'endpoints': {
            'projects': '/api/projects',
            'blog': '/api/blog',
            'contact': '/api/contact'
        }
    }

@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'service': 'Portfolio Backend API'
    }

if __name__ == '__main__':
    #Obtener  puerto de enviroment variable o usar 5000 por defecto 
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0', #permite las conexiones desde cualquier ip 
        port=port,
        debug=True #solo en desarrollo
    )
    