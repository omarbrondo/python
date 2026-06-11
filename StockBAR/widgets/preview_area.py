from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from widgets.label_item import LabelItem
from widgets.resizable_item import ResizableItem

import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io

class PreviewArea(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 800, 600)

        self.label_item = None

    def create_label(self, width_px, height_px):
        if self.label_item:
            self.scene.removeItem(self.label_item)

        self.label_item = LabelItem(width_px, height_px)
        self.label_item.setPos(50, 50)
        self.scene.addItem(self.label_item)

    def generate_barcode_pixmap(self, codigo):
        barcode_class = barcode.get_barcode_class("code128")
        barcode_obj = barcode_class(codigo, writer=ImageWriter())

        buffer = io.BytesIO()
        barcode_obj.write(buffer)
        buffer.seek(0)

        pil_image = Image.open(buffer).convert("RGB")
        data = pil_image.tobytes("raw", "RGB")
        qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGB888)

        return QPixmap.fromImage(qimage)

    def add_resizable_text(self, text, x, y):
        # crear item (parent será label_item temporalmente)
        item = self.label_item.add_text(text, x, y)
        # envolver en ResizableItem (esto reparenta el child al wrapper)
        wrapper = ResizableItem(item)
        # parentear el wrapper al label_item para que quede dentro del rectángulo
        wrapper.setParentItem(self.label_item)
        # agregar wrapper a la lista de items (para limpiar luego)
        self.label_item.items.append(wrapper)

    def add_resizable_barcode(self, pixmap, x, y):
        item = self.label_item.add_barcode(pixmap, x, y)
        wrapper = ResizableItem(item)
        wrapper.setParentItem(self.label_item)
        self.label_item.items.append(wrapper)
