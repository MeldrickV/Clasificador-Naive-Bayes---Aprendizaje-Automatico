# Clasificador Naïve Bayes - Aprendizaje Automático

Sistema de clasificación basado en el algoritmo Naïve Bayes con soporte para variables continuas y discretas.

## 🚀 Características

### Métodos para Variables Continuas
- **Distribución Gaussiana**: Asume distribución normal de los datos
- **KDE (Kernel Density Estimation)**: Estimación no paramétrica de densidad
- **Discretización por Anchos Iguales**: Divide el rango en intervalos de igual tamaño
- **Discretización por Frecuencias Iguales**: Divide en intervalos con igual cantidad de datos

### Métodos para Variables Discretas
- **Laplace Smoothing**: Suavizado de probabilidades para evitar ceros

### Métricas de Evaluación
- Matriz de Confusión
- Accuracy (Exactitud Global)
- Precisión por clase
- Recall (Exhaustividad/Especificidad) por clase
- F1-Score por clase
- Promedios Macro y Weighted

### Validación
- División simple configurable (X% entrenamiento, resto prueba)
- Semilla aleatoria configurable para reproducibilidad

## 🔧 Instalación

### Opción 1: Ejecutar desde código fuente

1. **Instalar Python** (si no lo tienes):
   - Windows: Descargar desde https://www.python.org/downloads/
   - Linux: `sudo apt-get install python3 python3-pip`

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

### Opción 2: Compilar a ejecutable

#### Para Windows:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Compilar
python compile_windows.py
```

El ejecutable se generará en `dist/NaiveBayesClassifier.exe`

#### Para Linux:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Compilar
python compile_linux.py
```

El ejecutable se generará en `dist/NaiveBayesClassifier`

## 📖 Uso de la Aplicación

### 1. Pestaña "Configuración"

#### Cargar Dataset
- Click en "Cargar Dataset (.csv)"
- Selecciona tu archivo CSV
- El dataset debe tener:
  - Una columna para cada atributo/característica
  - Una columna con la clase objetivo

#### Seleccionar Columna Objetivo
- Selecciona qué columna representa la clase a predecir

#### Configurar Parámetros del Modelo

**Método para Variables Continuas:**
- **Distribución Gaussiana**: Recomendado cuando los datos siguen distribución normal
- **KDE**: Recomendado para distribuciones complejas o multimodales
- **Discretización - Anchos Iguales**: Divide el rango en intervalos uniformes
- **Discretización - Frecuencias Iguales**: Cada intervalo tiene aproximadamente la misma cantidad de datos

**Laplace Alpha**: Parámetro de suavizado para variables discretas (por defecto: 1.0)

**Número de Bins**: Cantidad de intervalos para discretización (por defecto: 5)

**Bandwidth KDE**: Método para calcular el ancho de banda del kernel
- `scott`: Regla de Scott (por defecto)
- `silverman`: Regla de Silverman

**% Datos de Entrenamiento**: Porcentaje del dataset para entrenar (10-90%)

**Semilla Aleatoria**: Para reproducir los mismos resultados

### 2. Pestaña "Entrenamiento"

- Click en "Entrenar Modelo"
- El sistema dividirá automáticamente los datos en entrenamiento y prueba
- Se mostrará un log del proceso de entrenamiento
- Al finalizar, se evaluará automáticamente en el conjunto de prueba

### 3. Pestaña "Predicción"

#### Clasificar Nuevas Instancias
- Click en "Cargar Archivo de Instancias (.csv)"
- El archivo debe tener las mismas columnas que el dataset de entrenamiento (excepto la columna de clase)
- Click en "Clasificar Instancias"
- Se mostrarán las predicciones con sus probabilidades

### 4. Pestaña "Resultados"

- Muestra todas las métricas de evaluación
- Matriz de confusión detallada
- Métricas por clase y promedios
- Puedes exportar los resultados a archivo de texto

## 📁 Formato del Dataset

### Archivo CSV de Entrenamiento
```csv
atributo1,atributo2,atributo3,clase
5.1,3.5,1.4,setosa
4.9,3.0,1.4,setosa
7.0,3.2,4.7,versicolor
6.4,3.2,4.5,versicolor
```

### Archivo CSV de Instancias a Clasificar
```csv
atributo1,atributo2,atributo3
5.0,3.6,1.4
6.5,3.0,5.2
```

**Notas:**
- La primera fila debe contener los nombres de las columnas
- Las variables pueden ser continuas (números) o discretas (texto o enteros con pocos valores únicos)
- Los valores faltantes se ignoran automáticamente
- El sistema identifica automáticamente el tipo de cada variable

## 🎯 Ejemplos de Uso

### Dataset Iris (incluido)
Un dataset clásico de clasificación con 3 clases de flores:
- 4 atributos continuos (longitud y ancho de sépalos y pétalos)
- 3 clases: setosa, versicolor, virginica

Para probar:
1. Cargar `iris_dataset.csv`
2. Seleccionar columna "species" como objetivo
3. Usar método "Distribución Gaussiana" para variables continuas
4. Entrenar con 70% de datos
5. Ver resultados en la pestaña "Resultados"

## 🔍 Tips y Recomendaciones

### Selección del Método para Variables Continuas

1. **Distribución Gaussiana**
   - ✅ Rápido y eficiente
   - ✅ Funciona bien cuando los datos son aproximadamente normales
   - ❌ Asume normalidad de los datos

2. **KDE (Kernel Density Estimation)**
   - ✅ No asume distribución específica
   - ✅ Captura distribuciones complejas o multimodales
   - ❌ Más lento con datasets grandes
   - ❌ Puede sufrir overfitting con pocos datos

3. **Discretización**
   - ✅ Simple de interpretar
   - ✅ Robusto ante outliers
   - ❌ Pérdida de información al discretizar
   - ❌ Sensible al número de bins

### Configuración de Parámetros

- **Laplace Alpha**: 
  - Aumentar si hay clases o valores poco frecuentes
  - Valor típico: 1.0

- **Número de Bins**:
  - Pocos bins (3-5): Mayor generalización, menos detalle
  - Muchos bins (>10): Más detalle, riesgo de overfitting

- **% Entrenamiento**:
  - 70-80%: Balance común
  - Más alto (>80%): Usar con datasets grandes
  - Más bajo (<70%): Usar para mejor evaluación con pocos datos


### Error al cargar dataset
- Verifica que el archivo sea CSV válido
- Asegúrate de que tenga encabezados
- Revisa que no tenga caracteres especiales en nombres de columnas

### Accuracy muy bajo
- Verifica que las características sean relevantes para la clasificación
- Prueba diferentes métodos para variables continuas
- Aumenta el porcentaje de datos de entrenamiento
- Revisa si hay desbalance de clases en el dataset


## 📊 Interpretación de Resultados

### Accuracy
- Porcentaje de predicciones correctas
- 0.0 (0%) = Peor, 1.0 (100%) = Perfecto

### Precisión
- De las instancias predichas como clase X, cuántas realmente lo son
- Alta precisión = Pocas falsas alarmas

### Recall
- De las instancias que son clase X, cuántas se detectaron
- Alto recall = Pocas instancias perdidas

### F1-Score
- Media armónica entre precisión y recall
- Balance entre ambas métricas

### Matriz de Confusión
- Filas: Clases verdaderas
- Columnas: Clases predichas
- Diagonal: Predicciones correctas
- Fuera de diagonal: Errores

```
## 👨‍💻 Desarrollo

Interfaz: Tkinter (incluido en Python)
Librerías principales:
- NumPy: Operaciones numéricas
- Pandas: Manejo de datos
- SciPy: Funciones estadísticas y KDE
