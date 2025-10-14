import tkinter as tk
from Cliente import Cliente
from Producto import Producto
from Remito import Remito
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# ==================== BASE DE DATOS ====================
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

        saldo = remito.total - 0  # Al inicio no se ha pagado nada

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

        # Obtener datos actuales
        cursor.execute('SELECT total, pagado FROM remitos WHERE id = ?', (remito_id,))
        total, pagado_actual = cursor.fetchone()

        nuevo_pagado = pagado_actual + monto_pagado
        nuevo_saldo = total - nuevo_pagado

        # Determinar estado
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


# ==================== VENTANAS ====================
class VentanaNuevoCliente:
    """Ventana para registrar un nuevo cliente"""

    def __init__(self, parent, callback):
        self.callback = callback
        self.ventana = tk.Toplevel(parent)
        self.ventana.iconbitmap("iconos\cliente.ico")
        self.ventana.title("Nuevo Cliente")
        self.ventana.geometry("600x550")
        self.ventana.configure(bg='#fafbfc')
        self.ventana.resizable(False, False)

        self.crear_interfaz()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg='#D4A017',
                          height=70)  # LÍNEA 233 - Color miel (header ventana nuevo cliente)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="Registrar Nuevo Cliente",
                 font=('Segoe UI', 16, 'bold'),
                 bg='#D4A017', fg='white').pack(pady=20, padx=30, anchor='w')  # LÍNEA 239 - Color miel (bg label)

        # Formulario
        form_frame = tk.Frame(self.ventana, bg='white')
        form_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Campos
        self.entry_nombre = self.crear_campo(form_frame, "Nombre Completo:", 0)
        self.entry_localidad = self.crear_campo(form_frame, "Localidad:", 1)
        self.entry_direccion = self.crear_campo(form_frame, "Calle y Altura:", 2)
        self.entry_colmenas = self.crear_campo(form_frame, "Cantidad de Colmenas:", 3)
        self.entry_renapa = self.crear_campo(form_frame, "Código de RENAPA:", 4)

        # Radio buttons para facturación
        tk.Label(form_frame, text="Factura Producción:",
                 font=('Segoe UI', 10, 'bold'),
                 bg='white', fg='#333').grid(row=5, column=0, sticky='w', pady=(10, 5))

        self.factura_var = tk.StringVar(value="No")
        radio_frame = tk.Frame(form_frame, bg='white')
        radio_frame.grid(row=5, column=1, sticky='w', pady=(10, 5))

        tk.Radiobutton(radio_frame, text="Sí", variable=self.factura_var, value="Sí",
                       font=('Segoe UI', 10), bg='white', activebackground='white',
                       selectcolor='#D4A017').pack(side='left', padx=(0, 20))  # LÍNEA 264 - Color miel (radio button)

        tk.Radiobutton(radio_frame, text="No (NN)", variable=self.factura_var, value="No",
                       font=('Segoe UI', 10), bg='white', activebackground='white',
                       selectcolor='#D4A017').pack(side='left')  # LÍNEA 268 - Color miel (radio button)

        # Botones
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(30, 0))

        tk.Button(btn_frame, text='💾 Guardar Cliente',
                  font=('Segoe UI', 10, 'bold'), bg='#D4A017', fg='white',  # LÍNEA 273 - Color miel (botón guardar)
                  relief='flat', padx=20, pady=10, cursor='hand2',
                  command=self.guardar_cliente).pack(side='left', padx=5)

        tk.Button(btn_frame, text='❌ Cancelar',
                  font=('Segoe UI', 10), bg='#e0e0e0', fg='#333',
                  relief='flat', padx=20, pady=10, cursor='hand2',
                  command=self.ventana.destroy).pack(side='left', padx=5)

    def crear_campo(self, parent, label_text, row):
        tk.Label(parent, text=label_text, font=('Segoe UI', 10, 'bold'),
                 bg='white', fg='#333').grid(row=row, column=0, sticky='w', pady=(10, 5))

        entry = tk.Entry(parent, font=('Segoe UI', 10),
                         relief='solid', borderwidth=1, width=40)
        entry.grid(row=row, column=1, pady=(10, 5), ipady=5)
        return entry

    def guardar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        localidad = self.entry_localidad.get().strip()
        direccion = self.entry_direccion.get().strip()
        colmenas = self.entry_colmenas.get().strip()
        renapa = self.entry_renapa.get().strip()
        factura = self.factura_var.get() == "Sí"

        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return

        if not localidad:
            messagebox.showwarning("Advertencia", "La localidad es obligatoria")
            return

        # Crear objeto Cliente
        try:
            colmenas_num = int(colmenas) if colmenas else 0
        except ValueError:
            colmenas_num = 0

        cliente = Cliente(nombre, localidad, direccion, colmenas_num, renapa, factura)

        # Llamar al callback para agregar a la tabla y BD
        self.callback(cliente)

        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente")
        self.ventana.destroy()

class VentanaHistorialCliente:
    """Ventana para mostrar el historial de compras de un cliente"""

    def __init__(self, parent, cliente, db):
        self.cliente = cliente
        self.db = db
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Historial de {cliente.nombre}")
        self.ventana.geometry("900x600")
        self.ventana.configure(bg='#fafbfc')

        self.crear_interfaz()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg='#D4A017', height=80)  # LÍNEA 335 - Color miel (header historial)
        header.pack(fill='x')
        header.pack_propagate(False)

        info_frame = tk.Frame(header, bg='#D4A017')  # LÍNEA 339 - Color miel (frame info)
        info_frame.pack(fill='both', expand=True, padx=30, pady=15)

        tk.Label(info_frame, text=f"Cliente: {self.cliente.nombre}",
                 font=('Segoe UI', 16, 'bold'),
                 bg='#D4A017', fg='white').pack(anchor='w')  # LÍNEA 344 - Color miel (bg label)

        tk.Label(info_frame, text=f"ID: {self.cliente.id_db} | {self.cliente.localidad} | {self.cliente.telefono}",
                 font=('Segoe UI', 10),
                 bg='#D4A017', fg='white').pack(anchor='w')  # LÍNEA 348 - Color miel (bg label)

        # Resumen financiero
        self.crear_resumen_financiero()

        # Tabla de historial
        self.crear_tabla_historial()

        # Botón cerrar
        btn_frame = tk.Frame(self.ventana, bg='#fafbfc')
        btn_frame.pack(fill='x', padx=30, pady=(0, 20))

        tk.Button(btn_frame, text='Cerrar',
                  font=('Segoe UI', 10), bg='#e0e0e0', fg='#333',
                  relief='flat', padx=20, pady=8, cursor='hand2',
                  command=self.ventana.destroy).pack(side='right')

    def crear_resumen_financiero(self):
        resumen_frame = tk.Frame(self.ventana, bg='white')
        resumen_frame.pack(fill='x', padx=30, pady=20)

        cajas_frame = tk.Frame(resumen_frame, bg='white')
        cajas_frame.pack(fill='x', pady=10)

        # Obtener resumen desde la BD
        total_comprado, total_pagado, deuda = self.db.obtener_resumen_financiero_cliente(self.cliente.id_db)

        # Total comprado
        caja1 = tk.Frame(cajas_frame, bg='#e8f5e9', relief='solid', borderwidth=1)
        caja1.pack(side='left', padx=10, pady=10, ipadx=20, ipady=15)
        tk.Label(caja1, text='Total Comprado', font=('Segoe UI', 10),
                 bg='#e8f5e9', fg='#2e7d32').pack()
        tk.Label(caja1, text=f'${total_comprado:,.2f}', font=('Segoe UI', 16, 'bold'),
                 bg='#e8f5e9', fg='#1b5e20').pack()

        # Total pagado
        caja2 = tk.Frame(cajas_frame, bg='#e3f2fd', relief='solid', borderwidth=1)
        caja2.pack(side='left', padx=10, pady=10, ipadx=20, ipady=15)
        tk.Label(caja2, text='Total Pagado', font=('Segoe UI', 10),
                 bg='#e3f2fd', fg='#1976d2').pack()
        tk.Label(caja2, text=f'${total_pagado:,.2f}', font=('Segoe UI', 16, 'bold'),
                 bg='#e3f2fd', fg='#0d47a1').pack()

        # Deuda pendiente
        caja3 = tk.Frame(cajas_frame, bg='#ffebee', relief='solid', borderwidth=1)
        caja3.pack(side='left', padx=10, pady=10, ipadx=20, ipady=15)
        tk.Label(caja3, text='Deuda Pendiente', font=('Segoe UI', 10),
                 bg='#ffebee', fg='#c62828').pack()
        tk.Label(caja3, text=f'${deuda:,.2f}', font=('Segoe UI', 16, 'bold'),
                 bg='#ffebee', fg='#b71c1c').pack()

    def crear_tabla_historial(self):
        tk.Label(self.ventana, text="Historial de Compras",
                 font=('Segoe UI', 12, 'bold'),
                 bg='#fafbfc', fg='#333').pack(anchor='w', padx=30, pady=(10, 5))

        table_frame = tk.Frame(self.ventana, bg='white')
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))

        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')

        columnas = ('Fecha', 'Remito', 'Descripción', 'Total', 'Pagado', 'Saldo', 'Estado')
        tabla = ttk.Treeview(table_frame, columns=columnas, show='headings',
                             yscrollcommand=scrollbar.set, height=12)

        scrollbar.config(command=tabla.yview)

        # Configurar columnas
        for col in columnas:
            tabla.heading(col, text=col)

        tabla.column('Fecha', width=100)
        tabla.column('Remito', width=120)
        tabla.column('Descripción', width=250)
        tabla.column('Total', width=100)
        tabla.column('Pagado', width=100)
        tabla.column('Saldo', width=100)
        tabla.column('Estado', width=100)

        # Cargar datos desde la BD
        remitos = self.db.obtener_remitos_cliente(self.cliente.id_db)

        for remito in remitos:
            # remito: (numero, fecha, descripcion, total, pagado, saldo, estado)
            datos = (
                remito[1],  # fecha
                remito[0],  # numero
                remito[2],  # descripcion
                f'${remito[3]:,.2f}',  # total
                f'${remito[4]:,.2f}',  # pagado
                f'${remito[5]:,.2f}',  # saldo
                remito[6]  # estado
            )

            estado = remito[6]
            if '✅' in estado:
                tag = 'pagado'
            elif '⚠️' in estado:
                tag = 'parcial'
            else:
                tag = 'pendiente'

            tabla.insert('', 'end', values=datos, tags=(tag,))

        tabla.tag_configure('pagado', background='#e8f5e9')
        tabla.tag_configure('parcial', background='#fff9e6')
        tabla.tag_configure('pendiente', background='#ffebee')

        tabla.pack(fill='both', expand=True)


# ==================== COMPONENTES ====================
class TablaClientes:
    """Componente tabla de clientes"""

    def __init__(self, parent, on_doble_click, db):
        self.clientes = []  # Lista de objetos Cliente
        self.on_doble_click = on_doble_click
        self.db = db

        # Frame para la tabla
        self.frame = tk.Frame(parent, bg='white')

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame)
        scrollbar.pack(side='right', fill='y')

        # Treeview
        columnas = ('ID', 'Nombre', 'Email', 'Teléfono', 'Localidad')
        self.tabla = ttk.Treeview(self.frame, columns=columnas, show='headings',
                                  yscrollcommand=scrollbar.set, height=15)

        scrollbar.config(command=self.tabla.yview)

        # Configurar columnas
        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Nombre', text='Nombre')
        self.tabla.heading('Email', text='Email')
        self.tabla.heading('Teléfono', text='Teléfono')
        self.tabla.heading('Localidad', text='Localidad')

        self.tabla.column('ID', width=80)
        self.tabla.column('Nombre', width=200)
        self.tabla.column('Email', width=250)
        self.tabla.column('Teléfono', width=150)
        self.tabla.column('Localidad', width=200)

        # Vincular doble click
        self.tabla.bind('<Double-Button-1>', self.handle_doble_click)

        self.tabla.pack(fill='both', expand=True)

        # Cargar datos desde BD
        self.cargar_desde_bd()

    def cargar_desde_bd(self):
        """Cargar clientes desde la base de datos"""
        clientes_db = self.db.obtener_clientes()

        for cliente_tupla in clientes_db:
            cliente = Cliente.desde_db(cliente_tupla)
            self.clientes.append(cliente)
            self.tabla.insert('', 'end', values=cliente.get_datos_tabla())

    def agregar_cliente(self, cliente):
        """Agregar un nuevo cliente a la tabla y BD"""
        # Insertar en BD
        cliente_id = self.db.insertar_cliente(cliente)
        cliente.id_db = cliente_id

        # Agregar a la lista y tabla
        self.clientes.append(cliente)
        self.tabla.insert('', 'end', values=cliente.get_datos_tabla())

    def handle_doble_click(self, event):
        """Manejar doble click en la tabla"""
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        # Obtener índice del item seleccionado
        item_id = seleccion[0]
        index = self.tabla.index(item_id)

        # Obtener el objeto Cliente correspondiente
        if 0 <= index < len(self.clientes):
            cliente = self.clientes[index]
            self.on_doble_click(cliente)

    def eliminar_cliente_seleccionado(self):
        """Eliminar el cliente seleccionado"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para eliminar")
            return

        # Obtener índice del item seleccionado
        item_id = seleccion[0]
        index = self.tabla.index(item_id)

        # Obtener el objeto Cliente correspondiente
        if 0 <= index < len(self.clientes):
            cliente = self.clientes[index]

            # Confirmar eliminación
            respuesta = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está seguro de eliminar al cliente '{cliente.nombre}'?\n\n"
                f"Esta acción no se puede deshacer."
            )

            if respuesta:
                try:
                    # Eliminar de la base de datos
                    self.db.eliminar_cliente(cliente.id_db)

                    # Eliminar de la lista
                    self.clientes.pop(index)

                    # Eliminar de la tabla
                    self.tabla.delete(item_id)

                    messagebox.showinfo("Éxito", f"Cliente '{cliente.nombre}' eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{str(e)}")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class TablaProductos:
    """Componente tabla de productos"""

    def __init__(self, parent, db):
        self.productos = []
        self.db = db

        self.frame = tk.Frame(parent, bg='white')

        scrollbar = ttk.Scrollbar(self.frame)
        scrollbar.pack(side='right', fill='y')

        columnas = ('Código', 'Nombre', 'Categoría', 'Precio', 'Stock')
        self.tabla = ttk.Treeview(self.frame, columns=columnas, show='headings',
                                  yscrollcommand=scrollbar.set, height=15)

        scrollbar.config(command=self.tabla.yview)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200)

        self.tabla.pack(fill='both', expand=True)

        self.cargar_desde_bd()

    def cargar_desde_bd(self):
        """Cargar productos desde la base de datos"""
        productos_db = self.db.obtener_productos()

        for producto_tupla in productos_db:
            producto = Producto.desde_db(producto_tupla)
            self.productos.append(producto)
            self.tabla.insert('', 'end', values=producto.get_datos_tabla())

    def agregar_producto(self, producto):
        """Agregar producto a la tabla y BD"""
        producto_id = self.db.insertar_producto(producto)
        producto.id_db = producto_id

        self.productos.append(producto)
        self.tabla.insert('', 'end', values=producto.get_datos_tabla())

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class TablaRemitos:
    """Componente tabla de remitos"""

    def __init__(self, parent, db):
        self.remitos = []
        self.db = db

        self.frame = tk.Frame(parent, bg='white')

        scrollbar = ttk.Scrollbar(self.frame)
        scrollbar.pack(side='right', fill='y')

        columnas = ('Nº Remito', 'Fecha', 'Cliente', 'Total', 'Estado')
        self.tabla = ttk.Treeview(self.frame, columns=columnas, show='headings',
                                  yscrollcommand=scrollbar.set, height=15)

        scrollbar.config(command=self.tabla.yview)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200)

        self.tabla.pack(fill='both', expand=True)

        self.cargar_desde_bd()

    def cargar_desde_bd(self):
        """Cargar remitos desde la base de datos"""
        remitos_db = self.db.obtener_remitos()

        for remito_tupla in remitos_db:
            remito = Remito.desde_db(remito_tupla)
            self.remitos.append(remito)
            self.tabla.insert('', 'end', values=remito.get_datos_tabla())

    def agregar_remito(self, remito, cliente_id):
        """Agregar remito a la tabla y BD"""
        remito_id = self.db.insertar_remito(remito, cliente_id)
        remito.id_db = remito_id

        self.remitos.append(remito)
        self.tabla.insert('', 'end', values=remito.get_datos_tabla())

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


# ==================== APLICACIÓN PRINCIPAL ====================
class Principal:
    """Aplicación principal"""

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Sistema de gestion de Apicultura")
        self.ventana.state('zoomed')
        self.ventana.configure(bg='#D4A017')  # LÍNEA 677 - Color miel (fondo ventana)
        self.ventana.iconbitmap("iconos\colmena.ico")

        # Inicializar base de datos
        self.db = BaseDatos()

        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TNotebook', background='#f8f9fa', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10],
                        font=('Segoe UI', 10, 'bold'),
                        background='#f8f9fa', foreground='#666')
        style.map('TNotebook.Tab',
                  background=[('selected', 'white')],
                  foreground=[('selected', '#D4A017')])  # LÍNEA 694 - Color miel (pestaña activa)

        style.configure('Primary.TButton',
                        background='#D4A017', foreground='white',  # LÍNEA 697 - Color miel (botones primarios)
                        font=('Segoe UI', 9, 'bold'),
                        borderwidth=0, focuscolor='none')
        style.map('Primary.TButton',
                  background=[('active', '#5568d3')])

        style.configure('Secondary.TButton',
                        background='#e0e0e0', foreground='#333',
                        font=('Segoe UI', 9),
                        borderwidth=0, focuscolor='none')

        style.configure('Treeview',
                        background='white', foreground='#333',
                        fieldbackground='white',
                        font=('Segoe UI', 9), rowheight=30)
        style.configure('Treeview.Heading',
                        background='#f8f9fa', foreground='#333',
                        font=('Segoe UI', 10, 'bold'), relief='flat')
        style.map('Treeview',
                  background=[('selected', '#D4A017')],  # LÍNEA 713 - Color miel (selección en tabla)
                  foreground=[('selected', 'white')])

    def crear_interfaz(self):
        self.crear_header()
        self.crear_pestanas()

    def crear_header(self):
        header_frame = tk.Frame(self.ventana, bg='#D4A017', height=70)  # LÍNEA 720 - Color miel (header)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="Sistema de gestion Apicultor - Mario Merlo",
                 font=('Segoe UI', 18, 'bold'),
                 bg='#D4A017', fg='white').pack(side='left', padx=30, pady=20)  # LÍNEA 726 - Color miel (bg label)

        btn_frame = tk.Frame(header_frame, bg='#D4A017')  # LÍNEA 728 - Color miel (frame botones)
        btn_frame.pack(side='right', padx=30)

        tk.Button(btn_frame, text="⚙️ Configuración",
                  bg='#C4911A', fg='white', font=('Segoe UI', 9),  # LÍNEA 732 - Miel más oscuro (botón config)
                  relief='flat', padx=15, pady=5,
                  cursor='hand2').pack(side='left', padx=5)

        tk.Button(btn_frame, text="👤 Usuario",
                  bg='#C4911A', fg='white', font=('Segoe UI', 9),  # LÍNEA 737 - Miel más oscuro (botón usuario)
                  relief='flat', padx=15, pady=5,
                  cursor='hand2').pack(side='left', padx=5)

    def crear_pestanas(self):
        container = tk.Frame(self.ventana, bg='#D4A017')  # LÍNEA 742 - Color miel (container pestañas)
        container.pack(fill='both', expand=True, padx=2, pady=2)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill='both', expand=True)

        self.crear_tab_clientes()
        self.crear_tab_productos()
        self.crear_tab_remitos()

    def crear_tab_clientes(self):
        tab = tk.Frame(self.notebook, bg='#fafbfc')
        self.notebook.add(tab, text='👥 Clientes')

        # Toolbar
        toolbar = tk.Frame(tab, bg='white', relief='flat')
        toolbar.pack(fill='x', padx=30, pady=(30, 20))

        ttk.Button(toolbar, text='➕ Nuevo Cliente', style='Primary.TButton',
                   command=self.abrir_nuevo_cliente).pack(side='left', padx=5, pady=10)

        ttk.Button(toolbar, text='✏️ Editar',
                   style='Secondary.TButton').pack(side='left', padx=5)

        ttk.Button(toolbar, text='🗑️ Eliminar',
                   style='Secondary.TButton',
                   command=self.eliminar_cliente).pack(side='left', padx=5)

        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side='right', padx=10, fill='x', expand=True)

        tk.Entry(search_frame, font=('Segoe UI', 10),
                 relief='solid', borderwidth=1).pack(side='left', fill='x',
                                                     expand=True, padx=(100, 5), ipady=5)

        ttk.Button(search_frame, text='🔍', style='Primary.TButton',
                   width=5).pack(side='left')

        # Tabla de clientes
        self.tabla_clientes = TablaClientes(tab, self.abrir_historial_cliente, self.db)
        self.tabla_clientes.pack(fill='both', expand=True, padx=30, pady=(0, 30))

    def crear_tab_productos(self):
        tab = tk.Frame(self.notebook, bg='#fafbfc')
        self.notebook.add(tab, text='📦 Productos')

        toolbar = tk.Frame(tab, bg='white', relief='flat')
        toolbar.pack(fill='x', padx=30, pady=(30, 20))

        ttk.Button(toolbar, text='➕ Nuevo Producto',
                   style='Primary.TButton').pack(side='left', padx=5, pady=10)

        ttk.Button(toolbar, text='✏️ Editar',
                   style='Secondary.TButton').pack(side='left', padx=5)

        ttk.Button(toolbar, text='🗑️ Eliminar',
                   style='Secondary.TButton').pack(side='left', padx=5)

        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side='right', padx=10, fill='x', expand=True)

        tk.Entry(search_frame, font=('Segoe UI', 10),
                 relief='solid', borderwidth=1).pack(side='left', fill='x',
                                                     expand=True, padx=(100, 5), ipady=5)

        ttk.Button(search_frame, text='🔍', style='Primary.TButton',
                   width=5).pack(side='left')

        self.tabla_productos = TablaProductos(tab, self.db)
        self.tabla_productos.pack(fill='both', expand=True, padx=30, pady=(0, 30))

    def crear_tab_remitos(self):
        tab = tk.Frame(self.notebook, bg='#fafbfc')
        self.notebook.add(tab, text='📄 Remitos')

        toolbar = tk.Frame(tab, bg='white', relief='flat')
        toolbar.pack(fill='x', padx=30, pady=(30, 20))

        ttk.Button(toolbar, text='➕ Nuevo Remito',
                   style='Primary.TButton').pack(side='left', padx=5, pady=10)

        ttk.Button(toolbar, text='👁️ Ver',
                   style='Secondary.TButton').pack(side='left', padx=5)

        ttk.Button(toolbar, text='🖨️ Imprimir',
                   style='Secondary.TButton').pack(side='left', padx=5)

        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side='right', padx=10, fill='x', expand=True)

        entry_buscar = tk.Entry(search_frame, font=('Segoe UI', 10),
                                relief='solid', borderwidth=1)
        entry_buscar.pack(side='left', fill='x', expand=True, padx=(100, 5), ipady=5)

        ttk.Button(search_frame, text='🔍', style='Primary.TButton',
                   width=5).pack(side='left')

        self.tabla_remitos = TablaRemitos(tab, self.db)
        self.tabla_remitos.pack(fill='both', expand=True, padx=30, pady=(0, 30))

    def abrir_nuevo_cliente(self):
        """Abrir ventana para crear nuevo cliente"""
        VentanaNuevoCliente(self.ventana, self.agregar_cliente)

    def agregar_cliente(self, cliente):
        """Callback para agregar cliente a la tabla"""
        self.tabla_clientes.agregar_cliente(cliente)

    def abrir_historial_cliente(self, cliente):
        """Abrir ventana de historial de un cliente"""
        VentanaHistorialCliente(self.ventana, cliente, self.db)

    def eliminar_cliente(self):
        """Eliminar cliente seleccionado"""
        self.tabla_clientes.eliminar_cliente_seleccionado()

if __name__ == '__main__':
    root = tk.Tk()
    app = Principal(root)
    root.mainloop()