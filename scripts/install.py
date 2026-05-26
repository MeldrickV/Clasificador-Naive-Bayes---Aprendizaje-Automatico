"""
Script de instalación rápida
Instala todas las dependencias necesarias
"""

import sys
import subprocess
import os

def main():
    print("="*60)
    print("INSTALACIÓN CLASIFICADOR NAÏVE BAYES")
    print("="*60)
    print()
    
    print(f"Python: {sys.version}")
    print(f"Plataforma: {sys.platform}")
    print()
    
    # Verificar versión de Python
    if sys.version_info < (3, 7):
        print("✗ Error: Se requiere Python 3.7 o superior")
        print(f"  Versión actual: {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    
    print("✓ Versión de Python compatible")
    print()
    
    # Actualizar pip
    print("Actualizando pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ pip actualizado")
    except Exception as e:
        print(f"⚠ Advertencia al actualizar pip: {e}")
    
    print()
    
    # Instalar dependencias
    print("Instalando dependencias desde requirements.txt...")
    print()
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print()
        print("✓ Todas las dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print()
        print(f"✗ Error al instalar dependencias: {e}")
        sys.exit(1)
    
    print()
    print("="*60)
    print("✓ INSTALACIÓN COMPLETADA")
    print("="*60)
    print()
    print("Para ejecutar la aplicación:")
    print("  python main.py")
    print()
    print("Para compilar a ejecutable:")
    if sys.platform == "win32":
        print("  python compile_windows.py")
    else:
        print("  python compile_linux.py")
    print()

if __name__ == "__main__":
    main()
