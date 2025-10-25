import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from Login import VentanaLogin
from base_de_datos.BaseDatos import BaseDatos
from gui.TablaClientes import TablaClientes
from gui.TablaProductos import TablaProductos
from gui.TablaRemitos import TablaRemitos
from gui.VentanaNuevoCliente import VentanaNuevoCliente
from gui.VentanaHistorialCliente import VentanaHistorialCliente

# Es para que funcione el ejecutable y tenga en cuenta los iconos
def resource_path(relative_path):
    """Obtener la ruta absoluta del recurso"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ==================== APLICACIÓN PRINCIPAL ====================
class Principal:
    """Aplicación principal"""

    def __init__(self, root, tipo_usuario):
        self.ventana = root
        self.tipo_usuario = tipo_usuario  # GUARDAR EL TIPO DE USUARIO
        self.ventana.title("Sistema de gestion de Apicultura")
        self.ventana.state('zoomed')
        self.ventana.configure(bg='#D4A017')
        self.ventana.iconbitmap(resource_path("iconos/colmena.ico"))

        self.db = BaseDatos()

        self.configurar_estilos()
        self.crear_interfaz()

    def crear_header(self):
        header_frame = tk.Frame(self.ventana, bg='#D4A017', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="Sistema de gestion Apicultor",
                 font=('Segoe UI', 18, 'bold'),
                 bg='#D4A017', fg='white').pack(side='left', padx=30, pady=20)

        btn_frame = tk.Frame(header_frame, bg='#D4A017')
        btn_frame.pack(side='right', padx=30)

        # MOSTRAR EL TIPO DE USUARIO
        tipo_usuario_texto = "👤 Usuario" if self.tipo_usuario == "usuario" else "🔐 Administrador"
        tk.Label(btn_frame, text=tipo_usuario_texto,
                 bg='#C4911A', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief='flat', padx=15, pady=5).pack(side='left', padx=5)

        tk.Button(btn_frame, text="⚙️ Configuración",
                  bg='#C4911A', fg='white', font=('Segoe UI', 9),
                  relief='flat', padx=15, pady=5,
                  cursor='hand2').pack(side='left', padx=5)

        # BOTÓN PARA CERRAR SESIÓN
        tk.Button(btn_frame, text="🚪 Cerrar Sesión",
                  bg='#C4911A', fg='white', font=('Segoe UI', 9),
                  relief='flat', padx=15, pady=5,
                  cursor='hand2',
                  command=self.cerrar_sesion).pack(side='left', padx=5)


    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro que desea cerrar sesión?"
        )
        if respuesta:
            self.ventana.destroy()
            iniciar_aplicacion()  # Volver a mostrar el login


    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TNotebook', background='#f8f9fa', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10],
                        font=('Segoe UI', 10, 'bold'),
                        background='#f8f9fa', foreground='#666')
        style.map('TNotebook.Tab',
                  background=[('selected', 'white')],
                  foreground=[('selected', '#D4A017')])

        style.configure('Primary.TButton',
                        background='#D4A017', foreground='white',
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
                  background=[('selected', '#D4A017')],
                  foreground=[('selected', 'white')])

    def crear_interfaz(self):
        self.crear_header()
        self.crear_pestanas()

    def crear_pestanas(self):
        container = tk.Frame(self.ventana, bg='#D4A017')
        container.pack(fill='both', expand=True, padx=2, pady=2)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill='both', expand=True)

        self.crear_tab_clientes()
        self.crear_tab_productos()
        self.crear_tab_remitos()

    def crear_tab_clientes(self):
        tab = tk.Frame(self.notebook, bg='#fafbfc')
        self.notebook.add(tab, text='👥 Clientes')

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

        self.entry_buscar_cliente = tk.Entry(search_frame, font=('Segoe UI', 10),
                                             relief='solid', borderwidth=1)
        self.entry_buscar_cliente.pack(side='left', fill='x',
                                       expand=True, padx=(100, 5), ipady=5)

        self.entry_buscar_cliente.bind('<KeyRelease>', lambda e: self.buscar_cliente())

        ttk.Button(search_frame, text='🔍', style='Primary.TButton',
                   width=5, command=self.buscar_cliente).pack(side='left')

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

    def buscar_cliente(self):
        """Buscar clientes por nombre"""
        texto_busqueda = self.entry_buscar_cliente.get().strip().lower()

        for item in self.tabla_clientes.tabla.get_children():
            self.tabla_clientes.tabla.delete(item)

        if not texto_busqueda:
            for cliente in self.tabla_clientes.clientes:
                self.tabla_clientes.tabla.insert('', 'end', values=cliente.get_datos_tabla())
        else:
            for cliente in self.tabla_clientes.clientes:
                if texto_busqueda in cliente.nombre.lower():
                    self.tabla_clientes.tabla.insert('', 'end', values=cliente.get_datos_tabla())


def iniciar_aplicacion():
    """Función para iniciar la aplicación con login"""

    def callback_login_exitoso(tipo_usuario):
        """Callback cuando el login es exitoso"""
        root = tk.Tk()
        app = Principal(root, tipo_usuario)
        root.mainloop()

    # Mostrar ventana de login
    login = VentanaLogin(callback_login_exitoso)
    login.iniciar()

if __name__ == '__main__':
    iniciar_aplicacion()