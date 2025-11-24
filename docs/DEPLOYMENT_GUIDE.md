# 🚀 Guía de Despliegue (Deployment)

Esta guía te llevará paso a paso para publicar tu portafolio en internet de forma **gratuita** y sencilla.

## 📋 Prerrequisitos
1.  Tener tu código subido a **GitHub**.
2.  Tener cuentas en:
    *   [Render](https://render.com) (Para el Backend)
    *   [Vercel](https://vercel.com) (Para el Frontend)
    *   [Supabase](https://supabase.com) (Ya la tienes)

---

## 1️⃣ Paso 1: Desplegar el Backend (Render)
Render es excelente para aplicaciones Python/Flask y tiene un plan gratuito.

1.  Inicia sesión en **Render** y haz clic en **"New +"** -> **"Web Service"**.
2.  Conecta tu repositorio de GitHub (`My_port_folio`).
3.  Configura lo siguiente:
    *   **Name**: `my-portfolio-backend` (o lo que gustes)
    *   **Root Directory**: `backend` (¡Importante!)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn run:app`
    *   **Instance Type**: `Free`
4.  **Variables de Entorno (Environment Variables)**:
    Haz clic en "Advanced" o "Environment" y agrega:
    *   `DATABASE_URL`: (Tu URL de conexión de Supabase, la misma de tu `.env` local)
    *   `SECRET_KEY`: (Crea una clave segura aleatoria)
    *   `FLASK_ENV`: `production`
5.  Haz clic en **"Create Web Service"**.
6.  Espera a que termine el despliegue. Render te dará una URL (ej. `https://my-portfolio-backend.onrender.com`). **Copia esta URL**.

---

## 2️⃣ Paso 2: Configurar Frontend para Producción
Antes de subir el frontend, dile a dónde conectar.

1.  Abre `src/environments/environment.prod.ts` en tu editor.
2.  Cambia la `apiUrl` por la URL que te dio Render:
    ```typescript
    export const environment = {
      production: true,
      apiUrl: 'https://tu-backend-en-render.onrender.com/api' // 👈 Pega tu URL aquí
    };
    ```
3.  Guarda y haz un **commit** y **push** de este cambio a GitHub.

---

## 3️⃣ Paso 3: Desplegar el Frontend (Vercel)
Vercel es la mejor opción para Angular.

1.  Inicia sesión en **Vercel** y haz clic en **"Add New..."** -> **"Project"**.
2.  Importa tu repositorio de GitHub.
3.  En **"Framework Preset"**, selecciona **Angular**.
4.  En **"Root Directory"**, asegúrate que esté en `./` (la raíz).
5.  **Build & Output Settings**:
    *   Vercel suele detectar esto automáticamente (`dist/my-port-folio/browser`). Si falla, revisaremos esto.
6.  Haz clic en **"Deploy"**.

---

## 🎉 ¡Listo!
Vercel te dará una URL (ej. `https://my-portfolio-carlos.vercel.app`). Esa es la dirección de tu portafolio en vivo.

### ⚠️ Nota Importante sobre el Plan Gratuito de Render
El servicio gratuito de Render se "duerme" después de 15 minutos de inactividad. La primera vez que entres a tu portafolio después de un rato, la carga de datos (proyectos/blog) puede tardar unos **30-50 segundos** en despertar al backend. Esto es normal en el plan gratis.
