"""
Clasificador Naïve Bayes - Aprendizaje Automático
==================================================
Punto de entrada principal de la aplicación.
"""

import sys
import os

# Asegurar que src/ está en el path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.app import launch_app

if __name__ == "__main__":
    launch_app()
