from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QDoubleSpinBox, QSlider, QHBoxLayout, QPushButton, QSpinBox
)
from PySide6.QtCore import Qt, Signal

class PropertiesPanel(QWidget):
    # Señal para notificar cambios (opcional)
    properties_changed = Signal()

    def __init__(self, parent=None):
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
        wh_layout.addWidget(self.width_spin)
        wh_layout.addWidget(self.height_spin)
        form.addRow(QLabel("Ancho / Alto (px):"), wh_layout)

        # Botones
        btn_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Aplicar")
        self.reset_btn = QPushButton("Reset")
        btn_layout.addWidget(self.apply_btn)
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
        self.apply_btn.clicked.connect(self._on_apply_clicked)
        self.reset_btn.clicked.connect(self._on_reset_clicked)

    # API pública: asignar el wrapper seleccionado
    def set_target(self, wrapper):
        self._target = wrapper
        self._refresh_ui()

    def clear_target(self):
        self._target = None
        self._refresh_ui()

    def _refresh_ui(self):
        if not self._target:
            self.angle_spin.setValue(0)
            self.opacity_slider.setValue(100)
            self.opacity_label.setText("100%")
            self.font_spin.setValue(14)
            self.width_spin.setValue(0)
            self.height_spin.setValue(0)
            self.setEnabled(False)
            return

        self.setEnabled(True)
        # Ángulo
        angle = self._target.get_angle()
        self.angle_spin.blockSignals(True)
        self.angle_spin.setValue(angle)
        self.angle_spin.blockSignals(False)

        # Opacidad
        op = int(round(self._target.get_opacity() * 100))
        self.opacity_slider.blockSignals(True)
        self.opacity_slider.setValue(op)
        self.opacity_label.setText(f"{op}%")
        self.opacity_slider.blockSignals(False)

        # Si es texto, mostrar tamaño de fuente base (si existe)
        if self._target.child_has_font():
            base_font = self._target.get_font_size()
            self.font_spin.blockSignals(True)
            self.font_spin.setValue(base_font)
            self.font_spin.blockSignals(False)
            self.font_spin.setEnabled(True)
        else:
            self.font_spin.setEnabled(False)

        # Ancho / Alto (en px) según bounding rect del child
        w, h = self._target.get_dimensions()
        self.width_spin.blockSignals(True)
        self.height_spin.blockSignals(True)
        self.width_spin.setValue(int(round(w)))
        self.height_spin.setValue(int(round(h)))
        self.width_spin.blockSignals(False)
        self.height_spin.blockSignals(False)

    # Handlers UI
    def _on_angle_changed(self, value):
        if not self._target: return
        self._target.set_angle(value)
        self.properties_changed.emit()

    def _on_opacity_changed(self, value):
        if not self._target: return
        self.opacity_label.setText(f"{value}%")
        self._target.set_opacity(value / 100.0)
        self.properties_changed.emit()

    def _on_font_changed(self, value):
        if not self._target: return
        if self._target.child_has_font():
            # convertimos tamaño absoluto a factor relativo respecto al base_font_size
            self._target.set_font_size(value)
            self.properties_changed.emit()

    def _on_wh_changed(self):
        # cambios en ancho/alto actualizan en tiempo real
        if not self._target: return
        w = self.width_spin.value()
        h = self.height_spin.value()
        self._target.set_dimensions(w, h)
        self.properties_changed.emit()

    def _on_apply_clicked(self):
        # ya aplicamos en tiempo real; aquí podemos forzar un refresh
        if self._target:
            self._target.update_handles()
            self.properties_changed.emit()

    def _on_reset_clicked(self):
        if not self._target: return
        self._target.reset_to_original()
        self._refresh_ui()
        self.properties_changed.emit()
