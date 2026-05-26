"""
Generador de datasets sintéticos para pruebas
Útil para experimentar con el clasificador
"""

import numpy as np
import pandas as pd

def generate_simple_2class():
    """
    Genera un dataset simple con 2 clases y variables continuas
    """
    print("Generando dataset: Simple 2 Clases")
    
    np.random.seed(42)
    
    # Clase A
    n_samples_a = 100
    X_a = np.random.randn(n_samples_a, 4) + [2, 2, -1, -1]
    y_a = ['Clase_A'] * n_samples_a
    
    # Clase B
    n_samples_b = 100
    X_b = np.random.randn(n_samples_b, 4) + [-2, -2, 1, 1]
    y_b = ['Clase_B'] * n_samples_b
    
    # Combinar
    X = np.vstack([X_a, X_b])
    y = y_a + y_b
    
    # Crear DataFrame
    df = pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3', 'feature4'])
    df['clase'] = y
    
    # Guardar
    df.to_csv('dataset_simple_2class.csv', index=False)
    print(f"✓ Guardado: dataset_simple_2class.csv ({len(df)} instancias)")
    print()

def generate_multiclass():
    """
    Genera un dataset con 4 clases
    """
    print("Generando dataset: Multi-Clase (4 clases)")
    
    np.random.seed(42)
    
    # Clase A
    X_a = np.random.randn(80, 3) + [3, 0, 2]
    y_a = ['A'] * 80
    
    # Clase B
    X_b = np.random.randn(80, 3) + [-3, 0, -2]
    y_b = ['B'] * 80
    
    # Clase C
    X_c = np.random.randn(80, 3) + [0, 3, 0]
    y_c = ['C'] * 80
    
    # Clase D
    X_d = np.random.randn(80, 3) + [0, -3, 0]
    y_d = ['D'] * 80
    
    # Combinar
    X = np.vstack([X_a, X_b, X_c, X_d])
    y = y_a + y_b + y_c + y_d
    
    # Crear DataFrame
    df = pd.DataFrame(X, columns=['attr1', 'attr2', 'attr3'])
    df['categoria'] = y
    
    # Guardar
    df.to_csv('dataset_multiclass.csv', index=False)
    print(f"✓ Guardado: dataset_multiclass.csv ({len(df)} instancias)")
    print()

def generate_mixed_types():
    """
    Genera un dataset con variables continuas y discretas mezcladas
    """
    print("Generando dataset: Tipos Mixtos (continuas + discretas)")
    
    np.random.seed(42)
    
    n_samples = 200
    
    # Variables continuas
    edad = np.random.randint(18, 65, n_samples)
    salario = np.random.exponential(40000, n_samples) + 20000
    antiguedad = np.random.gamma(2, 3, n_samples)
    
    # Variables discretas
    educacion = np.random.choice(['Secundaria', 'Licenciatura', 'Maestria', 'Doctorado'], 
                                 n_samples, p=[0.2, 0.5, 0.2, 0.1])
    departamento = np.random.choice(['Ventas', 'IT', 'RRHH', 'Finanzas'], n_samples)
    
    # Generar clase basada en las características
    clase = []
    for i in range(n_samples):
        if salario[i] > 60000 and educacion[i] in ['Maestria', 'Doctorado']:
            clase.append('Alto')
        elif salario[i] < 40000:
            clase.append('Bajo')
        else:
            clase.append('Medio')
    
    # Crear DataFrame
    df = pd.DataFrame({
        'edad': edad,
        'salario': salario,
        'antiguedad': antiguedad,
        'educacion': educacion,
        'departamento': departamento,
        'nivel': clase
    })
    
    # Guardar
    df.to_csv('dataset_mixed_types.csv', index=False)
    print(f"✓ Guardado: dataset_mixed_types.csv ({len(df)} instancias)")
    print()

def generate_imbalanced():
    """
    Genera un dataset desbalanceado (útil para probar robustez)
    """
    print("Generando dataset: Desbalanceado")
    
    np.random.seed(42)
    
    # Clase mayoritaria (80%)
    n_majority = 400
    X_maj = np.random.randn(n_majority, 3) + [1, 1, 1]
    y_maj = ['Mayoritaria'] * n_majority
    
    # Clase minoritaria 1 (15%)
    n_min1 = 75
    X_min1 = np.random.randn(n_min1, 3) + [-2, -2, -2]
    y_min1 = ['Minoritaria_1'] * n_min1
    
    # Clase minoritaria 2 (5%)
    n_min2 = 25
    X_min2 = np.random.randn(n_min2, 3) + [0, 3, -3]
    y_min2 = ['Minoritaria_2'] * n_min2
    
    # Combinar
    X = np.vstack([X_maj, X_min1, X_min2])
    y = y_maj + y_min1 + y_min2
    
    # Crear DataFrame
    df = pd.DataFrame(X, columns=['x1', 'x2', 'x3'])
    df['clase'] = y
    
    # Guardar
    df.to_csv('dataset_imbalanced.csv', index=False)
    print(f"✓ Guardado: dataset_imbalanced.csv ({len(df)} instancias)")
    print(f"  - Mayoritaria: {n_majority} ({n_majority/len(df)*100:.1f}%)")
    print(f"  - Minoritaria_1: {n_min1} ({n_min1/len(df)*100:.1f}%)")
    print(f"  - Minoritaria_2: {n_min2} ({n_min2/len(df)*100:.1f}%)")
    print()

def generate_nonlinear():
    """
    Genera un dataset con relaciones no lineales
    """
    print("Generando dataset: Relaciones No Lineales")
    
    np.random.seed(42)
    
    n_samples = 300
    
    # Generar datos con patrones circulares
    angles_a = np.random.uniform(0, 2*np.pi, n_samples//2)
    radius_a = np.random.normal(2, 0.3, n_samples//2)
    X_a = np.column_stack([
        radius_a * np.cos(angles_a),
        radius_a * np.sin(angles_a),
        np.random.randn(n_samples//2)
    ])
    y_a = ['Interior'] * (n_samples//2)
    
    angles_b = np.random.uniform(0, 2*np.pi, n_samples//2)
    radius_b = np.random.normal(5, 0.3, n_samples//2)
    X_b = np.column_stack([
        radius_b * np.cos(angles_b),
        radius_b * np.sin(angles_b),
        np.random.randn(n_samples//2)
    ])
    y_b = ['Exterior'] * (n_samples//2)
    
    # Combinar
    X = np.vstack([X_a, X_b])
    y = y_a + y_b
    
    # Crear DataFrame
    df = pd.DataFrame(X, columns=['coord_x', 'coord_y', 'altura'])
    df['region'] = y
    
    # Guardar
    df.to_csv('dataset_nonlinear.csv', index=False)
    print(f"✓ Guardado: dataset_nonlinear.csv ({len(df)} instancias)")
    print()

def main():
    """Generar todos los datasets de ejemplo"""
    print("\n" + "="*60)
    print("GENERADOR DE DATASETS SINTÉTICOS")
    print("="*60)
    print()
    print("Este script genera varios datasets de ejemplo para probar")
    print("diferentes escenarios con el clasificador Naïve Bayes.")
    print()
    
    datasets = [
        generate_simple_2class,
        generate_multiclass,
        generate_mixed_types,
        generate_imbalanced,
        generate_nonlinear
    ]
    
    for generator in datasets:
        try:
            generator()
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("="*60)
    print("✓ GENERACIÓN COMPLETADA")
    print("="*60)
    print()
    print("Datasets generados:")
    print("  1. dataset_simple_2class.csv - Dos clases, fácil de separar")
    print("  2. dataset_multiclass.csv - Cuatro clases")
    print("  3. dataset_mixed_types.csv - Variables continuas y discretas")
    print("  4. dataset_imbalanced.csv - Clases desbalanceadas")
    print("  5. dataset_nonlinear.csv - Relaciones no lineales")
    print()
    print("Usa estos datasets para experimentar con diferentes configuraciones")
    print("del clasificador y comparar los resultados.")
    print()

if __name__ == "__main__":
    main()
