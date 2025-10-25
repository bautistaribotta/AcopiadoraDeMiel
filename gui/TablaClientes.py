import tkinter as tk
from tkinter import ttk, messagebox
from Cliente import Cliente

class TablaClientes:
    """Componente tabla de clientes"""

    def __init__(self, parent, on_doble_click, db):
        self.clientes = []
        self.on_doble_click = on_doble_click
        self.db = db

        self.frame = tk.Frame(parent, bg='white')

        scrollbar = ttk.Scrollbar(self.frame)
        scrollbar.pack(side='right', fill='y')

        columnas = ('ID', 'Nombre', 'Email', 'Teléfono', 'Localidad')
        self.tabla = ttk.Treeview(self.frame, columns=columnas, show='headings',
                                  yscrollcommand=scrollbar.set, height=15)

        scrollbar.config(command=self.tabla.yview)

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

        self.tabla.bind('<Double-Button-1>', self.handle_doble_click)

        self.tabla.pack(fill='both', expand=True)

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
        cliente_id = self.db.insertar_cliente(cliente)
        cliente.id_db = cliente_id

        self.clientes.append(cliente)
        self.tabla.insert('', 'end', values=cliente.get_datos_tabla())

    def handle_doble_click(self, event):
        """Manejar doble click en la tabla"""
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        item_id = seleccion[0]
        index = self.tabla.index(item_id)

        if 0 <= index < len(self.clientes):
            cliente = self.clientes[index]
            self.on_doble_click(cliente)

    def eliminar_cliente_seleccionado(self):
        """Eliminar el cliente seleccionado"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para eliminar")
            return

        item_id = seleccion[0]
        index = self.tabla.index(item_id)

        if 0 <= index < len(self.clientes):
            cliente = self.clientes[index]

            respuesta = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está seguro de eliminar al cliente '{cliente.nombre}'?\n\n"
                f"Esta acción no se puede deshacer."
            )

            if respuesta:
                try:
                    self.db.eliminar_cliente(cliente.id_db)
                    self.clientes.pop(index)
                    self.tabla.delete(item_id)
                    messagebox.showinfo("Éxito", f"Cliente '{cliente.nombre}' eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{str(e)}")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)