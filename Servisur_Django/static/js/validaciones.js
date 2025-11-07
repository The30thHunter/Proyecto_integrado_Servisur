// ========VALIDACIONES NOMBRE Y APELLIDO==========

// 🧍 Capitaliza cada palabra del campo
function capitalizarTexto(input) {
  let valor = input.value.trim();
  if (valor.length > 0) {
    input.value = valor
      .split(" ")
      .map(
        (palabra) =>
          palabra.charAt(0).toUpperCase() + palabra.slice(1).toLowerCase()
      )
      .join(" ");
  }
}

// ✅ Valida que el campo tenga al menos 4 caracteres
function validarMinimo(input, min = 4) {
  const valor = input.value.trim();
  if (valor.length < min) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else {
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
    return true;
  }
}

// 🔁 Aplica ambas validaciones al campo
function aplicarValidacionesTexto(idCampo) {
  const campo = document.getElementById(idCampo);
  if (!campo) return;

  campo.addEventListener("input", () => capitalizarTexto(campo));
  campo.addEventListener("blur", () => validarMinimo(campo));
}

// 🚫 Evita envío si hay errores y hace scroll al primero
function bloquearEnvioYEnfocarErrores() {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const nombre = document.getElementById("id_Nombre");
    const apellido = document.getElementById("id_Apellido");

    const nombreValido = validarMinimo(nombre);
    const apellidoValido = validarMinimo(apellido);

    if (!nombreValido || !apellidoValido) {
      e.preventDefault(); // ❌ bloquea envío

      // 🔍 Encuentra el primer campo inválido y sube hasta él
      const primerInvalido = document.querySelector(".is-invalid");
      if (primerInvalido) {
        primerInvalido.scrollIntoView({ behavior: "smooth", block: "center" });
        primerInvalido.focus();
      }
    }
  });
}

// ========VALIDACIONES TELEFONO==========

// ☎️ Valida formato internacional de teléfono
function validarTelefono(input) {
  const valor = input.value.trim();
  const regex = /^\+?\d{7,15}$/;

  if (!regex.test(valor)) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else {
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
    return true;
  }
}

// 🔁 Aplica validación al campo teléfono
function aplicarValidacionTelefono(idCampo) {
  const campo = document.getElementById(idCampo);
  if (!campo) return;

  campo.addEventListener("blur", () => validarTelefono(campo));
  campo.addEventListener("input", () => {
    if (campo.classList.contains("is-invalid")) {
      validarTelefono(campo); // actualiza en tiempo real si hay error
    }
  });
}

// 🚫 Bloquea envío si teléfono es inválido y enfoca
function bloquearEnvioSiTelefonoInvalido() {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const telefono = document.getElementById("id_Numero_telefono");
    const valido = validarTelefono(telefono);

    if (!valido) {
      e.preventDefault();

      telefono.scrollIntoView({ behavior: "smooth", block: "center" });
      telefono.focus();
    }
  });
}

// ========VALIDACIONES DIRECCIONES==========

// 🏠 Valida que la dirección tenga al menos 5 caracteres reales
function validarDireccion(input, min = 5) {
  const valor = input.value.trim();
  if (valor.length < min) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else {
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
    return true;
  }
}

// 🔁 Aplica validación al campo dirección
function aplicarValidacionDireccion(idCampo) {
  const campo = document.getElementById(idCampo);
  if (!campo) return;

  campo.addEventListener("blur", () => validarDireccion(campo));
  campo.addEventListener("input", () => {
    if (campo.classList.contains("is-invalid")) {
      validarDireccion(campo); // actualiza en tiempo real si hay error
    }
  });
}

// 🚫 Bloquea envío si dirección es inválida y enfoca
function bloquearEnvioSiDireccionInvalida() {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const direccion = document.getElementById("id_Direccion");
    const valido = validarDireccion(direccion);

    if (!valido) {
      e.preventDefault();
      direccion.scrollIntoView({ behavior: "smooth", block: "center" });
      direccion.focus();
    }
  });
}

// ========VALIDACIONES RUT==========
// 🔢 Valida el RUT chileno con dígito verificador
function validarRut(input) {
  const valor = input.value
    .replace(/\./g, "")
    .replace(/-/g, "")
    .toUpperCase()
    .trim();

  if (!/^\d{7,8}[0-9K]$/.test(valor)) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  }

  const cuerpo = valor.slice(0, -1);
  const dvIngresado = valor.slice(-1);

  let suma = 0;
  let multiplo = 2;

  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += parseInt(cuerpo.charAt(i)) * multiplo;
    multiplo = multiplo < 7 ? multiplo + 1 : 2;
  }

  const dvEsperado = 11 - (suma % 11);
  let dvCalculado = "";

  if (dvEsperado === 11) {
    dvCalculado = "0";
  } else if (dvEsperado === 10) {
    dvCalculado = "K";
  } else {
    dvCalculado = dvEsperado.toString();
  }

  if (dvCalculado !== dvIngresado) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  }

  input.classList.remove("is-invalid");
  input.classList.add("is-valid");
  return true;
}

// 🔁 Aplica validación al campo RUT
function aplicarValidacionRut(idCampo) {
  const campo = document.getElementById(idCampo);
  if (!campo) return;

  campo.addEventListener("blur", () => validarRut(campo));
  campo.addEventListener("input", () => {
    if (campo.classList.contains("is-invalid")) {
      validarRut(campo); // actualiza en tiempo real si hay error
    }
  });
}

// 🚫 Bloquea envío si RUT es inválido y enfoca
function bloquearEnvioSiRutInvalido() {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const rut = document.getElementById("id_Rut");
    const valido = validarRut(rut);

    if (!valido) {
      e.preventDefault();
      rut.scrollIntoView({ behavior: "smooth", block: "center" });
      rut.focus();
    }
  });
}

// ========VALIDACIONES TIPO FALLA==========

// ✅ Valida que la descripción de falla tenga al menos 10 caracteres y contenido válido
function validarFalla(input) {
  const valor = input.value.trim();
  const regex = /^[A-Za-zÁÉÍÓÚÑÜ0-9\s.,;:()\-¿?!¡]{10,}$/;

  if (!regex.test(valor)) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else {
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
    return true;
  }
}

// 🔁 Aplica validación al campo tipo de falla
function aplicarValidacionFalla(idCampo) {
  const campo = document.getElementById(idCampo);
  if (!campo) return;

  campo.addEventListener("blur", () => validarFalla(campo));
  campo.addEventListener("input", () => {
    if (campo.classList.contains("is-invalid")) {
      validarFalla(campo); // actualiza en tiempo real si hay error
    }
  });
}

// 🚫 Bloquea envío si tipo de falla es inválido
function bloquearEnvioSiFallaInvalida() {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const falla = document.getElementById("tipo_falla");
    if (falla) {
      const valido = validarFalla(falla);
      if (!valido) {
        e.preventDefault();
        falla.scrollIntoView({ behavior: "smooth", block: "center" });
        falla.focus();
      }
    }
  });
}

// ========VALIDACIONES FECHA=========

// ✅ Valida que la fecha no esté vacía ni sea futura
function validarFecha(input) {
  const valor = input.value;
  const hoy = new Date().toISOString().split("T")[0];

  if (!valor || valor > hoy) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    return false;
  } else {
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
    return true;
  }
}

// 🔁 Aplica validación al campo fecha
function aplicarValidacionFecha(idCampo) {
  const campo = document.getElementById(idCampo);
  if (!campo) return;

  campo.addEventListener("blur", () => validarFecha(campo));
  campo.addEventListener("input", () => {
    if (campo.classList.contains("is-invalid")) {
      validarFecha(campo);
    }
  });
}

// 🚫 Bloquea envío si la fecha es inválida
function bloquearEnvioSiFechaInvalida() {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const fecha = document.getElementById("fecha_orden");
    if (fecha) {
      const valido = validarFecha(fecha);
      if (!valido) {
        e.preventDefault();
        fecha.scrollIntoView({ behavior: "smooth", block: "center" });
        fecha.focus();
      }
    }
  });
}

// ========VALIDACIONES PAGO=========

// ✅ Valida que el valor sea un número positivo
function validarNumeroPositivo(input) {
  const valor = parseFloat(input.value);
  return !isNaN(valor) && valor >= 0;
}

// ✅ Valida el costo total
function validarCosto(input) {
  const valido = validarNumeroPositivo(input) && parseFloat(input.value) > 0;
  input.classList.toggle("is-valid", valido);
  input.classList.toggle("is-invalid", !valido);
  return valido;
}

// ✅ Valida el abono (menor o igual al costo)
function validarAbono(abonoInput, costoInput) {
  const abono = parseFloat(abonoInput.value);
  const costo = parseFloat(costoInput.value);
  const valido = validarNumeroPositivo(abonoInput) && abono <= costo;
  abonoInput.classList.toggle("is-valid", valido);
  abonoInput.classList.toggle("is-invalid", !valido);
  return valido;
}

// ✅ Calcula y muestra el restante
function calcularRestante(costoInput, abonoInput, restanteInput) {
  const costo = parseFloat(costoInput.value);
  const abono = parseFloat(abonoInput.value);
  if (!isNaN(costo) && !isNaN(abono)) {
    const restante = Math.max(costo - abono, 0);
    restanteInput.value = restante.toFixed(0);
  }
}

// 🚫 Bloquea envío si hay errores
function bloquearEnvioCostos() {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const costo = document.getElementById("costo_total");
    const abono = document.getElementById("abono");
    const restante = document.getElementById("restante");

    const validoCosto = validarCosto(costo);
    const validoAbono = validarAbono(abono, costo);

    if (!validoCosto || !validoAbono) {
      e.preventDefault();
      (validoCosto ? abono : costo).scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
      (validoCosto ? abono : costo).focus();
    } else {
      calcularRestante(costo, abono, restante);
    }
  });
}

// 🚀 Inicializa validaciones al cargar
document.addEventListener("DOMContentLoaded", () => {
  aplicarValidacionesTexto("id_Nombre");
  aplicarValidacionesTexto("id_Apellido");
  bloquearEnvioYEnfocarErrores();

  aplicarValidacionTelefono("id_Numero_telefono");
  bloquearEnvioSiTelefonoInvalido();

  aplicarValidacionDireccion("id_Direccion");
  bloquearEnvioSiDireccionInvalida();

  aplicarValidacionRut("id_Rut");
  bloquearEnvioSiRutInvalido();

  aplicarValidacionFalla("tipo_falla");
  bloquearEnvioSiFallaInvalida();

  aplicarValidacionFecha("fecha_orden");
  bloquearEnvioSiFechaInvalida();
});

document.addEventListener("DOMContentLoaded", () => {
  const costo = document.getElementById("costo_total");
  const abono = document.getElementById("abono");
  const restante = document.getElementById("restante");

  if (costo && abono && restante) {
    costo.addEventListener("blur", () => validarCosto(costo));
    abono.addEventListener("blur", () => validarAbono(abono, costo));
    abono.addEventListener("input", () =>
      calcularRestante(costo, abono, restante)
    );
    costo.addEventListener("input", () =>
      calcularRestante(costo, abono, restante)
    );
  }

  bloquearEnvioCostos();
});
