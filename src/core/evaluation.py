import numpy as np
import pandas as pd
from typing import Dict, Tuple


class ModelEvaluator:
    """
    Clase para evaluar el rendimiento del clasificador
    """
    
    @staticmethod
    def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, classes: np.ndarray) -> np.ndarray:
        """
        Calcula la matriz de confusión
        
        Parámetros:
        -----------
        y_true : array
            Etiquetas verdaderas
        y_pred : array
            Etiquetas predichas
        classes : array
            Lista de clases únicas
        
        Retorna:
        --------
        Matriz de confusión de forma (n_classes, n_classes)
        """
        n_classes = len(classes)
        cm = np.zeros((n_classes, n_classes), dtype=int)
        
        class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
        
        for true, pred in zip(y_true, y_pred):
            true_idx = class_to_idx[true]
            pred_idx = class_to_idx[pred]
            cm[true_idx, pred_idx] += 1
        
        return cm
    
    @staticmethod
    def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calcula la exactitud (accuracy)
        
        Accuracy = (TP + TN) / Total
        """
        correct = np.sum(y_true == y_pred)
        total = len(y_true)
        return correct / total if total > 0 else 0.0
    
    @staticmethod
    def precision_per_class(cm: np.ndarray, classes: np.ndarray) -> Dict[str, float]:
        """
        Calcula la precisión por clase
        
        Precision = TP / (TP + FP)
        """
        precision = {}
        
        for idx, cls in enumerate(classes):
            tp = cm[idx, idx]
            fp = cm[:, idx].sum() - tp
            
            if (tp + fp) > 0:
                precision[cls] = tp / (tp + fp)
            else:
                precision[cls] = 0.0
        
        return precision
    
    @staticmethod
    def recall_per_class(cm: np.ndarray, classes: np.ndarray) -> Dict[str, float]:
        """
        Calcula el recall (exhaustividad/especificidad) por clase
        
        Recall = TP / (TP + FN)
        """
        recall = {}
        
        for idx, cls in enumerate(classes):
            tp = cm[idx, idx]
            fn = cm[idx, :].sum() - tp
            
            if (tp + fn) > 0:
                recall[cls] = tp / (tp + fn)
            else:
                recall[cls] = 0.0
        
        return recall
    
    @staticmethod
    def f1_score_per_class(precision: Dict[str, float], recall: Dict[str, float]) -> Dict[str, float]:
        """
        Calcula el F1-score por clase
        
        F1 = 2 * (Precision * Recall) / (Precision + Recall)
        """
        f1 = {}
        
        for cls in precision.keys():
            p = precision[cls]
            r = recall[cls]
            
            if (p + r) > 0:
                f1[cls] = 2 * (p * r) / (p + r)
            else:
                f1[cls] = 0.0
        
        return f1
    
    @staticmethod
    def macro_average(metric_dict: Dict[str, float]) -> float:
        """
        Calcula el promedio macro de una métrica
        """
        return np.mean(list(metric_dict.values()))
    
    @staticmethod
    def weighted_average(metric_dict: Dict[str, float], cm: np.ndarray, classes: np.ndarray) -> float:
        """
        Calcula el promedio ponderado de una métrica
        """
        total = cm.sum()
        weighted = 0.0
        
        for idx, cls in enumerate(classes):
            class_count = cm[idx, :].sum()
            weight = class_count / total
            weighted += metric_dict[cls] * weight
        
        return weighted
    
    @classmethod
    def evaluate(cls, y_true: np.ndarray, y_pred: np.ndarray, classes: np.ndarray) -> Dict:
        """
        Evalúa el modelo y retorna todas las métricas
        
        Retorna:
        --------
        Diccionario con:
        - confusion_matrix: matriz de confusión
        - accuracy: exactitud global
        - precision: diccionario con precisión por clase
        - recall: diccionario con recall por clase
        - f1_score: diccionario con F1 por clase
        - precision_macro: precisión macro
        - recall_macro: recall macro
        - f1_macro: F1 macro
        - precision_weighted: precisión ponderada
        - recall_weighted: recall ponderado
        - f1_weighted: F1 ponderado
        """
        # Matriz de confusión
        cm = cls.confusion_matrix(y_true, y_pred, classes)
        
        # Accuracy
        acc = cls.accuracy(y_true, y_pred)
        
        # Precisión por clase
        precision = cls.precision_per_class(cm, classes)
        
        # Recall por clase
        recall = cls.recall_per_class(cm, classes)
        
        # F1-score por clase
        f1 = cls.f1_score_per_class(precision, recall)
        
        # Promedios
        precision_macro = cls.macro_average(precision)
        recall_macro = cls.macro_average(recall)
        f1_macro = cls.macro_average(f1)
        
        precision_weighted = cls.weighted_average(precision, cm, classes)
        recall_weighted = cls.weighted_average(recall, cm, classes)
        f1_weighted = cls.weighted_average(f1, cm, classes)
        
        return {
            'confusion_matrix': cm,
            'accuracy': acc,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'precision_macro': precision_macro,
            'recall_macro': recall_macro,
            'f1_macro': f1_macro,
            'precision_weighted': precision_weighted,
            'recall_weighted': recall_weighted,
            'f1_weighted': f1_weighted
        }


def print_evaluation_report(metrics: Dict, classes: np.ndarray):
    """
    Imprime un reporte formateado de las métricas de evaluación
    """
    print("\n" + "="*70)
    print(" REPORTE DE EVALUACIÓN DEL MODELO")
    print("="*70)
    
    # Accuracy
    print(f"\n Accuracy Global: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    
    # Matriz de confusión
    print("\n MATRIZ DE CONFUSIÓN:")
    print("-"*70)
    cm = metrics['confusion_matrix']
    
    # Encabezado
    header = "Verdadero\\Predicho |"
    for cls in classes:
        header += f" {str(cls)[:10]:>10} |"
    print(header)
    print("-"*70)
    
    # Filas
    for idx, cls in enumerate(classes):
        row = f"{str(cls)[:16]:>16} |"
        for val in cm[idx]:
            row += f" {val:>10} |"
        print(row)
    print("-"*70)
    
    # Métricas por clase
    print("\n MÉTRICAS POR CLASE:")
    print("-"*70)
    print(f"{'Clase':<20} {'Precisión':<15} {'Recall':<15} {'F1-Score':<15}")
    print("-"*70)
    
    for cls in classes:
        precision = metrics['precision'][cls]
        recall = metrics['recall'][cls]
        f1 = metrics['f1_score'][cls]
        print(f"{str(cls):<20} {precision:>6.4f} ({precision*100:>5.2f}%)  {recall:>6.4f} ({recall*100:>5.2f}%)  {f1:>6.4f} ({f1*100:>5.2f}%)")
    
    print("-"*70)
    
    # Promedios
    print("\n PROMEDIOS:")
    print("-"*70)
    print(f"{'Métrica':<20} {'Macro':<20} {'Weighted':<20}")
    print("-"*70)
    print(f"{'Precisión':<20} {metrics['precision_macro']:>6.4f} ({metrics['precision_macro']*100:>5.2f}%)     {metrics['precision_weighted']:>6.4f} ({metrics['precision_weighted']*100:>5.2f}%)")
    print(f"{'Recall':<20} {metrics['recall_macro']:>6.4f} ({metrics['recall_macro']*100:>5.2f}%)     {metrics['recall_weighted']:>6.4f} ({metrics['recall_weighted']*100:>5.2f}%)")
    print(f"{'F1-Score':<20} {metrics['f1_macro']:>6.4f} ({metrics['f1_macro']*100:>5.2f}%)     {metrics['f1_weighted']:>6.4f} ({metrics['f1_weighted']*100:>5.2f}%)")
    print("="*70 + "\n")
