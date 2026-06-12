# ui/splash_screen.py
#
# Splash screen reutilizable.
# Para usarlo en otra aplicación, copiá este archivo y solo modificá la
# sección "CONFIGURACIÓN" más abajo (título, versión, logo y duración).

import os
from PySide6.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtCore import Qt, QTimer


# =========================================================================
# CONFIGURACIÓN — Editá estos valores para personalizar el splash
# =========================================================================

# Título de la aplicación (se muestra en grande)
APP_TITLE = "StockBAR"

# Subtítulo / descripción corta (opcional, se puede dejar como "")
APP_SUBTITLE = "Generador de Etiquetas con Código de Barras"

# Versión de la aplicación
APP_VERSION = "v1.0.0"

# Ruta al logo de la empresa.
# - Podés usar una ruta relativa (ej: "assets/logo.png") o absoluta.
# - Formatos soportados: PNG, JPG, etc.
# - Si el archivo no existe o se deja en None, el splash se muestra sin logo.
LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

# Tamaño máximo del logo (ancho, alto) en píxeles. La imagen se escala
# manteniendo proporción si es más grande que esto.
LOGO_MAX_SIZE = (180, 180)

# Tamaño de la ventana del splash (ancho, alto)
SPLASH_SIZE = (420, 320)

# Duración en milisegundos que se muestra el splash antes de abrir
# la ventana principal. Poner 0 para que se cierre apenas la ventana
# principal esté lista (sin tiempo mínimo).
SPLASH_DURATION_MS = 2000

# Colores y estilos (podés ajustarlos a la imagen corporativa)
BACKGROUND_COLOR = "#FFFFFF"
TITLE_COLOR = "#222222"
SUBTITLE_COLOR = "#555555"
VERSION_COLOR = "#888888"

# =========================================================================
# FIN DE LA CONFIGURACIÓN — no es necesario editar nada debajo de esta línea
# =========================================================================


class SplashScreen(QSplashScreen):
    """
    Splash screen genérico con logo, título, subtítulo y versión.

    Uso típico (ver main.py):

        splash = SplashScreen()
        splash.show()
        app.processEvents()

        window = MainWindow()

        # Cerrar el splash y mostrar la ventana principal luego de
        # SPLASH_DURATION_MS milisegundos:
        QTimer.singleShot(SPLASH_DURATION_MS, lambda: (splash.close(), window.show()))
    """

    def __init__(self):
        # Pixmap base del splash (fondo). Se crea vacío y se pinta con
        # un QWidget interno para poder usar layouts (más fácil de
        # mantener que dibujar todo manualmente con QPainter).
        width, height = SPLASH_SIZE
        base_pixmap = QPixmap(width, height)
        base_pixmap.fill(QColor(BACKGROUND_COLOR))

        super().__init__(base_pixmap)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        # --- Widget contenedor con el contenido del splash ---
        content = QWidget(self)
        content.setGeometry(0, 0, width, height)
        content.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")

        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        # --- LOGO DE LA EMPRESA ---
        # Para agregar tu logo: definí LOGO_PATH arriba con la ruta al
        # archivo de imagen (PNG/JPG). Si LOGO_PATH es None o el archivo
        # no existe, esta sección simplemente no se muestra.
        if LOGO_PATH and os.path.exists(LOGO_PATH):
            logo_pixmap = QPixmap(LOGO_PATH)
            if not logo_pixmap.isNull():
                logo_pixmap = logo_pixmap.scaled(
                    LOGO_MAX_SIZE[0], LOGO_MAX_SIZE[1],
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                logo_label = QLabel()
                logo_label.setPixmap(logo_pixmap)
                logo_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(logo_label)

        # --- TÍTULO DE LA APLICACIÓN ---
        title_label = QLabel(APP_TITLE)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {TITLE_COLOR};")
        layout.addWidget(title_label)

        # --- SUBTÍTULO (opcional) ---
        if APP_SUBTITLE:
            subtitle_label = QLabel(APP_SUBTITLE)
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_font = QFont()
            subtitle_font.setPointSize(11)
            subtitle_label.setFont(subtitle_font)
            subtitle_label.setStyleSheet(f"color: {SUBTITLE_COLOR};")
            subtitle_label.setWordWrap(True)
            layout.addWidget(subtitle_label)

        # --- VERSIÓN DE LA APLICACIÓN ---
        version_label = QLabel(APP_VERSION)
        version_label.setAlignment(Qt.AlignCenter)
        version_font = QFont()
        version_font.setPointSize(9)
        version_label.setFont(version_font)
        version_label.setStyleSheet(f"color: {VERSION_COLOR};")
        layout.addWidget(version_label)

        # Centrar el splash en la pantalla
        self._center_on_screen(width, height)

    def _center_on_screen(self, width, height):
        screen = self.screen() if hasattr(self, "screen") else None
        if screen is not None:
            geometry = screen.availableGeometry()
            x = geometry.x() + (geometry.width() - width) // 2
            y = geometry.y() + (geometry.height() - height) // 2
            self.move(x, y)