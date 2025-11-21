import tkinter as tk
color_oscuro = "#2B303A"
color_claro = "#EEE5E9"


def centrar_ventana(ventana, aplicacion_ancho, aplicacion_alto):
    ancho = ventana.winfo_screenwidth()
    alto = ventana.winfo_screenheight()
    x = int(ancho / 2) - int(aplicacion_ancho / 2)
    y = int(alto / 2) - int(aplicacion_alto / 2) - 40 # Resto 40 para que quede mas arriba
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")


def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    ventana_login.resizable(False, False)
    # Llamo a la funcion que deja centrada la ventana
    centrar_ventana(ventana_login, 960, 600)

    frame_imagen_izquierda = tk.Frame(ventana_login, bg=color_oscuro)
    frame_imagen_izquierda.place(x=0, y=0, relwidth=0.6, relheight=1)

    frame_login_derecha = tk.Frame(ventana_login, bg=color_claro)
    frame_login_derecha.place(relx=0.6, y=0, relwidth=0.4, relheight=1)

    ventana_login.mainloop()

mostrar_login()