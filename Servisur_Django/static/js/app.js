document.addEventListener('DOMContentLoaded', function () {

  // Helpers
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  // 1) Toggle show/hide password for any button with data-toggle="password"
  function setupPasswordToggles() {
    const toggles = $$('[data-toggle="password"]');
    toggles.forEach(btn => {
      const target = btn.getAttribute('data-target');
      const input = target ? document.querySelector(target) : null;
      if (!input) return;
      btn.setAttribute('type', 'button');
      btn.setAttribute('aria-pressed', 'false');

      btn.addEventListener('click', () => {
        const isPwd = input.type === 'password';
        input.type = isPwd ? 'text' : 'password';
        btn.setAttribute('aria-pressed', String(isPwd));
        btn.setAttribute('aria-label', isPwd ? 'Ocultar contraseña' : 'Mostrar contraseña');
        const img = btn.querySelector('img');
        if (img) {
          // opcional: cambiar src si tienes icono distinto para "oculto"
          img.alt = isPwd ? 'Ocultar' : 'Mostrar';
        }
      });

      btn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          btn.click();
        }
      });
    });
  }

  // 2) Insertar/asegurar contenedor de estado justo debajo del label (para pw-status)
  function ensureStatusUnderLabel(inputEl) {
    if (!inputEl) return null;
    const id = inputEl.id;
    let label = document.querySelector(`label[for="${id}"]`);
    if (!label) {
      const parent = inputEl.closest('.mb-3') || inputEl.parentElement;
      label = parent ? parent.querySelector('label') : null;
    }
    if (!label) return null;

    let status = label.nextElementSibling;
    if (status && status.classList && status.classList.contains('pw-status')) return status;

    status = document.createElement('div');
    status.className = 'pw-status form-text mt-1';
    status.setAttribute('aria-live', 'polite');
    status.style.minHeight = '1.2em';
    label.parentNode.insertBefore(status, label.nextSibling);
    return status;
  }

  // 3) Live check: contraseñas coinciden (mensaje debajo del label del confirmar)
  function setupConfirmMatch() {
    const pw1 = $('#password1') || $('#nueva_contrasena') || $('#id_password');
    const pw2 = $('#password2') || $('#confirmar_contrasena') || $('#id_password_confirm');
    if (!pw1 || !pw2) return;

    const status = ensureStatusUnderLabel(pw2) || ensureStatusUnderLabel(pw1) || $('#pw-status');

    function update() {
      if (!status) return;
      if (!pw1.value && !pw2.value) {
        status.textContent = '';
        pw1.style.borderColor = '';
        pw2.style.borderColor = '';
        return;
      }
      if (pw1.value === pw2.value) {
        status.textContent = 'Las contraseñas coinciden';
        status.style.color = 'green';
        pw1.style.borderColor = 'green';
        pw2.style.borderColor = 'green';
      } else {
        status.textContent = 'Las contraseñas no coinciden';
        status.style.color = '#c82333';
        pw1.style.borderColor = 'red';
        pw2.style.borderColor = 'red';
      }
    }

    pw1.addEventListener('input', update);
    pw2.addEventListener('input', update);
    update();
  }

  // 4) Validaciones del formulario Crear Cuenta
  function setupCreateAccountValidation() {
    const form = document.querySelector('form');
    if (!form) return;

    const username = $('#username');
    const firstName = $('#first_name');
    const lastName = $('#last_name');
    const email = $('#email');
    const password1 = $('#password1');
    const password2 = $('#password2');
    const group = $('#group_id');

    // Reglas
    const empiezaMayusculaYMin3 = (v) => /^[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚáéíóúñÑ]{2,}$/.test(v.trim());
    const correoValido = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim());
    const contrasenaSegura = (v) => (
      v.length >= 8 &&
      /[A-Z]/.test(v) &&
      /[a-z]/.test(v) &&
      /\d/.test(v) &&
      /[^\w\s]/.test(v)
    );

    function mostrarError(input, mensaje) {
      if (!input) return;
      // buscar un .error-msg existente justo después del input (no del wrapper)
      let container = input.parentNode;
      // si el input está dentro de .input-group, colocar el error después del grupo
      if (container && container.classList && container.classList.contains('input-group')) {
        // el siguiente sibling del grupo
        let next = container.nextElementSibling;
        if (next && next.classList && next.classList.contains('error-msg')) {
          next.textContent = mensaje;
          return;
        }
        const err = document.createElement('div');
        err.className = 'error-msg text-danger small mt-1';
        err.textContent = mensaje;
        container.parentNode.insertBefore(err, container.nextSibling);
        return;
      }
      // caso normal
      let next = input.nextElementSibling;
      if (next && next.classList && next.classList.contains('error-msg')) {
        next.textContent = mensaje;
        return;
      }
      const err = document.createElement('div');
      err.className = 'error-msg text-danger small mt-1';
      err.textContent = mensaje;
      input.parentNode.insertBefore(err, input.nextSibling);
    }

    function limpiarError(input) {
      if (!input) return;
      let next = input.parentNode.querySelector('.error-msg');
      if (next) next.textContent = '';
      // también limpiar el que esté justo después del grupo
      const groupSibling = input.parentNode.nextElementSibling;
      if (groupSibling && groupSibling.classList && groupSibling.classList.contains('error-msg')) {
        groupSibling.textContent = '';
      }
    }

    // Validación en tiempo real (opcional)
    const campos = [username, firstName, lastName, email, password1, password2, group];
    campos.forEach(c => {
      if (!c) return;
      c.addEventListener('input', () => {
        limpiarError(c);
      });
    });

    form.addEventListener('submit', function (e) {
      let valido = true;

      // Usuario obligatorio
      if (!username || !username.value.trim()) {
        mostrarError(username, 'El nombre de usuario es obligatorio.');
        valido = false;
      } else if (!empiezaMayusculaYMin3(username.value)) {
        mostrarError(username, 'Debe comenzar con mayúscula y tener mínimo 3 caracteres.');
        valido = false;
      } else {
        limpiarError(username);
      }

      // Nombre obligatorio
      if (!firstName || !firstName.value.trim()) {
        mostrarError(firstName, 'El nombre es obligatorio.');
        valido = false;
      } else if (!empiezaMayusculaYMin3(firstName.value)) {
        mostrarError(firstName, 'Debe comenzar con mayúscula y tener mínimo 3 caracteres.');
        valido = false;
      } else {
        limpiarError(firstName);
      }

      // Apellido (si se completa, validar)
      if (lastName && lastName.value.trim() && !empiezaMayusculaYMin3(lastName.value)) {
        mostrarError(lastName, 'Debe comenzar con mayúscula y tener mínimo 3 caracteres.');
        valido = false;
      } else if (lastName) {
        limpiarError(lastName);
      }

      // Email (si se completa, validar)
      if (email && email.value.trim() && !correoValido(email.value)) {
        mostrarError(email, 'Formato de correo electrónico inválido.');
        valido = false;
      } else if (email) {
        limpiarError(email);
      }

      // Contraseña obligatoria y segura
      if (!password1 || !password1.value) {
        mostrarError(password1, 'La contraseña es obligatoria.');
        valido = false;
      } else if (!contrasenaSegura(password1.value)) {
        mostrarError(password1, 'Debe tener 8 caracteres, mayúscula, minúscula, número y símbolo.');
        valido = false;
      } else {
        limpiarError(password1);
      }

      // Confirmación
      if (password1 && password2 && password1.value !== password2.value) {
        mostrarError(password2, 'Las contraseñas no coinciden.');
        valido = false;
      } else if (password2) {
        limpiarError(password2);
      }

      // Grupo obligatorio
      if (!group || !group.value) {
        mostrarError(group, 'Debes seleccionar un grupo.');
        valido = false;
      } else {
        limpiarError(group);
      }

      if (!valido) {
        e.preventDefault();
        // Llevar foco al primer error visible
        const firstError = document.querySelector('.error-msg:not(:empty)');
        if (firstError) {
          const el = firstError.previousElementSibling;
          if (el && (el.tagName === 'INPUT' || el.tagName === 'SELECT' || el.tagName === 'TEXTAREA')) {
            el.focus();
          } else {
            // si el error está después de un input-group
            const groupEl = firstError.previousElementSibling && firstError.previousElementSibling.querySelector('input,select');
            if (groupEl) groupEl.focus();
          }
        }
      }
    });
  }

  // 5) Ocultar alertas automáticamente (si existen)
  function hideAlerts(ms = 4000) {
    const alerts = $$('.alert');
    alerts.forEach(a => {
      setTimeout(() => {
        a.style.transition = 'opacity 300ms';
        a.style.opacity = '0';
        setTimeout(() => { a.style.display = 'none'; }, 300);
      }, ms);
    });
  }

  // Inicializar
  setupPasswordToggles();
  setupConfirmMatch();
  setupCreateAccountValidation();
  hideAlerts(4000);

});
