import random
import time

# Almacenamiento temporal de OTPs {correo: {codigo, expira}}
otp_store = {}

def generate_otp(email: str) -> str:
    code = str(random.randint(100000, 999999))
    otp_store[email] = {
        "code": code,
        "expires": time.time() + 300  # expira en 5 minutos
    }
    return code

def verify_otp(email: str, code: str) -> bool:
    record = otp_store.get(email)
    if not record:
        return False
    if time.time() > record["expires"]:
        del otp_store[email]
        return False
    if record["code"] != code:
        return False
    del otp_store[email]  # elimina después de usarse
    return True