from Producto import Producto
import tkinter as tk
from tkinter import ttk

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