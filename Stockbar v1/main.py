import sys
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QFormLayout, QLineEdit, QSpinBox, 
    QPushButton, QGroupBox, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsPixmapItem
)
from PySide6.QtGui import QBrush, QPen, QColor, QFont, QPainter, QImage, QPixmap
from PySide6.QtCore import Qt

# --- NUEVA CLASE: Canvas Personalizado para escalar y rotar ---
class CustomGraphicsView(QGraphicsView):
    def wheelEvent(self, event):
        # Si hay elementos seleccionados, cambiamos su tamaño con la rueda del ratón
        if self.scene() and self.scene().selectedItems():
            factor = 1.1 if event.angleDelta().y() > 0 else 0.9
            for item in self.scene().selectedItems():
                item.setTransformOriginPoint(item.boundingRect().center())
                item.setScale(item.scale() * factor)
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        # Controles de teclado para elementos seleccionados
        if self.scene() and self.scene().selectedItems():
            if event.key() == Qt.Key_R:
                # Rotar 15 grados con la tecla 'R'
                for item in self.scene().selectedItems():
                    item.setTransformOriginPoint(item.boundingRect().center())
                    item.setRotation(item.rotation() + 15)
            elif event.key() == Qt.Key_Delete:
                # Eliminar el elemento con la tecla 'Supr' o 'Delete'
                for item in self.scene().selectedItems():
                    self.scene().removeItem(item)
        super().keyPressEvent(event)

class StockBarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StockBAR - Creador de Etiquetas")
        self.resize(1024, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- PANEL IZQUIERDO ---
        left_panel = QGroupBox("Datos del Artículo")
        left_panel.setFixedWidth(300)
        form_layout = QFormLayout(left_panel)

        self.input_code = QLineEdit()
        self.input_desc = QLineEdit()
        self.input_qty = QSpinBox()
        self.input_qty.setMinimum(1)

        btn_generate = QPushButton("Actualizar Vista Preliminar")
        btn_generate.clicked.connect(self.update_preview)

        form_layout.addRow("Código:", self.input_code)
        form_layout.addRow("Descripción:", self.input_desc)
        form_layout.addRow("Cantidad:", self.input_qty)
        form_layout.addRow(btn_generate)

        # --- PANEL DERECHO ---
        right_panel = QGroupBox("Vista Preliminar de la etiqueta")
        canvas_layout = QVBoxLayout(right_panel)
        
        self.scene = QGraphicsScene()
        # Usamos nuestra nueva vista personalizada
        self.canvas_view = CustomGraphicsView(self.scene)
        self.canvas_view.setRenderHint(QPainter.Antialiasing)
        canvas_layout.addWidget(self.canvas_view)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

    def update_preview(self):
        self.scene.clear()

        # Fondo de la etiqueta
        label_bg = QGraphicsRectItem(0, 0, 400, 200)
        label_bg.setBrush(QBrush(QColor("white")))
        label_bg.setPen(QPen(Qt.black))
        self.scene.addItem(label_bg)

        # Textos
        def create_interactive_text(text, font, x, y):
            item = QGraphicsTextItem(text)
            item.setFont(font)
            item.setDefaultTextColor(QColor("black"))
            item.setPos(x, y)
            item.setFlag(QGraphicsTextItem.ItemIsSelectable, True)
            item.setFlag(QGraphicsTextItem.ItemIsMovable, True)
            self.scene.addItem(item)
            return item

        create_interactive_text(f"Código: {self.input_code.text()}", QFont("Arial", 14, QFont.Bold), 20, 20)
        create_interactive_text(f"{self.input_desc.text()}", QFont("Arial", 12), 20, 50)
        create_interactive_text(f"Cant: {self.input_qty.value()}", QFont("Arial", 12), 20, 80)

        # --- GENERACIÓN DEL CÓDIGO DE BARRAS ---
        code_value = self.input_code.text()
        if code_value: # Solo generamos si hay texto
            try:
                # Usamos Code128, guardamos en memoria (BytesIO) para no crear archivos temporales
                code128 = barcode.get('code128', code_value, writer=ImageWriter())
                fp = BytesIO()
                code128.write(fp)
                fp.seek(0)
                
                # Convertimos la imagen generada a un formato que PySide entienda
                image = QImage.fromData(fp.read())
                pixmap = QPixmap.fromImage(image)
                
                # Creamos el elemento gráfico para la imagen
                barcode_item = QGraphicsPixmapItem(pixmap)
                barcode_item.setFlag(QGraphicsPixmapItem.ItemIsSelectable, True)
                barcode_item.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)
                
                # Achicamos un poco el código de barras por defecto para que entre bien
                barcode_item.setScale(0.5) 
                barcode_item.setPos(20, 110)
                
                self.scene.addItem(barcode_item)
            except Exception as e:
                print(f"No se pudo generar el código: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockBarApp()
    window.show()
    sys.exit(app.exec())