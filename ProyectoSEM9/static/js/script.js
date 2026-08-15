// Se asegura de que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Referencias al DOM (Elementos del formulario) ---
    const form = document.getElementById('formulario-registro');
    
    const inputNombre = document.getElementById('form-nombre');
    const inputCategoria = document.getElementById('form-categoria');
    const inputDescripcion = document.getElementById('form-descripcion');
    
    const msgNombre = document.getElementById('msg-nombre');
    const msgCategoria = document.getElementById('msg-categoria');
    const msgDescripcion = document.getElementById('msg-descripcion');
    
    const contenedorAlertas = document.getElementById('contenedor-alertas');
    const contenedorRegistros = document.getElementById('contenedor-registros');
    const contadorTotal = document.getElementById('contador-total');
    const mensajeVacio = document.getElementById('mensaje-vacio');

    let totalRegistros = 0;

    // --- 2. Event Listeners para validación en tiempo real (input, blur, change) ---
    
    // Eventos para el campo Nombre
    inputNombre.addEventListener('input', validarNombre);
    inputNombre.addEventListener('blur', validarNombre);

    // Eventos para el campo Categoría (select usa 'change' y 'blur')
    inputCategoria.addEventListener('change', validarCategoria);
    inputCategoria.addEventListener('blur', validarCategoria);

    // Eventos para el campo descripción
    inputDescripcion.addEventListener('input', validarDescripcion);
    inputDescripcion.addEventListener('blur', validarDescripcion);

    // Evento Submit del formulario
    form.addEventListener('submit', manejarSubmit);


    // --- 3. Funciones reutilizables de interfaz ---

    /**
     * Aplica estilos de error (is-invalid y alert-danger)
     */
    function establecerError(input, contenedorMensaje, mensaje) {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        
        contenedorMensaje.className = 'mt-1 p-2 small rounded d-block alert alert-danger mb-0';
        contenedorMensaje.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> ${mensaje}`;
    }

    /**
     * Aplica estilos de éxito (is-valid y alert-success)
     */
    function establecerExito(input, contenedorMensaje, mensaje) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        
        contenedorMensaje.className = 'mt-1 p-2 small rounded d-block alert alert-success mb-0';
        contenedorMensaje.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> ${mensaje}`;
    }

    /**
     * Limpia completamente los estilos de validación del formulario
     */
    function limpiarFormulario() {
        form.reset();
        
        const inputs = [inputNombre, inputCategoria, inputDescripcion];
        const msgs = [msgNombre, msgCategoria, msgDescripcion];
        
        inputs.forEach(input => {
            input.classList.remove('is-valid', 'is-invalid');
        });
        
        msgs.forEach(msg => {
            msg.className = 'd-none';
            msg.innerHTML = '';
        });
    }


    // --- 4. Funciones Específicas de validación lógica ---

    function validarNombre() {
        const valor = inputNombre.value.trim();
        
        // Regla 1: No debe estar vacío
        if (valor === '') {
            establecerError(inputNombre, msgNombre, 'El campo nombre no puede estar vacío.');
            return false;
        }
        
        // Regla 2: Longitud mínima
        if (valor.length < 5) {
            establecerError(inputNombre, msgNombre, 'El nombre debe tener al menos 5 caracteres.');
            return false;
        }

        // Si pasa todas las reglas:
        establecerExito(inputNombre, msgNombre, 'Nombre válido.');
        return true;
    }

    function validarCategoria() {
        const valor = inputCategoria.value;
        
        // Regla 1: Debe seleccionar una opción válida (diferente del valor por defecto)
        if (valor === '' || valor === null) {
            establecerError(inputCategoria, msgCategoria, 'Debe seleccionar una categoría o tipo de servicio.');
            return false;
        }

        establecerExito(inputCategoria, msgCategoria, 'Categoría seleccionada correctamente.');
        return true;
    }

    function validarDescripcion() {
        const valor = inputDescripcion.value.trim();
        
        // Regla 1: No debe estar vacío
        if (valor === '') {
            establecerError(inputDescripcion, msgDescripcion, 'La descripción es obligatoria.');
            return false;
        }

        // Regla 2: Información suficiente (mínimo de caracteres)
        if (valor.length < 15) {
            establecerError(inputDescripcion, msgDescripcion, 'Proporcione más información (Mín. 15 caracteres).');
            return false;
        }

        establecerExito(inputDescripcion, msgDescripcion, 'Descripción detallada aceptada.');
        return true;
    }


    // --- 5. Manejador del evento Submit Principal ---

    function manejarSubmit(evento) {
        // PREVENIR COMPORTAMIENTO POR DEFECTO (Recarga de página)
        evento.preventDefault();

        // Forzar todas las validaciones antes de procesar
        const esNombreValido = validarNombre();
        const esCategoriaValida = validarCategoria();
        const esDescripcionValida = validarDescripcion();

        // Comprobar si todas las reglas pasan exitosamente
        if (esNombreValido && esCategoriaValida && esDescripcionValida) {
            
            // Recolectar datos
            const datosRegistro = {
                nombre: inputNombre.value.trim(),
                categoria: inputCategoria.value,
                descripcion: inputDescripcion.value.trim()
            };

            // Crear el registro dinámico en el DOM
            crearRegistroDinamico(datosRegistro);
            
            // Resetear el formulario tras éxito
            limpiarFormulario();
            
            // Mostrar notificación de éxito general
            mostrarNotificacionGeneral('¡El registro ha sido almacenado en el sistema con éxito!', 'success');

        } else {
            // Mostrar notificación de error general
            mostrarNotificacionGeneral('Error: Verifique que todos los campos del formulario estén correctos.', 'danger');
        }
    }


    // --- 6. Lógica de creación, gestión y eliminación de registros dinámicos ---

    function crearRegistroDinamico(datos) {
        totalRegistros++;
        actualizarContadorUI();

        // Contenedor columna
        const colDiv = document.createElement('div');
        colDiv.className = 'col-md-6 mb-3';

        // Estructura de la tarjeta card (Glassmorphism)
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card bg-dark text-light border border-info border-opacity-25 h-100 shadow-sm';
        cardDiv.style.background = 'rgba(12, 30, 60, 0.8)';
        cardDiv.style.backdropFilter = 'blur(6px)';

        const cardBody = document.createElement('div');
        cardBody.className = 'card-body d-flex flex-column justify-content-between p-3';

        // Determinar Badge según la categoría
        let badgeStyle = 'bg-info text-dark';
        if (datos.categoria === 'Incidente de Seguridad') badgeStyle = 'bg-danger text-light';
        if (datos.categoria === 'Auditoría OWASP') badgeStyle = 'bg-warning text-dark';
        if (datos.categoria === 'Soporte de Infraestructura') badgeStyle = 'bg-success text-light';

        // Elementos internos dinámicos
        cardBody.innerHTML = `
            <h4 class="h6 card-title text-uppercase m-0 fw-bold border-bottom border-secondary pb-1" style="color: var(--cyan-neon);">
                ${datos.nombre}
            </h4>
            <span class="badge ${badgeStyle} my-2 align-self-start text-uppercase small font-monospace">
                ${datos.categoria}
            </span>
            <p class="card-text text-secondary-emphasis small mb-4 text-light">
                ${datos.descripcion}
            </p>
        `;

        // Botón Eliminar utilizando createElement para poder adjuntarle el EventListener de forma segura
        const botonEliminar = document.createElement('button');
        botonEliminar.className = 'btn btn-outline-danger btn-sm w-100 mt-auto';
        botonEliminar.innerHTML = '<i class="bi bi-trash3 me-1"></i>Eliminar Registro';
        
        // Manejar evento de eliminación
        botonEliminar.addEventListener('click', function() {
            colDiv.remove();
            totalRegistros--;
            actualizarContadorUI();
            mostrarNotificacionGeneral('Registro eliminado de la consola.', 'warning');
        });

        // Ensamblar DOM (appendChild)
        cardBody.appendChild(botonEliminar);
        cardDiv.appendChild(cardBody);
        colDiv.appendChild(cardDiv);
        contenedorRegistros.appendChild(colDiv);
    }

    function actualizarContadorUI() {
        contadorTotal.textContent = totalRegistros;
        if (totalRegistros === 0) {
            mensajeVacio.style.display = 'block';
        } else {
            mensajeVacio.style.display = 'none';
        }
    }

    function mostrarNotificacionGeneral(mensaje, tipo) {
        contenedorAlertas.innerHTML = '';
        const alerta = document.createElement('div');
        alerta.className = `alert alert-${tipo} alert-dismissible fade show small mb-0`;
        alerta.role = 'alert';
        alerta.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        contenedorAlertas.appendChild(alerta);
        
        // Eliminar automáticamente tras 3.5 segundos
        setTimeout(() => {
            if (alerta.parentNode) alerta.remove();
        }, 3500);
    }
});