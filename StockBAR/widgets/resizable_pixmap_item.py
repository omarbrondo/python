from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QRectF

class ResizablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap: QPixmap):
        super().__init__(pixmap)
        self.original_pixmap = pixmap
        self.base_width = pixmap.width()
        self.base_height = pixmap.height()

    def resize_pixmap(self, scale_x: float, scale_y: float):
        new_w = max(1, int(self.base_width * scale_x))
        new_h = max(1, int(self.base_height * scale_y))
        scaled = self.original_pixmap.scaled(new_w, new_h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled)

    def boundingRect(self) -> QRectF:
        return super().boundingRect()
