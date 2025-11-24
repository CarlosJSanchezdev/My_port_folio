# 🔧 Solución: Obtener la URL Correcta de Supabase

El error "Tenant or user not found" indica que la URL de conexión no está en el formato correcto. Sigue estos pasos EXACTOS:

---

## 📍 Paso 1: Ir a Supabase Dashboard

1. Ve a https://supabase.com/dashboard
2. Selecciona tu proyecto: **nmaerrqxvqsfzdmdrmum**
3. Click en el ícono de **Settings** (⚙️) en la barra lateral izquierda
4. Click en **Database**

---

## 📋 Paso 2: Copiar la Connection String Correcta

En la página de Database, busca la sección **"Connection string"**.

Verás varias opciones. **IMPORTANTE**: Usa **"Session mode"** o **"Transaction mode"**, NO uses "Direct connection".

### Opción Recomendada: Session Mode (Pooler)

1. Click en el tab **"Session mode"**
2. Copia la URI completa que se muestra
3. Debería verse algo así:

```
postgresql://postgres.nmaerrqxvqsfzdmdrmum:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

**NOTA**: El puerto puede ser **5432** o **6543** dependiendo del modo. Usa el que te muestre Supabase.

---

## 🔑 Paso 3: Reemplazar el Password

La URL copiada tendrá `[YOUR-PASSWORD]`. Reemplázalo con tu password real:

```
pdry01DpwrMpKqm1
```

URL final:
```
postgresql://postgres.nmaerrqxvqsfzdmdrmum:pdry01DpwrMpKqm1@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

---

## ✏️ Paso 4: Actualizar `.env`

Edita `backend/.env` y reemplaza la línea `DATABASE_URL`:

```env
# .env
SECRET_KEY=g4b1m1l4
FLASK_ENV=development

# Supabase PostgreSQL Connection
# IMPORTANTE: Copia la URL EXACTA de Supabase Dashboard
DATABASE_URL=postgresql://postgres.nmaerrqxvqsfzdmdrmum:pdry01DpwrMpKqm1@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

---

## 🧪 Paso 5: Probar Conexión

```bash
cd backend
source .venv/bin/activate
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('✅ Conexión exitosa!')"
```

---

## 🎯 Alternativa: Usar Conexión Directa (No Recomendado para Producción)

Si el pooler no funciona, puedes usar la conexión directa:

1. En Supabase Dashboard → Database
2. Click en **"Direct connection"**
3. Copia la URI
4. Debería usar el puerto **5432** y el host `db.nmaerrqxvqsfzdmdrmum.supabase.com`

```
postgresql://postgres:pdry01DpwrMpKqm1@db.nmaerrqxvqsfzdmdrmum.supabase.co:5432/postgres
```

---

## 📝 Formatos Posibles de Supabase

Supabase puede dar diferentes formatos dependiendo de la configuración:

### Formato 1: Pooler con project ref en username
```
postgresql://postgres.PROJECT_REF:PASSWORD@aws-0-REGION.pooler.supabase.com:6543/postgres
```

### Formato 2: Pooler sin project ref
```
postgresql://postgres:PASSWORD@aws-0-REGION.pooler.supabase.com:5432/postgres
```

### Formato 3: Conexión directa
```
postgresql://postgres:PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres
```

**IMPORTANTE**: Usa EXACTAMENTE el formato que te muestra Supabase en el dashboard.

---

## 🐛 Si Aún No Funciona

### Opción 1: Verificar Password

Ve a Supabase → Settings → Database → **"Reset database password"** si no estás seguro del password.

### Opción 2: Verificar IP Whitelist

Algunos proyectos de Supabase requieren whitelist de IPs:
1. Ve a Settings → Database
2. Busca "IP Address Restrictions"
3. Asegúrate de que tu IP esté permitida o desactiva las restricciones

### Opción 3: Usar Variables Separadas

En lugar de una URL completa, puedes usar variables separadas en `.env`:

```env
SUPABASE_HOST=aws-0-us-east-1.pooler.supabase.com
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres.nmaerrqxvqsfzdmdrmum
SUPABASE_PASSWORD=pdry01DpwrMpKqm1
```

Y en `config.py`:

```python
# Construir URL desde variables
if os.getenv('SUPABASE_HOST'):
    DATABASE_URL = f"postgresql://{os.getenv('SUPABASE_USER')}:{os.getenv('SUPABASE_PASSWORD')}@{os.getenv('SUPABASE_HOST')}:{os.getenv('SUPABASE_PORT')}/{os.getenv('SUPABASE_DB')}"
```

---

## ✅ Una Vez Conectado

Cuando la conexión funcione, ejecuta:

```bash
cd backend
source .venv/bin/activate
python -m app.seed
```

Esto creará las tablas y poblará la base de datos.

---

**IMPORTANTE**: El formato exacto de la URL depende de tu configuración de Supabase. Copia la URL EXACTA del dashboard.
