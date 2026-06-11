from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsSimpleTextItem
from PySide6.QtGui import QPen, QBrush, QColor, QFont
from PySide6.QtCore import QRectF, Qt, QPointF, QSizeF
import math

HANDLE_SIZE = 10
ROTATE_HANDLE_SIZE = 12
ROTATE_HANDLE_OFFSET = 20  # px above the top-center


class ResizableItem(QGraphicsItem):
    def __init__(self, child_item):
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
        # bounding rect del child en coords del child
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

        # mapFromItem transforma puntos del child a coordenadas de self
        mapped = [self.mapFromItem(self.child, p) for p in corners]

        for handle, pos in zip(self.handles, mapped):
            handle.setPos(pos - QPointF(HANDLE_SIZE / 2, HANDLE_SIZE / 2))

        # posicionar rotate_handle sobre el top-center (ROTATE_HANDLE_OFFSET px arriba)
        top_center = self.mapFromItem(
            self.child,
            QPointF(self.child.boundingRect().center().x(), self.child.boundingRect().top())
        )
        self.rotate_handle.setPos(top_center + QPointF(0, -ROTATE_HANDLE_OFFSET))

        # Mostrar rotate handle solo si el wrapper está seleccionado
        self.rotate_handle.setVisible(self.isSelected())

        # posicionar angle_label cerca del rotate_handle (arriba a la derecha)
        rh_pos = self.rotate_handle.pos()
        self.angle_label.setPos(rh_pos + QPointF(ROTATE_HANDLE_SIZE / 2 + 6, -ROTATE_HANDLE_SIZE / 2))

        # proteger acceso a self.rotating por si update_handles se llama muy temprano
        self.angle_label.setVisible(getattr(self, "rotating", False))

    def boundingRect(self):
        # bounding rect del child mapeado a self, expandido por handles y rotate handle
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

        # detectar rotate_handle usando coords de escena
        local_rh = self.rotate_handle.mapFromScene(scene_pos)
        if self.rotate_handle.contains(local_rh):
            self.rotating = True
            # centro del wrapper en escena (centro del boundingRect del wrapper)
            wrapper_center_local = (self.boundingRect().topLeft() + self.boundingRect().bottomRight()) / 2.0
            center_scene = self.mapToScene(wrapper_center_local)
            self._rotation_center_scene = center_scene
            dx = scene_pos.x() - center_scene.x()
            dy = scene_pos.y() - center_scene.y()
            self._initial_mouse_angle = math.atan2(dy, dx)
            self._initial_rotation = self.rotation()
            # mostrar label
            self.angle_label.setVisible(True)
            self.update_handles()
            return

        # detectar handles de resize (usando escena)
        for i, handle in enumerate(self.handles):
            local = handle.mapFromScene(scene_pos)
            if handle.contains(local):
                self.resizing = True
                self.current_handle = i
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        scene_pos = event.scenePos()

        # rotación estable usando centro del wrapper
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
            return

        # resize
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
            return

        if getattr(self, "resizing", False):
            self.resizing = False
            self.current_handle = None
            self.update_handles()
            return

        super().mouseReleaseEvent(event)

    def _resize(self, pos):
        child_pos = self.child.mapFromItem(self, pos)
        rect = self.child.boundingRect()

        if self.current_handle in [0, 1, 2]:  # top
            rect.setTop(child_pos.y())
        if self.current_handle in [4, 5, 6]:  # bottom
            rect.setBottom(child_pos.y())
        if self.current_handle in [0, 7, 6]:  # left
            rect.setLeft(child_pos.x())
        if self.current_handle in [2, 3, 4]:  # right
            rect.setRight(child_pos.x())

        rect = rect.normalized()
        if rect.width() < 2 or rect.height() < 2:
            return

        self.prepareGeometryChange()

        orig_w = self.orig_child_rect.width() if self.orig_child_rect.width() > 0 else 1.0
        orig_h = self.orig_child_rect.height() if self.orig_child_rect.height() > 0 else 1.0
        scale_x = rect.width() / orig_w
        scale_y = rect.height() / orig_h

        if hasattr(self.child, "resize_font"):
            scale = (scale_x + scale_y) / 2.0
            self.child.resize_font(scale)
        elif hasattr(self.child, "resize_pixmap"):
            try:
                self.child.resize_pixmap(scale_x, scale_y)
            except TypeError:
                self.child.resize_pixmap((scale_x + scale_y) / 2.0)
        else:
            self.child.setTransformOriginPoint(self.child.boundingRect().center())
            self.child.setScale((scale_x + scale_y) / 2.0)

        self.update_handles()
