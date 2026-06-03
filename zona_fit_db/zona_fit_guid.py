import customtkinter as ctk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from cliente_dao import ClienteDAO
from cliente import Cliente

ctk.set_appearance_mode("dark")      # "dark", "light" o "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class App(ctk.CTk):
    COLOR_FONDO = "#1d2d44"

    def __init__(self):
        super().__init__()
        self.id_cliente = None

        self.configurar_ventana()
        self.configurar_grid()
        self.mostrar_titulo()
        self.mostrar_formulario()
        self.crear_tabla()
        self.cargar_datos_tabla()
        self.mostrar_botones()

    # ---------------- VENTANA Y LAYOUT ----------------

    def configurar_ventana(self):
        self.title("Zona Fit APP")
        self.geometry("900x550")
        self.configure(fg_color=App.COLOR_FONDO)

    def configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

    def mostrar_titulo(self):
        titulo = ctk.CTkLabel(
            self,
            text="Zona Fit APP",
            font=("Arial", 28, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=15)

    # ---------------- FORMULARIO ----------------

    def mostrar_formulario(self):
        self.frame_form = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color="transparent"
        )
        self.frame_form.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        ctk.CTkLabel(self.frame_form, text="Nombre").grid(
            row=0, column=0, pady=10, sticky="w"
        )
        self.nombre_text = ctk.CTkEntry(self.frame_form, width=200)
        self.nombre_text.grid(row=0, column=1, pady=10, padx=5)

        ctk.CTkLabel(self.frame_form, text="Apellido").grid(
            row=1, column=0, pady=10, sticky="w"
        )
        self.apellido_text = ctk.CTkEntry(self.frame_form, width=200)
        self.apellido_text.grid(row=1, column=1, pady=10, padx=5)

        ctk.CTkLabel(self.frame_form, text="Membresía").grid(
            row=2, column=0, pady=10, sticky="w"
        )
        self.membresia_text = ctk.CTkEntry(self.frame_form, width=200)
        self.membresia_text.grid(row=2, column=1, pady=10, padx=5)

    # ---------------- TABLA ----------------

    def crear_tabla(self):
        self.frame_tabla = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color="transparent"
        )
        self.frame_tabla.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            font=("Arial", 14),
            rowheight=32,
            background=App.COLOR_FONDO,
            foreground="white",
            fieldbackground=App.COLOR_FONDO,
            bordercolor=App.COLOR_FONDO,
            borderwidth=0
        )
        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 15, "bold"),
            background="#0b3b5c",
            foreground="white",
            bordercolor=App.COLOR_FONDO,
            borderwidth=0
        )
        estilo.map(
            "Treeview",
            background=[("selected", "#0a9396")],
            foreground=[("selected", "white")]
        )

        estilo.configure(
            "Vertical.TScrollbar",
            background=App.COLOR_FONDO,
            troughcolor=App.COLOR_FONDO,
            bordercolor=App.COLOR_FONDO,
            arrowcolor=App.COLOR_FONDO
        )

        columnas = ("ID", "Nombre", "Apellido", "Membresía")
        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=columnas,
            show="headings",
            height=12
        )
        self.tabla.grid(row=0, column=0, sticky="nsew")

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=120)

        scrollbar = ttk.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla.yview,
            style="Vertical.TScrollbar"
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.bind("<<TreeviewSelect>>", self.cargar_cliente)

    def cargar_datos_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        clientes = ClienteDAO.seleccionar()
        for c in clientes:
            self.tabla.insert(
                "",
                "end",
                values=(c.id, c.nombre, c.apellido, c.membresia)
            )

    # ---------------- BOTONES ----------------

    def mostrar_botones(self):
        self.frame_botones = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color="transparent"
        )
        self.frame_botones.grid(row=2, column=0, columnspan=2, pady=15)

        ctk.CTkButton(
            self.frame_botones,
            text="Guardar",
            width=140,
            command=self.validar_cliente
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            self.frame_botones,
            text="Eliminar",
            width=140,
            fg_color="#bb3e03",
            hover_color="#ae2012",
            command=self.eliminar_cliente
        ).grid(row=0, column=1, padx=20)

        ctk.CTkButton(
            self.frame_botones,
            text="Limpiar",
            width=140,
            command=self.limpiar_formulario
        ).grid(row=0, column=2, padx=20)

    # ---------------- LÓGICA CRUD ----------------

    def validar_cliente(self):
        if not (self.nombre_text.get() and self.apellido_text.get() and self.membresia_text.get()):
            showerror("Error", "Todos los campos son obligatorios.")
            self.nombre_text.focus()
            return

        if not self.membresia_text.get().isdigit():
            showerror("Error", "La membresía debe ser un número entero.")
            self.membresia_text.delete(0, "end")
            self.membresia_text.focus()
            return

        self.guardar_cliente()

    def guardar_cliente(self):
        nombre = self.nombre_text.get()
        apellido = self.apellido_text.get()
        membresia = self.membresia_text.get()

        if self.id_cliente is None:
            cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)
            ClienteDAO.insertar(cliente)
            showinfo("Éxito", "Cliente guardado exitosamente.")
        else:
            cliente = Cliente(id=self.id_cliente, nombre=nombre,
                              apellido=apellido, membresia=membresia)
            ClienteDAO.actualizar(cliente)
            showinfo("Éxito", "Cliente actualizado exitosamente.")

        self.cargar_datos_tabla()
        self.limpiar_formulario()

    def cargar_cliente(self, event):
        if not self.tabla.selection():
            return

        item = self.tabla.selection()[0]
        datos = self.tabla.item(item)["values"]

        self.id_cliente = datos[0]

        self.nombre_text.delete(0, "end")
        self.apellido_text.delete(0, "end")
        self.membresia_text.delete(0, "end")

        self.nombre_text.insert(0, datos[1])
        self.apellido_text.insert(0, datos[2])
        self.membresia_text.insert(0, datos[3])

    def eliminar_cliente(self):
        if self.id_cliente is None:
            showerror("Error", "Seleccione un cliente para eliminar.")
            return

        ClienteDAO.eliminar(Cliente(id=self.id_cliente))
        showinfo("Éxito", "Cliente eliminado exitosamente.")
        self.cargar_datos_tabla()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.id_cliente = None
        self.nombre_text.delete(0, "end")
        self.apellido_text.delete(0, "end")
        self.membresia_text.delete(0, "end")
        self.nombre_text.focus()


if __name__ == "__main__":
    app = App()
    app.mainloop()
