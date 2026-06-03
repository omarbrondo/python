import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

ventana = ctk.CTk()
ventana.geometry("600x400")
ventana.title('Mi primera ventana')

#manejo del grid

boton1 = ttk.Button(ventana, text="Botón 1")
boton2 = ttk.Button(ventana, text="Botón 2")
boton3 = ttk.Button(ventana, text="Botón 3")

boton1.grid(row=0, column=0, sticky="nsew")
boton2.grid(row=1, column=1, sticky="ns")
boton3.grid(row=2, column=2, sticky="nsew")

ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=10)
ventana.columnconfigure(2, weight=1)


ventana.mainloop()