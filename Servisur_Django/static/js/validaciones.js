// ------------------ JS Unificado (completo y actualizado) ------------------
document.addEventListener("DOMContentLoaded", () => {
  // ---------- Notificaciones ----------
  const NOTIF_DURATION = 3000;
  function obtenerContenedorNotificaciones() {
    let cont = document.getElementById("js-notificaciones-global");
    if (!cont) {
      cont = document.createElement("div");
      cont.id = "js-notificaciones-global";
      cont.style.position = "fixed";
      cont.style.top = "1rem";
      cont.style.right = "1rem";
      cont.style.zIndex = 9999;
      cont.style.pointerEvents = "none";
      document.body.appendChild(cont);
    }
    return cont;
  }
  function mostrarNotificacionSuccess(texto, duracion = NOTIF_DURATION) {
    const cont = obtenerContenedorNotificaciones();
    if (Array.from(cont.children).some(n => n.textContent === texto)) return;
    const div = document.createElement("div");
    div.className = "js-notif js-notif-success";
    div.textContent = texto;
    div.style.background = "#28a745";
    div.style.color = "#fff";
    div.style.padding = "0.5rem 0.75rem";
    div.style.marginTop = "0.5rem";
    div.style.borderRadius = "6px";
    div.style.boxShadow = "0 6px 18px rgba(40,167,69,0.15)";
    div.style.fontSize = "0.95rem";
    div.style.pointerEvents = "auto";
    div.style.opacity = "0";
    div.style.transition = "opacity 220ms ease";
    cont.appendChild(div);
    requestAnimationFrame(() => { div.style.opacity = "1"; });
    const timeoutId = setTimeout(() => { div.style.opacity = "0"; setTimeout(() => div.remove(), 240); }, duracion);
    div.addEventListener("click", () => { clearTimeout(timeoutId); div.style.opacity = "0"; setTimeout(() => div.remove(), 200); });
  }
  function mostrarNotificacion(texto, tipo = "error") {
    if (typeof window.mostrarNotificacion === "function") { window.mostrarNotificacion(texto, tipo); return; }
    const cont = obtenerContenedorNotificaciones();
    if (Array.from(cont.children).some(n => n.textContent === texto)) return;
    const div = document.createElement("div");
    div.className = "js-notif js-notif-" + tipo;
    div.textContent = texto;
    // colores: error = rojo, advertencia = amarillo, success aparte
    div.style.background = tipo === "error" ? "#d9534f" : (tipo === "advertencia" ? "#f0ad4e" : "#28a745");
    div.style.color = "#fff";
    div.style.padding = "0.5rem 0.75rem";
    div.style.marginTop = "0.5rem";
    div.style.borderRadius = "6px";
    div.style.boxShadow = "0 6px 18px rgba(0,0,0,0.08)";
    div.style.fontSize = "0.95rem";
    div.style.pointerEvents = "auto";
    div.style.opacity = "0";
    div.style.transition = "opacity 220ms ease";
    cont.appendChild(div);
    requestAnimationFrame(() => { div.style.opacity = "1"; });
    setTimeout(() => { div.style.opacity = "0"; setTimeout(() => div.remove(), 240); }, NOTIF_DURATION);
  }

  // ---------- Selectores (según tu HTML) ----------
  const form = document.querySelector("form");

  // Identificación
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

  // Cliente
  const nombreInput = document.getElementById("id_cliente-Nombre");
  const apellidoInput = document.getElementById("id_cliente-Apellido");
  const telefonoInput = document.getElementById("id_cliente-Numero_telefono");

  // Marca / Modelo
  const marcaSelect = document.getElementById("marca-select");
  const nuevoBloqueMarca = document.getElementById("nuevo-bloque-marca");
  const nuevaMarcaInput = document.getElementById("nueva_marca");
  const modeloSelect = document.getElementById("modelo-select");
  const nuevoModeloBloque = document.getElementById("nuevo-modelo-input");
  const nuevaModeloInput = document.getElementById("nuevo_modelo");

  // Método bloqueo
  const metodoSelect = document.getElementById("id_dispositivo-Metodo_Bloqueo");
  const codigoInput = document.getElementById("id_dispositivo-Codigo_Bloqueo");
  const guiaPatron = document.getElementById("imagen-patron");

  // Tipo falla / observaciones
  const tipoFalla = document.getElementById("id_dispositivo-Tipo_Falla");
  const campoNuevaFalla = document.getElementById("campo-nueva-falla");
  const nuevaFallaInput = document.getElementById("nueva_falla");
  const observaciones = document.getElementById("id_dispositivo-Observaciones");

  // Pedido
  const fechaOrden = document.getElementById("fecha_orden");
  const costoTotal = document.getElementById("costo_total");
  const abono = document.getElementById("abono");
  const restante = document.getElementById("restante");

  // ---------- Utilidades de error inline ----------
  function obtenerOCrearContenedor(input, id) {
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
  errorRut = obtenerOCrearContenedor(inputRut, "error-rut");
  const errorPasaporte = obtenerOCrearContenedor(inputPasaporte, "error-pasaporte");
  const errorNombre = obtenerOCrearContenedor(nombreInput, "error-nombre");
  const errorApellido = obtenerOCrearContenedor(apellidoInput, "error-apellido");
  const errorTelefono = obtenerOCrearContenedor(telefonoInput, "error-telefono");

  function mostrarErrorCampo(el, mensaje) {
    if (!el) return;
    el.classList.add("is-invalid");
    let cont = el.nextElementSibling;
    if (!cont || !cont.classList.contains("invalid-feedback")) {
      cont = document.createElement("div");
      cont.className = "invalid-feedback";
      el.insertAdjacentElement("afterend", cont);
    }
    cont.textContent = mensaje;
    cont.style.display = "block";
  }
  function limpiarErrorCampo(el) {
    if (!el) return;
    el.classList.remove("is-invalid");
    const cont = el.nextElementSibling;
    if (cont && cont.classList.contains("invalid-feedback")) cont.style.display = "none";
  }
  function mostrarErrorPersistente(input, contenedor, mensaje) {
    if (!input || !contenedor) return;
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    contenedor.textContent = mensaje;
    contenedor.style.display = "block";
  }
  function marcarValido(input, contenedor) {
    if (!input || !contenedor) return;
    contenedor.style.display = "none";
    input.classList.remove("is-invalid");
    if (input === inputRut) { input.classList.remove("is-valid"); return; }
    input.classList.add("is-valid");
  }

  // ---------- Validadores locales ----------
  function calcularDv(rutCuerpo) {
    let suma = 0; let multiplo = 2;
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
    const cuerpo = limpio.slice(0, -1); const dv = limpio.slice(-1).toUpperCase();
    return calcularDv(cuerpo) === dv;
  }
  function formatoPasaporteValido(p) { if (!p) return false; return /^[A-Za-z0-9.\-]{6,}$/.test(p.trim()); }

  function validarRut() {
    const valor = inputRut?.value.trim() || "";
    const valido = formatoRutValido(valor);
    if (valido) {
      inputRut?.classList.remove("is-invalid"); if (mensajeRut) { mensajeRut.textContent = ""; mensajeRut.style.display = "none"; }
      if (errorRut) errorRut.style.display = "none";
    } else {
      inputRut?.classList.remove("is-valid"); inputRut?.classList.add("is-invalid");
      if (mensajeRut) { mensajeRut.textContent = "❌ El RUT ingresado no es válido."; mensajeRut.style.display = "block"; }
      if (errorRut) errorRut.style.display = "block";
    }
    return valido;
  }
  function validarPasaporte() {
    const valor = inputPasaporte?.value.trim() || "";
    const valido = formatoPasaporteValido(valor);
    inputPasaporte?.classList.toggle("is-valid", valido);
    inputPasaporte?.classList.toggle("is-invalid", !valido);
    if (mensajePasaporte) { mensajePasaporte.textContent = valido ? "" : "❌ Documento inválido. Usa letras, números y mínimo 6 caracteres."; mensajePasaporte.style.display = valido ? "none" : "block"; }
    if (errorPasaporte) errorPasaporte.style.display = valido ? "none" : "block";
    return valido;
  }

  // Nombre/apellido/teléfono helpers
  function empiezaConMayuscula(val) { return /^[A-ZÁÉÍÓÚÑ]/.test(val.trim()); }
  function validarNombreEnviado() {
    const val = (nombreInput?.value || "").trim();
    const valido = val && empiezaConMayuscula(val);
    if (!valido) mostrarErrorPersistente(nombreInput, errorNombre, "❌ El nombre debe comenzar con letra mayúscula.");
    else marcarValido(nombreInput, errorNombre);
    return !!valido;
  }
  function validarApellidoEnviado() {
    const val = (apellidoInput?.value || "").trim();
    const valido = !val || empiezaConMayuscula(val);
    if (!valido) mostrarErrorPersistente(apellidoInput, errorApellido, "❌ El apellido debe comenzar con letra mayúscula.");
    else if (val) marcarValido(apellidoInput, errorApellido);
    else { apellidoInput?.classList.remove("is-valid", "is-invalid"); errorApellido && (errorApellido.style.display = "none"); }
    return valido;
  }
  function validarTelefonoEnviado() {
    const val = (telefonoInput?.value || "").trim();
    const valido = !val || /^\+569\d{8}$/.test(val);
    if (!valido) mostrarErrorPersistente(telefonoInput, errorTelefono, "❌ Formato inválido. Usa +569 seguido de 8 dígitos.");
    else if (val) marcarValido(telefonoInput, errorTelefono);
    else { telefonoInput?.classList.remove("is-valid", "is-invalid"); errorTelefono && (errorTelefono.style.display = "none"); }
    return valido;
  }

  // ---------- Formateo automático del RUT (puntos y guión) ----------
  inputRut?.addEventListener("input", () => {
    let valorRaw = inputRut.value.replace(/[^\dkK]/gi, "").toUpperCase();
    if (valorRaw.length < 2) {
      inputRut.value = valorRaw;
      return;
    }
    const cuerpo = valorRaw.slice(0, -1);
    const dv = valorRaw.slice(-1);
    let cuerpoFormateado = "";
    let i = cuerpo.length;
    while (i > 3) {
      cuerpoFormateado = "." + cuerpo.slice(i - 3, i) + cuerpoFormateado;
      i -= 3;
    }
    cuerpoFormateado = cuerpo.slice(0, i) + cuerpoFormateado;
    inputRut.value = `${cuerpoFormateado}-${dv}`;
  });

  // ---------- Evitar envío con Enter en inputs (no textarea ni submit) ----------
  document.querySelectorAll('input').forEach((el) => {
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && this.tagName.toLowerCase() !== 'textarea') {
        const type = (this.getAttribute('type') || '').toLowerCase();
        if (type !== 'submit' && type !== 'button') e.preventDefault();
      }
    });
  });

  // ---------- Pedido: restante y validación numérica ----------
  function esNumeroNoNegativo(el) { if (!el) return false; const v = el.value; if (v === "" || v == null) return false; const n = Number(v); return !Number.isNaN(n) && n >= 0; }
  function actualizarRestante() {
    const costo = costoTotal ? Number(costoTotal.value || 0) : 0;
    const ab = abono ? Number(abono.value || 0) : 0;
    const res = Math.max(0, (isFinite(costo) ? costo : 0) - (isFinite(ab) ? ab : 0));
    if (restante) restante.value = isFinite(res) ? res.toFixed(2) : "";
  }
  if (costoTotal) costoTotal.addEventListener("input", () => { limpiarErrorCampo(costoTotal); actualizarRestante(); });
  if (abono) abono.addEventListener("input", () => { limpiarErrorCampo(abono); actualizarRestante(); });

  // ---------- Marca / Modelo / Falla: insertar inline evitando duplicados (case-insensitive) ----------
  function existeOInsertarOption(selectEl, texto, seleccionar = true) {
    if (!selectEl || !texto) return false;
    const t = String(texto).trim();
    if (!t) return false;

    // Normalizar para comparación
    const targetNorm = t.toLowerCase();

    // Buscar opciones existentes equivalentes (trim + case-insensitive)
    const iguales = Array.from(selectEl.options).filter(o => String(o.text || '').trim().toLowerCase() === targetNorm);

    if (iguales.length > 0) {
      // Si hay al menos una opción equivalente, seleccionar la primera y eliminar duplicados adicionales
      const primera = iguales[0];
      if (seleccionar) selectEl.value = primera.value;
      // eliminar duplicados extra (conservamos la primera encontrada)
      for (let i = 1; i < iguales.length; i++) {
        try {
          selectEl.removeChild(iguales[i]);
        } catch (err) {
          const idx = Array.from(selectEl.options).indexOf(iguales[i]);
          if (idx >= 0) selectEl.remove(idx);
        }
      }
      // Asegurarse que la selección exista en el select (por si value distinto)
      if (seleccionar) {
        const hasValue = Array.from(selectEl.options).some(o => o.value === selectEl.value);
        if (!hasValue) selectEl.value = primera.value;
      }
      selectEl.dispatchEvent(new Event("change", { bubbles: true }));
      return false; // no se creó
    }

    // No existe: crear nueva opción con value igual al texto limpio
    const opt = document.createElement("option");
    opt.value = t;
    opt.textContent = t;
    if (seleccionar) opt.selected = true;
    selectEl.appendChild(opt);
    selectEl.dispatchEvent(new Event("change", { bubbles: true }));
    return true; // se creó nueva opción
  }

  if (nuevaMarcaInput) {
    nuevaMarcaInput.addEventListener("keydown", function (e) {
      if (e.key !== "Enter") return;
      const visible = nuevoBloqueMarca && window.getComputedStyle(nuevoBloqueMarca).display !== "none";
      if (!visible) return;
      e.preventDefault();
      const valor = (this.value || "").trim();
      if (!valor) { mostrarNotificacion("❌ Ingresa el nombre de la marca antes de agregar", "error"); return; }
      const creado = existeOInsertarOption(marcaSelect, valor, true);
      if (creado) mostrarNotificacionSuccess("✅ Se agregó marca exitosamente");
      else mostrarNotificacion("⚠️ La marca ya existe", "advertencia");
      this.value = "";
    });
  }

  if (nuevaModeloInput) {
    nuevaModeloInput.addEventListener("keydown", function (e) {
      if (e.key !== "Enter") return;
      const visible = nuevoModeloBloque && window.getComputedStyle(nuevoModeloBloque).display !== "none";
      if (!visible) return;
      e.preventDefault();
      const valor = (this.value || "").trim();
      if (!valor) { mostrarNotificacion("❌ Ingresa el nombre del modelo antes de agregar", "error"); return; }
      const creado = existeOInsertarOption(modeloSelect, valor, true);
      if (creado) mostrarNotificacionSuccess("✅ Se agregó modelo exitosamente");
      else mostrarNotificacion("⚠️ El modelo ya existe", "advertencia");
      this.value = "";
    });
  }

  // ---------- Tipo de falla: agregar sin duplicados ----------
  if (tipoFalla) {
    tipoFalla.addEventListener("change", () => {
      const v = tipoFalla.value;
      if (v === "agregar_falla") {
        if (campoNuevaFalla) campoNuevaFalla.style.display = "block";
        setTimeout(() => nuevaFallaInput?.focus(), 50);
      } else {
        if (campoNuevaFalla) campoNuevaFalla.style.display = "none";
      }
    });
    tipoFalla.addEventListener("click", () => {
      if (tipoFalla.value === "agregar_falla") {
        if (campoNuevaFalla) campoNuevaFalla.style.display = "block";
        setTimeout(() => nuevaFallaInput?.focus(), 50);
      }
    });
  }

  if (nuevaFallaInput && campoNuevaFalla) {
    nuevaFallaInput.addEventListener("keydown", (e) => {
      if (e.key !== "Enter") return;
      e.preventDefault();
      const val = (nuevaFallaInput.value || "").trim();
      if (!val) { mostrarNotificacion("❌ Describe la nueva falla antes de agregar", "error"); return; }
      const creado = existeOInsertarOption(tipoFalla, val, true);
      if (creado) mostrarNotificacionSuccess("✅ Se agregó la nueva falla");
      else mostrarNotificacion("⚠️ La falla ya existe", "advertencia");
      nuevaFallaInput.value = "";
      campoNuevaFalla.style.display = "none";
    });
    nuevaFallaInput.addEventListener("blur", () => {
      const val = (nuevaFallaInput.value || "").trim();
      if (!val) return;
      setTimeout(() => {
        const creado = existeOInsertarOption(tipoFalla, val, true);
        if (creado) mostrarNotificacionSuccess("✅ Se agregó la nueva falla");
        else {
          const opt = Array.from(tipoFalla.options).find(o => o.text.trim().toLowerCase() === val.toLowerCase());
          if (opt) tipoFalla.value = opt.value;
        }
        nuevaFallaInput.value = "";
        campoNuevaFalla.style.display = "none";
      }, 120);
    });
  }

  // ---------- Método de bloqueo: ayuda + validación ----------
  const ayuda = document.createElement("div");
  if (codigoInput && codigoInput.parentNode) { ayuda.className = "form-text"; codigoInput.parentNode.appendChild(ayuda); }

  function actualizarAyudaBloqueo() {
    if (!metodoSelect || !codigoInput) return;
    const metodo = metodoSelect.value;
    codigoInput.classList.remove("is-invalid", "is-valid");
    if (metodo === "PIN") { codigoInput.placeholder = "Ej: 1234"; ayuda.textContent = "PIN opcional (no se valida)."; }
    else if (metodo === "PASS") { codigoInput.placeholder = "Ej: claveSegura123"; ayuda.textContent = "Contraseña opcional (no se valida)."; }
    else if (metodo === "PATRON") { codigoInput.placeholder = "Ej: 1-5-9"; ayuda.textContent = "Ingresa la secuencia del patrón usando números del 1 al 9 (ej: 1-5-9)."; }
    else { ayuda.textContent = ""; }
  }

  function validarCodigoBloqueo() {
    if (!metodoSelect || !codigoInput) return true;
    const metodo = metodoSelect.value;
    const valor = codigoInput.value.trim();
    if (!metodo || metodo === "" || metodo === "PIN" || metodo === "PASS") {
      codigoInput.classList.remove("is-invalid");
      codigoInput.classList.remove("is-valid");
      return true;
    }
    let valido = false;
    if (metodo === "PATRON") valido = /^([1-9](?:[-,][1-9]){2,})$/.test(valor);
    codigoInput.classList.toggle("is-valid", valido);
    codigoInput.classList.toggle("is-invalid", !valido);
    return valido;
  }

  if (metodoSelect) {
    const primera = metodoSelect.querySelector('option[value=""]');
    if (primera) primera.disabled = false;
  }
  metodoSelect?.addEventListener("change", () => { actualizarAyudaBloqueo(); actualizarGuiaVisual(); });
  codigoInput?.addEventListener("blur", validarCodigoBloqueo);
  function actualizarGuiaVisual() { if (!guiaPatron || !metodoSelect) return; guiaPatron.style.display = metodoSelect.value === "PATRON" ? "block" : "none"; }
  actualizarAyudaBloqueo();
  actualizarGuiaVisual();

  // ---------- Validación de fecha: forzar fecha actual (min/max) y función utilitaria robusta ----------
  (function fijarFechaHoy() {
    const hoy = new Date();
    const yyyy = hoy.getFullYear();
    const mm = String(hoy.getMonth() + 1).padStart(2, '0');
    const dd = String(hoy.getDate()).padStart(2, '0');
    const hoyStr = `${yyyy}-${mm}-${dd}`;
    if (fechaOrden) {
      fechaOrden.setAttribute('min', hoyStr);
      fechaOrden.setAttribute('max', hoyStr);
      // asegurar formato correcto y valor por defecto hoy
      if (!fechaOrden.value || fechaOrden.value !== hoyStr) fechaOrden.value = hoyStr;
    }
  })();

  function fechaEsHoy(valorFecha) {
    if (!valorFecha) return false;
    const raw = String(valorFecha).trim();
    // Si ya está en formato YYYY-MM-DD, comparar por string local (evita timezone issues)
    if (/^\d{4}-\d{2}-\d{2}$/.test(raw)) {
      const hoy = new Date();
      const hoyStr = `${hoy.getFullYear()}-${String(hoy.getMonth()+1).padStart(2,'0')}-${String(hoy.getDate()).padStart(2,'0')}`;
      return raw === hoyStr;
    }
    // Fallback: parsear y comparar componentes en zona local
    const f = new Date(raw);
    if (Number.isNaN(f.getTime())) return false;
    const hoy = new Date();
    return f.getFullYear() === hoy.getFullYear()
      && f.getMonth() === hoy.getMonth()
      && f.getDate() === hoy.getDate();
  }

  // ---------- Validación global in submit (ordenada y única) ----------
  if (form) {
    form.addEventListener("submit", function (e) {
      // limpiar errores visuales previos
      [inputRut, inputPasaporte, nombreInput, apellidoInput, telefonoInput, marcaSelect, modeloSelect, tipoFalla, fechaOrden, costoTotal, abono, codigoInput].forEach(limpiarErrorCampo);

      // 1) Identificación (RUT o Pasaporte)
      const rutVal = inputRut ? (String(inputRut.value || "").trim()) : "";
      const pasVal = inputPasaporte ? (String(inputPasaporte.value || "").trim()) : "";
      if (!((rutVal && formatoRutValido(rutVal)) || (pasVal && formatoPasaporteValido(pasVal)))) {
        e.preventDefault();
        if (rutVal) { mostrarErrorCampo(inputRut, "❌ RUT inválido o formato incorrecto."); inputRut.scrollIntoView({ behavior: "smooth", block: "center" }); inputRut.focus({ preventScroll: true }); }
        else if (pasVal) { mostrarErrorCampo(inputPasaporte, "❌ Pasaporte inválido o formato incorrecto."); inputPasaporte.scrollIntoView({ behavior: "smooth", block: "center" }); inputPasaporte.focus({ preventScroll: true }); }
        else { if (inputRut) mostrarErrorCampo(inputRut, "❌ Debes ingresar RUT o Pasaporte."); if (inputRut) { inputRut.scrollIntoView({ behavior: "smooth", block: "center" }); inputRut.focus({ preventScroll: true }); } }
        mostrarNotificacion("⚠️ Completa la identificación (RUT o Pasaporte).", "advertencia");
        return;
      }

      // 2) Nombre
      if (!validarNombreEnviado()) { e.preventDefault(); nombreInput.scrollIntoView({ behavior: "smooth", block: "center" }); nombreInput.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Revisa el nombre.", "advertencia"); return; }

      // 3) Apellido
      if (!validarApellidoEnviado()) { e.preventDefault(); apellidoInput.scrollIntoView({ behavior: "smooth", block: "center" }); apellidoInput.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Revisa el apellido.", "advertencia"); return; }

      // 4) Teléfono
      if (!validarTelefonoEnviado()) { e.preventDefault(); telefonoInput.scrollIntoView({ behavior: "smooth", block: "center" }); telefonoInput.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Revisa el teléfono.", "advertencia"); return; }

      // 5) Marca
      const marcaVal = marcaSelect ? String(marcaSelect.value || "").trim() : "";
      if (!marcaVal) { e.preventDefault(); mostrarErrorCampo(marcaSelect, "❌ Debes seleccionar o crear una marca."); marcaSelect.scrollIntoView({ behavior: "smooth", block: "center" }); marcaSelect.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Selecciona la marca.", "advertencia"); return; }

      // 6) Modelo
      const modeloVal = modeloSelect ? String(modeloSelect.value || "").trim() : "";
      if (!modeloVal) { e.preventDefault(); mostrarErrorCampo(modeloSelect, "❌ Debes seleccionar o crear un modelo."); modeloSelect.scrollIntoView({ behavior: "smooth", block: "center" }); modeloSelect.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Selecciona el modelo.", "advertencia"); return; }

      // 7) Tipo de falla
      const tipoVal = tipoFalla ? String(tipoFalla.value || "").trim() : "";
      if (!tipoVal) { e.preventDefault(); mostrarErrorCampo(tipoFalla, "❌ Debes seleccionar un tipo de falla."); tipoFalla.scrollIntoView({ behavior: "smooth", block: "center" }); tipoFalla.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Selecciona el tipo de falla.", "advertencia"); return; }

      // 8) Fecha de ingreso -> debe ser la fecha actual (lectura directa y trim)
      const fechaInputEl = document.getElementById('fecha_orden');
      const fechaRaw = fechaInputEl ? String(fechaInputEl.value || '').trim() : '';
      console.log('DEBUG validar fecha -> input:', fechaRaw);
      if (!fechaRaw || !fechaEsHoy(fechaRaw)) {
        e.preventDefault();
        mostrarErrorCampo(fechaInputEl, "❌ La fecha debe ser la fecha actual.");
        fechaInputEl && fechaInputEl.scrollIntoView({ behavior: "smooth", block: "center" });
        fechaInputEl && fechaInputEl.focus({ preventScroll: true });
        mostrarNotificacion("⚠️ Ingresa la fecha de hoy.", "advertencia");
        return;
      }

      // 9) Costo total
      if (!esNumeroNoNegativo(costoTotal)) { e.preventDefault(); mostrarErrorCampo(costoTotal, "❌ Debes indicar un costo válido (0 o mayor)."); costoTotal.scrollIntoView({ behavior: "smooth", block: "center" }); costoTotal.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Indica el costo total.", "advertencia"); return; }

      // 10) Abono opcional: si existe validar rango
      if (abono && (abono.value || "").trim() !== "") {
        const abVal = Number(abono.value);
        const cVal = Number(costoTotal.value || 0);
        if (Number.isNaN(abVal) || abVal < 0) { e.preventDefault(); mostrarErrorCampo(abono, "❌ Abono inválido."); abono.scrollIntoView({ behavior: "smooth", block: "center" }); abono.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Revisa el abono.", "advertencia"); return; }
        if (abVal > cVal) { e.preventDefault(); mostrarErrorCampo(abono, "❌ El abono no puede ser mayor que el costo total."); abono.scrollIntoView({ behavior: "smooth", block: "center" }); abono.focus({ preventScroll: true }); mostrarNotificacion("⚠️ El abono no puede exceder el costo total.", "advertencia"); return; }
      }

      // 11) Validar código de bloqueo si corresponde (solo PATRON valida)
      if (metodoSelect && metodoSelect.value && codigoInput) {
        if (!validarCodigoBloqueo()) { e.preventDefault(); codigoInput.scrollIntoView({ behavior: "smooth", block: "center" }); codigoInput.focus({ preventScroll: true }); mostrarNotificacion("⚠️ Revisa el código de bloqueo.", "advertencia"); return; }
      }

      // actualizar restante final antes de enviar
      actualizarRestante();

      // Si llegamos aquí, todo OK: submit natural
    }, { passive: false });
  }

  // ---------- UX: listeners input / blur ----------
  inputRut?.addEventListener("input", () => {
    const val = inputRut.value.trim();
    if (formatoRutValido(val)) { inputRut.classList.remove("is-invalid"); if (errorRut) errorRut.style.display = "none"; } else inputRut.classList.remove("is-valid");
  });
  inputRut?.addEventListener("blur", validarRut);
  inputPasaporte?.addEventListener("input", () => {
    const val = inputPasaporte.value.trim();
    if (formatoPasaporteValido(val)) marcarValido(inputPasaporte, errorPasaporte);
    else inputPasaporte.classList.remove("is-valid");
  });
  inputPasaporte?.addEventListener("blur", validarPasaporte);

  nombreInput?.addEventListener("input", () => { const val = nombreInput.value.trim(); if (empiezaConMayuscula(val)) marcarValido(nombreInput, errorNombre); });
  apellidoInput?.addEventListener("input", () => { const val = apellidoInput.value.trim(); if (!val) { apellidoInput.classList.remove("is-valid","is-invalid"); errorApellido && (errorApellido.style.display="none"); } else if (empiezaConMayuscula(val)) marcarValido(apellidoInput, errorApellido); });
  telefonoInput?.addEventListener("input", () => { const val = telefonoInput.value.trim(); if (!val) { telefonoInput.classList.remove("is-valid","is-invalid"); errorTelefono && (errorTelefono.style.display="none"); } else if (/^\+569\d{8}$/.test(val)) marcarValido(telefonoInput, errorTelefono); });

  metodoSelect?.addEventListener("change", () => { actualizarAyudaBloqueo(); actualizarGuiaVisual(); });
  codigoInput?.addEventListener("blur", validarCodigoBloqueo);

  // Inicializaciones
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
  btnRut?.addEventListener("change", () => { if (btnRut.checked) mostrarRut(); });
  btnPasaporte?.addEventListener("change", () => { if (btnPasaporte.checked) mostrarPasaporte(); });

  mostrarRut();
  actualizarRestante();
  actualizarAyudaBloqueo();
  actualizarGuiaVisual();
});
// ------------------ Fin JS Unificado ------------------





document.getElementById("btn-guardar-modal").addEventListener("click", async () => {
  const form = document.getElementById("form-editar-orden");
  const ordenId = form.querySelector("[name='orden_id']").value;

  const estadoSelect = form.querySelector("[name='nuevo_estado']");
  if (!estadoSelect || !estadoSelect.value) {
    alert("⚠️ Debes seleccionar un estado válido.");
    estadoSelect.focus();
    return;
  }

  const formData = new FormData(form);

  try {
    const res = await fetch(`/reparacion/${ordenId}/editar/`, {
      method: "POST",
      headers: { "X-CSRFToken": getCsrfToken() }, // asegúrate de tener esta función
      body: formData,
    });

    if (res.ok) {
      alert("✅ Orden actualizada correctamente");
      const modal = bootstrap.Modal.getInstance(document.getElementById("modal-editar"));
      modal.hide();
      location.reload();
    } else {
      alert("❌ Error al actualizar la orden");
    }
  } catch (err) {
    console.error("Error al enviar el formulario:", err);
    alert("❌ Error inesperado al guardar");
  }
});







