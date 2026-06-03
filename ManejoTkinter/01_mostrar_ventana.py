import tkinter as tk

ventana = tk.Tk()
ventana.geometry("600x400")

ventana.title('Mi primera ventana')

ventana.resizable(0, 0)

ventana.config(bg='lightblue')

ventana.configure(background='lightblue')

ventana.mainloop()