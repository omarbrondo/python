import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configurar_ventana()
        self.configurar_grid()
        self.mostrar_tabla()

    def configurar_ventana(self):
        self.geometry("600x400")
        self.configure(background='#1d2d44')
        self.title("Manejo de Ventanas con POO")

    def configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def mostrar_tabla(self):
        estilos = ttk.Style()
        estilos.theme_use("clam")
        estilos.configure("Treeview",
                          background="#1d2d44",
                          foreground="white",
                          fieldbackground="#1d2d44")
        estilos.map("Treeview",
                    background=[("selected", "#4a6fa5")],
                    foreground=[("selected", "white")])

        columnas = ("ID", "Nombre", "Edad")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Edad", text="Edad")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Nombre", width=200, anchor="center")
        self.tabla.column("Edad", width=100, anchor="center")

        datos = [
            ("1", "Juan", "25"),
            ("2", "María", "30"),
            ("3", "Pedro", "35")
        ] * 5

        for fila in datos:
            self.tabla.insert("", "end", values=fila)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, command=self.tabla.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        # 👉 Aquí sí va el grid
        self.tabla.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # 👉 Aquí sí va el bind
        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_registro_seleccionado)

    def mostrar_registro_seleccionado(self, event):
        item = self.tabla.selection()[0]
        valores = self.tabla.item(item)["values"]

        showinfo(
            title="Registro seleccionado",
            message=f"ID: {valores[0]}\nNombre: {valores[1]}\nEdad: {valores[2]}"
        )

if __name__ == "__main__":
    app = App()
    app.mainloop()
