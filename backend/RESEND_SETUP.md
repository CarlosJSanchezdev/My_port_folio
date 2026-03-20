# Configuración de Resend para Emails

## 📋 ¿Qué es Resend?

Resend es un servicio de emails transaccionales para desarrolladores.
- **Plan gratis:** 3,000 emails/mes (100 emails/día)
- **Setup:** 5 minutos
- **Confiabilidad:** 99.9% deliverability

---

## 🚀 Pasos para Configurar

### 1. Crear Cuenta en Resend

1. Ve a [https://resend.com](https://resend.com)
2. Click en "Get Started for Free"
3. Regístrate con GitHub o email

### 2. Obtener API Key

1. Una vez dentro, ve a **Settings** → **API Keys**
2. Click en **"Create API Key"**
3. Ponle nombre: `Portfolio Flask`
4. Copia la API key (empieza con `re_`)

### 3. Configurar Dominio de Envío

**Opción Rápida (Desarrollo):**
- Usa `onboarding@resend.dev` (ya configurado)
- Los emails llegan como "on behalf of resend.dev"

**Opción Profesional (Producción):**
1. Ve a **Domains** → **Add Domain**
2. Agrega tu dominio (ej: `carlosjsanchez.dev`)
3. Configura los DNS records que te dan:
   - MX records
   - TXT records (SPF, DKIM)
4. Espera propagación (5-30 min)

### 4. Configurar Variables de Entorno

**Local (.env):**
```bash
RESEND_API_KEY=re_AbCdEfGhIjKlMnOpQrStUvWxYz123456
PORTFOLIO_URL=http://localhost:4200
```

**Render (Dashboard):**
```
Environment → Add Environment Variable
Name: RESEND_API_KEY
Value: re_AbCdEfGhIjKlMnOpQrStUvWxYz123456

Name: PORTFOLIO_URL
Value: https://tu-api.onrender.com
```

### 5. Actualizar Backend

El código ya está actualizado para usar Resend. Solo necesitas:

1. **Instalar dependencia:**
```bash
cd backend
pip install resend==2.5.0
```

2. **En Render (requirements.txt ya incluye resend):**
```bash
# El deploy automático instalará la nueva dependencia
```

### 6. Probar

1. Abre tu portfolio: `http://localhost:4200/contact`
2. Llena el formulario con tu email
3. Click en "🔓 Desbloquear Información Premium"
4. Revisa tu email (y spam)
5. Ingresa el código de 6 dígitos

---

## 📧 Email Template

Los emails se envían con este formato:

**From:** Carlos Sánchez Portfolio \<onboarding@resend.dev\>
**Subject:** 🔐 Tu Código de Verificación - Portfolio Carlos Sánchez

**Contenido:**
- Saludo personalizado
- Código de 6 dígitos grande y claro
- Expiración en 10 minutos
- Beneficios de verificar
- Botón de retorno al portfolio

---

## 🔒 Seguridad

- Código expira en **10 minutos**
- Máximo **5 solicitudes por hora** por email
- Código de **6 dígitos** (1 millón de combinaciones)
- Verificación persiste por **30 días** en localStorage

---

## 📊 Monitoreo

### Dashboard de Resend

1. Ve a [resend.com/dashboard](https://resend.com/dashboard)
2. Verifica:
   - Emails enviados
   - Tasa de apertura
   - Rebotes
   - Quejas

### Logs del Backend

```python
# En Render: Logs → Ver logs en tiempo real
# Busca: "Email sent via Resend"
```

---

## ⚠️ Solución de Problemas

### Email no llega

1. **Revisa spam/promociones**
2. **Verifica API key** en variables de entorno
3. **Checa logs** del backend:
   ```bash
   # Error común: API key inválida
   "Resend email failed: Invalid API key"
   ```

### Error "Too many requests"

- Rate limit: 5 emails por hora
- Espera o usa otro email

### Error "Domain not verified"

- Si usas dominio personalizado, verifica los DNS records
- Mientras tanto, usa `onboarding@resend.dev`

---

## 💡 Mejores Prácticas

1. **Usa dominio personalizado en producción**
   - Mejora deliverability
   - Más profesional

2. **Monitorea tu cuota**
   - 3000 emails/mes = ~100 emails/día
   - Si necesitas más, upgrade a $30/mes

3. **Previene spam**
   - Rate limiting ya implementado
   - Considera agregar hCaptcha si recibes mucho spam

---

## 📞 Soporte

- **Resend Docs:** https://resend.com/docs
- **Resend Discord:** https://resend.com/discord
- **Email:** support@resend.com

---

## ✅ Checklist Final

- [ ] Cuenta Resend creada
- [ ] API key obtenida y guardada en .env
- [ ] API key agregada en Render
- [ ] requirements.txt actualizado (resend==2.5.0)
- [ ] Backend redeployado en Render
- [ ] Email de prueba recibido
- [ ] Código verificado correctamente
- [ ] Información premium visible después de verificar

---

**¡Listo! Tu sistema de verificación por email está funcionando con Resend 🎉**
