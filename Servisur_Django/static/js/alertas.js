document.addEventListener("DOMContentLoaded", function () {
  const alertBox = document.getElementById("alertBox");
  if (!alertBox) return;

  const closeBtn = document.createElement("span");
  closeBtn.innerHTML = "&times;";
  closeBtn.classList.add("close-btn");
  closeBtn.onclick = () => alertBox.classList.remove("show");
  alertBox.appendChild(closeBtn);

  // Mostrar si hay contenido
  if (alertBox.dataset.message) {
    alertBox.innerText = alertBox.dataset.message;
    alertBox.appendChild(closeBtn);

    const tipo = alertBox.dataset.type;
    if (tipo === "success") alertBox.classList.add("success");
    else if (tipo === "warning") alertBox.classList.add("warning");

    alertBox.classList.add("show");

    // Ocultar automáticamente
    setTimeout(() => {
      alertBox.classList.remove("show");
    }, 2000);
  }
});
