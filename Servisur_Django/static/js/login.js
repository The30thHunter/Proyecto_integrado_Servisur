// Mostrar/ocultar contraseña
document
  .getElementById("togglePassword")
  .addEventListener("click", function () {
    const input = document.getElementById("id_password");
    input.type = input.type === "password" ? "text" : "password";
  });

// Validación visual en tiempo real
const username = document.getElementById("id_username");
const password = document.getElementById("id_password");

username.addEventListener("input", function () {
  username.style.borderColor = username.value ? "green" : "red";
});

password.addEventListener("input", function () {
  password.style.borderColor = password.value ? "green" : "red";
});

// Foco automático al cargar
window.onload = function () {
  username.focus();
};
