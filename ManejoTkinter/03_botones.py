import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.geometry("600x400")

ventana.title('Mi primera ventana')


etiqueta = ttk.Label(ventana, text="¡Hola, Mundo!")
etiqueta.pack(pady=20)

#cambiar el texto usando configure

etiqueta.configure(text="¡Hola, Tkinter!")

# cambiar el texto usando la llave text

etiqueta['text'] = "¡Hola, Python!"

ventana.mainloop()