# 📂 Carpeta `data/`

Contiene los datasets de ejemplo incluidos con el proyecto.

## Archivos Incluidos

### `iris_dataset.csv`
- **Instancias**: 150
- **Clases**: 3 (setosa, versicolor, virginica)
- **Atributos**: 4 (sepal_length, sepal_width, petal_length, petal_width)
- **Tipo**: Solo variables continuas
- **Uso**: Cargar en la aplicación, seleccionar columna `species` como objetivo

### `iris_test_instances.csv`
- **Instancias**: 6 (sin etiqueta de clase)
- **Uso**: Cargar en pestaña "Predicción" para clasificar con el modelo entrenado

---

## Agregar Tu Propio Dataset

Coloca tu archivo CSV en esta carpeta. Formato requerido:

```csv
atributo1,atributo2,clase
valor1,valor2,A
valor3,valor4,B
```

---

## Datasets Externos Recomendados

Para descargar y probar con el clasificador:

| Dataset           | Fuente      | Instancias |
|-------------------|-------------|------------|
| Titanic           | Kaggle      | 891        |
| SMS Spam          | UCI ML      | 5574       |
| Wine Quality      | UCI ML      | 6497       |
| Heart Disease     | UCI ML      | 303        |
| Mushroom          | UCI ML      | 8124       |
| Breast Cancer     | UCI ML/sklearn | 569     |
| Car Evaluation    | UCI ML      | 1728       |

Ver la pestaña **"🗃 Datasets"** en la aplicación para descripciones completas y enlaces.

**URL UCI ML Repository**: https://archive.ics.uci.edu/ml/datasets.php
