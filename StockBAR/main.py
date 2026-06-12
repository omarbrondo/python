import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from ui.main_window import MainWindow
# CORRECCIÓN: Solo importamos la clase SplashScreen
from ui.splash_screen import SplashScreen

# Definimos la duración directamente acá (2000 milisegundos = 2 segundos)
SPLASH_DURATION_MS = 2000

def main():
    app = QApplication(sys.argv)

    # --- Mostrar splash screen ---
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # --- Crear la ventana principal (mientras se ve el splash) ---
    window = MainWindow()

    # --- Cerrar el splash y mostrar la ventana principal ---
    def show_main_window():
        splash.close()
        # window.show()
        window.showMaximized()

    # Se ejecuta la transición usando la variable local
    QTimer.singleShot(SPLASH_DURATION_MS, show_main_window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()