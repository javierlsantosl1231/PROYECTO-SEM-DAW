Proyecto Integrador: Cybersecurity Azhadkiel

El proyecto ha evolucionado desde una página web estática informativa hasta convertirse en una aplicación web estructurada bajo el patrón Modelo-Vista (con Flask), combinando un diseño frontend moderno, interactividad avanzada con JavaScript y la organización de un backend modular en Python.

Fase 1: Estructura base y diseño visual (HTML5 y CSS3)
En las primeras etapas, definimos la identidad del proyecto enfocada en servicios de ciberseguridad, soporte técnico y desarrollo web para pequeñas y medianas empresas.

Estructura Semántica HTML5: Se utilizaron etiquetas semánticas clave como:
<header>, <nav>, <main>, <section>, <article>, <aside> y <footer> para garantizar la accesibilidad y el SEO.

Diseño visual y estilos (style.css):

Se implementó una imagen de fondo temática de alta calidad (servidores y tecnología) combinada con un gradiente oscuro (overlay) para asegurar la legibilidad del texto.

Se aplicó el efecto glassmorphism (backdrop-filter: blur, transparencias y bordes sutiles) en las tarjetas principales (glass-hero).

Se configuró un diseño completamente adaptable (responsive) mediante media queries para computadoras, tablets y dispositivos móviles.

Fase 2: Integración de bootstrap 5 y componentes UI
Para optimizar el diseño y agilizar el desarrollo visual, se incorporó el framework Bootstrap 5 mediante CDN.

Barra de navegación (Navbar): Un menú superior fijo (sticky-top) adaptable a dispositivos móviles con botones colapsables.

Sistema de rejilla (Grid System): Uso intensivo de contenedores (container), filas (row) y columnas (col-lg-*) para organizar visualmente secciones como "Quiénes Somos", el catálogo y los formularios.

Componentes interactivos: incorporación de cards personalizadas, alertas de bootstrap (para avisos de éxito o error), un modal bootstrap (para mostrar información detallada de los servicios) y un spinner de bootstrap (para simular cargas asíncronas).

Fase 3: Interactividad y lógica frontend (JavaScript)
El archivo script.js aportó el dinamismo necesario en el navegador sin necesidad de recargar la página:

Arreglos y objetos de datos: Se crearon estructuras de datos en JavaScript para representar el catálogo inicial de servicios tecnológicos.

Estructuras repetitivas y condicionales: Mediante ciclos for...of y estructuras if/else, los datos del arreglo se recorren y se renderizan automáticamente en tarjetas dentro del HTML, evaluando condiciones como la disponibilidad ("Disponible" o "Próximamente").

Validaciones en tiempo real: El formulario de gestión evalúa los campos a medida que el usuario escribe (input y blur), aplicando clases dinámicas de Bootstrap (is-valid, is-invalid) y mostrando mensajes de error personalizados.

Gestión dinámica de registros: Los usuarios pueden agregar nuevos elementos desde el formulario, los cuales se renderizan instantáneamente en la interfaz junto con un contador actualizado y la opción de eliminar registros.

Fase 4: Transición al backend con flask y jinja2 (Etapa Actual)
En esta última fase, migramos la estructura estática a una aplicación web profesional con python y flask, separando la lógica del servidor de los recursos estáticos.

Entorno virtual y dependencias: Se configuró un entorno virtual (venv) en python y se instaló el framework flask (pip install flask).

Arquitectura de carpetas:

app.py: Archivo central del servidor flask donde se definen las rutas y los datos simulados de cada módulo.

templates/: Carpeta que almacena las vistas HTML.

static/: Carpeta que centraliza los recursos organizados en subcarpetas (css/style.css, js/script.js e imágenes).

Herencia de plantillas con jinja2 (base.html):

Se creó una plantilla principal denominada base.html que contiene los elementos repetitivos comunes (encabezado, menú de navegación, enlaces de Bootstrap, CSS/JS y pie de página).

Mediante las etiquetas de jinja2 {% extends "base.html" %} y {% block content %}, las páginas hijas inyectan su contenido específico, evitando duplicar código HTML.

Uso de la función url_for('static', filename='...') para enlazar correctamente los archivos estáticos y url_for('nombre_ruta') para la navegación interna.

Implementación de módulos con rutas flask (@app.route()):

/ (Ruta principal informativa).

/productos (Módulo de catálogo de servicios y hardware).

/clientes (Directorio de clientes registrados).

/proveedores (Red de aliados estratégicos).

/facturacion (Control y estados de facturas emitidas).

Nota técnica: En cada ruta de Flask, se envían estructuras de datos de prueba (listas de diccionarios en python) que se procesan y muestran dinámicamente en los archivos HTML usando bucles Jinja2 ({% for ... %}).

Estructura del proyecto-azhadkiel/
│
├── app.py
├── venv/                  <-- Entorno virtual de Python
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── img/               <-- Tus imágenes institucionales
└── templates/
    ├── base.html          <-- Plantilla principal compartida
    ├── index.html         <-- Página principal informativa
    ├── productos.html     <-- Módulo de Productos
    ├── clientes.html      <-- Módulo de Clientes
    ├── proveedores.html   <-- Módulo de Proveedores
    └── facturacion.html   <-- Módulo de Facturación

Entorno virtual python: python -m venv venv
Instalar o actualizar flask: pip install flask
Ejecutar app: python app.py
http://127.0.0.1:5000

git init
git add .
git commit -m "Primer commit: Mejoras del proyecto"
git remote add origin https://github.com/javierlsantosl1231/PROYECTO-SEM1-DAW.git
git branch -M main
git push -u origin main