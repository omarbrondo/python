import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen, SPLASH_DURATION_MS


def main():
    app = QApplication(sys.argv)

    # --- Mostrar splash screen ---
    # Para personalizar título, versión, logo, colores, etc. editá
    # la sección "CONFIGURACIÓN" en ui/splash_screen.py
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # --- Crear la ventana principal (mientras se ve el splash) ---
    window = MainWindow()

    # --- Cerrar el splash y mostrar la ventana principal luego del
    #     tiempo configurado en SPLASH_DURATION_MS ---
    def show_main_window():
        splash.close()
        window.show()

    QTimer.singleShot(SPLASH_DURATION_MS, show_main_window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()