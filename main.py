import tkinter

def abrir_ventana_clientes():
    ventana_clientes = tkinter.Toplevel(ventana)
    ventana_clientes.title("Clientes")
    ventana_clientes.geometry("600x400+700+100")
    ventana_clientes.configure(bg="white")

def abrir_ventana_productos():
    ventana_productos = tkinter.Toplevel(ventana)
    ventana_productos.title("Productos")
    ventana_productos.geometry("600x400+25+100")  # Tamaño y posición
    ventana_productos.configure(bg="white")

def test():
    ventana = tkinter.Tk()

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
    encabezado = tkinter.Frame(ventana, bg="gray25", height=50)
    encabezado.pack(fill="x")

    boton_productos = tkinter.Button(encabezado, text="Productos", command=abrir_ventana_productos)
    boton_productos.pack(side="left", padx=10, pady=10)

    boton_clientes = tkinter.Button(encabezado, text="Clientes", command=abrir_ventana_clientes)
    boton_clientes.pack(side="left", padx=10, pady=10)

    boton_remitos = tkinter.Button(encabezado, text="Remitos")
    boton_remitos.pack(side="left", padx=10, pady=10)

    # Frame principal
    frame1 = tkinter.Frame(ventana, bg="white", bd=5)
    frame1.pack(fill="both", expand=True)

    ventana.mainloop()

# Incio del programa
if __name__ == "__main__":
    test()