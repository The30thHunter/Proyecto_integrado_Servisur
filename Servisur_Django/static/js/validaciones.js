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

  // Cambiar a modo RUT
  function activarRut() {
    modoIdentificacion = "RUT";
    labelId.textContent = "RUT";
    inputId.placeholder = "Ej: 12.345.678-9";
    ayudaId.textContent = "Ingresa el RUT chileno con formato válido.";
    errorId.textContent = "Ingresa un RUT válido.";
    inputId.value = "";
    inputId.classList.remove("is-invalid", "is-valid");
  }

  // Cambiar a modo extranjero
  function activarExtranjero() {
    modoIdentificacion = "EXT";
    labelId.textContent = "Documento extranjero";
    inputId.placeholder = "Ej: AB123456, DNI987654";
    ayudaId.textContent = "Ingresa pasaporte, DNI u otro documento válido.";
    errorId.textContent = "Ingresa un documento válido.";
    inputId.value = "";
    inputId.classList.remove("is-invalid", "is-valid");
  }

  // Validar identificación según modo
  function validarIdentificacion() {
    const valor = inputId.value.trim();
    let valido = false;

    if (modoIdentificacion === "RUT") {
      const rutRegex = /^[0-9]{1,2}\.?\d{3}\.?\d{3}-[\dkK]$/;
      valido = rutRegex.test(valor);
    } else {
      const docRegex = /^[A-Za-z0-9.\-]{6,}$/;
      valido = docRegex.test(valor);
    }

    inputId.classList.toggle("is-valid", valido);
    inputId.classList.toggle("is-invalid", !valido);
    return valido;
  }

  // Eventos
  if (btnRut && btnExt) {
    btnRut.addEventListener("click", activarRut);
    btnExt.addEventListener("click", activarExtranjero);
  }

  inputId.addEventListener("blur", validarIdentificacion);

  // Validación al enviar
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      const valido = validarIdentificacion();
      if (!valido) {
        e.preventDefault();
        inputId.scrollIntoView({ behavior: "smooth", block: "center" });
        inputId.focus();
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const metodoSelect = document.getElementById("id_dispositivo-Metodo_Bloqueo");
  const codigoInput = document.getElementById("id_dispositivo-Codigo_Bloqueo");
  const ayuda = document.createElement("div");
  ayuda.className = "form-text";
  codigoInput.parentNode.appendChild(ayuda);

  function actualizarAyuda() {
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
      ayuda.textContent =
        "Ingresa la secuencia del patrón usando números del 1 al 9 (ej: 1-5-9).";
    }
  }

  function validarCodigo() {
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

  metodoSelect.addEventListener("change", actualizarAyuda);
  codigoInput.addEventListener("blur", validarCodigo);

  const form = document.querySelector("form");
  form.addEventListener("submit", function (e) {
    if (!validarCodigo()) {
      e.preventDefault();
      codigoInput.scrollIntoView({ behavior: "smooth", block: "center" });
      codigoInput.focus();
    }
  });

  actualizarAyuda(); // inicializa ayuda al cargar
});

document.addEventListener("DOMContentLoaded", () => {
  const metodoSelect = document.getElementById("id_dispositivo-Metodo_Bloqueo");
  const guiaPatron = document.getElementById("guia-patron");

  function actualizarGuiaVisual() {
    if (metodoSelect.value === "PATRON") {
      guiaPatron.style.display = "block";
    } else {
      guiaPatron.style.display = "none";
    }
  }

  metodoSelect.addEventListener("change", actualizarGuiaVisual);
  actualizarGuiaVisual(); // inicializa al cargar
});
