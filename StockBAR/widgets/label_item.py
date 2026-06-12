from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtCore import Qt

from widgets.resizable_text_item import ResizableTextItem
from widgets.resizable_pixmap_item import ResizablePixmapItem


# Rectángulo base de la etiqueta.
# Actúa como contenedor visual donde se colocan el texto, la barra y otras imágenes.
class LabelItem(QGraphicsRectItem):
    def __init__(self, width_px, height_px):
        # Crea el rectángulo base de la etiqueta con dimensiones en píxeles.
        super().__init__(0, 0, width_px, height_px)
        self.setPen(QPen(QColor("#444"), 2))
        self.setBrush(QBrush(Qt.white))
        self.items = []

    def add_text(self, text, x, y):
        # Añade un texto dentro del rectángulo de la etiqueta.
        item = ResizableTextItem(text)
        item.setBrush(QBrush(Qt.black))
        item.setParentItem(self)
        item.setPos(x, y)
        return item