# widgets/resizable_text_item.py
from PySide6.QtWidgets import QGraphicsSimpleTextItem, QGraphicsItem
from PySide6.QtGui import QFont, QFontMetricsF
from PySide6.QtCore import QRectF, Qt


class ResizableTextItem(QGraphicsSimpleTextItem):
    """
    QGraphicsSimpleTextItem que soporta:
    - base_font_size: tamaño base en puntos (float)
    - resize_font(factor_or_size): si recibe <= 10 lo interpreta como factor relativo,
      si recibe > 10 lo interpreta como tamaño absoluto en puntos.
    - recalcula boundingRect y fuerza repaint/geometry change.
    """

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)

        # Inicializar fuente base
        f = self.font() if self.font() else QFont("Arial", 14)
        base = f.pointSizeF() if f.pointSizeF() > 0 else 14.0
        self.base_font_size = float(base)

        # Asegurar que el item use la fuente inicial
        self.setFont(f)

        # Flags: usar las constantes de QGraphicsItem
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)

    def resize_font(self, value):
        """
        Interpreta `value` como tamaño absoluto en puntos si es > 0.
        Si por compatibilidad recibimos un factor (<= 10), lo convertimos a tamaño absoluto
        usando base_font_size.
        """
        try:
            v = float(value)
        except Exception:
            return

        if v <= 0:
            return

        # Si el valor es pequeño (<=10) lo tratamos como factor relativo
        if v <= 10.0:
            new_pt = max(1.0, self.base_font_size * v)
        else:
            # valor absoluto en puntos
            new_pt = max(1.0, v)

        old_font = self.font()
        new_font = QFont(old_font)
        new_font.setPointSizeF(new_pt)

        try:
            self.prepareGeometryChange()
        except Exception:
            pass

        self.setFont(new_font)
        self.update()

        # No sobrescribimos base_font_size automáticamente para evitar oscilaciones.
        # Si preferís que base se actualice al nuevo tamaño, descomenta la línea siguiente:
        # self.base_font_size = float(new_pt)

    def set_text(self, text: str):
        """
        Actualiza el texto y fuerza recalculo.
        """
        try:
            self.prepareGeometryChange()
        except Exception:
            pass
        self.setText(text)
        self.update()

    def get_pixel_dimensions(self):
        fm = QFontMetricsF(self.font())
        rect = fm.boundingRect(self.text())
        return rect.width(), rect.height()

    def boundingRect(self) -> QRectF:
        br = super().boundingRect()
        return QRectF(br)