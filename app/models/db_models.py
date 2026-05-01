from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime  # AGREGADO: Boolean y DateTime para tabla OTP
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    grade = Column(Float, nullable=False)


# AGREGADO: tabla para guardar los códigos OTP enviados por correo
class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)   # correo al que se envió
    code = Column(String, nullable=False)                # código de 6 dígitos
    expires_at = Column(DateTime, nullable=False)        # expira 5 minutos después
    used = Column(Boolean, default=False)                # True = ya fue usado
