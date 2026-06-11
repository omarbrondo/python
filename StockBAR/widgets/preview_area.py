# widgets/preview_area.py
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap, QImage, QPainter
from PySide6.QtCore import Qt

from widgets.label_item import LabelItem
from widgets.resizable_item import ResizableItem
from widgets.resizable_text_item import ResizableTextItem
from widgets.resizable_pixmap_item import ResizablePixmapItem
from widgets.properties_panel import PropertiesPanel

import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io


class PreviewArea(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Usar RenderHints válidos (QPainter flags)
        hints = self.renderHints()
        hints |= QPainter.Antialiasing
        hints |= QPainter.SmoothPixmapTransform
        self.setRenderHints(hints)

        # Opcional: anclar transformaciones al centro del view
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.setSceneRect(0, 0, 800, 600)

        self.label_item = None

        # Panel de propiedades (instancia, no añadida al layout aquí)
        self.properties_panel = PropertiesPanel()
        # conectar selección de escena para actualizar panel
        self.scene.selectionChanged.connect(self._on_scene_selection_changed)

    def create_label(self, width_px, height_px):
        # eliminar label anterior si existe
        if self.label_item:
            try:
                self.scene.removeItem(self.label_item)
            except Exception:
                pass

        self.label_item = LabelItem(width_px, height_px)
        # posicionar la etiqueta en la escena
        self.label_item.setPos(50, 50)
        self.scene.addItem(self.label_item)
        # limpiar lista de items
        self.label_item.items = []

    def generate_barcode_pixmap(self, codigo: str) -> QPixmap:
        """
        Genera un QPixmap a partir de python-barcode + PIL de forma segura.
        Evita problemas de stride/bytesPerLine que corren las filas.
        """
        barcode_class = barcode.get_barcode_class("code128")
        barcode_obj = barcode_class(codigo, writer=ImageWriter())

        buffer = io.BytesIO()
        barcode_obj.write(buffer)
        buffer.seek(0)

        pil_image = Image.open(buffer).convert("RGBA")
        w, h = pil_image.size
        data = pil_image.tobytes("raw", "RGBA")
        bytes_per_line = 4 * w  # 4 bytes por píxel en RGBA

        qimage = QImage(data, w, h, bytes_per_line, QImage.Format_RGBA8888)
        return QPixmap.fromImage(qimage)

    def add_resizable_text(self, text: str, x: float, y: float):
        """
        Crea un ResizableTextItem, lo envuelve en ResizableItem y lo parenta a label_item.
        """
        if not self.label_item:
            raise RuntimeError("No hay label creado. Llamá a create_label primero.")

        text_item = ResizableTextItem(text)
        text_item.setParentItem(self.label_item)
        text_item.setPos(x, y)

        wrapper = ResizableItem(text_item)
        wrapper.setParentItem(self.label_item)
        wrapper.setZValue(5)

        self.label_item.items.append(wrapper)
        wrapper.setSelected(True)

    def add_resizable_barcode(self, pixmap: QPixmap, x: float, y: float):
        """
        Crea un ResizablePixmapItem con el pixmap original, lo envuelve y lo parenta.
        """
        if not self.label_item:
            raise RuntimeError("No hay label creado. Llamá a create_label primero.")

        pix_item = ResizablePixmapItem(pixmap)
        pix_item.setParentItem(self.label_item)
        pix_item.setPos(x, y)

        wrapper = ResizableItem(pix_item)
        wrapper.setParentItem(self.label_item)
        wrapper.setZValue(5)

        self.label_item.items.append(wrapper)
        wrapper.setSelected(True)

    def _on_scene_selection_changed(self):
        """
        Actualiza el PropertiesPanel con el primer ResizableItem seleccionado.
        """
        selected = self.scene.selectedItems()
        wrapper = None
        for it in selected:
            from widgets.resizable_item import ResizableItem as _RI
            if isinstance(it, _RI):
                wrapper = it
                break
            parent = it.parentItem()
            if isinstance(parent, _RI):
                wrapper = parent
                break

        if wrapper:
            self.properties_panel.set_target(wrapper)
        else:
            self.properties_panel.clear_target()
