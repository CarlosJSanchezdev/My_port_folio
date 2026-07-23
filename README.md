# MyPortFolio - Carlos Sánchez

Portfolio personal desarrollado con Angular 20 (SPA estático) + Flask backend desplegado en Render + PostgreSQL en Supabase.

## Tech Stack

| Capa       | Tecnología                          |
|------------|-------------------------------------|
| Frontend   | Angular 20 (SSR migrado a SPA estático) |
| Backend    | Flask + SQLAlchemy                  |
| Base de datos | PostgreSQL (Supabase)            |
| Emails     | Resend API                          |
| Hosting    | Vercel (frontend), Render (backend) |

## Arquitectura

- **Frontend**: SPA estático compilado con `outputMode: "static"`. Sirve desde Vercel con rewrites para SPA.
- **Backend**: API Flask en Render con CORS configurado para el dominio Vercel. Cookies con `SameSite=None` para entorno cross-site.
- **Base de datos**: PostgreSQL en Supabase con migraciones Flask-Migrate.

## Desarrollo local

```bash
# Frontend
ng serve

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask run
```

## Build

```bash
ng build
```

Los artefactos se generan en `dist/my-port-folio/browser`.

## Despliegue

El frontend se despliega automáticamente en Vercel desde la rama `main`. El build command es `npm run build` y el output directory es `dist/my-port-folio/browser`.

## Funcionalidades

- Blog con artículos desde BD
- Formulario de contacto con almacenamiento en BD
- Verificación por email vía Resend (código de 6 dígitos)
- Panel de administración de mensajes y blog
- Diseño responsive

## Variables de entorno backend (`.env`)

```
DATABASE_URL=postgresql://...
RESEND_API_KEY=re_...
FRONTEND_URL=https://carlosjsanchezdev.vercel.app
SECRET_KEY=...
```
