# ui/splash_screen.py
# =========================================================================
# SPLASH SCREEN PROFESIONAL Y REUTILIZABLE (PySide6)
# =========================================================================
# Instrucciones de uso:
# 1. Copiá este archivo en la carpeta de interfaz de tu nuevo proyecto.
# 2. Modificá exclusivamente la sección "CONFIGURACIÓN DE IDENTIDAD" abajo.
# 3. No es necesario alterar la lógica interna a menos que busques cambios estructurales.

import os
from PySide6.QtWidgets import (
    QSplashScreen, QLabel, QVBoxLayout, QWidget, 
    QGraphicsDropShadowEffect, QProgressBar
)
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtCore import Qt


# =========================================================================
# 1. CONFIGURACIÓN DE IDENTIDAD Y ESTILO — Personalizá aquí tu Splash
# =========================================================================

# --- TEXTOS DE LA APLICACIÓN ---
APP_TITLE = "StockBAR"
APP_SUBTITLE = "Generador de Etiquetas con Código de Barras"
APP_VERSION = "v1.0.0"

# --- RECURSOS VISUALES (LOGO) ---
# Ruta al logo. Soporta PNG, JPG, SVG, etc. Se auto-oculta si el archivo no existe.
LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
LOGO_MAX_SIZE = (140, 140)  # Ancho y alto máximo para mantener las proporciones

# --- DIMENSIONES Y GEOMETRÍA ---
SPLASH_SIZE = (460, 340)    # Tamaño de la tarjeta del splash (Ancho, Alto)
BORDER_RADIUS = 16          # Redondeado de las esquinas en píxeles (0 para recto)

# --- PALETA DE COLORES (Formatos HEX válidos para CSS) ---
COLOR_BG = "#D7D7D8FE"           # Fondo principal de la ventana
COLOR_TITLE = "#020000"        # Color del título principal
COLOR_SUBTITLE = "#272088"     # Color del subtítulo o descripción
COLOR_VERSION = "#050101"      # Color del texto de la versión

# --- BARRA DE PROGRESO (OPCIONAL) ---
SHOW_PROGRESS_BAR = True       # Cambiar a False si no se desea barra de carga
COLOR_PROGRESS_BG = "#E0E0E0"  # Fondo del canal de la barra
COLOR_PROGRESS_FILL = "#0078D4" # Color del indicador de carga (ej: azul corporativo)
PROGRESS_BAR_HEIGHT = 4        # Grosor en píxeles de la barra de progreso

# --- CONFIGURACIÓN DE LA SOMBRA (EFECTO DROP SHADOW) ---
ENABLE_SHADOW = True
SHADOW_COLOR = QColor(0, 0, 0, 45)  # Color RGBA (R, G, B, Alfa/Opacidad)
SHADOW_BLUR_RADIUS = 20             # Qué tan suave es la difuminación de la sombra
SHADOW_OFFSET = (0, 4)              # Desplazamiento horizontal y vertical (X, Y)

# =========================================================================
# FIN DE LA CONFIGURACIÓN — Lógica interna del componente
# =========================================================================


class SplashScreen(QSplashScreen):
    """
    Splash Screen moderno con soporte para bordes redondeados, capas de layout
    limpias, sombras fluidas y barra de carga configurable de forma nativa.
    
    Uso estándar en main.py:
    -----------------------
    splash = SplashScreen()
    splash.show()
    app.processEvents()
    
    # Inicializar ventana principal
    window = MainWindow()
    
    # Ejemplo de cierre mediante un timer o al finalizar la carga de datos:
    QTimer.singleShot(2500, lambda: (splash.close(), window.show()))
    """

    def __init__(self):
        # Parámetros de tamaño base
        width, height = SPLASH_SIZE
        
        # Margen adicional para que la sombra del contenedor no se corte en los bordes
        self.padding = SHADOW_BLUR_RADIUS * 2 if ENABLE_SHADOW else 0
        total_width = width + self.padding
        total_height = height + self.padding

        # Crear un Pixmap base completamente transparente para servir de lienzo
        base_pixmap = QPixmap(total_width, total_height)
        base_pixmap.fill(Qt.transparent)

        # Inicializar la clase base QSplashScreen con el lienzo transparente
        super().__init__(base_pixmap)
        
        # Flags indispensables para ventanas personalizadas sin marcos rígidos
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # --- CONTENEDOR PRINCIPAL (La tarjeta visual) ---
        self.container = QWidget(self)
        self.container.setGeometry(
            self.padding // 2, 
            self.padding // 2, 
            width, 
            height
        )
        
        # Aplicación del estilo general de la tarjeta (Fondo y Bordes)
        self.container.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_BG};
                border-radius: {BORDER_RADIUS}px;
            }}
        """)

        # --- EFECTO DE SOMBRA REALISTA ---
        if ENABLE_SHADOW:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
            shadow.setColor(SHADOW_COLOR)
            shadow.setOffset(SHADOW_OFFSET[0], SHADOW_OFFSET[1])
            self.container.setGraphicsEffect(shadow)

        # --- DISEÑO Y DISTRIBUCIÓN DE COMPONENTES ---
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(32, 32, 32, 24)
        layout.setSpacing(14)
        layout.setAlignment(Qt.AlignCenter)

        # 1. Componente: Logo corporativo
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
                # Forzar que el fondo del label sea transparente para no romper el contenedor
                logo_label.setStyleSheet("background: transparent;")
                layout.addWidget(logo_label)

        # Espaciador sutil entre el logo y el texto
        layout.addSpacing(4)

        # 2. Componente: Título de la aplicación
        title_label = QLabel(APP_TITLE)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Segoe UI", 24)  # Tipografía limpia por defecto
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {COLOR_TITLE}; background: transparent;")
        layout.addWidget(title_label)

        # 3. Componente: Subtítulo descriptivo
        if APP_SUBTITLE:
            subtitle_label = QLabel(APP_SUBTITLE)
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_font = QFont("Segoe UI", 10)
            subtitle_label.setFont(subtitle_font)
            subtitle_label.setStyleSheet(f"color: {COLOR_SUBTITLE}; background: transparent;")
            subtitle_label.setWordWrap(True)
            layout.addWidget(subtitle_label)

        # Margen expansible para empujar la versión y el progreso al fondo
        layout.addStretch()

        # 4. Componente: Barra de progreso (Carga)
        if SHOW_PROGRESS_BAR:
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            self.progress_bar.setTextVisible(False)  # Oculta el porcentaje numérico molesto
            self.progress_bar.setFixedHeight(PROGRESS_BAR_HEIGHT)
            self.progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    background-color: {COLOR_PROGRESS_BG};
                    border-radius: {PROGRESS_BAR_HEIGHT // 2}px;
                }}
                QProgressBar::chunk {{
                    background-color: {COLOR_PROGRESS_FILL};
                    border-radius: {PROGRESS_BAR_HEIGHT // 2}px;
                }}
            """)
            layout.addWidget(self.progress_bar)

        # 5. Componente: Etiqueta de versión
        version_label = QLabel(APP_VERSION)
        version_label.setAlignment(Qt.AlignCenter)
        version_font = QFont("Segoe UI", 9)
        version_label.setFont(version_font)
        version_label.setStyleSheet(f"color: {COLOR_VERSION}; background: transparent;")
        layout.addWidget(version_label)

        # Ejecutar centrado dinámico en pantalla considerando el área de la sombra
        self._center_on_screen(total_width, total_height)

    def set_progress(self, value: int):
        """
        Permite actualizar el valor de la barra de progreso de forma externa 
        si se realiza una carga basada en pasos medibles (0-100).
        """
        if SHOW_PROGRESS_BAR and hasattr(self, 'progress_bar'):
            self.progress_bar.setValue(value)

    def _center_on_screen(self, width, height):
        """Calcula el centro geométrico de la pantalla activa para posicionar el splash."""
        screen = self.screen() if hasattr(self, "screen") else None
        if screen is not None:
            geometry = screen.availableGeometry()
            x = geometry.x() + (geometry.width() - width) // 2
            y = geometry.y() + (geometry.height() - height) // 2
            self.move(x, y)