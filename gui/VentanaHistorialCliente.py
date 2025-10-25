import tkinter as tk
from tkinter import ttk

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
        header = tk.Frame(self.ventana, bg='#D4A017', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        info_frame = tk.Frame(header, bg='#D4A017')
        info_frame.pack(fill='both', expand=True, padx=30, pady=15)

        tk.Label(info_frame, text=f"Cliente: {self.cliente.nombre}",
                 font=('Segoe UI', 16, 'bold'),
                 bg='#D4A017', fg='white').pack(anchor='w')

        tk.Label(info_frame, text=f"ID: {self.cliente.id_db} | {self.cliente.localidad} | {self.cliente.telefono}",
                 font=('Segoe UI', 10),
                 bg='#D4A017', fg='white').pack(anchor='w')

        self.crear_resumen_financiero()
        self.crear_tabla_historial()

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

        total_comprado, total_pagado, deuda = self.db.obtener_resumen_financiero_cliente(self.cliente.id_db)

        caja1 = tk.Frame(cajas_frame, bg='#e8f5e9', relief='solid', borderwidth=1)
        caja1.pack(side='left', padx=10, pady=10, ipadx=20, ipady=15)
        tk.Label(caja1, text='Total Comprado', font=('Segoe UI', 10),
                 bg='#e8f5e9', fg='#2e7d32').pack()
        tk.Label(caja1, text=f'${total_comprado:,.2f}', font=('Segoe UI', 16, 'bold'),
                 bg='#e8f5e9', fg='#1b5e20').pack()

        caja2 = tk.Frame(cajas_frame, bg='#e3f2fd', relief='solid', borderwidth=1)
        caja2.pack(side='left', padx=10, pady=10, ipadx=20, ipady=15)
        tk.Label(caja2, text='Total Pagado', font=('Segoe UI', 10),
                 bg='#e3f2fd', fg='#1976d2').pack()
        tk.Label(caja2, text=f'${total_pagado:,.2f}', font=('Segoe UI', 16, 'bold'),
                 bg='#e3f2fd', fg='#0d47a1').pack()

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

        for col in columnas:
            tabla.heading(col, text=col)

        tabla.column('Fecha', width=100)
        tabla.column('Remito', width=120)
        tabla.column('Descripción', width=250)
        tabla.column('Total', width=100)
        tabla.column('Pagado', width=100)
        tabla.column('Saldo', width=100)
        tabla.column('Estado', width=100)

        remitos = self.db.obtener_remitos_cliente(self.cliente.id_db)

        for remito in remitos:
            datos = (
                remito[1],
                remito[0],
                remito[2],
                f'${remito[3]:,.2f}',
                f'${remito[4]:,.2f}',
                f'${remito[5]:,.2f}',
                remito[6]
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