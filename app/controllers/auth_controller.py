# ARCHIVO NUEVO: lógica del login con OTP
# request_otp -> genera código, lo guarda en BD y lo envía por correo
# verify_otp  -> valida que el código sea correcto y no haya expirado

import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import get_db
from app.models.db_models import OTP
from app.models.auth_model import OTPRequest, OTPVerify
from app.services.otp_service import generate_otp
from app.services.email_service import send_otp_email

load_dotenv()
OTP_EXPIRATION_MINUTES = int(os.getenv("OTP_EXPIRATION_MINUTES", "5"))


class AuthController:

    @staticmethod
    def request_otp(payload: OTPRequest, db: Session = Depends(get_db)) -> dict:
        codigo = generate_otp()
        expira = datetime.utcnow() + timedelta(minutes=OTP_EXPIRATION_MINUTES)

        nuevo_otp = OTP(
            email=payload.email,
            code=codigo,
            expires_at=expira,
            used=False,
        )
        db.add(nuevo_otp)
        db.commit()
        db.refresh(nuevo_otp)

        try:
            send_otp_email(payload.email, codigo)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"No se pudo enviar el correo: {str(e)}"
            )

        return {"message": "Codigo enviado al correo", "email": payload.email}

    @staticmethod
    def verify_otp(payload: OTPVerify, db: Session = Depends(get_db)) -> dict:
        otp = (
            db.query(OTP)
            .filter(
                OTP.email == payload.email,
                OTP.code == payload.code,
                OTP.used == False,
            )
            .order_by(OTP.id.desc())
            .first()
        )

        if not otp:
            raise HTTPException(status_code=400, detail="Codigo invalido")

        if otp.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Codigo expirado")

        otp.used = True  # marcar como usado para que no se pueda reutilizar
        db.commit()

        return {"message": "Login exitoso", "email": payload.email}
