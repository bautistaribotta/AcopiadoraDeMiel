import tkinter as tk

def abrir_ventana_clientes():
    ventana_clientes = tk.Toplevel(ventana)
    ventana_clientes.title("Clientes")
    ventana_clientes.geometry("600x400+700+100")
    ventana_clientes.configure(bg="white")

def abrir_ventana_productos():
    ventana_productos = tk.Toplevel(ventana)
    ventana_productos.title("Productos")
    ventana_productos.geometry("600x400+25+100")  # Tamaño y posición
    ventana_productos.configure(bg="white")

def main():
    global ventana  # Hacer la variable ventana global
    ventana = tk.Tk()

    # Obtener tamaño de pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Configurar ventana principal
    ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    ventana.title("Miel")
    ventana.configure(bg="gray16")
    ventana.resizable(True, True)
    ventana.attributes("-alpha", 1)

    # Encabezado superior con botones
    encabezado = tk.Frame(ventana, bg="gray25", height=50)
    encabezado.pack(fill="x")

    boton_productos = tk.Button(encabezado, text="Productos", command=abrir_ventana_productos)
    boton_productos.pack(side="left", padx=10, pady=10)

    boton_clientes = tk.Button(encabezado, text="Clientes", command=abrir_ventana_clientes)
    boton_clientes.pack(side="left", padx=10, pady=10)

    boton_remitos = tk.Button(encabezado, text="Remitos")
    boton_remitos.pack(side="left", padx=10, pady=10)

    # Frame principal
    frame1 = tk.Frame(ventana, bg="white", bd=5)
    frame1.pack(fill="both", expand=True)

    ventana.mainloop()

# Incio del programa
if __name__ == "__main__":
    main()