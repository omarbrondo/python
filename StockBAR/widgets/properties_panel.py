# widgets/properties_panel.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QDoubleSpinBox, QSlider, QHBoxLayout, QPushButton, QSpinBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal


# Panel lateral de propiedades del elemento seleccionado.
# Permite modificar ángulo, opacidad, tamaño, proporción y restaurar el estado original.
class PropertiesPanel(QWidget):
    properties_changed = Signal()

    def __init__(self, parent=None):
        # Inicializa el panel lateral con controles para modificar el elemento actualmente seleccionado.
        super().__init__(parent)
        self.setMinimumWidth(220)

        self._target = None  # wrapper seleccionado (ResizableItem)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Ángulo
        self.angle_spin = QDoubleSpinBox()
        self.angle_spin.setRange(-360.0, 360.0)
        self.angle_spin.setSingleStep(1.0)
        form.addRow(QLabel("Ángulo (°):"), self.angle_spin)

        # Opacidad
        opacity_layout = QHBoxLayout()
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_label = QLabel("100%")
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_label)
        form.addRow(QLabel("Opacidad:"), opacity_layout)

        # Tamaño de fuente (solo para texto)
        self.font_spin = QSpinBox()
        self.font_spin.setRange(6, 200)
        self.font_spin.setSingleStep(1)
        form.addRow(QLabel("Tamaño fuente:"), self.font_spin)

        # Ancho / Alto numérico (px)
        wh_layout = QHBoxLayout()
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        # después de crear width_spin / height_spin
        self.width_spin.setSingleStep(1)
        self.height_spin.setSingleStep(1)

        # Asegurar que valueChanged se emite mientras se escribe y con flechas
        self.width_spin.setKeyboardTracking(True)
        self.height_spin.setKeyboardTracking(True)

        # Conectar editingFinished para cubrir casos donde valueChanged no se dispare
        self.width_spin.editingFinished.connect(self._on_wh_changed)
        self.height_spin.editingFinished.connect(self._on_wh_changed)

        wh_layout.addWidget(self.width_spin)
        wh_layout.addWidget(self.height_spin)
        form.addRow(QLabel("Ancho / Alto (px):"), wh_layout)

        # Mantener proporción
        self.keep_aspect_cb = QCheckBox("Mantener proporción")
        self.keep_aspect_cb.setChecked(True)
        form.addRow(self.keep_aspect_cb)

        # Botones
        btn_layout = QHBoxLayout()
        self.reset_btn = QPushButton("Reset")
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(form)
        layout.addLayout(btn_layout)
        layout.addStretch()

        # Conexiones UI
        self.angle_spin.valueChanged.connect(self._on_angle_changed)
        self.opacity_slider.valueChanged.connect(self._on_opacity_changed)
        self.font_spin.valueChanged.connect(self._on_font_changed)
        self.width_spin.valueChanged.connect(self._on_wh_changed)
        self.height_spin.valueChanged.connect(self._on_wh_changed)
        self.keep_aspect_cb.toggled.connect(self._on_keep_aspect_changed)
        self.reset_btn.clicked.connect(self._on_reset_clicked)

        # Estado inicial
        self.clear_target()

    # API pública: asignar el wrapper seleccionado
    def set_target(self, wrapper):
        # Asigna un elemento de la etiqueta como objetivo del panel de edición.
        self._target = wrapper
        self._refresh_ui()

    def clear_target(self):
        # Limpia el objetivo actual cuando no hay ningún elemento seleccionado.
        self._target = None
        self._refresh_ui()

    def _refresh_ui(self):
        # Actualiza los controles del panel para reflejar el estado del elemento actual.
        if not self._target:
            self.setEnabled(False)
            # valores por defecto visuales
            self.angle_spin.setValue(0)
            self.opacity_slider.setValue(100)
            self.opacity_label.setText("100%")
            self.font_spin.setValue(14)
            self.width_spin.setValue(0)
            self.height_spin.setValue(0)
            self.keep_aspect_cb.setChecked(True)
            return

        self.setEnabled(True)

        # Ángulo
        try:
            angle = float(self._target.get_angle())
        except Exception:
            angle = 0.0
        self.angle_spin.blockSignals(True)
        self.angle_spin.setValue(angle)
        self.angle_spin.blockSignals(False)

        # Opacidad
        try:
            op = int(round(self._target.get_opacity() * 100))
        except Exception:
            op = 100
        self.opacity_slider.blockSignals(True)
        self.opacity_slider.setValue(op)
        self.opacity_label.setText(f"{op}%")
        self.opacity_slider.blockSignals(False)

        # Tamaño de fuente (si aplica)
        if self._target.child_has_font():
            try:
                base_font = int(self._target.get_font_size())
            except Exception:
                base_font = 14
            self.font_spin.blockSignals(True)
            self.font_spin.setValue(base_font)
            self.font_spin.blockSignals(False)
            self.font_spin.setEnabled(True)
        else:
            self.font_spin.setEnabled(False)

        # Ancho / Alto (en px) según bounding rect del child
        try:
            w, h = self._target.get_dimensions()
            w = int(round(w))
            h = int(round(h))
        except Exception:
            w, h = 0, 0

        self.width_spin.blockSignals(True)
        self.height_spin.blockSignals(True)
        self.width_spin.setValue(w)
        self.height_spin.setValue(h)
        self.width_spin.blockSignals(False)
        self.height_spin.blockSignals(False)

        # Mantener proporción: reflejar estado actual del wrapper
        self.keep_aspect_cb.blockSignals(True)
        self.keep_aspect_cb.setChecked(getattr(self._target, "keep_aspect", True))
        self.keep_aspect_cb.blockSignals(False)

    # Handlers UI
    def _on_angle_changed(self, value):
        # Aplica la rotación indicada al elemento seleccionado.
        if not self._target:
            return
        try:
            self._target.set_angle(float(value))
            self.properties_changed.emit()
        except Exception:
            pass

    def _on_opacity_changed(self, value):
        # Ajusta la transparencia del elemento y actualiza la etiqueta visual del porcentaje.
        if not self._target:
            return
        try:
            self.opacity_label.setText(f"{value}%")
            self._target.set_opacity(value / 100.0)
            self.properties_changed.emit()
        except Exception:
            pass

    def _on_font_changed(self, value):
        # Cambia el tamaño de la fuente cuando el elemento seleccionado es de tipo texto.
        if not self._target:
            return
        if self._target.child_has_font():
            try:
                self._target.set_font_size(int(value))
                self.properties_changed.emit()
            except Exception:
                pass

    def _on_wh_changed(self):
        # Redimensiona el elemento según ancho y alto ingresados por el usuario.
        if not self._target:
            return
        try:
            w = self.width_spin.value()
            h = self.height_spin.value()
            keep = self.keep_aspect_cb.isChecked()
            # set_dimensions acepta keep_aspect (ver ResizableItem)
            self._target.set_dimensions(w, h, keep_aspect=keep)
            self.properties_changed.emit()
        except Exception:
            pass

    def _on_keep_aspect_changed(self, checked):
        # Activa o desactiva la restricción de mantener proporciones al escalar.
        if not self._target:
            return
        try:
            self._target.set_keep_aspect(bool(checked))
        except Exception:
            pass

    def _on_reset_clicked(self):
        # Vuelve al estado original del elemento seleccionado.
        if not self._target:
            return
        try:
            self._target.reset_to_original()
            self._refresh_ui()
            self.properties_changed.emit()
        except Exception:
            pass