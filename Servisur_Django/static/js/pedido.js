document.addEventListener("DOMContentLoaded", function () {
  // 🧮 Cálculo automático del campo Restante
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

  // 📦 Elementos del formulario
  const marcaSelect = document.getElementById("marca-select");
  const modeloSelect = document.getElementById("modelo-select");
  const nuevoModeloWrapper = document.getElementById("nuevo-modelo-input");
  const nuevoModeloInput = document.getElementById("nuevo_modelo");
  const nuevoBloque = document.getElementById("nuevo-bloque-marca-modelo");
  const nuevaMarcaInput = document.getElementById("nueva_marca");

  modeloSelect.disabled = true;

  // 📦 Carga dinámica de modelos según marca
  marcaSelect.addEventListener("change", function () {
    const marcaId = this.value;
    modeloSelect.innerHTML = "";
    nuevoModeloWrapper.style.display = "none";
    nuevoModeloInput.value = "";
    nuevoModeloInput.classList.remove("is-invalid");

    if (marcaId === "agregar_marca") {
      nuevoBloque.style.display = "block";
      nuevaMarcaInput.required = true;
      return;
    } else {
      nuevoBloque.style.display = "none";
      nuevaMarcaInput.required = false;
      nuevaMarcaInput.value = "";
      nuevaMarcaInput.classList.remove("is-invalid");
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
      .then((response) => {
        if (!response.ok) throw new Error("Respuesta no válida del servidor");
        return response.json();
      })
      .then((data) => {
        modeloSelect.innerHTML = "";

        const defaultOption = document.createElement("option");
        defaultOption.textContent = "Seleccione modelo";
        defaultOption.value = "";
        modeloSelect.appendChild(defaultOption);

        if (data.length === 0) {
          const noModelOption = document.createElement("option");
          noModelOption.textContent = "No hay modelos disponibles";
          noModelOption.disabled = true;
          modeloSelect.appendChild(noModelOption);
        } else {
          data.forEach((modelo) => {
            const option = document.createElement("option");
            option.value = modelo.id;
            option.textContent = modelo.Modelo;
            modeloSelect.appendChild(option);
          });
        }

        const addOption = document.createElement("option");
        addOption.textContent = "➕ Agregar nuevo modelo";
        addOption.value = "agregar_nuevo";
        modeloSelect.appendChild(addOption);

        modeloSelect.disabled = false;
      })
      .catch((error) => {
        console.error("❌ Error al cargar modelos:", error);
        modeloSelect.innerHTML = "";
        const errorOption = document.createElement("option");
        errorOption.textContent = "Error al cargar modelos";
        errorOption.disabled = true;
        modeloSelect.appendChild(errorOption);
        modeloSelect.disabled = true;
      });
  });

  // ✏️ Mostrar campo de nuevo modelo
  modeloSelect.addEventListener("change", function () {
    if (this.value === "agregar_nuevo") {
      nuevoModeloWrapper.style.display = "block";
      nuevoModeloInput.required = true;
      nuevoModeloInput.focus();
    } else {
      nuevoModeloWrapper.style.display = "none";
      nuevoModeloInput.required = false;
      nuevoModeloInput.value = "";
      nuevoModeloInput.classList.remove("is-invalid");
    }
  });

  // ✅ Agregar nueva marca (flujo completo)
  nuevaMarcaInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();

      const nombreMarca = nuevaMarcaInput.value.trim();
      console.log("Valor ingresado en nueva_marca:", nombreMarca);

      if (!nombreMarca) {
        nuevaMarcaInput.classList.add("is-invalid");
        return;
      }

      fetch("/agregar_marca_ajax/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `nombre=${encodeURIComponent(nombreMarca)}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.error) {
            console.error("Error:", data.error);
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
          nuevoBloque.style.display = "none";

          marcaSelect.dispatchEvent(new Event("change"));
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

          mostrarMensaje("✅ Marca agregada correctamente");
        })
        .catch((err) => {
          console.error("Error al agregar marca:", err);
          nuevaMarcaInput.classList.add("is-invalid");
        });
    }
  });

  // ✅ Agregar nuevo modelo para marca existente
  nuevoModeloInput.addEventListener("keydown", function (event) {
    if (
      event.key === "Enter" &&
      marcaSelect.value &&
      marcaSelect.value !== "agregar_marca" &&
      nuevoBloque.style.display === "none"
    ) {
      event.preventDefault();

      const modeloNombre = this.value.trim();
      const marcaId = marcaSelect.value;

      if (!modeloNombre || !marcaId) {
        this.classList.add("is-invalid");
        return;
      }

      fetch("/agregar_modelo_ajax/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `nombre=${encodeURIComponent(
          modeloNombre
        )}&marca_id=${encodeURIComponent(marcaId)}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.error) {
            console.error("Error:", data.error);
            this.classList.add("is-invalid");
            return;
          }

          const nuevaOpcion = document.createElement("option");
          nuevaOpcion.value = data.id;
          nuevaOpcion.textContent = data.nombre;

          const agregarNuevo = modeloSelect.querySelector(
            'option[value="agregar_nuevo"]'
          );
          modeloSelect.insertBefore(nuevaOpcion, agregarNuevo);
          nuevaOpcion.selected = true;

          this.value = "";
          this.classList.remove("is-invalid");
          document.getElementById("nuevo-modelo-input").style.display = "none";
          modeloSelect.dispatchEvent(new Event("change"));

          mostrarMensaje("✅ Modelo agregado correctamente");
        })
        .catch((err) => {
          console.error("Error al agregar modelo:", err);
          this.classList.add("is-invalid");
        });
    }
  });

  // ✅ Mensaje sutil de éxito
  function mostrarMensaje(texto) {
    const mensaje = document.createElement("div");
    mensaje.textContent = texto;
    mensaje.className = "text-success small mt-1 fade-in";
    mensaje.style.transition = "opacity 0.5s ease";
    mensaje.style.opacity = "0";

    const destino =
      document.querySelector("#modelo-select")?.parentElement || document.body;
    destino.appendChild(mensaje);

    setTimeout(() => (mensaje.style.opacity = "1"), 50);
    setTimeout(() => {
      mensaje.style.opacity = "0";
      setTimeout(() => mensaje.remove(), 500);
    }, 2500);
  }

  // 🔄 Carga de tipos de falla y reparación
  function cargarOpciones(endpoint, selectId, label) {
    const select = document.getElementById(selectId);
    if (!select) return;

    fetch(endpoint)
      .then((res) => res.json())
      .then((data) => {
        select.innerHTML = `<option value="">Seleccione ${label}</option>`;
        data.forEach((item) => {
          const option = document.createElement("option");
          option.value = item.id;
          option.textContent = item.nombre;
          select.appendChild(option);
        });
      })
      .catch((err) => {
        console.error(`Error al cargar ${label}:`, err);
        select.innerHTML = `<option disabled>Error al cargar ${label}</option>`;
      });
  }

  cargarOpciones("/obtener_tipos_falla", "tipo-falla-select", "tipo de falla");
  cargarOpciones(
    "/obtener_tipos_reparacion",
    "tipo-reparacion-select",
    "tipo de reparación"
  );
});
