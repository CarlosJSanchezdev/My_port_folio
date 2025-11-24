# 🔌 Conectar Backend Flask con Supabase

Esta guía te ayudará a migrar tu backend de SQLite a Supabase (PostgreSQL).

---

## 📋 Requisitos Previos

1. Cuenta de Supabase (https://supabase.com)
2. Proyecto creado en Supabase
3. Credenciales de conexión de tu base de datos

---

## 🔑 Paso 1: Obtener Credenciales de Supabase

1. Ve a tu proyecto en Supabase
2. Click en **Settings** (⚙️) → **Database**
3. En la sección **Connection string**, copia la **URI** (Connection pooling)
4. Debería verse así:
   ```
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

---

## 🛠️ Paso 2: Instalar Dependencias

```bash
cd backend
source .venv/bin/activate
pip install psycopg2-binary
pip freeze > requirements.txt
```

---

## 🔧 Paso 3: Actualizar `.env`

Edita `backend/.env`:

```env
# .env
SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=development

# Supabase PostgreSQL Connection
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres

# O usa variables separadas
SUPABASE_DB_HOST=aws-0-us-east-1.pooler.supabase.com
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.[PROJECT-REF]
SUPABASE_DB_PASSWORD=tu-password
```

> ⚠️ **IMPORTANTE**: Nunca subas el archivo `.env` a Git. Está en `.gitignore`.

---

## 📝 Paso 4: Actualizar `config.py` (Opcional)

El archivo actual ya está configurado para leer `DATABASE_URL` del `.env`, pero puedes mejorarlo:

```python
import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuracion de la aplicacion Flask"""
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Fix for Supabase/Heroku postgres:// vs postgresql://
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## 🗄️ Paso 5: Crear Tablas en Supabase

### Opción A: Usando Flask-Migrate (Recomendado)

```bash
cd backend
source .venv/bin/activate

# Inicializar migraciones (si no existe)
flask db init

# Crear migración
flask db migrate -m "Initial migration with Supabase"

# Aplicar migración
flask db upgrade
```

### Opción B: Usando el Script de Seed

```bash
cd backend
source .venv/bin/activate
python -m app.seed
```

Esto creará las tablas y poblará con datos.

---

## ✅ Paso 6: Verificar Conexión

```bash
cd backend
source .venv/bin/activate
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('✅ Conexión exitosa a Supabase!')"
```

---

## 🧪 Paso 7: Poblar Base de Datos

```bash
cd backend
source .venv/bin/activate
python -m app.seed
```

Deberías ver:
```
✅ Base de datos sembrada exitosamente!
📁 Proyectos creados: 8
📝 Posts de blog creados: 3
```

---

## 🚀 Paso 8: Iniciar Backend

```bash
cd backend
source .venv/bin/activate
PORT=5001 python run.py
```

---

## 🔍 Verificar en Supabase

1. Ve a tu proyecto en Supabase
2. Click en **Table Editor**
3. Deberías ver las tablas:
   - `projects`
   - `blog_posts`
   - `contact_messages`

---

## 🌐 Para Producción

### Variables de Entorno en Producción

Cuando despliegues (Render, Railway, etc.), configura:

```env
DATABASE_URL=tu-url-de-supabase
SECRET_KEY=clave-secreta-fuerte
FLASK_ENV=production
```

### CORS para Producción

Actualiza `backend/app/__init__.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:4200",
            "https://tu-dominio.com",  # Tu dominio de producción
            "https://tu-dominio.vercel.app"  # Si usas Vercel
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": False
    }
})
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "could not connect to server"
- Verifica que la URL de Supabase sea correcta
- Verifica que el password esté correcto
- Verifica que uses el puerto 6543 (pooler) o 5432 (directo)

### Error: "SSL connection required"
Agrega `?sslmode=require` al final de tu DATABASE_URL:
```
postgresql://...@...supabase.com:6543/postgres?sslmode=require
```

### Tablas no se crean
```bash
# Forzar recreación
python -m app.seed
```

---

## 📊 Ventajas de Supabase

✅ **PostgreSQL completo** - Base de datos relacional robusta
✅ **Escalable** - Crece con tu proyecto
✅ **Backups automáticos** - Tus datos están seguros
✅ **Dashboard visual** - Gestiona datos fácilmente
✅ **API REST automática** - Supabase genera APIs
✅ **Realtime** - Suscripciones a cambios en tiempo real
✅ **Gratis hasta 500MB** - Perfecto para empezar

---

## 🎯 Próximos Pasos

1. ✅ Configurar `.env` con credenciales de Supabase
2. ✅ Instalar `psycopg2-binary`
3. ✅ Ejecutar `python -m app.seed`
4. ✅ Verificar tablas en Supabase Dashboard
5. ✅ Iniciar backend y probar endpoints

---

## 💡 Tip Pro

Puedes usar **Supabase Studio** (el dashboard) para:
- Ver y editar datos directamente
- Ejecutar queries SQL
- Gestionar usuarios y permisos
- Ver logs en tiempo real

¡Tu backend ahora está conectado a una base de datos profesional! 🎉
