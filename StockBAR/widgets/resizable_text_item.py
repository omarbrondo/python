from PySide6.QtWidgets import QGraphicsTextItem
from PySide6.QtGui import QFont
from PySide6.QtCore import QRectF, Qt

class ResizableTextItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.font_family = "Arial"
        self.base_font_size = 14
        self.setFont(QFont(self.font_family, self.base_font_size))
        # Color por defecto (asegura que se vea sobre fondo blanco)
        self.setDefaultTextColor(Qt.black)
        # Forzar layout inicial y guardar ancho base
        self.document().adjustSize()
        self.base_width = self.document().size().width()
        # Asegurar que el texto esté por encima de la caja (si hace falta)
        self.setZValue(1)

    def resize_font(self, scale_factor):
        # scale_factor relativo al tamaño base
        new_size = max(6, int(self.base_font_size * scale_factor))
        self.setFont(QFont(self.font_family, new_size))
        # Forzar re-layout para que boundingRect sea correcto
        self.document().adjustSize()

    def boundingRect(self) -> QRectF:
        doc_size = self.document().size()
        return QRectF(0, 0, doc_size.width(), doc_size.height())
