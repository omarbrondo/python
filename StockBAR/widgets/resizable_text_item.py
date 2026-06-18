# widgets/resizable_text_item.py
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsItem
from PySide6.QtGui import QFont, QColor, QTextOption
from PySide6.QtCore import QRectF, Qt


class ResizableTextItem(QGraphicsTextItem):
    """
    QGraphicsTextItem que soporta:
    - base_font_size: tamaño base en puntos (float)
    - resize_font(value): interpreta valores <= 10 como factor relativo y > 10 como tamaño absoluto.
    - set_text_width(px): fija ancho para wrap y recalcula layout.
    """

    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)

        f = self.font() if self.font() else QFont("Arial", 14)
        self.base_font_size = float(f.pointSizeF() if f.pointSizeF() > 0 else 14.0)
        self.setFont(f)

        opt = QTextOption()
        opt.setWrapMode(QTextOption.WordWrap)
        opt.setAlignment(Qt.AlignCenter)
        self.document().setDefaultTextOption(opt)
        self.document().setDefaultFont(self.font())

        self.setPlainText(text)
        self.setDefaultTextColor(QColor("#000000"))
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setTextWidth(0)

    def resize_font(self, value):
        try:
            v = float(value)
        except Exception:
            return

        if v <= 0:
            return

        if v <= 10.0:
            new_pt = max(1.0, self.base_font_size * v)
        else:
            new_pt = max(1.0, v)

        old_font = self.font()
        new_font = QFont(old_font)
        new_font.setPointSizeF(new_pt)

        try:
            self.prepareGeometryChange()
        except Exception:
            pass

        self.setFont(new_font)
        self.document().setDefaultFont(self.font())
        try:
            self.document().adjustSize()
        except Exception:
            pass
        self.base_font_size = float(new_pt)
        self.update()

        parent = self.parentItem()
        if parent is not None:
            try:
                parent.update_handles()
            except Exception:
                pass

        sc = self.scene()
        if sc is not None:
            try:
                sc.update()
            except Exception:
                pass

    def set_text(self, text: str):
        try:
            self.prepareGeometryChange()
        except Exception:
            pass
        self.setPlainText(text)
        try:
            self.document().adjustSize()
        except Exception:
            pass
        self.update()

    def set_text_width(self, px: float):
        try:
            self.prepareGeometryChange()
        except Exception:
            pass
        if px and px > 0:
            self.setTextWidth(float(px))
        else:
            self.setTextWidth(0.0)
        try:
            self.document().adjustSize()
        except Exception:
            pass
        self.update()

    def get_pixel_dimensions(self):
        try:
            self.document().adjustSize()
            return float(self.document().size().width()), float(self.document().size().height())
        except Exception:
            br = super().boundingRect()
            return float(br.width()), float(br.height())

    def boundingRect(self) -> QRectF:
        return QRectF(super().boundingRect())
