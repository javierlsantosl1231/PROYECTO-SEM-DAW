document.addEventListener('DOMContentLoaded', () => {
    // 1. Arreglo de objetos para renderizar el catálogo con botones para abrir el Modal
    const catalogoServicios = [
        {
            titulo: "Desarrollo Web Seguro",
            descripcion: "Creación de sitios corporativos y aplicaciones optimizados bajo normativas estrictas contra vulnerabilidades web.",
            categoria: "Desarrollo Web",
            disponible: true
        },
        {
            titulo: "Auditoría y Pentesting",
            descripcion: "Pruebas de penetración controladas para identificar y mitigar fallos antes de que sean explotados por terceros.",
            categoria: "Ciberseguridad",
            disponible: true
        },
        {
            titulo: "Infraestructura y Redes",
            descripcion: "Soporte técnico especializado, mantenimiento preventivo de equipos y configuración segura de redes.",
            categoria: "Mantenimiento IT",
            disponible: true
        },
        {
            titulo: "Consultoría Integral",
            descripcion: "Asesoría estratégica para el cumplimiento de normativas de protección de datos y gestión de riesgos.",
            categoria: "Ciberseguridad",
            disponible: false
        },
        {
            titulo: "Infraestructura y Redes",
            descripcion: "Soporte Técnico Red, mantenimiento preventivo de equipos y configuración de infraestructura de red.",
            categoria: "Mantenimiento IT",
            disponible: true
        }
    ];

    const contenedorCatalogo = document.getElementById('contenedorCatalogo');
    const modalTextoDetalle = document.getElementById('modalTextoDetalle');
    const modalElement = document.getElementById('modalDetalleServicio');
    const bootstrapModal = new bootstrap.Modal(modalElement);

    function renderizarCatalogo() {
        if (!contenedorCatalogo) return;
        contenedorCatalogo.innerHTML = '';

        for (const servicio of catalogoServicios) {
            const colDiv = document.createElement('div');
            colDiv.className = 'col-md-6 col-lg-3';

            const cardDiv = document.createElement('div');
            cardDiv.className = 'card card-custom h-100 p-3 border shadow-sm';

            const cardBody = document.createElement('div');
            cardBody.className = 'card-body d-flex flex-column justify-content-between';

            let badgeEstadoHtml = servicio.disponible 
                ? '<span class="badge bg-success mb-2">Disponible</span>' 
                : '<span class="badge bg-secondary mb-2">Próximamente</span>';

            cardBody.innerHTML = `
                <div>
                    ${badgeEstadoHtml}
                    <h5 class="card-title fw-bold text-info">${servicio.titulo}</h5>
                    <p class="card-text text-muted small">${servicio.descripcion}</p>
                </div>
                <div>
                    <span class="badge bg-dark text-light mb-3 d-block">${servicio.categoria}</span>
                    <button class="btn btn-outline-info btn-sm w-100 btn-detalles">Ver Detalles</button>
                </div>
            `;

            // Evento para activar el Modal de Bootstrap con la información del servicio
            const btnDetalles = cardBody.querySelector('.btn-detalles');
            btnDetalles.addEventListener('click', () => {
                modalTextoDetalle.innerHTML = `<strong>${servicio.titulo}</strong><br><br>${servicio.descripcion}<br><br><em>Categoría: ${servicio.categoria}</em>`;
                bootstrapModal.show();
            });

            cardDiv.appendChild(cardBody);
            colDiv.appendChild(cardDiv);
            contenedorCatalogo.appendChild(colDiv);
        }
    }

    renderizarCatalogo();

    // 2. Lógica del formulario, validaciones, spinner y alertas
    const formRegistro = document.getElementById('formRegistro');
    const inputNombre = document.getElementById('inputNombre');
    const inputDescripcion = document.getElementById('inputDescripcion');
    const inputCategoria = document.getElementById('inputCategoria');
    const contenedorLista = document.getElementById('contenedorLista');
    const contadorRegistros = document.getElementById('contadorRegistros');
    const mensajeVacio = document.getElementById('mensajeVacio');
    const alertaGeneral = document.getElementById('alerta-general');
    const spinnerCarga = document.getElementById('spinnerCarga');

    let totalRegistros = 0;

    function actualizarContador() {
        contadorRegistros.textContent = totalRegistros;
        mensajeVacio.classList.toggle('d-none', totalRegistros > 0);
    }

    function validarNombre() {
        const valido = inputNombre.value.trim().length >= 3;
        inputNombre.classList.toggle('is-valid', valido);
        inputNombre.classList.toggle('is-invalid', !valido);
        return valido;
    }

    function validarDescripcion() {
        const valido = inputDescripcion.value.trim().length >= 10;
        inputDescripcion.classList.toggle('is-valid', valido);
        inputDescripcion.classList.toggle('is-invalid', !valido);
        return valido;
    }

    function validarCategoria() {
        const valido = inputCategoria.value !== '';
        inputCategoria.classList.toggle('is-valid', valido);
        inputCategoria.classList.toggle('is-invalid', !valido);
        return valido;
    }

    inputNombre.addEventListener('input', validarNombre);
    inputDescripcion.addEventListener('input', validarDescripcion);
    inputCategoria.addEventListener('change', validarCategoria);

    formRegistro.addEventListener('submit', (evento) => {
        evento.preventDefault();

        if (!validarNombre() || !validarDescripcion() || !validarCategoria()) {
            mostrarAlertaGeneral('Por favor, corrija los campos marcados en rojo.', 'danger');
            return;
        }

        // Mostrar spinner de Bootstrap simulando proceso de guardado
        spinnerCarga.classList.remove('d-none');
        formRegistro.style.opacity = '0.5';

        setTimeout(() => {
            spinnerCarga.classList.add('d-none');
            formRegistro.style.opacity = '1';

            const nombre = inputNombre.value.trim();
            const descripcion = inputDescripcion.value.trim();
            const categoria = inputCategoria.value;

            totalRegistros++;
            actualizarContador();
            crearTarjetaRegistro(nombre, descripcion, categoria);

            formRegistro.reset();
            inputNombre.classList.remove('is-valid', 'is-invalid');
            inputDescripcion.classList.remove('is-valid', 'is-invalid');
            inputCategoria.classList.remove('is-valid', 'is-invalid');

            mostrarAlertaGeneral('¡Registro agregado correctamente al sistema!', 'success');
        }, 1000);
    });

    function crearTarjetaRegistro(nombre, descripcion, categoria) {
        const colDiv = document.createElement('div');
        colDiv.className = 'col-md-6';

        const cardDiv = document.createElement('div');
        cardDiv.className = 'card card-custom h-100 p-3 border shadow-sm';

        const cardBody = document.createElement('div');
        cardBody.className = 'card-body d-flex flex-column justify-content-between';

        cardBody.innerHTML = `
            <div>
                <span class="badge bg-info text-dark mb-2">${categoria}</span>
                <h5 class="card-title fw-bold text-primary">${nombre}</h5>
                <p class="card-text text-muted small">${descripcion}</p>
            </div>
            <button class="btn btn-outline-danger btn-sm mt-3 align-self-start btn-eliminar">Eliminar Registro</button>
        `;

        cardBody.querySelector('.btn-eliminar').addEventListener('click', () => {
            colDiv.remove();
            totalRegistros--;
            actualizarContador();
            mostrarAlertaGeneral('Registro eliminado correctamente.', 'warning');
        });

        cardDiv.appendChild(cardBody);
        colDiv.appendChild(cardDiv);
        contenedorLista.appendChild(colDiv);
    }

    function mostrarAlertaGeneral(mensaje, tipo) {
        if (!alertaGeneral) return;
        alertaGeneral.textContent = mensaje;
        alertaGeneral.className = `alert alert-${tipo} mb-3 shadow-sm`;
        alertaGeneral.classList.remove('d-none');

        setTimeout(() => {
            alertaGeneral.classList.add('d-none');
        }, 4000);
    }
});