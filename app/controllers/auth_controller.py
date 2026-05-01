from flask import Blueprint, request, jsonify
from app.services.otp_service import generate_otp, verify_otp
from app.services.email_service import send_otp_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/request-otp", methods=["POST"])
def request_otp():
    email = request.json.get("email")
    if not email:
        return jsonify({"error": "Correo requerido"}), 400
    code = generate_otp(email)
    send_otp_email(email, code)
    return jsonify({"message": "Código enviado"}), 200

@auth_bp.route("/verify-otp", methods=["POST"])
def verify():
    email = request.json.get("email")
    code = request.json.get("code")
    if verify_otp(email, code):
        return jsonify({"message": "Acceso concedido"}), 200
    return jsonify({"error": "Código inválido o expirado"}), 401