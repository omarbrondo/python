import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.geometry("600x400")

ventana.title('Mi primera ventana')

def saludar(nombre):
    print(f"¡Hola, {nombre}!")

boton1 = ttk.Button(ventana, text="Botón 1", command=lambda: saludar('Omar'))
boton1.pack(pady=20)

ventana.mainloop()