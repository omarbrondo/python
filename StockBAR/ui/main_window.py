from PySide6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFormLayout, QFrame,
    QRadioButton, QComboBox, QGroupBox, QFileDialog, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from widgets.preview_area import PreviewArea


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StockBAR - Generador de Etiquetas")
        self.setMinimumSize(1000, 700) 

        # =====================================================================
        # ESTILOS GLOBALES (QSS) - Dark/Grey Mode Profesional
        # =====================================================================
        self.setStyleSheet("""
            /* Fondo general de la ventana (Gris oscuro, no te deja ciego) */
            QMainWindow {
                background-color: #2B2B2B;
            }

            /* Estilo general para todos los textos */
            QWidget {
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
                font-size: 14px;
                color: #E0E0E0;
            }

            /* Contenedores tipo tarjeta gris */
            #CardPanel {
                background-color: #363636;
                border-radius: 12px;
                border: 1px solid #4D4D4D;
            }

            /* Ventanas de aviso (QMessageBox) grises en lugar de negras */
            QMessageBox {
                background-color: #3A3A3A;
                border: 1px solid #555555;
            }
            QMessageBox QLabel {
                color: #E0E0E0;
            }

            /* Campos de texto (Inputs) */
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #555555;
                border-radius: 6px;
                background-color: #222222;
                color: #FFFFFF;
                selection-background-color: #0078D4;
            }
            QLineEdit:focus {
                border: 1px solid #0078D4;
                background-color: #1A1A1A;
            }

            /* Menú desplegable */
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #555555;
                border-radius: 6px;
                background-color: #222222;
                color: #FFFFFF;
            }
            QComboBox:hover {
                border: 1px solid #0078D4;
            }
            QComboBox QAbstractItemView {
                background-color: #363636;
                color: #E0E0E0;
                selection-background-color: #0078D4;
            }

            /* Botones principales (Azul corporativo intacto) */
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QPushButton:pressed {
                background-color: #004578;
            }

            /* Botón secundario (Examinar imagen) */
            QPushButton#SecondaryButton {
                background-color: #555555;
                color: #FFFFFF;
                font-weight: normal;
            }
            QPushButton#SecondaryButton:hover {
                background-color: #666666;
            }

            /* GroupBox (Caja de tamaño de etiqueta) */
            QGroupBox {
                font-weight: bold;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                left: 10px;
                color: #CCCCCC;
            }

            /* Botones de radio */
            QRadioButton {
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }

            /* RECUPERAR Y ESTILIZAR BARRAS DE DESPLAZAMIENTO DEL CANVAS */
            QScrollBar:horizontal {
                border: none;
                background: #2B2B2B;
                height: 14px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #555555;
                min-width: 20px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #777777;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #2B2B2B;
                width: 14px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # --- Panel de selección de tamaño ---
        size_group = QGroupBox("Tamaño de etiqueta")
        size_layout = QVBoxLayout()
        size_layout.setSpacing(10)
        size_layout.setContentsMargins(15, 20, 15, 15)

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

        # Armar layout del groupbox
        size_layout.addWidget(self.radio_predef)
        size_layout.addWidget(self.combo_predef)
        size_layout.addSpacing(10)
        size_layout.addWidget(self.radio_custom)
        
        # Layout horizontal para los campos de ancho y alto
        dimensions_layout = QHBoxLayout()
        dimensions_layout.addWidget(self.input_ancho)
        dimensions_layout.addWidget(QLabel("x"))
        dimensions_layout.addWidget(self.input_alto)
        size_layout.addLayout(dimensions_layout)
        
        size_layout.addSpacing(10)
        size_layout.addWidget(btn_crear)

        size_group.setLayout(size_layout)

        # --- Layout principal ---
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Panel izquierdo: formulario (Con estilo de Tarjeta oscura) ---
        left_panel = QWidget()
        left_panel.setObjectName("CardPanel") 
        
        # Layout interno del panel izquierdo
        left_inner_layout = QVBoxLayout(left_panel)
        left_inner_layout.setContentsMargins(20, 20, 20, 20)
        left_inner_layout.setSpacing(15)

        # Formulario de datos
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Ej: 779123456789")
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setPlaceholderText("Nombre del producto")
        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Ej: 10")

        # Agregar el GroupBox primero
        left_inner_layout.addWidget(size_group)
        
        # Línea divisoria sutil
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #4D4D4D;")
        left_inner_layout.addWidget(line)

        # Agregar campos al formulario
        form_layout.addRow(QLabel("Código:"), self.input_codigo)
        form_layout.addRow(QLabel("Descripción:"), self.input_descripcion)
        form_layout.addRow(QLabel("Cantidad:"), self.input_cantidad)
        
        left_inner_layout.addLayout(form_layout)

        # Botones de acción del formulario
        btn_generar = QPushButton("Actualizar Vista Previa")
        btn_generar.clicked.connect(self.update_preview)
        left_inner_layout.addWidget(btn_generar)

        # Botón para agregar una imagen
        btn_imagen = QPushButton("Examinar imagen...")
        btn_imagen.setObjectName("SecondaryButton") 
        btn_imagen.clicked.connect(self.agregar_imagen)
        left_inner_layout.addWidget(btn_imagen)
        
        # Empujar todo hacia arriba
        left_inner_layout.addStretch()

        # Presionar Enter en cualquiera de los campos de texto
        self.input_codigo.returnPressed.connect(self.update_preview)
        self.input_descripcion.returnPressed.connect(self.update_preview)
        self.input_cantidad.returnPressed.connect(self.update_preview)

        left_panel.setMaximumWidth(380)
        left_panel.setMinimumWidth(320)

        # --- Panel derecho: vista previa ---
        self.preview = PreviewArea()
        # NOTA: Se quitó el objectName("CardPanel") acá para no romper las barras de desplazamiento

        # Obtener el panel de propiedades desde PreviewArea
        self.properties_widget = self.preview.properties_panel
        self.properties_widget.setObjectName("CardPanel")
        self.properties_widget.setMinimumWidth(250)
        self.properties_widget.setMaximumWidth(360)

        # --- Agregar al layout principal en el orden: formulario | propiedades | preview ---
        main_layout.addWidget(left_panel, 0)
        main_layout.addWidget(self.properties_widget, 0)
        main_layout.addWidget(self.preview, 1)

        self.setCentralWidget(main_widget)

    def crear_etiqueta(self):
        MM_TO_PX = 8

        try:
            if self.radio_predef.isChecked():
                texto = self.combo_predef.currentText()
                parts = texto.split("x")
                ancho_mm = int(parts[0].strip())
                alto_mm = int(parts[1].replace("mm", "").strip())
            else:
                ancho_mm = int(self.input_ancho.text())
                alto_mm = int(self.input_alto.text())
        except Exception:
            ancho_mm, alto_mm = 80, 50

        ancho_px = ancho_mm * MM_TO_PX
        alto_px = alto_mm * MM_TO_PX

        self.preview.create_label(ancho_px, alto_px)

    def update_preview(self):
        if not self.preview.label_item:
            QMessageBox.information(self, "Aviso", "Primero creá una etiqueta desde el panel de tamaño.")
            return

        codigo = self.input_codigo.text()
        descripcion = self.input_descripcion.text()
        cantidad = self.input_cantidad.text()

        for item in list(self.preview.label_item.items):
            if getattr(item, "is_custom_image", False):
                continue
            scene = self.preview.label_item.scene()
            if scene:
                scene.removeItem(item)
            self.preview.label_item.items.remove(item)

        self.preview.add_resizable_text(f"Código: {codigo}", 10, 10)
        self.preview.add_resizable_text(f"Descripción: {descripcion}", 10, 40)
        self.preview.add_resizable_text(f"Cantidad: {cantidad}", 10, 70)

        pixmap = self.preview.generate_barcode_pixmap(codigo)
        self.preview.add_resizable_barcode(pixmap, 10, 120)

    def agregar_imagen(self):
        if not self.preview.label_item:
            QMessageBox.warning(self, "Atención", "Primero creá una etiqueta.")
            return

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen",
            "",
            "Imágenes (*.jpg *.jpeg *.png);;Todos los archivos (*)"
        )
        if not filepath:
            return

        pixmap = QPixmap(filepath)
        if pixmap.isNull():
            QMessageBox.warning(self, "Error", "No se pudo cargar la imagen seleccionada.")
            return

        wrapper = self.preview.add_resizable_image(pixmap, 10, 170)
        if wrapper is not None:
            wrapper.is_custom_image = True