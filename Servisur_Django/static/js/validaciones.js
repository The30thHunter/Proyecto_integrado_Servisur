// ==========================
// VALIDACIONES: Identificación y bloqueo
// ==========================

document.addEventListener("DOMContentLoaded", () => {
  // Estado actual del modo de identificación
  let modoIdentificacion = "RUT";

  // Elementos
  const btnRut = document.getElementById("btn-rut");
  const btnExt = document.getElementById("btn-extranjero");
  const inputId = document.getElementById("id_cliente-Rut");
  const labelId = document.getElementById("label-identificacion");
  const ayudaId = document.getElementById("ayuda-identificacion");
  const errorId = document.getElementById("error-identificacion");

  // 🔄 Cambiar a modo RUT
  function activarRut() {
    modoIdentificacion = "RUT";
    labelId.textContent = "RUT";
    inputId.placeholder = "Ej: 12.345.678-9";
    ayudaId.textContent = "Ingresa el RUT chileno con formato válido.";
    errorId.textContent = "Ingresa un RUT válido.";
    inputId.value = "";
    inputId.classList.remove("is-invalid", "is-valid");
  }

  // 🔄 Cambiar a modo extranjero
  function activarExtranjero() {
    modoIdentificacion = "EXT";
    labelId.textContent = "Documento extranjero";
    inputId.placeholder = "Ej: AB123456, DNI987654";
    ayudaId.textContent = "Ingresa pasaporte, DNI u otro documento válido.";
    errorId.textContent = "Ingresa un documento válido.";
    inputId.value = "";
    inputId.classList.remove("is-invalid", "is-valid");
  }

  // ✅ Validar RUT chileno
  function validarRut(rut) {
    rut = rut.replace(/\./g, "").replace(/-/g, "").toUpperCase();
    if (!/^(\d{7,8})([0-9K])$/.test(rut)) return false;
    const cuerpo = rut.slice(0, -1);
    const dv = rut.slice(-1);
    let suma = 0, multiplo = 2;
    for (let i = cuerpo.length - 1; i >= 0; i--) {
      suma += parseInt(cuerpo[i]) * multiplo;
      multiplo = multiplo < 7 ? multiplo + 1 : 2;
    }
    const dvEsperado = 11 - (suma % 11);
    const dvFinal = dvEsperado === 11 ? "0" : dvEsperado === 10 ? "K" : dvEsperado.toString();
    return dv === dvFinal;
  }

  // ✅ Validar identificación según modo
  function validarIdentificacion() {
    const valor = inputId.value.trim();
    let valido = false;

    if (modoIdentificacion === "RUT") {
      const rutRegex = /^[0-9]{7,8}-?[0-9Kk]$/;
      valido = rutRegex.test(valor) && validarRut(valor);
    } else {
      const docRegex = /^[A-Za-z0-9.\-]{6,}$/;
      valido = docRegex.test(valor);
    }

    inputId.classList.toggle("is-valid", valido);
    inputId.classList.toggle("is-invalid", !valido);
    return valido;
  }

  // 🧩 Eventos
  btnRut?.addEventListener("click", activarRut);
  btnExt?.addEventListener("click", activarExtranjero);
  inputId?.addEventListener("blur", validarIdentificacion);

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
});

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
