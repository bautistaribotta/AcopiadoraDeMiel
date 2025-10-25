import tkinter as tk
from tkinter import ttk
from Remito import Remito

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