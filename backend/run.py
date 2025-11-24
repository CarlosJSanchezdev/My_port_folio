from app import create_app
import os



#Crear la aplicacion Flask

app = create_app()

"""@app.route('/')
def hello():
    return {
        'message': '¡Backend del Portafolio funcionando correctamente!',
        'status': 'success',
        'endpoints': {
            'projects': '/api/projects',
            'blog': '/api/blog',
            'contact': '/api/contact'
        }
    }"""

"""@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'service': 'Portfolio Backend API',
        'timestamp': os.time()
    }"""
"""@app.route('/api/security/info')
def security_info():
    if app.debug:
        return {
            'client_ip':  request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'headers': dict(request.headers)
        }
    else:
        return {
            'message': 'Security info endpoint is disabled in production mode.'
        } , 404"""

if __name__ == '__main__':
    #Obtener  puerto de enviroment variable o usar 5000 por defecto 
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0', #permite las conexiones desde cualquier ip 
        port=port,
        debug=True, #solo en desarrollo
        #hreaded=True
    )
    