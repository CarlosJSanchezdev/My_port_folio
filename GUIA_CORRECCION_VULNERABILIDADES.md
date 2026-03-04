# Guía de Corrección de Vulnerabilidades de Seguridad

## 1. Credenciales Expuestas en Git (Crítico - YA RESUELTO)

**Problema:** Las credenciales del email quedaron expuestas en el historial de git.

**Estado:** Ya se ejecutó `git rm --cached backend/.env` para dejar de rastrear el archivo.

**Acción requerida:**
- Cambiar la contraseña del correo `cafefincasanrafael@gmail.com` inmediatamente
- Generar una nueva contraseña de aplicación en https://myaccount.google.com/apppasswords
- Actualizar el archivo `.env` local con las nuevas credenciales

---

## 2. SECRET_KEY Hardcodeada (Alto)

**Archivo:** `backend/app/config.py:9`

**Problema:** Si la variable de entorno no está configurada, usa una clave por defecto pública.

```python
# Actual (inseguro):
SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-change-in-production'
```

**Corrección:**

```python
# Seguro:
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no está configurada en las variables de entorno")
```

**Pasos:**
1. Abrir `backend/app/config.py`
2. Reemplazar la línea 9
3. Asegurarse de que `SECRET_KEY` esté definida en el archivo `.env`

---

## 3. SESSION_COOKIE_SECURE = False (Medio)

**Archivo:** `backend/app/config.py:47`

**Problema:** Las cookies de sesión se transmiten sin cifrar si no hay HTTPS.

**Corrección:**

```python
# En producción (cuando tengas HTTPS):
SESSION_COOKIE_SECURE = True
```

**Pasos:**
1. Abrir `backend/app/config.py`
2. Cambiar la línea 47 a `SESSION_COOKIE_SECURE = True` (solo cuando tengas HTTPS configurado)
3. O usar variable de entorno:

```python
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
```

---

## 4. Depuración Habilitada en Producción (Medio)

**Archivos:** 
- `backend/run_local.py:26`
- `backend/run.py:48`

**Problema:** El modo debug está habilitado.

**Corrección:**

```python
# run.py - línea 48:
debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true',
```

**Pasos:**
1. Abrir `backend/run.py`
2. Cambiar `debug=True` por `debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'`
3. En el archivo `.env`, asegurar que `FLASK_DEBUG=false` (o no definirla)

---

## 5. Errores Expuestos al Cliente (Medio)

**Archivo:** `backend/app/routes/auth.py:188`

**Problema:** Los errores de servidor se exponen directamente al cliente.

```python
# Actual (inseguro):
return jsonify({
    'success': False,
    'error': str(e)
}), 500
```

**Corrección:**

```python
# Seguro:
current_app.logger.error(f"Error in get_owner_info: {str(e)}")
return jsonify({
    'success': False,
    'error': 'Error interno del servidor'
}), 500
```

**Pasos:**
1. Abrir `backend/app/routes/auth.py`
2. Buscar la función `get_owner_info()` (línea 167)
3. Reemplazar el return de error (línea 188) con un mensaje genérico
4. Agregar logging del error real

---

## 6. Falta de Protección CSRF (Bajo)

**Problema:** No hay protección CSRF en los endpoints de autenticación.

**Corrección:**

```python
# En Flask, instalar flask-wtf:
# pip install flask-wtf

from flask_wtf.csrf import CSRFProtect

# En app/__init__.py:
csrf = CSRFProtect()
csrf.init_app(app)
```

**Pasos:**
1. Instalar `flask-wtf`: `pip install flask-wtf`
2. En `backend/app/__init__.py`, agregar protección CSRF

---

## 7. Sistema de Verificación Débil (Medio)

**Archivo:** `backend/app/routes/auth.py`

**Problema:** El sistema de verificación por email asigna acceso nivel 3 inmediatamente sin verificación real de propiedad del email.

**Análisis actual:**
- El código genera un código de verificación y lo envía por email
- Cuando el usuario ingresa el código, se le da acceso nivel 3 automáticamente
- Esto es correcto si el email真的有 acceso al email

**Recomendaciones:**
1. El sistema actual es correcto para verificación de email
2. Considerar agregar verificación en dos pasos (2FA)
3. Limitar el acceso a información sensible hasta verificación adicional

---

## Resumen de Acciones Inmediatas

| # | Vulnerabilidad | Severidad | Estado |
|---|---------------|-----------|--------|
| 1 | Credenciales expuestas | Crítico | ⚠️ Rotar credenciales |
| 2 | SECRET_KEY hardcodeada | Alto | Por hacer |
| 3 | SESSION_COOKIE_SECURE | Medio | Por hacer |
| 4 | DEBUG enabled | Medio | Por hacer |
| 5 | Errores expuestos | Medio | Por hacer |
| 6 | CSRF protection | Bajo | Por hacer |
| 7 | Verificación débil | Medio | Revisar |
