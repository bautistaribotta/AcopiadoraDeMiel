import tkinter as tk


def centrar_ventana(ventana, aplicacion_ancho, aplicacion_alto):
    ancho = ventana.winfo_screenwidth()
    alto = ventana.winfo_screenheight()
    x = int(ancho / 2) - int(aplicacion_ancho / 2)
    y = int(alto / 2) - int(aplicacion_alto / 2) - 40
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")


def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    ventana_login.resizable(False, False)
    centrar_ventana(ventana_login, 960, 600)

    # --- FRAME IZQUIERDO (Imagen/Color) ---
    frame_izq = tk.Frame(ventana_login, bg="#3b5998")  # Azul estilo Facebook
    frame_izq.place(x=0, y=0, relwidth=0.6, relheight=1)

    # --- FRAME DERECHO (Formulario) ---
    frame_der = tk.Frame(ventana_login, bg="white")
    frame_der.place(relx=0.6, y=0, relwidth=0.4, relheight=1)

    # Titulo
    titulo = tk.Label(frame_der, text="Bienvenido", font=("Arial", 24, "bold"), bg="white", fg="#333")
    titulo.pack(pady=(80, 20))  # 80px arriba, 20px abajo

    # Usuario
    lbl_user = tk.Label(frame_der, text="Usuario:", font=("Arial", 12), bg="white", fg="#555")
    lbl_user.pack(pady=5)

    inp_user = tk.Entry(frame_der, font=("Arial", 12), width=30, bd=2, relief="groove")
    inp_user.pack(pady=5)

    # Contraseña
    lbl_pass = tk.Label(frame_der, text="Contraseña:", font=("Arial", 12), bg="white", fg="#555")
    lbl_pass.pack(pady=5)

    inp_pass = tk.Entry(frame_der, font=("Arial", 12), width=30, bd=2, relief="groove", show="*")
    inp_pass.pack(pady=5)

    # Boton
    btn_login = tk.Button(frame_der, text="Iniciar Sesión", font=("Arial", 12, "bold"), bg="#3b5998", fg="white",
                          width=25, cursor="hand2")
    btn_login.pack(pady=30)

    ventana_login.mainloop()


mostrar_login()