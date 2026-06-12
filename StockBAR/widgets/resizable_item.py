from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsSimpleTextItem
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QTransform
from PySide6.QtCore import QRectF, Qt, QPointF, QSizeF
import math


# Wrapper visual que añade comportamiento interactivo a cualquier elemento de la etiqueta.
# Se encarga de mover, redimensionar, rotar y mostrar controles de edición.

HANDLE_SIZE = 10
ROTATE_HANDLE_SIZE = 12
ROTATE_HANDLE_OFFSET = 20  # px above the top-center


class ResizableItem(QGraphicsItem):
    def __init__(self, child_item):
        # Envuelve un elemento gráfico para añadirle control visual y edición interactiva.
        super().__init__()

        # --- child / referencia original ---
        self.child = child_item
        self.orig_child_rect = self.child.boundingRect()

        # Guardar la posición del child antes de reparentar
        child_pos = self.child.pos()

        # Reparentar: ponemos el wrapper en la posición del child y movemos el child a (0,0)
        self.setPos(child_pos)
        self.child.setParentItem(self)
        self.child.setPos(0, 0)

        # Escalas independientes en X e Y aplicadas al child vía QTransform
        self.scale_x = 1.0
        self.scale_y = 1.0

        # Mantener proporción al redimensionar (controlado por PropertiesPanel)
        self.keep_aspect = True

        # Mantener z-order: wrapper en z original, child por encima
        try:
            orig_z = self.child.zValue()
        except Exception:
            orig_z = 0
        self.setZValue(orig_z)
        self.child.setZValue(orig_z + 1)

        # Flags del wrapper
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )

        # --- Inicializar estados ANTES de crear handles ---
        self.resizing = False
        self.current_handle = None
        self.rotating = False

        # Datos para rotación estable
        self._rotation_center_scene = None
        self._initial_mouse_angle = 0.0
        self._initial_rotation = 0.0

        # --- Handle de rotación (se mostrará solo cuando esté seleccionado) ---
        self.rotate_handle = QGraphicsRectItem(
            -ROTATE_HANDLE_SIZE / 2,
            -ROTATE_HANDLE_SIZE / 2,
            ROTATE_HANDLE_SIZE,
            ROTATE_HANDLE_SIZE,
            self
        )
        self.rotate_handle.setBrush(QBrush(QColor("#FFAA00")))
        self.rotate_handle.setPen(QPen(Qt.black, 1))
        self.rotate_handle.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.rotate_handle.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.rotate_handle.setVisible(False)

        # label numérico del ángulo (oculto hasta rotar)
        self.angle_label = QGraphicsSimpleTextItem("", self)
        self.angle_label.setBrush(QBrush(QColor("#222")))
        self.angle_label.setFont(QFont("Arial", 10))
        # asegurar z por encima del child
        try:
            self.angle_label.setZValue(self.child.zValue() + 2)
        except Exception:
            self.angle_label.setZValue(10)
        self.angle_label.setVisible(False)

        # --- Handles de resize ---
        self.handles = []
        self._create_handles()

    # --- Métodos públicos para el panel de propiedades ---

    def get_angle(self) -> float:
        # Devuelve el ángulo actual de rotación del elemento.
        return self.rotation()

    def set_angle(self, degrees: float):
        # Aplica una rotación específica al elemento seleccionado.
        self.setRotation(degrees)
        self.update_handles()

    def get_opacity(self) -> float:
        # Devuelve la opacidad actual del elemento, en valor entre 0 y 1.
        return self.opacity()

    def set_opacity(self, value: float):
        # Ajusta la opacidad del elemento y la mantiene dentro del rango válido.
        self.setOpacity(max(0.0, min(1.0, value)))
        self.update_handles()

    def child_has_font(self) -> bool:
        # Indica si el elemento interno soporta cambios de fuente.
        return hasattr(self.child, "resize_font") and hasattr(self.child, "base_font_size")

    def get_font_size(self) -> int:
        if self.child_has_font():
            try:
                f = self.child.font()
                pt = f.pointSizeF()
                if pt and pt > 0:
                    return int(round(pt))
            except Exception:
                pass
            try:
                return int(self.child.base_font_size)
            except Exception:
                return 14
        return 0

    def set_font_size(self, absolute_size: int):
        if self.child_has_font():
            try:
                self.child.resize_font(float(absolute_size))
                # al cambiar la fuente, el bounding rect base cambia: reseteamos
                # las escalas para que el tamaño numérico reportado coincida
                # con el nuevo bounding rect real.
                self.orig_child_rect = self.child.boundingRect()
                self.scale_x = 1.0
                self.scale_y = 1.0
                self._apply_transform()
                self.update_handles()
            except Exception:
                pass

    def get_dimensions(self):
        br = self.child.boundingRect()
        w = br.width() * self.scale_x
        h = br.height() * self.scale_y
        return w, h

    def _apply_transform(self):
        """Aplica las escalas independientes X/Y al child mediante QTransform."""
        self.prepareGeometryChange()
        t = QTransform()
        t.scale(self.scale_x, self.scale_y)
        self.child.setTransform(t)

    def set_keep_aspect(self, value: bool):
        self.keep_aspect = bool(value)

    def set_dimensions(self, width_px: float, height_px: float, keep_aspect: bool = True):
        # Ajusta tamaño del elemento según ancho y alto en píxeles.
        self.keep_aspect = keep_aspect

        base_rect = self.child.boundingRect()
        base_w = base_rect.width() if base_rect.width() > 0 else 1.0
        base_h = base_rect.height() if base_rect.height() > 0 else 1.0

        new_scale_x = width_px / base_w
        new_scale_y = height_px / base_h

        if keep_aspect:
            current_w = base_w * self.scale_x
            current_h = base_h * self.scale_y
            if current_w > 0 and abs(width_px - current_w) >= abs(height_px - current_h):
                factor = new_scale_x
            else:
                factor = new_scale_y
            new_scale_x = factor
            new_scale_y = factor

        new_scale_x = max(0.01, new_scale_x)
        new_scale_y = max(0.01, new_scale_y)

        self.scale_x = new_scale_x
        self.scale_y = new_scale_y
        self._apply_transform()
        self.update_handles()

    def _notify_property_change(self):
        try:
            sc = self.scene()
            if not sc:
                return
            views = sc.views()
            if not views:
                return
            view = views[0]
            panel = getattr(view, "properties_panel", None)
            if not panel:
                return
            if getattr(panel, "_target", None) is self:
                panel._refresh_ui()
        except Exception:
            pass

    def reset_to_original(self):
        self.setRotation(0)
        self.setOpacity(1.0)
        if hasattr(self.child, "original_pixmap"):
            try:
                self.child.setPixmap(self.child.original_pixmap)
            except Exception:
                pass
        if hasattr(self.child, "base_font_size"):
            try:
                self.child.resize_font(self.child.base_font_size)
            except Exception:
                pass
        self.orig_child_rect = self.child.boundingRect()
        self.scale_x = 1.0
        self.scale_y = 1.0
        self._apply_transform()
        self.update_handles()
        self._notify_property_change()

    def _create_handles(self):
        self.handles.clear()
        for _ in range(8):
            rect = QGraphicsRectItem(0, 0, HANDLE_SIZE, HANDLE_SIZE, self)
            rect.setBrush(QBrush(QColor("#00A8FF")))
            rect.setPen(QPen(Qt.black, 1))
            rect.setFlag(QGraphicsItem.ItemIsMovable, False)
            rect.setFlag(QGraphicsItem.ItemIsSelectable, False)
            self.handles.append(rect)
        self.update_handles()

    def update_handles(self):
        # Posiciona los puntos de ajuste del elemento según su rectángulo actual.
        child_rect = self.child.boundingRect()

        corners = [
            QPointF(child_rect.left(), child_rect.top()),              # 0 top-left
            QPointF(child_rect.center().x(), child_rect.top()),        # 1 top-center
            QPointF(child_rect.right(), child_rect.top()),             # 2 top-right
            QPointF(child_rect.right(), child_rect.center().y()),      # 3 right-center
            QPointF(child_rect.right(), child_rect.bottom()),          # 4 bottom-right
            QPointF(child_rect.center().x(), child_rect.bottom()),     # 5 bottom-center
            QPointF(child_rect.left(), child_rect.bottom()),           # 6 bottom-left
            QPointF(child_rect.left(), child_rect.center().y()),       # 7 left-center
        ]

        mapped = [self.mapFromItem(self.child, p) for p in corners]

        for handle, pos in zip(self.handles, mapped):
            handle.setPos(pos - QPointF(HANDLE_SIZE / 2, HANDLE_SIZE / 2))

        top_center = self.mapFromItem(
            self.child,
            QPointF(self.child.boundingRect().center().x(), self.child.boundingRect().top())
        )
        self.rotate_handle.setPos(top_center + QPointF(0, -ROTATE_HANDLE_OFFSET))

        self.rotate_handle.setVisible(self.isSelected())

        rh_pos = self.rotate_handle.pos()
        self.angle_label.setPos(rh_pos + QPointF(ROTATE_HANDLE_SIZE / 2 + 6, -ROTATE_HANDLE_SIZE / 2))

        self.angle_label.setVisible(getattr(self, "rotating", False))

    def boundingRect(self):
        child_rect = self.child.boundingRect()
        top_left = self.mapFromItem(self.child, child_rect.topLeft())
        bottom_right = self.mapFromItem(self.child, child_rect.bottomRight())
        rect = QRectF(top_left, bottom_right).normalized()
        return rect.adjusted(-HANDLE_SIZE, -HANDLE_SIZE - ROTATE_HANDLE_OFFSET, HANDLE_SIZE, HANDLE_SIZE)

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            pen = QPen(Qt.DashLine)
            pen.setColor(Qt.blue)
            painter.setPen(pen)
            child_rect = self.child.boundingRect()
            top_left = self.mapFromItem(self.child, child_rect.topLeft())
            bottom_right = self.mapFromItem(self.child, child_rect.bottomRight())
            rect = QRectF(top_left, bottom_right).normalized()
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        scene_pos = event.scenePos()

        local_rh = self.rotate_handle.mapFromScene(scene_pos)
        if self.rotate_handle.contains(local_rh):
            self.rotating = True
            wrapper_center_local = (self.boundingRect().topLeft() + self.boundingRect().bottomRight()) / 2.0
            center_scene = self.mapToScene(wrapper_center_local)
            self._rotation_center_scene = center_scene
            dx = scene_pos.x() - center_scene.x()
            dy = scene_pos.y() - center_scene.y()
            self._initial_mouse_angle = math.atan2(dy, dx)
            self._initial_rotation = self.rotation()
            self.angle_label.setVisible(True)
            self.update_handles()
            return

        for i, handle in enumerate(self.handles):
            local = handle.mapFromScene(scene_pos)
            if handle.contains(local):
                self.resizing = True
                self.current_handle = i
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        scene_pos = event.scenePos()

        if getattr(self, "rotating", False) and self._rotation_center_scene is not None:
            dx = scene_pos.x() - self._rotation_center_scene.x()
            dy = scene_pos.y() - self._rotation_center_scene.y()
            current_mouse_angle = math.atan2(dy, dx)
            delta = current_mouse_angle - self._initial_mouse_angle
            deg = math.degrees(delta) + self._initial_rotation
            if event.modifiers() & Qt.ShiftModifier:
                deg = round(deg / 15) * 15
            self.setRotation(deg)
            display_deg = int(round(deg)) % 360
            self.angle_label.setText(f"{display_deg}°")
            self.update_handles()
            self._notify_property_change()
            return

        if getattr(self, "resizing", False) and self.current_handle is not None:
            pos_in_self = self.mapFromScene(scene_pos)
            self._resize(pos_in_self)
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if getattr(self, "rotating", False):
            self.rotating = False
            self._rotation_center_scene = None
            self.angle_label.setVisible(False)
            self.update_handles()
            self._notify_property_change()
            return

        if getattr(self, "resizing", False):
            self.resizing = False
            self.current_handle = None
            self.update_handles()
            self._notify_property_change()
            return

        super().mouseReleaseEvent(event)

    def _resize(self, pos):
        """
        Redimensiona el elemento arrastrando uno de sus handles.
        Calcula nuevos tamaños a partir de la posición del cursor y la geometría original.

        Redimensiona el item arrastrando un handle.

        `pos` está en coordenadas locales de self (el wrapper). Para calcular
        el nuevo tamaño deseado, lo convertimos a coordenadas "base" del child
        (es decir, sin la transformación de escala actual aplicada), y lo
        comparamos contra self.orig_child_rect.
        """
        inv_transform, ok = self.child.transform().inverted()
        if not ok:
            inv_transform = QTransform()

        pos_in_child = self.mapFromItem(self.child, pos)  # incluye transform actual del child
        base_pos = inv_transform.map(pos_in_child)         # posición en coords "sin escalar"

        rect = self.orig_child_rect

        new_left = rect.left()
        new_top = rect.top()
        new_right = rect.right()
        new_bottom = rect.bottom()

        is_left = self.current_handle in (0, 7, 6)
        is_right = self.current_handle in (2, 3, 4)
        is_top = self.current_handle in (0, 1, 2)
        is_bottom = self.current_handle in (4, 5, 6)

        if is_top:
            new_top = base_pos.y()
        if is_bottom:
            new_bottom = base_pos.y()
        if is_left:
            new_left = base_pos.x()
        if is_right:
            new_right = base_pos.x()

        new_width = new_right - new_left
        new_height = new_bottom - new_top

        if new_width < 2 or new_height < 2:
            return

        orig_w = rect.width() if rect.width() > 0 else 1.0
        orig_h = rect.height() if rect.height() > 0 else 1.0

        new_scale_x = new_width / orig_w
        new_scale_y = new_height / orig_h

        horizontal_only = (is_left or is_right) and not (is_top or is_bottom)
        vertical_only = (is_top or is_bottom) and not (is_left or is_right)

        if self.keep_aspect:
            if horizontal_only:
                factor = new_scale_x
            elif vertical_only:
                factor = new_scale_y
            else:
                # handle de esquina: usar el eje con mayor cambio relativo
                if abs(new_scale_x - self.scale_x) >= abs(new_scale_y - self.scale_y):
                    factor = new_scale_x
                else:
                    factor = new_scale_y
            new_scale_x = factor
            new_scale_y = factor
        else:
            # Sin mantener proporción: cada handle afecta solo su(s) eje(s).
            if horizontal_only:
                new_scale_y = self.scale_y
            elif vertical_only:
                new_scale_x = self.scale_x
            # handle de esquina: ambos ejes cambian de forma independiente

        new_scale_x = max(0.01, new_scale_x)
        new_scale_y = max(0.01, new_scale_y)

        self.scale_x = new_scale_x
        self.scale_y = new_scale_y
        self._apply_transform()

        self.update_handles()
        self._notify_property_change()