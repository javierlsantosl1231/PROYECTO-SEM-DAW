from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_cybersecurity_azhadkiel_2026'

# Configuración de la base de datos MySQL (XAMPP)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/cybersecurity_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta sección protegida.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ==========================================
# 1. MODELOS DE BASE DE DATOS (MÍNIMO 3 TABLAS RELACIONADAS)
# ==========================================

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    # Relación uno a muchos con Productos
    productos = db.relationship('Producto', backref='categoria_rel', lazy=True, cascade="all, delete-orphan")

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    # CLAVE FORÁNEA (FOREIGN KEY) que vincula Producto con Categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)

class Solicitud(db.Model):
    __tablename__ = 'solicitudes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    servicio = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

# Inicializar tablas y datos semilla por defecto si están vacías
with app.app_context():
    db.create_all()
    if Usuario.query.count() == 0:
        admin_user = Usuario(username="admin", password=generate_password_hash("admin123"))
        db.session.add(admin_user)
        db.session.commit()
    
    if Categoria.query.count() == 0:
        cat1 = Categoria(nombre="Ciberseguridad")
        cat2 = Categoria(nombre="Infraestructura")
        db.session.add_all([cat1, cat2])
        db.session.commit()

# ==========================================
# 2. RUTAS DE AUTENTICACIÓN
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user() # Cierra la sesión activa
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login')) # Redirige a la pantalla de login

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Usuario.query.filter_by(username=username).first():
            flash('El usuario ya existe.', 'warning')
            return redirect(url_for('registro'))
        nuevo_usuario = Usuario(username=username, password=generate_password_hash(password))
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('¡Cuenta creada con éxito! Inicia sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

# ==========================================
# 3. RUTAS PÚBLICAS Y PANEL ADMIN
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar_solicitud', methods=['POST'])
def enviar_solicitud():
    if request.method == 'POST':
        nueva = Solicitud(
            nombre=request.form['nombre'],
            correo=request.form['correo'],
            servicio=request.form['servicio'],
            mensaje=request.form['mensaje']
        )
        db.session.add(nueva)
        db.session.commit()
        flash('¡Solicitud enviada con éxito!', 'success')
        return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    solicitudes = Solicitud.query.all()
    return render_template('admin.html', solicitudes=solicitudes)

# ==========================================
# 4. OPERACIONES CRUD COMPLETAS (CLIENTES)
# ==========================================
@app.route('/clientes')
@login_required
def clientes():
    lista = Cliente.query.all()
    return render_template('clientes.html', clientes=lista)

@app.route('/crear_cliente', methods=['POST'])
@login_required
def crear_cliente():
    nuevo = Cliente(
        nombre=request.form['nombre'],
        contacto=request.form['contacto'],
        correo=request.form['correo'],
        telefono=request.form['telefono']
    )
    db.session.add(nuevo)
    db.session.commit()
    flash('¡Cliente registrado con éxito!', 'success')
    return redirect(url_for('clientes'))

# RUTA UPDATE (ACTUALIZAR) CLIENTE
@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.contacto = request.form['contacto']
        cliente.correo = request.form['correo']
        cliente.telefono = request.form['telefono']
        db.session.commit()
        flash('¡Cliente actualizado correctamente!', 'success')
        return redirect(url_for('clientes'))
    return render_template('editar_cliente.html', cliente=cliente)

# RUTA DELETE (ELIMINAR) CLIENTE
@app.route('/eliminar_cliente/<int:id>')
@login_required
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('¡Cliente eliminado con éxito!', 'info')
    return redirect(url_for('clientes'))


# ==========================================
# 5. MÓDULO PRODUCTOS (CON CONSULTA JOIN Y CRUD)
# ==========================================
@app.route('/productos')
@login_required
def productos():
    # Obtenemos directamente todos los productos (la relación con categorías ya está mapeada)
    lista_productos = Producto.query.all()
    categorias = Categoria.query.all()
    return render_template('productos.html', productos=lista_productos, categorias=categorias)

@app.route('/crear_producto', methods=['POST'])
@login_required
def crear_producto():
    nuevo = Producto(
        nombre=request.form['nombre'],
        precio=float(request.form['precio']),
        stock=int(request.form['stock']),
        categoria_id=int(request.form['categoria_id'])
    )
    db.session.add(nuevo)
    db.session.commit()
    flash('¡Producto agregado correctamente!', 'success')
    return redirect(url_for('productos'))

@app.route('/eliminar_producto/<int:id>')
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('¡Producto eliminado del catálogo!', 'info')
    return redirect(url_for('productos'))

@app.route('/proveedores')
@login_required
def proveedores():
    return render_template('proveedores.html')

@app.route('/facturacion')
@login_required
def facturacion():
    return render_template('facturacion.html')

if __name__ == '__main__':
    app.run(debug=True)