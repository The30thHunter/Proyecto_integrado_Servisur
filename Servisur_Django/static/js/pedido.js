document.addEventListener("DOMContentLoaded", function () {
  const costeInput = document.getElementById("id_pedido-Coste");
  const abonoInput = document.getElementById("id_pedido-Abono");
  const restanteInput = document.getElementById("id_pedido-Restante");

  function calcularRestante() {
    const coste = parseFloat(costeInput.value) || 0;
    const abono = parseFloat(abonoInput.value) || 0;
    const restante = coste - abono;
    restanteInput.value = restante >= 0 ? restante.toFixed(0) : 0;
  }

  costeInput.addEventListener("input", calcularRestante);
  abonoInput.addEventListener("input", calcularRestante);
});
