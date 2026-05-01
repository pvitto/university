// ARCHIVO NUEVO: lógica del login con OTP en el frontend
const API_URL = "/auth";

const stepEmail  = document.getElementById("step-email");
const stepOtp    = document.getElementById("step-otp");
const emailInput = document.getElementById("email-input");
const otpInput   = document.getElementById("otp-input");
const emailShown = document.getElementById("email-shown");
const sendBtn    = document.getElementById("send-btn");
const verifyBtn  = document.getElementById("verify-btn");
const backBtn    = document.getElementById("back-btn");
const msg        = document.getElementById("msg");


// Paso 1: pedir el código
sendBtn.addEventListener("click", async () => {
    const email = emailInput.value.trim();
    if (!email) { showMsg("Escribe tu correo", "err"); return; }

    sendBtn.disabled = true;
    showMsg("Enviando código...", "ok");

    try {
        const res = await fetch(`${API_URL}/request-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Error enviando el código");

        emailShown.textContent = email;
        stepEmail.classList.add("hidden");
        stepOtp.classList.remove("hidden");
        showMsg("Revisa tu correo 📧", "ok");
        otpInput.focus();
    } catch (err) {
        showMsg(err.message, "err");
    } finally {
        sendBtn.disabled = false;
    }
});


// Paso 2: verificar el código
verifyBtn.addEventListener("click", async () => {
    const email = emailInput.value.trim();
    const code  = otpInput.value.trim();

    if (code.length !== 6) { showMsg("El código debe tener 6 dígitos", "err"); return; }

    verifyBtn.disabled = true;
    showMsg("Verificando...", "ok");

    try {
        const res = await fetch(`${API_URL}/verify-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, code })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Código inválido");

        showMsg("Login exitoso ✅", "ok");
        sessionStorage.setItem("user_email", email);
        setTimeout(() => { window.location.href = "/index"; }, 800);
    } catch (err) {
        showMsg(err.message, "err");
    } finally {
        verifyBtn.disabled = false;
    }
});


backBtn.addEventListener("click", () => {
    stepOtp.classList.add("hidden");
    stepEmail.classList.remove("hidden");
    otpInput.value = "";
    showMsg("", "");
});


function showMsg(text, type) {
    msg.textContent = text;
    msg.className = "msg " + type;
}
