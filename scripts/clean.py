"""
Script para limpiar archivos temporales generados durante compilación
"""

import os
import shutil
import sys

def remove_directory(path):
    """Elimina un directorio y su contenido"""
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"✓ Eliminado: {path}")
            return True
        except Exception as e:
            print(f"✗ Error al eliminar {path}: {e}")
            return False
    return True

def remove_file(path):
    """Elimina un archivo"""
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"✓ Eliminado: {path}")
            return True
        except Exception as e:
            print(f"✗ Error al eliminar {path}: {e}")
            return False
    return True

def main():
    print("="*60)
    print("LIMPIEZA DE ARCHIVOS TEMPORALES")
    print("="*60)
    print()
    
    # Directorios a eliminar
    directories = [
        'build',
        'dist',
        '__pycache__',
        '*.egg-info'
    ]
    
    # Archivos a eliminar
    files = [
        'NaiveBayesClassifier.spec',
        '*.pyc',
    ]
    
    print("Eliminando directorios temporales...")
    print()
    
    for directory in directories:
        if '*' in directory:
            # Buscar directorios que coincidan con el patrón
            import glob
            for path in glob.glob(directory):
                remove_directory(path)
        else:
            remove_directory(directory)
    
    print()
    print("Eliminando archivos temporales...")
    print()
    
    for file_pattern in files:
        if '*' in file_pattern:
            # Buscar archivos que coincidan con el patrón
            import glob
            for path in glob.glob(file_pattern):
                remove_file(path)
        else:
            remove_file(file_pattern)
    
    # Buscar y eliminar archivos .pyc en subdirectorios
    for root, dirs, files_list in os.walk('.'):
        for file in files_list:
            if file.endswith('.pyc'):
                filepath = os.path.join(root, file)
                remove_file(filepath)
    
    print()
    print("="*60)
    print("✓ LIMPIEZA COMPLETADA")
    print("="*60)
    print()
    print("Se han eliminado todos los archivos temporales.")
    print("Puedes compilar nuevamente con compile_windows.py o compile_linux.py")
    print()

if __name__ == "__main__":
    main()
