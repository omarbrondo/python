from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QRectF

class ResizablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap: QPixmap):
        super().__init__(pixmap)
        self.original_pixmap = pixmap
        self.base_width = pixmap.width()
        self.base_height = pixmap.height()

    def resize_pixmap(self, scale_x: float, scale_y: float, keep_aspect: bool = True):
        if keep_aspect:
            # usar la escala promedio para mantener proporción
            scale = (scale_x + scale_y) / 2.0
            new_w = max(1, int(self.base_width * scale))
            new_h = max(1, int(self.base_height * scale))
            scaled = self.original_pixmap.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            new_w = max(1, int(self.base_width * scale_x))
            new_h = max(1, int(self.base_height * scale_y))
            scaled = self.original_pixmap.scaled(new_w, new_h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        self.setPixmap(scaled)

    def boundingRect(self) -> QRectF:
        return super().boundingRect()
