# Punto de entrada principal de la aplicación.
# Este archivo crea la app Qt, muestra el splash y luego lanza la ventana principal.

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from ui.main_window import MainWindow
# CORRECCIÓN: Solo importamos la clase SplashScreen
from ui.splash_screen import SplashScreen

# Definimos la duración directamente acá (2000 milisegundos = 2 segundos)
SPLASH_DURATION_MS = 2000

def main():
    # Crea la aplicación Qt principal y prepara el entorno gráfico.
    app = QApplication(sys.argv)

    # --- Mostrar splash screen ---
    # El splash se muestra primero para dar una experiencia visual de carga.
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # --- Crear la ventana principal (mientras se ve el splash) ---
    # Se instancia la ventana real de la aplicación en segundo plano para que aparezca rápido.
    window = MainWindow()

    # --- Cerrar el splash y mostrar la ventana principal ---
    # Este timer retrasa la muestra de la ventana principal durante 2 segundos.
    def show_main_window():
        splash.close()
        # window.show()
        window.showMaximized()

    # Se ejecuta la transición usando la variable local
    QTimer.singleShot(SPLASH_DURATION_MS, show_main_window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()