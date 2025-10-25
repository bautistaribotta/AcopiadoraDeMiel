import tkinter as tk
from tkinter import messagebox
import os
import sys


def resource_path(relative_path):
    """Obtener la ruta absoluta del recurso"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class VentanaLogin:
    """Ventana de inicio de sesión"""

    def __init__(self, callback_exito):
        self.callback_exito = callback_exito
        self.tipo_usuario = None

        self.ventana = tk.Tk()
        self.ventana.title("Inicio de Sesión - Sistema Apícola")
        self.ventana.geometry("500x600")
        self.ventana.configure(bg='#fafbfc')
        self.ventana.resizable(False, False)

        # Intentar cargar el icono si existe
        try:
            self.ventana.iconbitmap(resource_path("iconos/colmena.ico"))
        except:
            pass

        self.crear_interfaz()
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        self.ventana.update_idletasks()
        width = self.ventana.winfo_width()
        height = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2 + 40)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        # Header con degradado simulado
        header = tk.Frame(self.ventana, bg='#D4A017', height=140)
        header.pack(fill='x')
        header.pack_propagate(False)

        # Contenedor centrado para icono y título
        header_content = tk.Frame(header, bg='#D4A017')
        header_content.place(relx=0.5, rely=0.5, anchor='center')

        # Icono y título
        tk.Label(header_content, text="🐝", font=('Segoe UI', 45),
                 bg='#D4A017', fg='white').pack(pady=(0, 5))

        tk.Label(header_content, text="Sistema de Gestión Apícola",
                 font=('Segoe UI', 18, 'bold'),
                 bg='#D4A017', fg='white').pack()

        # Formulario
        form_frame = tk.Frame(self.ventana, bg='white')
        form_frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Título del formulario
        tk.Label(form_frame, text="Iniciar Sesión",
                 font=('Segoe UI', 18, 'bold'),
                 bg='white', fg='#333').pack(pady=(0, 30))

        # Selección de tipo de usuario
        tk.Label(form_frame, text="Tipo de Usuario:",
                 font=('Segoe UI', 11, 'bold'),
                 bg='white', fg='#333').pack(anchor='w', pady=(10, 5))

        self.tipo_usuario_var = tk.StringVar(value="usuario")

        # Frame para los radio buttons
        radio_frame = tk.Frame(form_frame, bg='white')
        radio_frame.pack(fill='x', pady=(0, 20))

        rb_usuario = tk.Radiobutton(
            radio_frame,
            text="👤 Usuario",
            variable=self.tipo_usuario_var,
            value="usuario",
            font=('Segoe UI', 11),
            bg='white',
            activebackground='white',
            selectcolor='#D4A017',
            command=self.cambiar_tipo_usuario,
            cursor='hand2'
        )
        rb_usuario.pack(side='left', padx=(0, 30))

        rb_admin = tk.Radiobutton(
            radio_frame,
            text="🔐 Administrador",
            variable=self.tipo_usuario_var,
            value="administrador",
            font=('Segoe UI', 11),
            bg='white',
            activebackground='white',
            selectcolor='#D4A017',
            command=self.cambiar_tipo_usuario,
            cursor='hand2'
        )
        rb_admin.pack(side='left')

        # Frame para la contraseña (inicialmente oculto)
        self.password_frame = tk.Frame(form_frame, bg='white')

        tk.Label(self.password_frame, text="Contraseña:",
                 font=('Segoe UI', 11, 'bold'),
                 bg='white', fg='#333').pack(anchor='w', pady=(10, 5))

        password_entry_frame = tk.Frame(self.password_frame, bg='white')
        password_entry_frame.pack(fill='x', pady=(0, 10))

        self.entry_password = tk.Entry(
            password_entry_frame,
            font=('Segoe UI', 12),
            relief='solid',
            borderwidth=1,
            show='●'
        )
        self.entry_password.pack(side='left', fill='x', expand=True, ipady=8)
        self.entry_password.bind('<Return>', lambda e: self.iniciar_sesion())

        # Botón para mostrar/ocultar contraseña
        self.btn_mostrar = tk.Button(
            password_entry_frame,
            text="👁️",
            font=('Segoe UI', 10),
            bg='#f0f0f0',
            relief='flat',
            cursor='hand2',
            width=3,
            command=self.toggle_password
        )
        self.btn_mostrar.pack(side='left', padx=(5, 0))

        # Información de ayuda
        self.info_label = tk.Label(
            form_frame,
            text="✓ Acceso directo sin contraseña",
            font=('Segoe UI', 9),
            bg='white',
            fg='#4CAF50'
        )
        self.info_label.pack(pady=(10, 30))

        # Botones
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(pady=(20, 0))

        tk.Button(
            btn_frame,
            text='🚀 Ingresar',
            font=('Segoe UI', 11, 'bold'),
            bg='#D4A017',
            fg='white',
            relief='flat',
            padx=40,
            pady=12,
            cursor='hand2',
            command=self.iniciar_sesion
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text='❌ Salir',
            font=('Segoe UI', 11),
            bg='#e0e0e0',
            fg='#333',
            relief='flat',
            padx=40,
            pady=12,
            cursor='hand2',
            command=self.ventana.destroy
        ).pack(side='left', padx=5)

        # Footer
        footer = tk.Frame(self.ventana, bg='#fafbfc', height=40)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="© 2025 - Sistema de Gestión Apícola",
            font=('Segoe UI', 8),
            bg='#fafbfc',
            fg='#999'
        ).pack(pady=10)

    def cambiar_tipo_usuario(self):
        """Mostrar u ocultar campo de contraseña según el tipo de usuario"""
        if self.tipo_usuario_var.get() == "administrador":
            self.password_frame.pack(fill='x', pady=(0, 10))
            self.info_label.config(
                text="🔒 Ingrese la contraseña de administrador",
                fg='#FF9800'
            )
            self.entry_password.focus()
        else:
            self.password_frame.pack_forget()
            self.info_label.config(
                text="✓ Acceso directo sin contraseña",
                fg='#4CAF50'
            )
            self.entry_password.delete(0, tk.END)

    def toggle_password(self):
        """Mostrar u ocultar contraseña"""
        if self.entry_password.cget('show') == '●':
            self.entry_password.config(show='')
            self.btn_mostrar.config(text='🙈')
        else:
            self.entry_password.config(show='●')
            self.btn_mostrar.config(text='👁️')

    def iniciar_sesion(self):
        """Validar credenciales e iniciar sesión"""
        tipo_usuario = self.tipo_usuario_var.get()

        if tipo_usuario == "usuario":
            # Usuario normal: acceso directo
            self.tipo_usuario = "usuario"
            messagebox.showinfo(
                "Bienvenido",
                "Acceso concedido como Usuario\n\n"
                "Podrás gestionar clientes, productos y remitos."
            )
            self.ventana.destroy()
            self.callback_exito(self.tipo_usuario)

        elif tipo_usuario == "administrador":
            # Administrador: requiere contraseña
            password = self.entry_password.get()

            if password == "494189":
                self.tipo_usuario = "administrador"
                messagebox.showinfo(
                    "Bienvenido Administrador",
                    "Acceso concedido como Administrador\n\n"
                    "Tendrás acceso completo al sistema."
                )
                self.ventana.destroy()
                self.callback_exito(self.tipo_usuario)
            else:
                messagebox.showerror(
                    "Error de Autenticación",
                    "Contraseña incorrecta\n\n"
                    "Por favor, verifique la contraseña e intente nuevamente."
                )
                self.entry_password.delete(0, tk.END)
                self.entry_password.focus()

    def iniciar(self):
        """Iniciar el loop de la ventana"""
        self.ventana.mainloop()