import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

ventana = ctk.CTk()
ventana.geometry("600x400")
ventana.title('Mi primera ventana')

def mostrar():
    contenido = caja_texto.get()
    print(f"Contenido de la caja de texto: {contenido}")
    etiqueta.configure(text=f"Has escrito: {contenido}")

caja_texto = ctk.CTkEntry(ventana, font=('Arial', 14))
caja_texto.pack(pady=20)

boton = ctk.CTkButton(ventana, text="Enviar", command=mostrar)
boton.pack(pady=20)

etiqueta = ctk.CTkLabel(ventana, text="Escribe algo en la caja de texto y presiona el botón", font=('Arial', 12))
etiqueta.pack(pady=20)

ventana.mainloop()
