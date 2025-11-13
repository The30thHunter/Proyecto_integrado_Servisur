// ==========================
// VALIDACIONES: Identificación y bloqueo (RUT y Pasaporte con verificación de existencia)
// ==========================
// ==========================
// VALIDACIONES: Identificación y bloqueo (validaciones locales RUT y Pasaporte)
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
  let errorRut = document.getElementById("error-rut");

  let modo = "rut";

  function mostrarRut() {
    modo = "rut";
    if (campoRut) campoRut.style.display = "block";
    if (campoPasaporte) campoPasaporte.style.display = "none";
    if (inputRut) inputRut.value = "";
    if (inputPasaporte) inputPasaporte.value = "";
    if (mensajeRut) mensajeRut.style.display = "none";
    if (mensajePasaporte) mensajePasaporte.style.display = "none";
    if (errorRut) errorRut.style.display = "none";
    inputRut?.classList.remove("is-valid", "is-invalid");
  }

  function mostrarPasaporte() {
    modo = "pasaporte";
    if (campoRut) campoRut.style.display = "none";
    if (campoPasaporte) campoPasaporte.style.display = "block";
    if (inputRut) inputRut.value = "";
    if (inputPasaporte) inputPasaporte.value = "";
    if (mensajeRut) mensajeRut.style.display = "none";
    if (mensajePasaporte) mensajePasaporte.style.display = "none";
    if (errorRut) errorRut.style.display = "none";
    inputPasaporte?.classList.remove("is-valid", "is-invalid");
  }

  btnRut?.addEventListener("change", () => {
    if (btnRut.checked) mostrarRut();
  });

  btnPasaporte?.addEventListener("change", () => {
    if (btnPasaporte.checked) mostrarPasaporte();
  });

  function obtenerOCrearContenedor(input, existingElement, id) {
    if (existingElement) return existingElement;
    if (!input) return null;
    let next = input.nextElementSibling;
    if (next && next.classList.contains("invalid-feedback")) return next;
    const div = document.createElement("div");
    div.className = "invalid-feedback";
    if (id) div.id = id;
    div.style.display = "none";
    input.insertAdjacentElement("afterend", div);
    return div;
  }

  errorRut = obtenerOCrearContenedor(inputRut, errorRut, "error-rut");
  const errorPasaporte = obtenerOCrearContenedor(inputPasaporte, null, "error-pasaporte");

  // Formatear RUT en tiempo real (sin DV calc; solo formato visual)
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
    } else {
      inputRut.value = valor;
    }
  });

  // ---- RUT: validar dígito verificador
  function calcularDv(rutCuerpo) {
    // rutCuerpo sin puntos ni guion, sin DV
    let suma = 0;
    let multiplo = 2;
    for (let i = rutCuerpo.length - 1; i >= 0; i--) {
      suma += parseInt(rutCuerpo.charAt(i), 10) * multiplo;
      multiplo = multiplo === 7 ? 2 : multiplo + 1;
    }
    const res = 11 - (suma % 11);
    if (res === 11) return "0";
    if (res === 10) return "K";
    return String(res);
  }

  function formatoRutValido(rut) {
    if (!rut) return false;
    const limpio = rut.replace(/\./g, "").replace(/-/g, "");
    if (!/^\d{2,8}[\dKk]$/.test(limpio)) return false;
    const cuerpo = limpio.slice(0, -1);
    const dv = limpio.slice(-1).toUpperCase();
    return calcularDv(cuerpo) === dv;
  }

  function formatoPasaporteValido(p) {
    if (!p) return false;
    return /^[A-Za-z0-9.\-]{6,}$/.test(p.trim());
  }

  // Mostrar mensajes persistentes
  function mostrarErrorPersistente(input, contenedor, mensaje) {
    if (!input || !contenedor) return;
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    contenedor.textContent = mensaje;
    contenedor.style.display = "block";
  }

  // marcarValido general pero sin aplicar is-valid al RUT
  function marcarValido(input, contenedor) {
    if (!input || !contenedor) return;
    contenedor.style.display = "none";
    input.classList.remove("is-invalid");
    // Si el input es el RUT, no añadir is-valid (solicitud previa)
    if (input === inputRut) {
      input.classList.remove("is-valid");
      return;
    }
    input.classList.add("is-valid");
  }

  // Validaciones en blur (solo formato + visual)
  function validarRut() {
    const valor = inputRut?.value.trim() || "";
    const valido = formatoRutValido(valor);
    // NO aplicar is-valid en el RUT; solo quitar is-invalid cuando es válido
    if (valido) {
      inputRut?.classList.remove("is-invalid");
      if (mensajeRut) mensajeRut.textContent = "";
      if (mensajeRut) mensajeRut.style.display = "none";
      if (errorRut) errorRut.style.display = "none";
    } else {
      inputRut?.classList.remove("is-valid");
      inputRut?.classList.add("is-invalid");
      if (mensajeRut) mensajeRut.textContent = "❌ El RUT ingresado no es válido.";
      if (mensajeRut) mensajeRut.style.display = "block";
      if (errorRut) errorRut.style.display = "block";
    }
    return valido;
  }

  function validarPasaporte() {
    const valor = inputPasaporte?.value.trim() || "";
    const valido = formatoPasaporteValido(valor);
    inputPasaporte?.classList.toggle("is-valid", valido);
    inputPasaporte?.classList.toggle("is-invalid", !valido);
    if (mensajePasaporte) mensajePasaporte.textContent = valido ? "" : "❌ Documento inválido. Usa letras, números y mínimo 6 caracteres.";
    if (mensajePasaporte) mensajePasaporte.style.display = valido ? "none" : "block";
    if (errorPasaporte) errorPasaporte.style.display = valido ? "none" : "block";
    return valido;
  }

  inputRut?.addEventListener("blur", validarRut);
  inputPasaporte?.addEventListener("blur", validarPasaporte);

  // --- Enviar: validar formato según modo (sin verificar existencia en servidor) ---
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      let validoFormato = true;
      if (modo === "rut") {
        validoFormato = validarRut();
      } else {
        validoFormato = validarPasaporte();
      }

      if (!validoFormato) {
        e.preventDefault();
        if (modo === "rut") {
          inputRut?.scrollIntoView({ behavior: "smooth", block: "center" });
          inputRut?.focus({ preventScroll: true });
        } else {
          inputPasaporte?.scrollIntoView({ behavior: "smooth", block: "center" });
          inputPasaporte?.focus({ preventScroll: true });
        }
        mostrarNotificacion("⚠️ Debes ingresar un documento válido.", "error");
        return;
      }

      // si todo es válido, permitir envío normal
    });
  }

  // Limpiar mensajes cuando el usuario corrige
  inputRut?.addEventListener("input", () => {
    const val = inputRut.value.trim();
    if (formatoRutValido(val)) {
      // NO marcar is-valid para RUT, solo quitar is-invalid
      inputRut.classList.remove("is-invalid");
      if (errorRut) errorRut.style.display = "none";
    } else {
      inputRut.classList.remove("is-valid");
    }
  });

  inputPasaporte?.addEventListener("input", () => {
    const val = inputPasaporte.value.trim();
    if (formatoPasaporteValido(val)) {
      marcarValido(inputPasaporte, errorPasaporte);
    } else {
      inputPasaporte.classList.remove("is-valid");
    }
  });

  // Inicializar vista
  mostrarRut();

  // Notificación auxiliar
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
});


// 1) Evitar envío con Enter dentro de inputs (previene envíos accidentales)
document.querySelectorAll('input').forEach((el) => {
  el.addEventListener('keydown', function (e) {
    // permite Enter si el elemento es un textarea
    if (e.key === 'Enter' && this.tagName.toLowerCase() !== 'textarea') {
      // si el elemento tiene type="submit" o es un botón no lo bloqueamos
      const type = (this.getAttribute('type') || '').toLowerCase();
      if (type !== 'submit' && type !== 'button') {
        e.preventDefault();
      }
    }
  });
});

// 2) Validación central al submit: chequear campos requeridos y reglas antes de enviar
const form = document.querySelector('form');
if (form) {
  form.addEventListener('submit', function (e) {
    // lista de validaciones que YA tienes; aquí combinamos las tuyas y
    // además verificamos que los campos obligatorios no estén vacíos
    // Ajusta nombres según tu formulario si difieren

    // ejemplo: campos que deben existir y no estar vacíos
    const requiredSelectors = [
      '#id_cliente-Nombre',      // nombre obligatorio
      // agrega otros required si aplica, por ejemplo:
      // '#id_dispositivo-Modelo',
      // '#id_cliente-Email'
    ];

    // encontrar primer campo vacío entre los requeridos
    let primerInvalido = null;
    for (const sel of requiredSelectors) {
      const el = document.querySelector(sel);
      if (!el) continue; // si no existe, lo ignoramos
      const val = (el.value || '').trim();
      if (!val) {
        primerInvalido = el;
        // marcar visualmente
        el.classList.add('is-invalid');
        // crear/mostrar mensaje si no existe (reutiliza tu helper si lo tienes)
        let cont = el.nextElementSibling;
        if (!cont || !cont.classList.contains('invalid-feedback')) {
          cont = document.createElement('div');
          cont.className = 'invalid-feedback';
          el.insertAdjacentElement('afterend', cont);
        }
        cont.textContent = '❌ Este campo es obligatorio.';
        cont.style.display = 'block';
        break;
      }
    }

    // ahora ejecuta tus validaciones específicas existentes
    // (ejemplo usando tus funciones: validarRut(), validarPasaporte(), validarNombreEnviado(), etc.)
    // Si tienes validaciones asíncronas no olvides adaptarlas (await + async listener).
    let okIdentificacion = true;
    // si usas modo (rut/pasaporte), validar formato según modo
    const modoSeleccion = (typeof modo !== 'undefined') ? modo : null;
    if (modoSeleccion === 'rut') {
      okIdentificacion = validarRut(); // tu función local de formato
    } else if (modoSeleccion === 'pasaporte') {
      okIdentificacion = validarPasaporte();
    }

    // validación nombre (ejemplo: exigir mayúscula inicial)
    const nombreEl = document.getElementById('id_cliente-Nombre');
    let okNombre = true;
    if (nombreEl) {
      const val = (nombreEl.value || '').trim();
      okNombre = /^[A-ZÁÉÍÓÚÑ]/.test(val);
      if (!okNombre && !primerInvalido) {
        primerInvalido = nombreEl;
        nombreEl.classList.add('is-invalid');
        let cont = nombreEl.nextElementSibling;
        if (!cont || !cont.classList.contains('invalid-feedback')) {
          cont = document.createElement('div');
          cont.className = 'invalid-feedback';
          nombreEl.insertAdjacentElement('afterend', cont);
        }
        cont.textContent = '❌ El nombre debe comenzar con mayúscula.';
        cont.style.display = 'block';
      }
    }

    // si ya hay un primerInvalido, prevenimos y enfocamos
    if (primerInvalido || !okIdentificacion || !okNombre) {
      e.preventDefault();

      // preferir el primerInvalido si existe, sino buscar otro fallo
      const foco = primerInvalido || (okIdentificacion ? null : (document.getElementById('id_cliente-Rut') || document.getElementById('id_cliente-Pasaporte')));
      if (foco) {
        foco.scrollIntoView({ behavior: 'smooth', block: 'center' });
        foco.focus({ preventScroll: true });
      }

      // notificación global opcional
      if (typeof mostrarNotificacion === 'function') {
        mostrarNotificacion('⚠️ Completa los campos obligatorios antes de enviar.', 'advertencia');
      }
    } else {
      // permite el envío: limpiar mensajes visibles redundantes
      document.querySelectorAll('.invalid-feedback').forEach((c) => {
        if (c.textContent === '❌ Este campo es obligatorio.' || c.textContent.includes('mayúscula')) {
          c.style.display = 'none';
        }
      });
    }
  }, { passive: false });
}



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
  if (!guiaPatron || !metodoSelect) return; // Evita error si no existen
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

  // Obtener o crear contenedor de error bajo cada input
  function obtenerContenedorError(input, id) {
    if (!input) return null;
    let cont = input.nextElementSibling;
    if (cont && cont.classList.contains("invalid-feedback")) return cont;
    cont = document.createElement("div");
    cont.className = "invalid-feedback";
    if (id) cont.id = id;
    cont.style.display = "none";
    input.insertAdjacentElement("afterend", cont);
    return cont;
  }

  const errorNombre = obtenerContenedorError(nombreInput, "error-nombre");
  const errorApellido = obtenerContenedorError(apellidoInput, "error-apellido");
  const errorTelefono = obtenerContenedorError(telefonoInput, "error-telefono");

  // Mostrar mensaje persistente (no se oculta automáticamente)
  function mostrarErrorPersistente(input, contenedor, mensaje) {
    if (!input || !contenedor) return;
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    contenedor.textContent = mensaje;
    contenedor.style.display = "block";
  }

  // Limpiar y marcar válido
  function marcarValido(input, contenedor) {
    if (!input || !contenedor) return;
    contenedor.style.display = "none";
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
  }

  // Validación simple de mayúscula inicial
  function empiezaConMayuscula(val) {
    return /^[A-ZÁÉÍÓÚÑ]/.test(val.trim());
  }

  // VALIDACIONES usadas al enviar
  function validarNombreEnviado() {
    const val = (nombreInput?.value || "").trim();
    const valido = val && empiezaConMayuscula(val);
    if (!valido) {
      mostrarErrorPersistente(nombreInput, errorNombre, "❌ El nombre debe comenzar con letra mayúscula.");
    } else {
      marcarValido(nombreInput, errorNombre);
    }
    return !!valido;
  }

  function validarApellidoEnviado() {
    const val = (apellidoInput?.value || "").trim();
    const valido = !val || empiezaConMayuscula(val);
    if (!valido) {
      mostrarErrorPersistente(apellidoInput, errorApellido, "❌ El apellido debe comenzar con letra mayúscula.");
    } else if (val) {
      marcarValido(apellidoInput, errorApellido);
    } else {
      // vacío: limpiar visuales
      apellidoInput?.classList.remove("is-valid", "is-invalid");
      errorApellido && (errorApellido.style.display = "none");
    }
    return valido;
  }

  function validarTelefonoEnviado() {
    const val = (telefonoInput?.value || "").trim();
    const valido = !val || /^\+569\d{8}$/.test(val);
    if (!valido) {
      mostrarErrorPersistente(telefonoInput, errorTelefono, "❌ Formato inválido. Usa +569 seguido de 8 dígitos.");
    } else if (val) {
      marcarValido(telefonoInput, errorTelefono);
    } else {
      telefonoInput?.classList.remove("is-valid", "is-invalid");
      errorTelefono && (errorTelefono.style.display = "none");
    }
    return valido;
  }

  // Al enviar: validar y enfocar primer error
  const form = document.querySelector("form");
  form?.addEventListener("submit", (e) => {
    const okNombre = validarNombreEnviado();
    const okApellido = validarApellidoEnviado();
    const okTelefono = validarTelefonoEnviado();

    if (!okNombre || !okApellido || !okTelefono) {
      e.preventDefault();

      // encontrar primer campo inválido en el orden: nombre, apellido, telefono
      const primerosInvalidos = [];
      if (!okNombre) primerosInvalidos.push(nombreInput);
      if (!okApellido) primerosInvalidos.push(apellidoInput);
      if (!okTelefono) primerosInvalidos.push(telefonoInput);

      const primero = primerosInvalidos.find(Boolean);
      if (primero) {
        primero.scrollIntoView({ behavior: "smooth", block: "center" });
        primero.focus({ preventScroll: true });
      }

      if (typeof mostrarNotificacion === "function") {
        mostrarNotificacion("⚠️ Revisa los datos del cliente antes de continuar", "advertencia");
      }
    }
  });

  // Al escribir: limpiar el error inmediatamente cuando el campo sea correcto
  nombreInput?.addEventListener("input", () => {
    const val = nombreInput.value.trim();
    if (empiezaConMayuscula(val)) {
      marcarValido(nombreInput, errorNombre);
    } else {
      // mantener is-invalid visible hasta que corrija en envío o cambie a válido
    }
  });

  apellidoInput?.addEventListener("input", () => {
    const val = apellidoInput.value.trim();
    if (!val) {
      apellidoInput.classList.remove("is-valid", "is-invalid");
      errorApellido.style.display = "none";
    } else if (empiezaConMayuscula(val)) {
      marcarValido(apellidoInput, errorApellido);
    }
  });

  telefonoInput?.addEventListener("input", () => {
    const val = telefonoInput.value.trim();
    if (!val) {
      telefonoInput.classList.remove("is-valid", "is-invalid");
      errorTelefono.style.display = "none";
    } else if (/^\+569\d{8}$/.test(val)) {
      marcarValido(telefonoInput, errorTelefono);
    }
  });
});



// ==========================
// VALIDACIONES: Datos de equipo
// ==========================
