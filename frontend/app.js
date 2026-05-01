const API_URL = "/students";

// Guardia de sesión: si no hay correo guardado, manda al login
const userEmail = sessionStorage.getItem("user_email");
if (!userEmail) {
    window.location.href = "/";
}

const form        = document.getElementById("student-form");
const formTitle   = document.getElementById("form-title");
const idInput     = document.getElementById("student-id");
const nameInput   = document.getElementById("name");
const ageInput    = document.getElementById("age");
const gradeInput  = document.getElementById("grade");
const submitBtn   = document.getElementById("submit-btn");
const cancelBtn   = document.getElementById("cancel-btn");
const tbody       = document.getElementById("students-list");
const emptyState  = document.getElementById("empty-state");
const toast       = document.getElementById("toast");


document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("user-session").textContent = userEmail;
    document.getElementById("logout-btn").addEventListener("click", logout);
    form.addEventListener("submit", saveStudent);
    cancelBtn.addEventListener("click", resetForm);
    loadStudents();
});


async function loadStudents() {
    try {
        const response = await fetch(`${API_URL}/`);
        if (!response.ok) throw new Error("No se pudo cargar la lista");
        const students = await response.json();

        tbody.innerHTML = "";
        if (students.length === 0) {
            emptyState.style.display = "block";
            return;
        }
        emptyState.style.display = "none";

        students.forEach(s => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${s.id}</td>
                <td>${escapeHtml(s.name)}</td>
                <td>${s.age}</td>
                <td>${gradeBadge(s.grade)}</td>
                <td>
                    <button class="btn btn-warning" onclick="editStudent(${s.id}, '${escapeHtml(s.name)}', ${s.age}, ${s.grade})">✏️ Editar</button>
                    <button class="btn btn-danger" onclick="deleteStudent(${s.id})">🗑️ Eliminar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        showToast(err.message, "error");
    }
}


async function saveStudent(e) {
    e.preventDefault();
    const id = idInput.value;
    const data = {
        name: nameInput.value.trim(),
        age: parseInt(ageInput.value),
        grade: parseFloat(gradeInput.value)
    };

    const method = id ? "PUT" : "POST";
    const url    = id ? `${API_URL}/${id}` : `${API_URL}/`;

    try {
        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error al guardar");
        }

        showToast(id ? "Estudiante actualizado ✅" : "Estudiante creado ✅", "success");
        resetForm();
        loadStudents();
    } catch (err) {
        showToast(err.message, "error");
    }
}


function editStudent(id, name, age, grade) {
    idInput.value    = id;
    nameInput.value  = name;
    ageInput.value   = age;
    gradeInput.value = grade;
    formTitle.textContent = "✏️ Editar Estudiante";
    submitBtn.textContent = "Actualizar";
    nameInput.focus();
    window.scrollTo({ top: 0, behavior: "smooth" });
}


async function deleteStudent(id) {
    if (!confirm("¿Seguro que quieres eliminar este estudiante?")) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error al eliminar");
        }
        showToast("Estudiante eliminado 🗑️", "success");
        loadStudents();
    } catch (err) {
        showToast(err.message, "error");
    }
}


function resetForm() {
    form.reset();
    idInput.value = "";
    formTitle.textContent = "➕ Nuevo Estudiante";
    submitBtn.textContent = "Guardar";
}


function logout() {
    sessionStorage.removeItem("user_email");
    window.location.href = "/";
}


function gradeBadge(grade) {
    const cls = grade >= 4 ? "grade-good" : grade >= 3 ? "grade-mid" : "grade-bad";
    return `<span class="grade-badge ${cls}">${grade.toFixed(1)}</span>`;
}


function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, c => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
}


function showToast(message, type) {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => toast.classList.remove("show"), 3000);
}
