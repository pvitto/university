const API = "http://127.0.0.1:8000";
let emailGlobal = "";

function sendOTP() {
  emailGlobal = document.getElementById("email").value;
  fetch(`${API}/auth/send-otp?email=${emailGlobal}`, { method: "POST" });
  mostrar("otp");
}

function verifyOTP() {
  const otp = document.getElementById("otpInput").value;
  fetch(`${API}/auth/verify-otp?email=${emailGlobal}&otp=${otp}`, { method: "POST" })
  .then(res => {
    if (!res.ok) throw new Error();
    return res.json();
  })
  .then(() => {
    mostrar("app");
    cargar();
  })
  .catch(() => alert("OTP incorrecto"));
}

function mostrar(id) {
  document.getElementById("login").classList.add("hidden");
  document.getElementById("otp").classList.add("hidden");
  document.getElementById("app").classList.add("hidden");
  document.getElementById(id).classList.remove("hidden");
}

function cargar() {
  fetch(`${API}/students`)
    .then(res => res.json())
    .then(data => {
      let lista = document.getElementById("lista");
      lista.innerHTML = "";
      data.forEach(e => {
        lista.innerHTML += `<li>${e.nombre} (${e.edad}) <button onclick="eliminar(${e.id})">X</button></li>`;
      });
    });
}

function crear() {
  let n = document.getElementById("nombre").value;
  let e = document.getElementById("edad").value;
  let no = document.getElementById("nota").value;

  fetch(`${API}/students?nombre=${n}&edad=${e}&nota=${no}`, { method: "POST" })
    .then(() => cargar());
}

function eliminar(id) {
  fetch(`${API}/students/${id}`, { method: "DELETE" })
    .then(() => cargar());
}
