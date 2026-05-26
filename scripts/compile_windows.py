"""
Script para compilar la aplicación a ejecutable de Windows (.exe)
Ejecutar desde la RAÍZ del proyecto: python scripts/compile_windows.py
"""

import os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

print("="*60)
print("COMPILACIÓN PARA WINDOWS")
print(f"Directorio: {ROOT}")
print("="*60)

try:
    import PyInstaller
    print("✓ PyInstaller encontrado")
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

comando = [
    "pyinstaller", "--name=NaiveBayesClassifier",
    "--onefile", "--windowed", "--clean", "--noconfirm",
    "--add-data=data;data", "--paths=src", "main.py"
]

try:
    subprocess.check_call(comando)
    print("\n✓ Ejecutable generado en: dist\\NaiveBayesClassifier.exe")
except subprocess.CalledProcessError as e:
    print(f"\n✗ ERROR: {e}"); sys.exit(1)
