from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal informativa
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el módulo de Productos
@app.route('/productos')
def productos():
    lista_productos = [
        {"id": 1, "nombre": "Firewall Perimetral Hardware", "categoria": "Ciberseguridad", "precio": 1200.00, "stock": 15},
        {"id": 2, "nombre": "Licencia Antivirus Enterprise (10 PC)", "categoria": "Ciberseguridad", "precio": 450.00, "stock": 50},
        {"id": 3, "nombre": "Servidor Rack 1U Xeon", "categoria": "Infraestructura", "precio": 2500.00, "stock": 5},
        {"id": 4, "nombre": "Certificado SSL Wildcard Anual", "categoria": "Desarrollo Web", "precio": 180.00, "stock": 100}
    ]
    return render_template('productos.html', productos=lista_productos)

# Ruta para el módulo de Clientes
@app.route('/clientes')
def clientes():
    lista_clientes = [
        {"id": 1, "nombre": "Comercial del Tìo Cuchy", "contacto": "Ing. Carlos Santos", "correo": "ventas@cuchyesmeraldas.ec", "telefono": "0983380884"},
        {"id": 2, "nombre": "Centro de Turorias La Churona", "contacto": "Lic. Thais Palma", "correo": "atencion al cliente@churona.ec", "telefono": "09638886015"},
        {"id": 3, "nombre": "Los Recuerditos de la Gasa", "contacto": "Ing. Genesis Palma", "correo": "pgenesis@diciembre.ec", "telefono": "0977778899"}
    ]
    return render_template('clientes.html', clientes=lista_clientes)

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
        {"num": "FAC-001", "cliente": "Comercial del Tìo Cuchy", "fecha": "2026-08-01", "total": 1200.00, "estado": "Pagado"},
        {"num": "FAC-002", "cliente": "Centro de Turorias La Churona", "fecha": "2026-08-05", "total": 450.00, "estado": "Pendiente"},
        {"num": "FAC-003", "cliente": "Los Recuerditos de la Gasa", "fecha": "2026-08-10", "total": 2680.00, "estado": "Pagado"}
    ]
    return render_template('facturacion.html', facturas=lista_facturas)

if __name__ == '__main__':
    app.run(debug=True)