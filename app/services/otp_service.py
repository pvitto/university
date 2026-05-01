# ARCHIVO NUEVO: genera códigos OTP de 6 dígitos de forma segura
import secrets


def generate_otp() -> str:
    numero = secrets.randbelow(1_000_000)
    return f"{numero:06d}"
