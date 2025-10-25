import tkinter as tk
from tkinter import messagebox
from Cliente import Cliente
import os
import sys

def resource_path(relative_path):
    """Obtener la ruta absoluta del recurso"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class VentanaNuevoCliente:
    """Ventana para registrar un nuevo cliente"""

    def __init__(self, parent, callback):
        self.callback = callback
        self.ventana = tk.Toplevel(parent)
        self.ventana.iconbitmap(resource_path("iconos/cliente.ico"))
        self.ventana.title("Nuevo Cliente")
        self.ventana.geometry("600x650")
        self.ventana.configure(bg='#fafbfc')
        self.ventana.resizable(False, False)

        self.crear_interfaz()

    def crear_interfaz(self):
        header = tk.Frame(self.ventana, bg='#D4A017', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="Registrar Nuevo Cliente",
                 font=('Segoe UI', 16, 'bold'),
                 bg='#D4A017', fg='white').pack(pady=20, padx=30, anchor='w')

        form_frame = tk.Frame(self.ventana, bg='white')
        form_frame.pack(fill='both', expand=True, padx=30, pady=30)

        self.entry_nombre = self.crear_campo(form_frame, "Nombre Completo:", 0)
        self.entry_email = self.crear_campo(form_frame, "Email:", 1)
        self.entry_telefono = self.crear_campo(form_frame, "Teléfono:", 2)
        self.entry_localidad = self.crear_campo(form_frame, "Localidad:", 3)
        self.entry_direccion = self.crear_campo(form_frame, "Calle y Altura:", 4)
        self.entry_colmenas = self.crear_campo(form_frame, "Cantidad de Colmenas:", 5)
        self.entry_renapa = self.crear_campo(form_frame, "Código de RENAPA:", 6)

        tk.Label(form_frame, text="Factura Producción:",
                 font=('Segoe UI', 10, 'bold'),
                 bg='white', fg='#333').grid(row=7, column=0, sticky='w', pady=(10, 5))

        self.factura_var = tk.StringVar(value="No")
        radio_frame = tk.Frame(form_frame, bg='white')
        radio_frame.grid(row=7, column=1, sticky='w', pady=(10, 5))

        tk.Radiobutton(radio_frame, text="Sí", variable=self.factura_var, value="Sí",
                       font=('Segoe UI', 10), bg='white', activebackground='white',
                       selectcolor='#D4A017').pack(side='left', padx=(0, 20))

        tk.Radiobutton(radio_frame, text="No (NN)", variable=self.factura_var, value="No",
                       font=('Segoe UI', 10), bg='white', activebackground='white',
                       selectcolor='#D4A017').pack(side='left')

        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.grid(row=8, column=0, columnspan=2, pady=(30, 0))

        tk.Button(btn_frame, text='💾 Guardar Cliente',
                  font=('Segoe UI', 10, 'bold'), bg='#D4A017', fg='white',
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
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()
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

        try:
            colmenas_num = int(colmenas) if colmenas else 0
        except ValueError:
            colmenas_num = 0

        cliente = Cliente(
            nombre=nombre,
            email=email,
            localidad=localidad,
            telefono=telefono,
            direccion=direccion,
            colmenas=colmenas_num,
            renapa=renapa,
            factura=factura
        )

        self.callback(cliente)
        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente")
        self.ventana.destroy()