// ==========================
// Lógica principal (marcas, modelos, fallas, etc.)
// ==========================


// ✅ Cálculo automático del campo Restante
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

  if (costeInput && abonoInput && restanteInput) {
    costeInput.addEventListener("input", calcularRestante);
    abonoInput.addEventListener("input", calcularRestante);
  }

  // 🔄 Carga dinámica de modelos según marca
  const marcaSelect = document.getElementById("marca-select");
  const modeloSelect = document.getElementById("modelo-select");
  const nuevoModeloInput = document.getElementById("nuevo_modelo");
  const nuevoModeloWrapper = document.getElementById("nuevo-modelo-input");
  const nuevaMarcaInput = document.getElementById("nueva_marca");
  const nuevoBloqueMarca = document.getElementById("nuevo-bloque-marca");

  modeloSelect.disabled = true;

  marcaSelect.addEventListener("change", function () {
    const marcaId = this.value;
    modeloSelect.innerHTML = "";
    nuevoModeloWrapper.style.display = "none";
    nuevoModeloInput.value = "";

    if (marcaId === "agregar_marca") {
      nuevoBloqueMarca.style.display = "block";
      nuevaMarcaInput.required = true;
      return;
    } else {
      nuevoBloqueMarca.style.display = "none";
      nuevaMarcaInput.required = false;
      nuevaMarcaInput.value = "";
    }

    if (!marcaId || isNaN(marcaId)) {
      modeloSelect.disabled = true;
      return;
    }

    const loadingOption = document.createElement("option");
    loadingOption.textContent = "Cargando modelos...";
    loadingOption.disabled = true;
    loadingOption.selected = true;
    modeloSelect.appendChild(loadingOption);
    modeloSelect.disabled = true;

    fetch(`/obtener_modelos_por_marca?marca_id=${marcaId}`)
      .then((res) => res.json())
      .then((data) => {
        modeloSelect.innerHTML = '<option value="">Seleccione modelo</option>';
        data.forEach((modelo) => {
          const opt = document.createElement("option");
          opt.value = modelo.id;
          opt.textContent = modelo.Modelo;
          modeloSelect.appendChild(opt);
        });

        const optExtra = document.createElement("option");
        optExtra.value = "agregar_nuevo";
        optExtra.textContent = "➕ Agregar nuevo modelo";
        modeloSelect.appendChild(optExtra);

        modeloSelect.disabled = false;
      })
      .catch((err) => {
        console.error("Error al cargar modelos:", err);
        modeloSelect.innerHTML =
          "<option disabled>Error al cargar modelos</option>";
        modeloSelect.disabled = true;
      });
  });

  modeloSelect.addEventListener("change", function () {
    if (this.value === "agregar_nuevo") {
      nuevoModeloWrapper.style.display = "block";
      nuevoModeloInput.required = true;
      nuevoModeloInput.focus();
    } else {
      nuevoModeloWrapper.style.display = "none";
      nuevoModeloInput.required = false;
      nuevoModeloInput.value = "";
    }
  });

  // ✅ Agregar nueva marca y activar campo de nuevo modelo
  nuevaMarcaInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      const nombre = nuevaMarcaInput.value.trim();
      if (!nombre) {
        nuevaMarcaInput.classList.add("is-invalid");
        return;
      }

      fetch("/agregar_marca_ajax/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `nombre=${encodeURIComponent(nombre)}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.error) {
            nuevaMarcaInput.classList.add("is-invalid");
            return;
          }

          const nuevaOpcion = document.createElement("option");
          nuevaOpcion.value = data.id;
          nuevaOpcion.textContent = data.nombre;

          const agregarOpcion = marcaSelect.querySelector(
            'option[value="agregar_marca"]'
          );
          marcaSelect.insertBefore(nuevaOpcion, agregarOpcion);
          nuevaOpcion.selected = true;

          nuevaMarcaInput.value = "";
          nuevaMarcaInput.classList.remove("is-invalid");
          nuevoBloqueMarca.style.display = "none";

          marcaSelect.dispatchEvent(new Event("change"));

          // ✅ Seleccionar automáticamente “Agregar nuevo modelo”
          setTimeout(() => {
            const agregarNuevo = modeloSelect.querySelector(
              'option[value="agregar_nuevo"]'
            );
            if (agregarNuevo) {
              agregarNuevo.selected = true;
              modeloSelect.dispatchEvent(new Event("change"));
              nuevoModeloInput.focus();
            }
          }, 300);
        })
        .catch(() => nuevaMarcaInput.classList.add("is-invalid"));
    }
  });

  // ✅ Agregar nuevo modelo
  nuevoModeloInput.addEventListener("keydown", function (e) {
    if (
      e.key === "Enter" &&
      marcaSelect.value &&
      marcaSelect.value !== "agregar_marca"
    ) {
      e.preventDefault();
      const nombre = nuevoModeloInput.value.trim();
      const marcaId = marcaSelect.value;

      if (!nombre) {
        nuevoModeloInput.classList.add("is-invalid");
        return;
      }

      fetch("/agregar_modelo_ajax/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `nombre=${encodeURIComponent(
          nombre
        )}&marca_id=${encodeURIComponent(marcaId)}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.error) {
            nuevoModeloInput.classList.add("is-invalid");
            return;
          }

          const nuevaOpcion = document.createElement("option");
          nuevaOpcion.value = data.id;
          nuevaOpcion.textContent = data.nombre;

          const agregarOpcion = modeloSelect.querySelector(
            'option[value="agregar_nuevo"]'
          );
          modeloSelect.insertBefore(nuevaOpcion, agregarOpcion);
          nuevaOpcion.selected = true;

          nuevoModeloInput.value = "";
          nuevoModeloInput.classList.remove("is-invalid");
          nuevoModeloWrapper.style.display = "none";
        })
        .catch(() => nuevoModeloInput.classList.add("is-invalid"));
    }
  });
});

// ✅ Mostrar/ocultar campo de nueva falla
const selectFalla = document.getElementById("id_dispositivo-Tipo_Falla");
const campoNuevaFalla = document.getElementById("campo-nueva-falla");
const inputNuevaFalla = document.getElementById("nueva_falla");
const btnAgregarFalla = document.getElementById("btn-agregar-falla");

selectFalla?.addEventListener("change", () => {
  const mostrar = selectFalla.value === "agregar_falla";
  campoNuevaFalla.style.display = mostrar ? "block" : "none";
  inputNuevaFalla.classList.remove("is-invalid", "is-valid");
});

 /*// ✅ Validar selección antes de enviar el formulario
document.querySelector("form")?.addEventListener("submit", function (e) {
  const seleccion = selectFalla.value;
  let valido = true;

  if (seleccion === "") {
    selectFalla.classList.add("is-invalid");
    valido = false;
  } else {
    selectFalla.classList.remove("is-invalid");
    selectFalla.classList.add("is-valid");
  }

  if (seleccion === "agregar_falla") {
    const texto = inputNuevaFalla.value.trim();
    if (texto.length < 3) {
      inputNuevaFalla.classList.add("is-invalid");
      valido = false;
    } else {
      inputNuevaFalla.classList.remove("is-invalid");
      inputNuevaFalla.classList.add("is-valid");
    }
  }

  if (!valido) {
    e.preventDefault();
    selectFalla.scrollIntoView({ behavior: "smooth", block: "center" });
    selectFalla.focus();
  }
});*/

// ✅ Función para agregar nueva falla vía AJAX
function agregarFalla() {
  const texto = inputNuevaFalla.value.trim();
  if (texto.length < 3) {
    inputNuevaFalla.classList.add("is-invalid");
    return;
  }

  fetch("/agregar_falla_ajax/", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `falla=${encodeURIComponent(texto)}`,
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        inputNuevaFalla.classList.add("is-invalid");
        return;
      }

      const nuevaOpcion = document.createElement("option");
      nuevaOpcion.value = data.Falla || data.nombre || data.id;
      nuevaOpcion.textContent = data.Falla || data.nombre;

      const agregarOpcion = selectFalla.querySelector(
        'option[value="agregar_falla"]'
      );
      selectFalla.insertBefore(nuevaOpcion, agregarOpcion);
      nuevaOpcion.selected = true;

      inputNuevaFalla.classList.remove("is-invalid");
      inputNuevaFalla.classList.add("is-valid");
      campoNuevaFalla.style.display = "none";
      inputNuevaFalla.value = "";

      mostrarMensaje("✅ Falla agregada correctamente.");
    })
    .catch(() => {
      inputNuevaFalla.classList.add("is-invalid");
    });
}

// ✅ Agregar falla con Enter o botón
btnAgregarFalla?.addEventListener("click", agregarFalla);
inputNuevaFalla?.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    agregarFalla();
  }
});

// ✅ Cargar todas las fallas desde el backend
function poblarSelectFallas(selectedId = null) {
  fetch("/obtener_tipos_falla/")
    .then((res) => res.json())
    .then((tipos) => {
      const select = document.getElementById("id_dispositivo-Tipo_Falla");
      if (!select) return;

      const placeholder = '<option value="" disabled>Seleccione una falla</option>';

      tipos.forEach((t) => {
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.textContent = t.Falla;
        if (selectedId && String(selectedId) === String(t.id))
          opt.selected = true;
        select.appendChild(opt);
      });

      const optExtra = document.createElement("option");
      optExtra.value = "agregar_falla";
      optExtra.textContent = "➕ Agregar nueva falla";
      select.appendChild(optExtra);
    })
    .catch((err) => console.error("Error cargando tipos de falla:", err));
}

// ✅ Carga inicial al abrir la página
document.addEventListener("DOMContentLoaded", () => {
  poblarSelectFallas();
});

// ✅ Mensaje sutil de éxito
function mostrarMensaje(texto) {
  const mensaje = document.createElement("div");
  mensaje.textContent = texto;
  mensaje.className = "text-success small mt-1 fade-in";
  mensaje.style.transition = "opacity 0.5s ease";
  mensaje.style.opacity = "0";

  const destino = campoNuevaFalla || document.body;
  destino.appendChild(mensaje);

  setTimeout(() => (mensaje.style.opacity = "1"), 50);
  setTimeout(() => {
    mensaje.style.opacity = "0";
    setTimeout(() => mensaje.remove(), 500);
  }, 2500);
}

//PARTE DE METODO DE BLOQUEO

document.addEventListener("DOMContentLoaded", () => {
  const metodoSelect = document.getElementById("id_dispositivo-Metodo_Bloqueo");
  const imagenPatron = document.getElementById("imagen-patron");
  const bloqueCodigo = document.getElementById("bloque-codigo");
  const codigoInput = document.getElementById("id_dispositivo-Codigo_Bloqueo");

  function actualizarAyudaBloqueo() {
    let ayuda = document.getElementById("ayuda-bloqueo");

    if (!ayuda) {
      ayuda = document.createElement("div");
      ayuda.id = "ayuda-bloqueo";
      ayuda.className = "form-text mt-1";
      codigoInput.parentNode.appendChild(ayuda);
    }

    const metodo = metodoSelect.value;

    if (metodo === "PIN") {
      codigoInput.placeholder = "Ej: 1234";
      ayuda.textContent = "Ingresa un PIN numérico de 4 a 6 dígitos.";
    } else if (metodo === "PASS") {
      codigoInput.placeholder = "Ej: claveSegura123";
      ayuda.textContent = "Ingresa una contraseña de al menos 6 caracteres.";
    } else if (metodo === "PATRON") {
      codigoInput.placeholder = "Ej: 1-2-4-5";
      ayuda.textContent = "Ingresa la secuencia del patrón usando números del 1 al 9 (ej: 1-2-4-5).";
    } else {
      codigoInput.placeholder = "";
      ayuda.textContent = "";
    }
  }

  function actualizarVisibilidadBloqueo() {
    const valor = metodoSelect.value;
    const mostrar = valor === "PIN" || valor === "PASS" || valor === "PATRON";
    bloqueCodigo.style.display = mostrar ? "block" : "none";
    imagenPatron.style.display = valor === "PATRON" ? "block" : "none";
    actualizarAyudaBloqueo();
  }

  metodoSelect?.addEventListener("change", actualizarVisibilidadBloqueo);
  actualizarVisibilidadBloqueo(); // inicializa al cargar
});


document.addEventListener("DOMContentLoaded", () => {
  const btnRut = document.getElementById("btn-rut");
  const btnPasaporte = document.getElementById("btn-pasaporte");
  const campoRut = document.getElementById("campo-rut");
  const campoPasaporte = document.getElementById("campo-pasaporte");

  function actualizarCampos() {
    campoRut.style.display = btnRut.checked ? "block" : "none";
    campoPasaporte.style.display = btnPasaporte.checked ? "block" : "none";
  }

  btnRut?.addEventListener("change", actualizarCampos);
  btnPasaporte?.addEventListener("change", actualizarCampos);
});

