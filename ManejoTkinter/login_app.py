# pyrefly: ignore [missing-import]
import customtkinter as ctk
# pyrefly: ignore [missing-import]
from CTkMessagebox import CTkMessagebox
import subprocess   # 👉 IMPORTANTE para ejecutar otro archivo

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.geometry("400x300")
ventana.title("Login")

def login():
    usuario = usuario_entry.get()
    password = password_entry.get()

    if usuario == "admin" and password == "1234":
        CTkMessagebox(title="Login", message="¡Login exitoso!", icon="check")

        # 👉 Ejecutar el archivo de crud_gui.py
        subprocess.Popen(["python", "zona_fit_db/crud_gui.py"])


        # 👉 Cerrar la ventana de login
        ventana.destroy()

    elif usuario == "" or password == "":
        CTkMessagebox(title="Login", message="Por favor, complete todos los campos.", icon="info")

    else:
        CTkMessagebox(title="Login", message="Usuario o contraseña incorrectos.", icon="warning")

# 👉 Permitir Enter para iniciar sesión
ventana.bind("<Return>", lambda event: login())

frame = ctk.CTkFrame(ventana)
frame.pack(pady=40, padx=40, fill="both", expand=True)

titulo = ctk.CTkLabel(frame, text="Login", font=("Arial", 22))
titulo.pack(pady=10)

usuario_entry = ctk.CTkEntry(frame, placeholder_text="Usuario")
usuario_entry.pack(pady=10, fill="x")

password_entry = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*")
password_entry.pack(pady=10, fill="x")

boton = ctk.CTkButton(frame, text="Iniciar Sesión", command=login)
boton.pack(pady=20)

ventana.mainloop()
