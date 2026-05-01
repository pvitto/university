# Importación de FastAPI y CORS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles    # AGREGADO: para servir archivos estáticos del frontend
from fastapi.responses import FileResponse     # AGREGADO: para servir login.html e index.html

# Routers originales del profesor
from app.routes import students, email
from app.routes import auth                    # AGREGADO: router del login con OTP

# Base de datos
from app.database import engine, Base

# Middlewares del profesor
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.middleware.audit_middleware import AuditMiddleware

# Crea todas las tablas (students + otps)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS para permitir solicitudes del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middlewares del profesor
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware)

# Routers
app.include_router(students.router)
app.include_router(email.router)
app.include_router(auth.router)                # AGREGADO: expone /auth/request-otp y /auth/verify-otp

# AGREGADO: servir archivos estáticos del frontend (JS, CSS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# AGREGADO: servir login.html en la raíz
@app.get("/")
def serve_login():
    return FileResponse("frontend/login.html")


# AGREGADO: servir index.html en /index
@app.get("/index")
def serve_index():
    return FileResponse("frontend/index.html")
