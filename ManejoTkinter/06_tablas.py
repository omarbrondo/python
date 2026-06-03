import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.geometry("700x450")
ventana.title("Manejo de tablas")

# Frame principal
frame = ctk.CTkFrame(ventana)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Estilos del Treeview
estilos = ttk.Style()
estilos.theme_use("clam")
estilos.configure("Treeview",
                  background="#2b2b2b",
                  foreground="white",
                  fieldbackground="#2b2b2b",
                  rowheight=28,
                  font=("Arial", 12))
estilos.map("Treeview",
            background=[("selected", "#00cc5f")],
            foreground=[("selected", "white")])

columnas = ("Id", "Nombre", "Edad")

tabla = ttk.Treeview(frame, columns=columnas, show="headings")
tabla.pack(side="left", fill="both", expand=True)

# Cabeceras
tabla.heading("Id", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Edad", text="Edad")

# Columnas
tabla.column("Id", width=50, anchor="center")
tabla.column("Nombre", width=200, anchor="center")
tabla.column("Edad", width=200, anchor="center")

# Datos
datos = [
    ("1", "Juan", "25"),
    ("2", "María", "30"),
    ("3", "Pedro", "35")
] * 5

for fila in datos:
    tabla.insert("", ctk.END, values=fila)

# Scrollbar CTk
scrollbar = ctk.CTkScrollbar(frame, command=tabla.yview)
scrollbar.pack(side="right", fill="y")
tabla.configure(yscrollcommand=scrollbar.set)

# Evento selección
def mostrar_registro(event):
    item = tabla.selection()[0]
    valores = tabla.item(item)["values"]
    CTkMessagebox(title="Registro seleccionado",
                  message=f"ID: {valores[0]}\nNombre: {valores[1]}\nEdad: {valores[2]}",
                  icon="info")

tabla.bind("<<TreeviewSelect>>", mostrar_registro)

ventana.mainloop()
