from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_cybersecurity_azhadkiel_2026'

# Configuración de la base de datos MySQL (XAMPP)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/cybersecurity_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# DECORADORES DE SEGURIDAD Y ROLES
# ==========================================

def roles_permitidos(roles_necesarios):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            
            # El administrador tiene acceso total e incondicional
            if current_user.rol == 'admin':
                return f(*args, **kwargs)
                
            if current_user.rol not in roles_necesarios:
                flash('No tienes los permisos necesarios para acceder a esta sección.', 'danger')
                return redirect(url_for('index'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def verificar_permiso_escritura():
    """
    Decorador para restringir acciones de registro/modificación (POST) 
    según la regla de negocio exacta de cada rol.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debe iniciar sesión para realizar esta acción.', 'danger')
                return redirect(url_for('login'))
            
            rol = current_user.rol
            
            if request.method == 'POST':
                # 1. admin: Permiso total de escritura
                if rol == 'admin':
                    return f(*args, **kwargs)
                
                # 2. tecnico: Puede registrar en general, pero NO en facturación
                elif rol == 'tecnico':
                    if 'facturacion' in request.path:
                        flash('El rol técnico no tiene autorización para realizar registros de facturación.', 'danger')
                        return redirect(url_for('facturacion'))
                    return f(*args, **kwargs)
                
                # 3. tesorero: Solo puede registrar en facturación y proveedores
                elif rol == 'tesorero':
                    if 'facturacion' in request.path or 'proveedores' in request.path:
                        return f(*args, **kwargs)
                    else:
                        flash('Su rol de tesorero solo permite realizar registros en facturación y proveedores.', 'warning')
                        return redirect(url_for('index'))
                
                # 4. proveedor y cliente: No pueden realizar ningún tipo de registro
                elif rol in ['proveedor', 'cliente']:
                    flash('Su rol actual tiene acceso exclusivo de visualización y no permite registrar datos.', 'danger')
                    return redirect(url_for('index'))
                
                else:
                    abort(403)
                    
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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
# 1. MODELOS DE BASE DE DATOS
# ==========================================

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='cliente')
    # Roles esperados: 'admin', 'tecnico', 'tesorero', 'proveedor', 'cliente'

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    productos = db.relationship('Producto', backref='categoria_rel', lazy=True, cascade="all, delete-orphan")

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
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

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(120), nullable=False)

class Factura(db.Model):
    __tablename__ = 'facturas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_factura = db.Column(db.String(50), unique=True, nullable=False)
    cliente_nombre = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())

# Inicializar tablas y datos semilla por defecto
with app.app_context():
    db.create_all()
    if Usuario.query.count() == 0:
        admin_user = Usuario(
            nombre="Administrador",
            correo="admin@azhadkiel.com",
            password=generate_password_hash("admin123"),
            rol="admin"
        )
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
        correo = request.form['correo']
        password = request.form['password']
        user = Usuario.query.filter_by(correo=correo).first()       
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'¡Bienvenido de nuevo, {user.nombre}!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')          
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        if Usuario.query.filter_by(correo=correo).first():
            flash('El correo ya está registrado.', 'warning')
            return redirect(url_for('registro'))
        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password=generate_password_hash(password),
            rol='cliente' # Rol por defecto para registros web
        )
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
@roles_permitidos(['admin', 'tecnico', 'tesorero', 'proveedor', 'cliente'])
def admin():
    solicitudes = Solicitud.query.all()
    return render_template('admin.html', solicitudes=solicitudes)

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

@app.route('/admin/crear_usuario', methods=['POST'])
@login_required
def crear_usuario_admin():
    # Validar estrictamente que solo el administrador pueda registrar usuarios
    if current_user.rol != 'admin':
        flash('Acceso denegado. No tienes privilegios de administración.', 'danger')
        return redirect(url_for('index'))
    
    # Obtener los datos enviados desde el formulario del panel
    username = request.form.get('username')
    password = request.form.get('password')
    rol = request.form.get('rol')
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    
    if not username or not password or not rol or not nombre or not correo:
        flash('Por favor completa todos los campos para registrar el usuario.', 'warning')
        return redirect(url_for('admin'))
    
    try:
        cursor = mysql.connection.cursor()
        
        # Verificar si el username o correo ya existen
        cursor.execute("SELECT id FROM usuarios WHERE username = %s OR correo = %s", (username, correo))
        if cursor.fetchone():
            flash('El nombre de usuario o el correo electrónico ya están registrados.', 'danger')
            cursor.close()
            return redirect(url_for('admin'))
        
        # Cifrar la contraseña de forma segura
        password_hash = generate_password_hash(password)
        
        # Insertar el nuevo usuario con el rol seleccionado
        cursor.execute(
            "INSERT INTO usuarios (username, password, rol, nombre, correo) VALUES (%s, %s, %s, %s, %s)",
            (username, password_hash, rol, nombre, correo)
        )
        mysql.connection.commit()
        cursor.close()
        
        flash(f'¡Usuario "{nombre}" creado exitosamente con el rol de {rol}!', 'success')
    except Exception as e:
        flash(f'Error al registrar el usuario: {str(e)}', 'danger')
        
    return redirect(url_for('admin'))

# ==========================================
# 4. OPERACIONES CRUD (CLIENTES)
# ==========================================
@app.route('/clientes')
@login_required
@roles_permitidos(['admin', 'tecnico', 'tesorero', 'proveedor', 'cliente'])
def clientes():
    lista = Cliente.query.all()
    return render_template('clientes.html', clientes=lista)

@app.route('/crear_cliente', methods=['POST'])
@login_required
@roles_permitidos(['admin', 'tecnico'])
@verificar_permiso_escritura()
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

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_permitidos(['admin', 'tecnico'])
@verificar_permiso_escritura()
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

@app.route('/eliminar_cliente/<int:id>')
@login_required
@roles_permitidos(['admin'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('¡Cliente eliminado con éxito!', 'info')
    return redirect(url_for('clientes'))

# ==========================================
# 5. MÓDULO PRODUCTOS
# ==========================================
@app.route('/productos')
@login_required
@roles_permitidos(['admin', 'tecnico', 'tesorero', 'proveedor', 'cliente'])
def productos():
    lista_productos = Producto.query.all()
    categorias = Categoria.query.all()
    return render_template('productos.html', productos=lista_productos, categorias=categorias)

@app.route('/crear_producto', methods=['POST'])
@login_required
@roles_permitidos(['admin', 'tecnico'])
@verificar_permiso_escritura()
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
@roles_permitidos(['admin'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('¡Producto eliminado del catálogo!', 'info')
    return redirect(url_for('productos'))

# ==========================================
# 6. MÓDULO PROVEEDORES Y FACTURACIÓN
# ==========================================
@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
@roles_permitidos(['admin', 'tecnico', 'tesorero', 'proveedor', 'cliente'])
@verificar_permiso_escritura()
def proveedores():
    if request.method == 'POST':
        nuevo_prov = Proveedor(
            nombre=request.form['nombre'],
            contacto=request.form['contacto'],
            telefono=request.form['telefono'],
            correo=request.form['correo']
        )
        db.session.add(nuevo_prov)
        db.session.commit()
        flash('¡Proveedor registrado con éxito!', 'success')
        return redirect(url_for('proveedores'))
    
    lista_proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=lista_proveedores)

@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
@roles_permitidos(['admin', 'tecnico', 'tesorero', 'proveedor', 'cliente'])
@verificar_permiso_escritura()
def facturacion():
    if request.method == 'POST':
        nueva_fact = Factura(
            numero_factura=request.form['numero_factura'],
            cliente_nombre=request.form['cliente_nombre'],
            total=float(request.form['total'])
        )
        db.session.add(nueva_fact)
        db.session.commit()
        flash('¡Factura registrada con éxito!', 'success')
        return redirect(url_for('facturacion'))
        
    lista_facturas = Factura.query.all()
    return render_template('facturacion.html', facturas=lista_facturas)

if __name__ == '__main__':
    app.run(debug=True)