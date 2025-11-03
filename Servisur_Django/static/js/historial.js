document.addEventListener("DOMContentLoaded", function () {
  const filas = document.querySelectorAll(".historial-table tbody tr");
  filas.forEach((fila) => {
    const estado = fila.cells[7]?.textContent.trim();
    if (estado === "Pendiente") {
      fila.style.backgroundColor = "#fff8e1";
    }
  });
});
