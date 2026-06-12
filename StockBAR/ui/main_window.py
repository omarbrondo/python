from PySide6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFormLayout, QFrame,
    QRadioButton, QComboBox, QGroupBox
)

from widgets.preview_area import PreviewArea


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StockBAR - Generador de Etiquetas")
        self.setMinimumSize(900, 600)

        # --- Panel de selección de tamaño ---
        size_group = QGroupBox("Tamaño de etiqueta")
        size_layout = QVBoxLayout()

        # Radio: predefinido
        self.radio_predef = QRadioButton("Usar tamaño predefinido")
        self.radio_predef.setChecked(True)

        self.combo_predef = QComboBox()
        self.combo_predef.addItems([
            "80 x 50 mm",
            "58 x 40 mm",
            "50 x 25 mm",
            "100 x 70 mm"
        ])

        # Radio: personalizado
        self.radio_custom = QRadioButton("Usar tamaño personalizado")

        self.input_ancho = QLineEdit()
        self.input_ancho.setPlaceholderText("Ancho (mm)")
        self.input_alto = QLineEdit()
        self.input_alto.setPlaceholderText("Alto (mm)")

        # Botón crear etiqueta
        btn_crear = QPushButton("Crear etiqueta")
        btn_crear.clicked.connect(self.crear_etiqueta)

        # Armar layout
        size_layout.addWidget(self.radio_predef)
        size_layout.addWidget(self.combo_predef)
        size_layout.addWidget(self.radio_custom)
        size_layout.addWidget(QLabel("Ancho (mm):"))
        size_layout.addWidget(self.input_ancho)
        size_layout.addWidget(QLabel("Alto (mm):"))
        size_layout.addWidget(self.input_alto)
        size_layout.addWidget(btn_crear)

        size_group.setLayout(size_layout)

        # --- Layout principal ---
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # --- Panel izquierdo: formulario ---
        form_layout = QFormLayout()

        self.input_codigo = QLineEdit()
        self.input_descripcion = QLineEdit()
        self.input_cantidad = QLineEdit()

        form_layout.addRow(size_group)
        form_layout.addRow("Código:", self.input_codigo)
        form_layout.addRow("Descripción:", self.input_descripcion)
        form_layout.addRow("Cantidad:", self.input_cantidad)

        btn_generar = QPushButton("Actualizar Vista Previa")
        form_layout.addRow(btn_generar)
        btn_generar.clicked.connect(self.update_preview)

        # Presionar Enter en cualquiera de los campos de texto ejecuta la
        # misma acción que el botón "Actualizar Vista Previa"
        self.input_codigo.returnPressed.connect(self.update_preview)
        self.input_descripcion.returnPressed.connect(self.update_preview)
        self.input_cantidad.returnPressed.connect(self.update_preview)

        left_panel = QWidget()
        left_panel.setLayout(form_layout)
        left_panel.setMaximumWidth(350)
        left_panel.setMinimumWidth(250)

        # --- Panel derecho: vista previa ---
        self.preview = PreviewArea()

        # Obtener el panel de propiedades desde PreviewArea (ya creado dentro de PreviewArea)
        self.properties_widget = self.preview.properties_panel
        # Ajustes de ancho del panel de propiedades (centro)
        self.properties_widget.setMinimumWidth(220)
        self.properties_widget.setMaximumWidth(360)

        # --- Agregar al layout principal en el orden: formulario | propiedades | preview ---
        main_layout.addWidget(left_panel, 0)               # izquierda: formulario
        main_layout.addWidget(self.properties_widget, 0)   # centro: panel de propiedades
        main_layout.addWidget(self.preview, 1)             # derecha: preview (ocupa resto)

        self.setCentralWidget(main_widget)

    def crear_etiqueta(self):
        MM_TO_PX = 8

        try:
            if self.radio_predef.isChecked():
                texto = self.combo_predef.currentText()
                # texto ejemplo: "80 x 50 mm"
                parts = texto.split("x")
                ancho_mm = int(parts[0].strip())
                alto_mm = int(parts[1].replace("mm", "").strip())
            else:
                ancho_mm = int(self.input_ancho.text())
                alto_mm = int(self.input_alto.text())
        except Exception:
            # valores por defecto si hay error de parseo
            ancho_mm, alto_mm = 80, 50

        ancho_px = ancho_mm * MM_TO_PX
        alto_px = alto_mm * MM_TO_PX

        self.preview.create_label(ancho_px, alto_px)

    def update_preview(self):
        if not self.preview.label_item:
            print("Primero creá una etiqueta.")
            return

        codigo = self.input_codigo.text()
        descripcion = self.input_descripcion.text()
        cantidad = self.input_cantidad.text()

        # Limpiar elementos anteriores (son wrappers ResizableItem)
        # Usamos una copia de la lista porque la removemos durante la iteración
        for item in list(self.preview.label_item.items):
            # item es el wrapper (ResizableItem); remover de la escena
            scene = self.preview.label_item.scene()
            if scene:
                scene.removeItem(item)

        self.preview.label_item.items.clear()

        # Agregar texto (resizable)
        self.preview.add_resizable_text(f"Código: {codigo}", 10, 10)
        self.preview.add_resizable_text(f"Descripción: {descripcion}", 10, 40)
        self.preview.add_resizable_text(f"Cantidad: {cantidad}", 10, 70)

        # Agregar código de barras (resizable)
        pixmap = self.preview.generate_barcode_pixmap(codigo)
        self.preview.add_resizable_barcode(pixmap, 10, 120)