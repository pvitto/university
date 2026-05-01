# Servicio de envío de correos por Gmail SMTP.
# send_email: función original del profesor (correo genérico)
# send_otp_email: AGREGADO para enviar el código OTP del login

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


# Función original del profesor: enviar correo genérico
async def send_email(to_email: str, body: str) -> dict:
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Mensaje desde FastAPI"
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

    return {"status": "success", "message": f"Correo enviado a {to_email}"}


# AGREGADO: enviar el código OTP por correo para el login
def send_otp_email(to_email: str, code: str) -> None:
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Tu código de verificación"

    cuerpo_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Hola 👋</h2>
            <p>Tu código de verificación es:</p>
            <h1 style="color:#2563eb; letter-spacing:4px;">{code}</h1>
            <p>Este código expira en 5 minutos.</p>
            <p style="color:#888; font-size:12px;">
                Si no solicitaste este código, ignora este correo.
            </p>
        </body>
    </html>
    """
    msg.attach(MIMEText(cuerpo_html, "html"))

    # Puerto 465 = SMTP sobre SSL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(SMTP_EMAIL, SMTP_PASSWORD)
        servidor.sendmail(SMTP_EMAIL, to_email, msg.as_string())
