"""
src/app.py
Punto de entrada principal para ejecutar la aplicación de escritorio andercal.visuals — Selector.
"""

import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en el PATH de Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.gui.main_window import MainWindow


def main():
    """Inicializa y ejecuta el bucle de eventos de la aplicación."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
