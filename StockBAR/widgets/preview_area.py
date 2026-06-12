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


# Lienzo de vista previa de la etiqueta.
# Gestiona la escena gráfica donde se muestran texto, barras y imágenes.
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
        # Crea un nuevo rectángulo base de etiqueta en la escena gráfica.
        # Se usa como contenedor de todos los elementos que aparecerán en la vista previa.
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
        Genera una imagen de código de barras a partir del texto ingresado.
        Esta función convierte la barra a un QPixmap para poder insertarla en la etiqueta.
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
        Añade un bloque de texto editable en la etiqueta.
        El texto se coloca en una posición inicial y queda listo para mover o modificar.
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
        Inserta un código de barras como imagen editable dentro de la etiqueta.
        Se envuelve en el mecanismo de redimensionado y selección visual.
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
        return wrapper

    def add_resizable_image(self, pixmap: QPixmap, x: float, y: float):
        """
        Añade una imagen cargada por el usuario a la etiqueta.
        Si la imagen es demasiado grande, se escala para que quepa de forma razonable.
        agregadas manualmente por el usuario (logos, fotos, etc.).
        Se comporta como cualquier otro elemento: se puede mover,
        redimensionar, rotar y ajustar su opacidad.
        """
        if not self.label_item:
            raise RuntimeError("No hay label creado. Llamá a create_label primero.")

        # Si la imagen es muy grande respecto a la etiqueta, la escalamos
        # a un tamaño inicial razonable manteniendo la proporción.
        label_rect = self.label_item.rect()
        max_w = max(1, label_rect.width() - x)
        max_h = max(1, label_rect.height() - y)

        if pixmap.width() > max_w or pixmap.height() > max_h:
            pixmap = pixmap.scaled(
                int(max_w), int(max_h),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

        pix_item = ResizablePixmapItem(pixmap)
        pix_item.setParentItem(self.label_item)
        pix_item.setPos(x, y)

        wrapper = ResizableItem(pix_item)
        wrapper.setParentItem(self.label_item)
        wrapper.setZValue(5)

        self.label_item.items.append(wrapper)
        wrapper.setSelected(True)
        return wrapper

    def _on_scene_selection_changed(self):
        """
        Detecta qué elemento está seleccionado en la escena y actualiza el panel de propiedades.
        Esto permite editar el objeto actual desde la interfaz lateral.
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