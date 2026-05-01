# ARCHIVO NUEVO: rutas del login con OTP
#   POST /auth/request-otp -> pide enviar código al correo
#   POST /auth/verify-otp  -> verifica el código recibido

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.auth_model import OTPRequest, OTPVerify
from app.controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/request-otp")
def request_otp(payload: OTPRequest, db: Session = Depends(get_db)):
    return AuthController.request_otp(payload, db)


@router.post("/verify-otp")
def verify_otp(payload: OTPVerify, db: Session = Depends(get_db)):
    return AuthController.verify_otp(payload, db)
