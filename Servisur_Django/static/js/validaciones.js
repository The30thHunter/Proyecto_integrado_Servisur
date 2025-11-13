// ==========================
// VALIDACIONES: Identificación y bloqueo
// ==========================
document.addEventListener("DOMContentLoaded", () => {
  const btnRut = document.getElementById("btn-rut");
  const btnPasaporte = document.getElementById("btn-pasaporte");

  const campoRut = document.getElementById("campo-rut");
  const campoPasaporte = document.getElementById("campo-pasaporte");

  const inputRut = document.getElementById("id_cliente-Rut");
  const inputPasaporte = document.getElementById("id_cliente-Pasaporte");

  const mensajeRut = document.getElementById("mensaje-identificacion");
  const mensajePasaporte = document.getElementById("mensaje-pasaporte");
  const errorRut = document.getElementById("error-rut");

  let modo = "rut";

  function mostrarRut() {
    modo = "rut";
    campoRut.style.display = "block";
    campoPasaporte.style.display = "none";
    inputRut.value = "";
    inputPasaporte.value = "";
    mensajeRut.style.display = "none";
    mensajePasaporte.style.display = "none";
    errorRut.style.display = "none";
    inputRut.classList.remove("is-valid", "is-invalid");
  }

  function mostrarPasaporte() {
    modo = "pasaporte";
    campoRut.style.display = "none";
    campoPasaporte.style.display = "block";
    inputRut.value = "";
    inputPasaporte.value = "";
    mensajeRut.style.display = "none";
    mensajePasaporte.style.display = "none";
    errorRut.style.display = "none";
    inputPasaporte.classList.remove("is-valid", "is-invalid");
  }

  btnRut?.addEventListener("change", () => {
    if (btnRut.checked) mostrarRut();
  });

  btnPasaporte?.addEventListener("change", () => {
    if (btnPasaporte.checked) mostrarPasaporte();
  });

  // Formatear RUT en tiempo real
  inputRut?.addEventListener("input", () => {
    const valor = inputRut.value.replace(/[^\dkK]/gi, "").toUpperCase();
    if (valor.length >= 2) {
      const cuerpo = valor.slice(0, -1);
      const dv = valor.slice(-1);
      let cuerpoFormateado = "";
      let i = cuerpo.length;
      while (i > 3) {
        cuerpoFormateado = "." + cuerpo.slice(i - 3, i) + cuerpoFormateado;
        i -= 3;
      }
      cuerpoFormateado = cuerpo.slice(0, i) + cuerpoFormateado;
      inputRut.value = `${cuerpoFormateado}-${dv}`;
    }
  });

  function validarRut() {
    const valor = inputRut.value.trim();
    const rutRegex = /^[0-9]{1,2}\.?\d{3}\.?\d{3}-[\dkK]$/;
    const valido = rutRegex.test(valor);

    inputRut.classList.toggle("is-valid", valido);
    inputRut.classList.toggle("is-invalid", !valido);
    mensajeRut.textContent = valido ? "" : "❌ El RUT ingresado no tiene el formato correcto.";
    mensajeRut.style.display = valido ? "none" : "block";
    errorRut.style.display = valido ? "none" : "block";

    return valido;
  }

  function validarPasaporte() {
    const valor = inputPasaporte.value.trim();
    const valido = /^[A-Za-z0-9.\-]{6,}$/.test(valor);

    inputPasaporte.classList.toggle("is-valid", valido);
    inputPasaporte.classList.toggle("is-invalid", !valido);
    mensajePasaporte.textContent = valido ? "" : "❌ Documento inválido. Usa letras, números y mínimo 6 caracteres.";
    mensajePasaporte.style.display = valido ? "none" : "block";

    return valido;
  }

  inputRut?.addEventListener("blur", validarRut);
  inputPasaporte?.addEventListener("blur", validarPasaporte);

  const form = document.querySelector("form");
  form?.addEventListener("submit", function (e) {
    let valido = false;

    if (modo === "rut") {
      valido = validarRut();
    } else {
      valido = validarPasaporte();
    }

    if (!valido) {
      e.preventDefault();
      mostrarNotificacion("⚠️ Debes ingresar un documento válido.", "error");
    }
  });

  function mostrarNotificacion(texto, tipo = "error") {
    const div = document.createElement("div");
    div.className = `notificacion ${tipo}`;
    div.textContent = texto;
    document.body.appendChild(div);
    setTimeout(() => div.classList.add("mostrar"), 50);
    setTimeout(() => {
      div.classList.remove("mostrar");
      setTimeout(() => div.remove(), 400);
    }, 3000);
  }

  mostrarRut(); // inicializa en modo RUT
});


  // ✅ Validación al enviar
  const form = document.querySelector("form");
  form?.addEventListener("submit", function (e) {
    const valido = validarIdentificacion();
    if (!valido) {
      e.preventDefault();
      inputId.scrollIntoView({ behavior: "smooth", block: "center" });
      inputId.focus();
    }
  });
  

  // 🔐 Ayuda dinámica para método de bloqueo
  const metodoSelect = document.getElementById("id_dispositivo-Metodo_Bloqueo");
  const codigoInput = document.getElementById("id_dispositivo-Codigo_Bloqueo");
  const ayuda = document.createElement("div");
  ayuda.className = "form-text";
  codigoInput?.parentNode.appendChild(ayuda);

  function actualizarAyudaBloqueo() {
    const metodo = metodoSelect.value;
    codigoInput.value = "";
    codigoInput.classList.remove("is-invalid", "is-valid");

    if (metodo === "PIN") {
      codigoInput.placeholder = "Ej: 1234";
      ayuda.textContent = "Ingresa un PIN numérico de 4 a 6 dígitos.";
    } else if (metodo === "PASS") {
      codigoInput.placeholder = "Ej: claveSegura123";
      ayuda.textContent = "Ingresa una contraseña de al menos 6 caracteres.";
    } else if (metodo === "PATRON") {
      codigoInput.placeholder = "Ej: 1-5-9";
      ayuda.textContent = "Ingresa la secuencia del patrón usando números del 1 al 9 (ej: 1-5-9).";
    }
  }

  function validarCodigoBloqueo() {
    const metodo = metodoSelect.value;
    const valor = codigoInput.value.trim();
    let valido = false;

    if (metodo === "PIN") {
      valido = /^[0-9]{4,6}$/.test(valor);
    } else if (metodo === "PASS") {
      valido = /^[A-Za-z0-9]{6,}$/.test(valor);
    } else if (metodo === "PATRON") {
      valido = /^([1-9](?:[-,][1-9]){2,})$/.test(valor);
    }

    codigoInput.classList.toggle("is-valid", valido);
    codigoInput.classList.toggle("is-invalid", !valido);
    return valido;
  }

  metodoSelect?.addEventListener("change", actualizarAyudaBloqueo);
  codigoInput?.addEventListener("blur", validarCodigoBloqueo);

  form?.addEventListener("submit", function (e) {
    if (!validarCodigoBloqueo()) {
      e.preventDefault();
      codigoInput.scrollIntoView({ behavior: "smooth", block: "center" });
      codigoInput.focus();
    }
  });

  actualizarAyudaBloqueo(); // inicializa ayuda al cargar

  // 🧩 Mostrar guía visual del patrón
  const guiaPatron = document.getElementById("guia-patron");
  function actualizarGuiaVisual() {
    guiaPatron.style.display = metodoSelect.value === "PATRON" ? "block" : "none";
  }
  metodoSelect?.addEventListener("change", actualizarGuiaVisual);
  actualizarGuiaVisual();

// ==========================
// VALIDACIONES: Cliente
// ==========================

document.addEventListener("DOMContentLoaded", () => {
  const nombreInput = document.getElementById("id_cliente-Nombre");
  const apellidoInput = document.getElementById("id_cliente-Apellido");
  const telefonoInput = document.getElementById("id_cliente-Numero_telefono");

  const tickNombre = document.getElementById("tick-nombre");
  const tickApellido = document.getElementById("tick-apellido");
  const tickTelefono = document.getElementById("tick-telefono");

  // ✅ Validar nombre (obligatorio, mínimo 4 letras, primera mayúscula)
  function validarNombre() {
    const val = nombreInput.value.trim();
    const valido = val.length >= 4 && /^[A-ZÁÉÍÓÚÑ]/.test(val);
    tickNombre?.classList.toggle("valid", valido);
    nombreInput.classList.toggle("is-valid", valido);
    nombreInput.classList.toggle("is-invalid", !valido);
    return valido;
  }

  // ✅ Validar apellido (opcional, si se rellena debe ser válido)
  function validarApellido() {
    const val = apellidoInput.value.trim();
    const valido = !val || (val.length >= 4 && /^[A-ZÁÉÍÓÚÑ]/.test(val));
    tickApellido?.classList.toggle("valid", valido);
    apellidoInput.classList.toggle("is-valid", valido && val);
    apellidoInput.classList.toggle("is-invalid", !valido && val);
    return valido;
  }

  // ✅ Validar teléfono chileno (opcional, si se rellena debe ser válido)
  function validarTelefono() {
    const val = telefonoInput.value.trim();
    const valido = !val || /^\+569\d{8}$/.test(val);
    tickTelefono?.classList.toggle("valid", valido);
    telefonoInput.classList.toggle("is-valid", valido && val);
    telefonoInput.classList.toggle("is-invalid", !valido && val);
    return valido;
  }

  // 🧩 Eventos en tiempo real
  nombreInput?.addEventListener("input", validarNombre);
  apellidoInput?.addEventListener("input", validarApellido);
  telefonoInput?.addEventListener("input", validarTelefono);

  // ✅ Validación al enviar formulario
  const form = document.querySelector("form");
  form?.addEventListener("submit", function (e) {
    const validoNombre = validarNombre();
    const validoApellido = validarApellido();
    const validoTelefono = validarTelefono();

    if (!validoNombre || !validoApellido || !validoTelefono) {
      e.preventDefault();
      mostrarNotificacion("⚠️ Revisa los datos del cliente antes de continuar", "advertencia");
    }
  });
});

function mostrarNotificacion(texto, tipo = "error") {
  const div = document.createElement("div");
  div.className = `notificacion ${tipo}`;
  div.textContent = texto;
  document.body.appendChild(div);
  setTimeout(() => div.classList.add("mostrar"), 50);
  setTimeout(() => {
    div.classList.remove("mostrar");
    setTimeout(() => div.remove(), 400);
  }, 3000);
}
