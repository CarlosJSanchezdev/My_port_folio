# 🚀 Guía de Integración Backend-Frontend

## ✅ Lo que se ha completado

### Frontend (Angular)
- ✅ Servicios creados:
  - `ApiService` - Servicio base para HTTP
  - `ProjectsService` - Gestión de proyectos
  - `BlogService` - Gestión de blog posts
  - `ContactService` - Envío de mensajes de contacto

- ✅ Componentes actualizados:
  - `ProjectsComponent` - Carga proyectos desde API con fallback a datos estáticos
  - `ContactComponent` - Envía mensajes reales a la API
  - `BlogComponent` - **Necesita actualización manual** (ver abajo)

- ✅ Configuración:
  - `environment.ts` - Configuración de desarrollo (localhost:5000)
  - `environment.prod.ts` - Configuración de producción

### Backend (Flask)
- ✅ Script de seed actualizado con datos reales del portafolio
- ✅ 8 proyectos migrados
- ✅ 3 posts de blog de ejemplo

## 🔧 Cómo Iniciar el Proyecto

### 1. Instalar Dependencias del Backend

```bash
cd backend

# Crear entorno virtual (si no existe)
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # En Linux/Mac
# .venv\\Scripts\\activate  # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Poblar la Base de Datos

```bash
# Desde la carpeta backend con el entorno virtual activado
python -m app.seed
```

Deberías ver:
```
✅ Base de datos sembrada exitosamente!
📁 Proyectos creados: 8
📝 Posts de blog creados: 3
```

### 3. Iniciar el Backend

```bash
# Desde la carpeta backend
python run.py
```

El backend estará disponible en: `http://localhost:5000`

### 4. Iniciar el Frontend

En otra terminal:

```bash
# Desde la raíz del proyecto
ng serve
```

El frontend estará disponible en: `http://localhost:4200`

## 🧪 Verificar la Integración

### 1. Probar el Backend directamente

```bash
# Verificar que el backend está corriendo
curl http://localhost:5000/

# Obtener proyectos
curl http://localhost:5000/api/projects

# Obtener posts de blog
curl http://localhost:5000/api/blog
```

### 2. Probar en el Frontend

1. Abre `http://localhost:4200`
2. Ve a la página de **Projects** - Deberías ver los proyectos cargados desde la API
3. Ve a la página de **Contact** - Envía un mensaje de prueba
4. Revisa la consola del navegador (F12) para ver los logs

## ⚠️ Tareas Pendientes

### BlogComponent - Actualización Manual Necesaria

El `BlogComponent` necesita ser actualizado manualmente. Aquí está lo que debes hacer:

1. Abre `src/app/blog/blog.component.ts`
2. Importa el servicio:
   ```typescript
   import { BlogService, BlogPost } from '../services/blog.service';
   ```
3. Inyecta el servicio en el constructor:
   ```typescript
   constructor(private blogService: BlogService) {}
   ```
4. Agrega estados de loading:
   ```typescript
   isLoading: boolean = true;
   error: string | null = null;
   ```
5. Crea un método `loadPosts()` similar al de `ProjectsComponent`

## 🐛 Solución de Problemas

### Error: CORS
Si ves errores de CORS en la consola:
- Verifica que el backend esté corriendo en `localhost:5000`
- Verifica que la configuración de CORS en `backend/app/__init__.py` incluya `localhost:4200`

### Error: "Module not found"
```bash
cd backend
pip install -r requirements.txt
```

### Error: "Database not found"
```bash
cd backend
python -m app.seed
```

### Los proyectos no se cargan
- Abre la consola del navegador (F12)
- Revisa si hay errores de red
- Verifica que el backend esté corriendo
- Si el backend no está disponible, el frontend usará datos estáticos automáticamente

## 📝 Notas Importantes

1. **Fallback a Datos Estáticos**: Si el backend no está disponible, el frontend automáticamente usa los datos de `portfolio.config.ts`

2. **Desarrollo**: Durante el desarrollo, puedes trabajar sin el backend y todo funcionará con datos estáticos

3. **Producción**: Para producción, necesitarás:
   - Deployar el backend (Render, Railway, Heroku)
   - Actualizar `environment.prod.ts` con la URL del backend
   - Configurar CORS en el backend para permitir tu dominio de producción

## 🎯 Próximos Pasos

1. ✅ Actualizar `BlogComponent` manualmente
2. ✅ Probar toda la integración
3. ✅ Deployar el backend a un servicio cloud
4. ✅ Actualizar `environment.prod.ts` con la URL real
5. ✅ Deployar el frontend

## 📞 Contacto

Si tienes problemas, revisa:
- Logs del backend en la terminal
- Consola del navegador (F12)
- Network tab en DevTools
