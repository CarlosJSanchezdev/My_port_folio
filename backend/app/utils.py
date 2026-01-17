import os
from flask_mail import Message
from flask import current_app
from app import mail

def send_verification_email(email, name, code):
    """Envía email con código de verificación"""
    try:
        msg = Message(
            subject='Código de Verificación - Portfolio Carlos Sánchez',
            recipients=[email],
            sender=os.getenv('MAIL_DEFAULT_SENDER', 'Cafefincasanrafael@gmail.com')
        )
        
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f3f4f6;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px 20px;">
                <!-- Header -->
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2563eb; margin: 0; font-size: 28px;">Portfolio Carlos Sánchez</h1>
                </div>
                
                <!-- Greeting -->
                <div style="margin-bottom: 30px;">
                    <h2 style="color: #1f2937; font-size: 24px; margin: 0 0 10px 0;">¡Hola {name}! 👋</h2>
                    <p style="color: #4b5563; font-size: 16px; line-height: 1.6; margin: 0;">
                        Gracias por tu interés en contactarme. Aquí está tu código de verificación:
                    </p>
                </div>
                
                <!-- Verification Code -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 30px; 
                            border-radius: 12px; 
                            text-align: center; 
                            margin: 30px 0;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <p style="color: #ffffff; font-size: 14px; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 2px;">
                        Tu Código de Verificación
                    </p>
                    <h1 style="color: #ffffff; 
                               font-size: 48px; 
                               letter-spacing: 12px; 
                               margin: 0;
                               font-weight: bold;
                               text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);">
                        {code}
                    </h1>
                </div>
                
                <!-- Expiration Notice -->
                <div style="background-color: #fef3c7; 
                            border-left: 4px solid #f59e0b; 
                            padding: 15px; 
                            margin: 20px 0;
                            border-radius: 4px;">
                    <p style="color: #92400e; margin: 0; font-size: 14px;">
                        ⏱️ Este código expira en <strong>15 minutos</strong>.
                    </p>
                </div>
                
                <!-- Benefits -->
                <div style="margin: 30px 0;">
                    <p style="color: #1f2937; font-size: 16px; font-weight: bold; margin: 0 0 15px 0;">
                        Una vez verificado, tendrás acceso Premium completo:
                    </p>
                    <ul style="color: #4b5563; font-size: 15px; line-height: 1.8; padding-left: 20px;">
                        <li>📱 Mi número de teléfono directo</li>
                        <li>💬 WhatsApp para contacto rápido</li>
                        <li>⏰ Mis horarios de disponibilidad</li>
                        <li>📄 Descarga de mi CV completo</li>
                        <li>🔐 Acceso a portafolio privado</li>
                    </ul>
                </div>
                
                <!-- Footer -->
                <div style="margin-top: 40px; 
                            padding-top: 20px; 
                            border-top: 1px solid #e5e7eb; 
                            text-align: center;">
                    <p style="color: #9ca3af; font-size: 13px; margin: 0 0 10px 0;">
                        Si no solicitaste este código, puedes ignorar este email.
                    </p>
                    <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                        © 2024 Carlos Sánchez - Desarrollador Full Stack
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Versión texto plano como fallback
        msg.body = f"""
        ¡Hola {name}!
        
        Gracias por tu interés en contactarme. Aquí está tu código de verificación:
        
        {code}
        
        Este código expira en 15 minutos.
        
        Una vez verificado, tendrás acceso Premium completo:
        - Mi número de teléfono directo
        - WhatsApp para contacto rápido
        - Mis horarios de disponibilidad
        - Descarga de mi CV completo
        - Acceso a portafolio privado
        
        Si no solicitaste este código, puedes ignorar este email.
        
        Saludos,
        Carlos Sánchez
        Desarrollador Full Stack
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error sending verification email: {str(e)}")
        raise e
