from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos MySQL (XAMPP)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/cybersecurity_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# 1. DEFINICIÓN DE MODELOS (TABLAS MYSQL)
# ==========================================
class Solicitud(db.Model):
    __tablename__ = 'solicitudes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    servicio = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Crear las tablas automáticamente
with app.app_context():
    db.create_all()
    
    # Datos por defecto para productos si la tabla está vacía
    if Producto.query.count() == 0:
        productos_iniciales = [
            Producto(nombre="Firewall Perimetral Hardware", categoria="Ciberseguridad", precio=450.00, stock=10),
            Producto(nombre="Licencia Antivirus Enterprise (10 PC)", categoria="Ciberseguridad", precio=120.00, stock=25),
            Producto(nombre="Servidor Rack 1U Xeon", categoria="Infraestructura", precio=1200.00, stock=5),
            Producto(nombre="Certificado SSL Wildcard Anual", categoria="Desarrollo", precio=80.00, stock=50)
        ]
        db.session.bulk_save_objects(productos_iniciales)
        db.session.commit()

    # Datos por defecto para clientes si la tabla está vacía
    if Cliente.query.count() == 0:
        clientes_iniciales = [
            Cliente(nombre="Comercial del Tío Cuchy", contacto="Ing. Carlos Santos", correo="contacto@cuchy.com", telefono="+593999999999")
        ]
        db.session.bulk_save_objects(clientes_iniciales)
        db.session.commit()

# ==========================================
# 2. RUTAS DE LA APLICACIÓN
# ==========================================

# Ruta principal informativa
@app.route('/')
def index():
    todas_las_solicitudes = Solicitud.query.all()
    return render_template('index.html', solicitudes=todas_las_solicitudes)

# Ruta para procesar y guardar el formulario de solicitudes en MySQL
@app.route('/enviar_solicitud', methods=['POST'])
def enviar_solicitud():
    if request.method == 'POST':
        nueva_solicitud = Solicitud(
            nombre=request.form['nombre'],
            correo=request.form['correo'],
            servicio=request.form['servicio'],
            mensaje=request.form['mensaje']
        )
        db.session.add(nueva_solicitud)
        db.session.commit()
        return redirect(url_for('index'))

# Ruta para el módulo de Clientes (Vista)
@app.route('/clientes')
def clientes():
    lista_clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=lista_clientes)

# Ruta para registrar un nuevo cliente desde la web hacia MySQL
@app.route('/crear_cliente', methods=['POST'])
def crear_cliente():
    if request.method == 'POST':
        nuevo_cliente = Cliente(
            nombre=request.form['nombre'],
            contacto=request.form['contacto'],
            correo=request.form['correo'],
            telefono=request.form['telefono']
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return redirect(url_for('clientes'))

# Ruta para el módulo de Productos (Vista)
@app.route('/productos')
def productos():
    lista_productos = Producto.query.all()
    return render_template('productos.html', productos=lista_productos)

# Ruta para registrar un nuevo producto desde la web hacia MySQL
@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    if request.method == 'POST':
        nuevo_producto = Producto(
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock'])
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('productos'))

# Ruta para el módulo de Proveedores
@app.route('/proveedores')
def proveedores():
    lista_proveedores = [
        {"id": 1, "nombre": "Cisco Systems Ecuador", "servicio": "Equipos de Red y Firewall", "pais": "Estados Unidos / Local"},
        {"id": 2, "nombre": "AWS Cloud Services", "servicio": "Infraestructura en la Nube", "pais": "Global"},
        {"id": 3, "nombre": "GlobalSign SSL Provider", "servicio": "Certificados Digitales", "pais": "Reino Unido"}
    ]
    return render_template('proveedores.html', proveedores=lista_proveedores)

# Ruta para el módulo de Facturación
@app.route('/facturacion')
def facturacion():
    lista_facturas = [
        {"num": "FAC-001", "cliente": "Comercial del Tío Cuchy", "fecha": "2026-08-01", "total": 1200.00, "estado": "Pagado"},
        {"num": "FAC-002", "cliente": "Centro de Tutorías La Churona", "fecha": "2026-08-05", "total": 450.00, "estado": "Pendiente"},
        {"num": "FAC-003", "cliente": "Los Recuerditos de la Gasa", "fecha": "2026-08-10", "total": 2680.00, "estado": "Pagado"}
    ]
    return render_template('facturacion.html', facturas=lista_facturas)

if __name__ == '__main__':
    app.run(debug=True)