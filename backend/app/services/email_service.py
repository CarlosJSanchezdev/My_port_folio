"""
Servicio de emails con Brevo
Migrado desde Resend el 24/03/2026
"""
import requests
import os
from flask import current_app

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

def send_verification_email(email: str, name: str, code: str) -> bool:
    """
    Envía email de verificación usando Brevo API
    
    Args:
        email: Email del destinatario
        name: Nombre del usuario
        code: Código de 6 dígitos
        
    Returns:
        bool: True si se envió correctamente
        
    Raises:
        Exception: Si el envío falla
    """
    try:
        api_key = os.getenv('BREVO_API_KEY')
        if not api_key:
            current_app.logger.error("BREVO_API_KEY no configurada")
            raise Exception("Configuración de email incompleta")
        
        sender_email = os.getenv('BREVO_SENDER_EMAIL', 'tu-email@gmail.com')
        sender_name = os.getenv('BREVO_SENDER_NAME', 'Carlos Sánchez Portfolio')
        portfolio_url = os.getenv('PORTFOLIO_URL', 'http://localhost:4200')
        
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1f2937; background-color: #f3f4f6; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 40px auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center; color: white; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 40px 30px; }}
        .greeting {{ font-size: 24px; font-weight: 600; margin-bottom: 15px; color: #1f2937; }}
        .message {{ font-size: 16px; color: #4b5563; margin-bottom: 30px; }}
        .code-container {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px; text-align: center; margin: 30px 0; }}
        .code-label {{ color: rgba(255,255,255,0.9); font-size: 14px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }}
        .code {{ font-size: 48px; font-weight: 700; color: white; letter-spacing: 12px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }}
        .expiration {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        .expiration p {{ margin: 0; color: #92400e; font-size: 14px; }}
        .benefits {{ margin: 30px 0; }}
        .benefits h3 {{ color: #1f2937; font-size: 18px; margin-bottom: 15px; }}
        .benefits ul {{ list-style: none; padding: 0; }}
        .benefits li {{ padding: 8px 0; color: #4b5563; font-size: 15px; }}
        .footer {{ background: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb; }}
        .footer p {{ margin: 5px 0; color: #9ca3af; font-size: 13px; }}
        .button {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 600; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Portfolio Carlos Sánchez</h1>
        </div>
        <div class="content">
            <div class="greeting">¡Hola {name}! 👋</div>
            <div class="message">Gracias por tu interés en contactarme. Aquí está tu código de verificación:</div>
            <div class="code-container">
                <div class="code-label">Código de Verificación</div>
                <div class="code">{code}</div>
            </div>
            <div class="expiration">
                <p>⏱️ <strong>Este código expira en 10 minutos</strong></p>
            </div>
            <div class="benefits">
                <h3>Una vez verificado, tendrás acceso a:</h3>
                <ul>
                    <li>📱 Mi número de teléfono directo</li>
                    <li>💬 WhatsApp para contacto rápido</li>
                    <li>⏰ Horarios de disponibilidad</li>
                    <li>📄 Descarga de CV completo</li>
                </ul>
            </div>
            <div style="text-align: center;">
                <a href="{portfolio_url}/contact" class="button">Volver al Portfolio</a>
            </div>
        </div>
        <div class="footer">
            <p>Si no solicitaste este código, puedes ignorar este email.</p>
            <p>© 2026 Carlos Sánchez - Desarrollador Full Stack</p>
        </div>
    </div>
</body>
</html>"""
        
        text_content = f"""¡Hola {name}!

Gracias por tu interés en contactarme. Aquí está tu código de verificación:

{code}

⏱️ Este código expira en 10 minutos.

Una vez verificado, tendrás acceso a:
- Mi número de teléfono directo
- WhatsApp para contacto rápido
- Horarios de disponibilidad
- Descarga de CV completo

Si no solicitaste este código, puedes ignorar este email.

Saludos,
Carlos Sánchez
Desarrollador Full Stack
{portfolio_url}/contact"""
        
        payload = {
            "sender": {
                "name": sender_name,
                "email": sender_email
            },
            "to": [{
                "email": email,
                "name": name
            }],
            "subject": "🔐 Tu Código de Verificación - Portfolio Carlos Sánchez",
            "htmlContent": html_content,
            "textContent": text_content
        }
        
        headers = {
            "api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        current_app.logger.info(f"Enviando email vía Brevo a {email}")
        
        response = requests.post(
            BREVO_API_URL, 
            json=payload, 
            headers=headers, 
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            current_app.logger.info(f"✅ Email enviado vía Brevo a {email}: {result.get('messageId', 'sin ID')}")
            return True
        else:
            error_msg = f"Brevo API error {response.status_code}: {response.text}"
            current_app.logger.error(f"❌ Error enviando email a {email}: {error_msg}")
            raise Exception(error_msg)
            
    except requests.exceptions.Timeout:
        error_msg = "Timeout conectando con Brevo API"
        current_app.logger.error(f"❌ Timeout enviando email a {email}")
        raise Exception(error_msg)
        
    except requests.exceptions.ConnectionError:
        error_msg = "Error de conexión con Brevo API"
        current_app.logger.error(f"❌ Error de conexión enviando email a {email}")
        raise Exception(error_msg)
        
    except Exception as e:
        current_app.logger.error(f"❌ Error enviando email a {email}: {str(e)}")
        raise e
