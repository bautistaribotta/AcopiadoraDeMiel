import sqlite3
from datetime import *

class BaseDatos:
    """Clase para manejar la base de datos SQLite"""

    def __init__(self, nombre_db="gestion_apicola.db"):
        self.nombre_db = nombre_db
        self.conexion = None
        self.crear_tablas()

    def conectar(self):
        """Establecer conexión con la base de datos"""
        self.conexion = sqlite3.connect(self.nombre_db)
        return self.conexion

    def desconectar(self):
        """Cerrar conexión"""
        if self.conexion:
            self.conexion.close()

    def crear_tablas(self):
        """Crear las tablas si no existen"""
        conn = self.conectar()
        cursor = conn.cursor()

        # Tabla Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT,
                telefono TEXT,
                localidad TEXT NOT NULL,
                direccion TEXT,
                colmenas INTEGER DEFAULT 0,
                renapa TEXT,
                factura BOOLEAN DEFAULT 0,
                fecha_registro TEXT
            )
        ''')

        # Tabla Productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                categoria TEXT,
                precio REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                fecha_registro TEXT
            )
        ''')

        # Tabla Remitos/Operaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS remitos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                fecha TEXT NOT NULL,
                cliente_id INTEGER NOT NULL,
                total REAL NOT NULL,
                pagado REAL DEFAULT 0,
                saldo REAL NOT NULL,
                estado TEXT,
                descripcion TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')

        # Tabla Detalle de Remitos (items de cada remito)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS remito_detalle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remito_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (remito_id) REFERENCES remitos (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')

        conn.commit()
        self.desconectar()

    # ========== MÉTODOS PARA CLIENTES ==========
    def insertar_cliente(self, cliente):
        """Insertar un nuevo cliente"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO clientes (nombre, email, telefono, localidad, direccion, 
                                colmenas, renapa, factura, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cliente.nombre, cliente.email, cliente.telefono, cliente.localidad,
              cliente.direccion, cliente.colmenas, cliente.renapa,
              cliente.factura, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        cliente_id = cursor.lastrowid
        conn.commit()
        self.desconectar()
        return cliente_id

    def obtener_clientes(self):
        """Obtener todos los clientes"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM clientes ORDER BY nombre')
        clientes = cursor.fetchall()

        self.desconectar()
        return clientes

    def obtener_cliente_por_id(self, cliente_id):
        """Obtener un cliente específico"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        cliente = cursor.fetchone()

        self.desconectar()
        return cliente

    def actualizar_cliente(self, cliente_id, datos):
        """Actualizar datos de un cliente"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE clientes 
            SET nombre=?, email=?, telefono=?, localidad=?, direccion=?,
                colmenas=?, renapa=?, factura=?
            WHERE id=?
        ''', (*datos, cliente_id))

        conn.commit()
        self.desconectar()

    def eliminar_cliente(self, cliente_id):
        """Eliminar un cliente"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))

        conn.commit()
        self.desconectar()

    # ========== MÉTODOS PARA PRODUCTOS ==========
    def insertar_producto(self, producto):
        """Insertar un nuevo producto"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO productos (codigo, nombre, categoria, precio, stock, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (producto.codigo, producto.nombre, producto.categoria,
              producto.precio, producto.stock,
              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        producto_id = cursor.lastrowid
        conn.commit()
        self.desconectar()
        return producto_id

    def obtener_productos(self):
        """Obtener todos los productos"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM productos ORDER BY nombre')
        productos = cursor.fetchall()

        self.desconectar()
        return productos

    def actualizar_stock(self, producto_id, nuevo_stock):
        """Actualizar stock de un producto"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('UPDATE productos SET stock = ? WHERE id = ?',
                       (nuevo_stock, producto_id))

        conn.commit()
        self.desconectar()

    def eliminar_producto(self, producto_id):
        """Eliminar un producto"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))

        conn.commit()
        self.desconectar()

    # ========== MÉTODOS PARA REMITOS ==========
    def insertar_remito(self, remito, cliente_id):
        """Insertar un nuevo remito"""
        conn = self.conectar()
        cursor = conn.cursor()

        saldo = remito.total - 0

        cursor.execute('''
            INSERT INTO remitos (numero, fecha, cliente_id, total, pagado, 
                               saldo, estado, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (remito.numero, remito.fecha, cliente_id, remito.total,
              0, saldo, remito.estado, 'Remito generado'))

        remito_id = cursor.lastrowid
        conn.commit()
        self.desconectar()
        return remito_id

    def obtener_remitos(self):
        """Obtener todos los remitos con nombres de clientes"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT r.id, r.numero, r.fecha, c.nombre, r.total, r.estado
            FROM remitos r
            JOIN clientes c ON r.cliente_id = c.id
            ORDER BY r.fecha DESC
        ''')
        remitos = cursor.fetchall()

        self.desconectar()
        return remitos

    def obtener_remitos_cliente(self, cliente_id):
        """Obtener remitos de un cliente específico"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT numero, fecha, descripcion, total, pagado, saldo, estado
            FROM remitos
            WHERE cliente_id = ?
            ORDER BY fecha DESC
        ''', (cliente_id,))
        remitos = cursor.fetchall()

        self.desconectar()
        return remitos

    def obtener_resumen_financiero_cliente(self, cliente_id):
        """Obtener resumen financiero de un cliente"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                COALESCE(SUM(total), 0) as total_comprado,
                COALESCE(SUM(pagado), 0) as total_pagado,
                COALESCE(SUM(saldo), 0) as deuda_pendiente
            FROM remitos
            WHERE cliente_id = ?
        ''', (cliente_id,))

        resumen = cursor.fetchone()
        self.desconectar()

        return resumen if resumen else (0, 0, 0)

    def actualizar_pago_remito(self, remito_id, monto_pagado):
        """Actualizar el pago de un remito"""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('SELECT total, pagado FROM remitos WHERE id = ?', (remito_id,))
        total, pagado_actual = cursor.fetchone()

        nuevo_pagado = pagado_actual + monto_pagado
        nuevo_saldo = total - nuevo_pagado

        if nuevo_saldo <= 0:
            estado = '✅ Pagado'
        elif nuevo_pagado > 0:
            estado = '⚠️ Parcial'
        else:
            estado = '❌ Pendiente'

        cursor.execute('''
            UPDATE remitos 
            SET pagado = ?, saldo = ?, estado = ?
            WHERE id = ?
        ''', (nuevo_pagado, nuevo_saldo, estado, remito_id))

        conn.commit()
        self.desconectar()