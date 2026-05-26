"""
Clasificador Naïve Bayes
Soporta variables continuas y discretas con múltiples métodos de estimación
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class NaiveBayesClassifier:
    """
    Clasificador Naïve Bayes que soporta:
    - Variables discretas con Laplace smoothing
    - Variables continuas con:
        * Distribución Gaussiana
        * KDE (Kernel Density Estimation)
        * Discretización por frecuencias iguales
        * Discretización por anchos iguales
    """
    
    def __init__(self, 
                 continuous_method='gaussian',
                 laplace_alpha=1.0,
                 n_bins=5,
                 binning_strategy='equal_width',
                 kde_bandwidth='scott'):
        """
        Parámetros:
        -----------
        continuous_method : str
            Método para variables continuas: 'gaussian', 'kde', 'equal_width', 'equal_freq'
        laplace_alpha : float
            Parámetro alpha para Laplace smoothing (por defecto 1.0)
        n_bins : int
            Número de bins para discretización
        binning_strategy : str
            Estrategia de binning: 'equal_width' o 'equal_freq'
        kde_bandwidth : str or float
            Bandwidth para KDE: 'scott', 'silverman' o valor numérico
        """
        self.continuous_method = continuous_method
        self.laplace_alpha = laplace_alpha
        self.n_bins = n_bins
        self.binning_strategy = binning_strategy
        self.kde_bandwidth = kde_bandwidth
        
        # Almacenamiento de parámetros del modelo
        self.classes_ = None
        self.class_priors_ = {}
        self.feature_types_ = {}
        self.categorical_probs_ = {}
        self.continuous_params_ = {}
        self.bins_ = {}
        self.kde_models_ = {}
        self.feature_names_ = None
        
    def _identify_feature_types(self, X: pd.DataFrame) -> Dict[str, str]:
        """Identifica si cada característica es continua o discreta"""
        feature_types = {}
        
        for col in X.columns:
            # Consideramos discretas las columnas con tipo object, bool o con pocos valores únicos
            if X[col].dtype == 'object' or X[col].dtype == 'bool':
                feature_types[col] = 'discrete'
            elif X[col].dtype in ['int64', 'int32'] and X[col].nunique() < 20:
                feature_types[col] = 'discrete'
            else:
                feature_types[col] = 'continuous'
                
        return feature_types
    
    def _calculate_class_priors(self, y: pd.Series) -> Dict:
        """Calcula las probabilidades a priori de cada clase"""
        priors = {}
        total = len(y)
        
        for class_val in self.classes_:
            count = (y == class_val).sum()
            priors[class_val] = count / total
            
        return priors
    
    def _fit_discrete_feature(self, X: pd.DataFrame, y: pd.Series, feature: str):
        """Ajusta probabilidades para una variable discreta con Laplace smoothing"""
        self.categorical_probs_[feature] = {}
        
        unique_values = X[feature].unique()
        n_values = len(unique_values)
        
        for class_val in self.classes_:
            class_mask = (y == class_val)
            class_data = X[class_mask][feature]
            class_count = class_mask.sum()
            
            self.categorical_probs_[feature][class_val] = {}
            
            for value in unique_values:
                # Laplace smoothing
                count = (class_data == value).sum()
                prob = (count + self.laplace_alpha) / (class_count + self.laplace_alpha * n_values)
                self.categorical_probs_[feature][class_val][value] = prob
    
    def _fit_gaussian(self, X: pd.DataFrame, y: pd.Series, feature: str):
        """Ajusta distribución Gaussiana para una variable continua"""
        self.continuous_params_[feature] = {}
        
        for class_val in self.classes_:
            class_data = X[y == class_val][feature]
            
            # Calcular media y desviación estándar
            mean = class_data.mean()
            std = class_data.std()
            
            # Evitar desviación estándar cero
            if std == 0:
                std = 1e-6
                
            self.continuous_params_[feature][class_val] = {
                'mean': mean,
                'std': std
            }
    
    def _fit_kde(self, X: pd.DataFrame, y: pd.Series, feature: str):
        """Ajusta KDE (Kernel Density Estimation) para una variable continua"""
        self.kde_models_[feature] = {}
        
        for class_val in self.classes_:
            class_data = X[y == class_val][feature].values
            
            # Crear modelo KDE
            if len(class_data) > 0:
                kde = stats.gaussian_kde(class_data, bw_method=self.kde_bandwidth)
                self.kde_models_[feature][class_val] = kde
    
    def _fit_binning(self, X: pd.DataFrame, y: pd.Series, feature: str):
        """Discretiza una variable continua usando binning"""
        # Crear bins
        if self.binning_strategy == 'equal_width':
            # Anchos iguales
            bins = pd.cut(X[feature], bins=self.n_bins, duplicates='drop')
        else:  # equal_freq
            # Frecuencias iguales
            bins = pd.qcut(X[feature], q=self.n_bins, duplicates='drop')
        
        self.bins_[feature] = bins.cat.categories
        
        # Tratar como variable discreta
        X_binned = bins.astype(str)
        self.categorical_probs_[feature] = {}
        
        unique_bins = X_binned.unique()
        n_bins_actual = len(unique_bins)
        
        for class_val in self.classes_:
            class_mask = (y == class_val)
            class_data = X_binned[class_mask]
            class_count = class_mask.sum()
            
            self.categorical_probs_[feature][class_val] = {}
            
            for bin_val in unique_bins:
                count = (class_data == bin_val).sum()
                prob = (count + self.laplace_alpha) / (class_count + self.laplace_alpha * n_bins_actual)
                self.categorical_probs_[feature][class_val][bin_val] = prob
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Entrena el clasificador Naïve Bayes
        
        Parámetros:
        -----------
        X : DataFrame
            Características de entrenamiento
        y : Series
            Etiquetas de clase
        """
        self.feature_names_ = X.columns.tolist()
        self.classes_ = np.unique(y)
        
        # Identificar tipos de características
        self.feature_types_ = self._identify_feature_types(X)
        
        # Calcular probabilidades a priori
        self.class_priors_ = self._calculate_class_priors(y)
        
        # Ajustar cada característica según su tipo
        for feature in X.columns:
            if self.feature_types_[feature] == 'discrete':
                self._fit_discrete_feature(X, y, feature)
            else:
                # Variable continua
                if self.continuous_method == 'gaussian':
                    self._fit_gaussian(X, y, feature)
                elif self.continuous_method == 'kde':
                    self._fit_kde(X, y, feature)
                elif self.continuous_method in ['equal_width', 'equal_freq']:
                    self._fit_binning(X, y, feature)
        
        return self
    
    def _predict_proba_discrete(self, value, feature: str, class_val) -> float:
        """Calcula P(feature=value|class) para variable discreta"""
        if value in self.categorical_probs_[feature][class_val]:
            return self.categorical_probs_[feature][class_val][value]
        else:
            # Valor no visto, usar Laplace smoothing
            n_values = len(self.categorical_probs_[feature][class_val])
            return self.laplace_alpha / (sum(self.categorical_probs_[feature][class_val].values()) + self.laplace_alpha * n_values)
    
    def _predict_proba_gaussian(self, value: float, feature: str, class_val) -> float:
        """Calcula P(feature=value|class) usando distribución Gaussiana"""
        params = self.continuous_params_[feature][class_val]
        mean = params['mean']
        std = params['std']
        
        # Función de densidad de probabilidad
        prob = stats.norm.pdf(value, loc=mean, scale=std)
        
        # Evitar probabilidad cero
        if prob == 0:
            prob = 1e-10
            
        return prob
    
    def _predict_proba_kde(self, value: float, feature: str, class_val) -> float:
        """Calcula P(feature=value|class) usando KDE"""
        kde = self.kde_models_[feature][class_val]
        prob = kde.evaluate(value)[0]
        
        # Evitar probabilidad cero
        if prob == 0:
            prob = 1e-10
            
        return prob
    
    def _predict_proba_binning(self, value: float, feature: str, class_val) -> float:
        """Calcula P(feature=value|class) usando binning"""
        # Determinar en qué bin cae el valor
        bins = self.bins_[feature]
        
        bin_label = None
        for bin_interval in bins:
            if value >= bin_interval.left and value <= bin_interval.right:
                bin_label = str(bin_interval)
                break
        
        # Si no está en ningún bin, usar el más cercano
        if bin_label is None:
            if value < bins[0].left:
                bin_label = str(bins[0])
            else:
                bin_label = str(bins[-1])
        
        return self._predict_proba_discrete(bin_label, feature, class_val)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predice probabilidades de clase para cada instancia
        
        Retorna:
        --------
        Array de forma (n_samples, n_classes) con probabilidades
        """
        n_samples = len(X)
        n_classes = len(self.classes_)
        proba = np.zeros((n_samples, n_classes))
        
        for i, (idx, row) in enumerate(X.iterrows()):
            for j, class_val in enumerate(self.classes_):
                # Log-probabilidad a priori
                log_prob = np.log(self.class_priors_[class_val])
                
                # Multiplicar por P(feature|class) para cada característica
                for feature in self.feature_names_:
                    value = row[feature]
                    
                    if pd.isna(value):
                        continue
                    
                    if self.feature_types_[feature] == 'discrete':
                        prob_feature = self._predict_proba_discrete(value, feature, class_val)
                    else:
                        if self.continuous_method == 'gaussian':
                            prob_feature = self._predict_proba_gaussian(value, feature, class_val)
                        elif self.continuous_method == 'kde':
                            prob_feature = self._predict_proba_kde(value, feature, class_val)
                        elif self.continuous_method in ['equal_width', 'equal_freq']:
                            prob_feature = self._predict_proba_binning(value, feature, class_val)
                    
                    log_prob += np.log(prob_feature)
                
                proba[i, j] = log_prob
        
        # Convertir de log-probabilidades a probabilidades
        # Normalizar para evitar overflow
        proba = proba - proba.max(axis=1, keepdims=True)
        proba = np.exp(proba)
        proba = proba / proba.sum(axis=1, keepdims=True)
        
        return proba
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predice la clase para cada instancia
        
        Retorna:
        --------
        Array de predicciones de clase
        """
        proba = self.predict_proba(X)
        predictions = [self.classes_[i] for i in np.argmax(proba, axis=1)]
        return np.array(predictions)
