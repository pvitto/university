# Importación de FastAPI y CORS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.auth_controller import auth_bp

# Importación del router de estudiantes
# students.py contiene todas las rutas relacionadas con estudiantes
from app.routes import students, email

# Importación de engine y Base para crear las tablas
# engine: conexión a la base de datos SQLite
# Base: clase base para los modelos ORM
from app.database import engine, Base

# Importación de los middlewares
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.middleware.audit_middleware import AuditMiddleware

# create_all(): crea todas las tablas definidas en los modelos
# Se ejecuta al iniciar la app y crea el archivo 'students.db' si no existe
Base.metadata.create_all(bind=engine)

# Instancia principal de FastAPI
app = FastAPI()

# Middleware CORS para permitir solicitudes del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de middlewares
# El orden de add_middleware determina el orden de ejecución:
# 1. RateLimitMiddleware - primero (más cercano al cliente)
# 2. AuditMiddleware - segundo
# 3. LoggingMiddleware - último (más cercano a la app)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware)

# Registro del router de estudiantes
# Todas las rutas de students.py estarán disponibles en /students
app.include_router(students.router)
app.include_router(email.router)

service_otp
app.register_blueprint(auth_bp, url_prefix="/auth")
=======
app.include_router(students.router, prefix="/api/v1", tags=["Students"])

@app.get("/")
def read_root():
    return {"message": "API de Universidad funcionando"}
main
