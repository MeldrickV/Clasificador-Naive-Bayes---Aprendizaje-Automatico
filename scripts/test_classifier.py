"""
Script de pruebas para verificar el funcionamiento del clasificador
"""

import pandas as pd
import numpy as np
from core.classifier import NaiveBayesClassifier
from core.evaluation import ModelEvaluator

def test_gaussian():
    """Test con método Gaussiano"""
    print("\n" + "="*60)
    print("TEST 1: Método Gaussiano")
    print("="*60)
    
    # Cargar dataset
    df = pd.read_csv('iris_dataset.csv')
    X = df.drop(columns=['species'])
    y = df['species']
    
    # Split
    np.random.seed(42)
    indices = np.random.permutation(len(X))
    train_size = int(len(X) * 0.7)
    
    X_train = X.iloc[indices[:train_size]].reset_index(drop=True)
    X_test = X.iloc[indices[train_size:]].reset_index(drop=True)
    y_train = y.iloc[indices[:train_size]].reset_index(drop=True)
    y_test = y.iloc[indices[train_size:]].reset_index(drop=True)
    
    # Entrenar
    clf = NaiveBayesClassifier(continuous_method='gaussian')
    clf.fit(X_train, y_train)
    
    # Predecir
    y_pred = clf.predict(X_test)
    
    # Evaluar
    metrics = ModelEvaluator.evaluate(y_test.values, y_pred, clf.classes_)
    
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1-Score Macro: {metrics['f1_macro']:.4f}")
    
    if metrics['accuracy'] > 0.8:
        print("✓ Test PASADO")
        return True
    else:
        print("✗ Test FALLIDO")
        return False

def test_kde():
    """Test con método KDE"""
    print("\n" + "="*60)
    print("TEST 2: Método KDE")
    print("="*60)
    
    # Cargar dataset
    df = pd.read_csv('iris_dataset.csv')
    X = df.drop(columns=['species'])
    y = df['species']
    
    # Split
    np.random.seed(42)
    indices = np.random.permutation(len(X))
    train_size = int(len(X) * 0.7)
    
    X_train = X.iloc[indices[:train_size]].reset_index(drop=True)
    X_test = X.iloc[indices[train_size:]].reset_index(drop=True)
    y_train = y.iloc[indices[:train_size]].reset_index(drop=True)
    y_test = y.iloc[indices[train_size:]].reset_index(drop=True)
    
    # Entrenar
    clf = NaiveBayesClassifier(continuous_method='kde')
    clf.fit(X_train, y_train)
    
    # Predecir
    y_pred = clf.predict(X_test)
    
    # Evaluar
    metrics = ModelEvaluator.evaluate(y_test.values, y_pred, clf.classes_)
    
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1-Score Macro: {metrics['f1_macro']:.4f}")
    
    if metrics['accuracy'] > 0.7:
        print("✓ Test PASADO")
        return True
    else:
        print("✗ Test FALLIDO")
        return False

def test_discretization_equal_width():
    """Test con discretización de anchos iguales"""
    print("\n" + "="*60)
    print("TEST 3: Discretización - Anchos Iguales")
    print("="*60)
    
    # Cargar dataset
    df = pd.read_csv('iris_dataset.csv')
    X = df.drop(columns=['species'])
    y = df['species']
    
    # Split
    np.random.seed(42)
    indices = np.random.permutation(len(X))
    train_size = int(len(X) * 0.7)
    
    X_train = X.iloc[indices[:train_size]].reset_index(drop=True)
    X_test = X.iloc[indices[train_size:]].reset_index(drop=True)
    y_train = y.iloc[indices[:train_size]].reset_index(drop=True)
    y_test = y.iloc[indices[train_size:]].reset_index(drop=True)
    
    # Entrenar
    clf = NaiveBayesClassifier(continuous_method='equal_width', n_bins=5)
    clf.fit(X_train, y_train)
    
    # Predecir
    y_pred = clf.predict(X_test)
    
    # Evaluar
    metrics = ModelEvaluator.evaluate(y_test.values, y_pred, clf.classes_)
    
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1-Score Macro: {metrics['f1_macro']:.4f}")
    
    if metrics['accuracy'] > 0.7:
        print("✓ Test PASADO")
        return True
    else:
        print("✗ Test FALLIDO")
        return False

def test_discretization_equal_freq():
    """Test con discretización de frecuencias iguales"""
    print("\n" + "="*60)
    print("TEST 4: Discretización - Frecuencias Iguales")
    print("="*60)
    
    # Cargar dataset
    df = pd.read_csv('iris_dataset.csv')
    X = df.drop(columns=['species'])
    y = df['species']
    
    # Split
    np.random.seed(42)
    indices = np.random.permutation(len(X))
    train_size = int(len(X) * 0.7)
    
    X_train = X.iloc[indices[:train_size]].reset_index(drop=True)
    X_test = X.iloc[indices[train_size:]].reset_index(drop=True)
    y_train = y.iloc[indices[:train_size]].reset_index(drop=True)
    y_test = y.iloc[indices[train_size:]].reset_index(drop=True)
    
    # Entrenar
    clf = NaiveBayesClassifier(continuous_method='equal_freq', n_bins=5)
    clf.fit(X_train, y_train)
    
    # Predecir
    y_pred = clf.predict(X_test)
    
    # Evaluar
    metrics = ModelEvaluator.evaluate(y_test.values, y_pred, clf.classes_)
    
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1-Score Macro: {metrics['f1_macro']:.4f}")
    
    if metrics['accuracy'] > 0.7:
        print("✓ Test PASADO")
        return True
    else:
        print("✗ Test FALLIDO")
        return False

def test_prediction():
    """Test de predicción de nuevas instancias"""
    print("\n" + "="*60)
    print("TEST 5: Predicción de Nuevas Instancias")
    print("="*60)
    
    # Cargar dataset y entrenar
    df = pd.read_csv('iris_dataset.csv')
    X = df.drop(columns=['species'])
    y = df['species']
    
    clf = NaiveBayesClassifier(continuous_method='gaussian')
    clf.fit(X, y)
    
    # Cargar instancias de prueba
    instances = pd.read_csv('iris_test_instances.csv')
    
    # Predecir
    predictions = clf.predict(instances)
    probabilities = clf.predict_proba(instances)
    
    print(f"\nPredicciones realizadas: {len(predictions)}")
    for i, (pred, probs) in enumerate(zip(predictions, probabilities)):
        print(f"\nInstancia {i+1}: {pred}")
        for cls, prob in zip(clf.classes_, probs):
            print(f"  {cls}: {prob:.4f}")
    
    print("\n✓ Test PASADO")
    return True

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*60)
    print("SUITE DE PRUEBAS - CLASIFICADOR NAÏVE BAYES")
    print("="*60)
    
    tests = [
        test_gaussian,
        test_kde,
        test_discretization_equal_width,
        test_discretization_equal_freq,
        test_prediction
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Error en test: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests pasados: {passed}/{total}")
    
    if passed == total:
        print("\n✓ ¡TODAS LAS PRUEBAS PASARON!")
        print("\nEl clasificador está funcionando correctamente.")
        print("Puedes ejecutar la aplicación con: python main.py")
    else:
        print(f"\n✗ {total - passed} prueba(s) fallaron")
        print("\nRevisa los errores anteriores.")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
