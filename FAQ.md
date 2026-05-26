# Preguntas Frecuentes (FAQ)

## 📋 General

### ¿Qué es Naïve Bayes?
Naïve Bayes es un algoritmo de clasificación basado en el teorema de Bayes con la suposición de independencia entre características. A pesar de su simplicidad, es muy efectivo para muchos problemas reales.

### ¿Para qué tipo de problemas sirve?
- Clasificación de texto (spam, sentimientos)
- Diagnóstico médico
- Predicción de categorías
- Filtrado de contenido
- Análisis de riesgo crediticio
- Cualquier problema de clasificación supervisada

### ¿Cuándo NO usar Naïve Bayes?
- Cuando las características son altamente dependientes entre sí
- Problemas de regresión (solo hace clasificación)
- Cuando necesitas entender relaciones complejas entre variables

---

## 🔧 Instalación y Configuración

### ¿Qué versión de Python necesito?
Python 3.7 o superior. Puedes verificar tu versión con:
```bash
python --version
```

### Error: "pip no se reconoce como comando"
**Windows:**
1. Reinstala Python desde python.org
2. Marca "Add Python to PATH" durante instalación

**Linux:**
```bash
sudo apt-get install python3-pip
```

### ¿Puedo usar un entorno virtual?
Sí, es recomendado:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 📊 Uso del Dataset

### ¿Qué formato debe tener mi dataset?
Archivo CSV con:
- Primera fila: nombres de columnas
- Una columna para la clase objetivo
- Resto de columnas: características
- Ejemplo:
  ```csv
  feature1,feature2,categoria
  1.5,alto,A
  2.3,bajo,B
  ```

### ¿Puede tener valores faltantes?
Sí, el sistema los ignora automáticamente. Sin embargo, es mejor limpiar el dataset antes para mejores resultados.

### ¿Cuántos datos necesito?
- **Mínimo**: 50-100 instancias
- **Recomendado**: 200-500 instancias
- **Óptimo**: 1000+ instancias

Más datos = mejor generalización.

### ¿Qué pasa si mis clases están desbalanceadas?
El clasificador funcionará, pero las clases minoritarias pueden tener menor recall. Considera:
- Usar más datos de entrenamiento
- Generar datos sintéticos (oversampling)
- Evaluar con F1-Score en lugar de solo Accuracy

### ¿Puedo mezclar números y texto?
Sí, el sistema detecta automáticamente qué columnas son continuas (números) y cuáles discretas (texto/categorías).

---

## ⚙️ Configuración del Modelo

### ¿Qué método debo elegir para variables continuas?

**Distribución Gaussiana:**
- ✅ Usa cuando: Datos aproximadamente normales
- ✅ Ventajas: Rápido, eficiente
- ❌ Desventajas: Asume normalidad

**KDE:**
- ✅ Usa cuando: Distribuciones complejas o multimodales
- ✅ Ventajas: No asume distribución
- ❌ Desventajas: Más lento, necesita más datos

**Discretización (Anchos Iguales):**
- ✅ Usa cuando: Datos con outliers
- ✅ Ventajas: Simple, robusto
- ❌ Desventajas: Pérdida de información

**Discretización (Frecuencias Iguales):**
- ✅ Usa cuando: Distribución muy desigual
- ✅ Ventajas: Bins balanceados
- ❌ Desventajas: Bins de anchos diferentes

**¿No estás seguro?** Prueba Gaussiana primero.

### ¿Qué es Laplace Alpha?
Parámetro de suavizado para variables discretas. Previene probabilidad cero cuando un valor no aparece en entrenamiento.
- **α = 1.0**: Valor estándar (recomendado)
- **α > 1**: Más suavizado (mayor generalización)
- **α < 1**: Menos suavizado (más específico)

### ¿Cuántos bins usar en discretización?
- **3-5 bins**: Pocos datos, alta generalización
- **5-10 bins**: Casos generales (recomendado)
- **10+ bins**: Muchos datos, más detalle

Muy pocos = pérdida de información
Muy muchos = overfitting

### ¿Qué porcentaje de entrenamiento usar?
- **60-70%**: Datasets pequeños (<500 instancias)
- **70-80%**: Datasets medianos (500-5000)
- **80-90%**: Datasets grandes (>5000)

Más entrenamiento = mejor modelo, pero menor validación

---

## 📈 Interpretación de Resultados

### Mi Accuracy es 50%, ¿es malo?
Depende del número de clases:
- **2 clases**: 50% = azar (muy malo)
- **10 clases**: 50% = muy bueno (azar sería 10%)

Compara con el baseline (elegir clase más frecuente).

### ¿Qué métrica es más importante?

**Para clases balanceadas:** Accuracy
**Para clases desbalanceadas:** F1-Score
**Para detectar fraudes/spam:** Recall (no perder positivos)
**Para diagnósticos médicos:** Precision (evitar falsos positivos)

### ¿Qué significa la matriz de confusión?
```
                Predicho A    Predicho B
Real A              85            15       <- 85 correctos, 15 errores
Real B              10            90       <- 90 correctos, 10 errores
```

Diagonal = Predicciones correctas
Fuera diagonal = Errores

### ¿Precision o Recall?

**Alta Precision, Bajo Recall:**
- Predice positivos solo cuando está muy seguro
- Pocos falsos positivos, pero pierde muchos casos reales

**Alto Recall, Baja Precision:**
- Predice positivos generosamente
- Detecta casi todos los casos, pero con falsas alarmas

**F1-Score:** Balance entre ambos

---

## 🐛 Problemas Comunes

### Accuracy muy bajo (<30%)
1. Verifica que la columna objetivo sea correcta
2. Asegúrate de que las características sean relevantes
3. Prueba otro método para variables continuas
4. Revisa si hay errores en los datos

### El programa se cierra inmediatamente
**Windows:** Ejecuta desde terminal para ver errores:
```bash
python main.py
```

**Linux:** Verifica permisos:
```bash
chmod +x dist/NaiveBayesClassifier
```

### Error: "No module named 'pandas'"
```bash
pip install -r requirements.txt
```

### Error al cargar dataset: "UnicodeDecodeError"
Tu CSV tiene codificación especial. Resuélvelo:
1. Abre el CSV en Excel o LibreOffice
2. Guárdalo como CSV UTF-8

### Error: "ValueError: could not convert string to float"
Tu dataset tiene valores no numéricos en columnas que deberían ser numéricas. Limpia los datos o codifica las categorías.

### La predicción toma mucho tiempo
- **KDE** es lento con muchos datos. Prueba Gaussiana
- Dataset muy grande: considera muestreo
- Demasiadas características: reduce dimensionalidad

### Warnings de SciPy
Son normales, no afectan el funcionamiento. Para ocultarlos, el código ya incluye:
```python
warnings.filterwarnings('ignore')
```

---

## 🔨 Compilación

### El ejecutable es muy grande (>100 MB)
Normal con PyInstaller. Incluye Python completo y librerías. Considera:
- Comprimir con UPX: `pyinstaller --upx-dir=path/to/upx`
- Aceptar el tamaño (usuarios no necesitan instalar nada)

### Antivirus bloquea el ejecutable
PyInstaller genera falsos positivos. Soluciones:
1. Agrega excepción en tu antivirus
2. Distribuye el código fuente
3. Firma digitalmente el ejecutable (avanzado)

### Error: "Cannot find Python"
Compila en el sistema objetivo:
- Windows → compilar en Windows
- Linux → compilar en Linux

---

## 📚 Mejores Prácticas

### Preparación de Datos
1. Limpia valores faltantes
2. Normaliza nombres de columnas (sin espacios)
3. Codifica categorías consistentemente
4. Elimina duplicados

### Experimentación
1. Prueba con diferentes métodos
2. Varia el porcentaje de entrenamiento
3. Compara múltiples métricas
4. Usa diferentes semillas aleatorias

### Documentación de Resultados
1. Guarda los parámetros usados
2. Exporta las métricas
3. Documenta observaciones
4. Compara con otros modelos

---

## 🚀 Casos de Uso Reales

### Ejemplo 1: Clasificación de Correos (Spam)
- **Características**: Palabras clave, longitud, remitente
- **Método**: Discretización (palabras son frecuencias)
- **Resultado esperado**: 85-95% accuracy

### Ejemplo 2: Diagnóstico Médico
- **Características**: Síntomas, valores de laboratorio
- **Método**: Gaussiana (valores de laboratorio son continuos)
- **Prioridad**: Alto Recall (no perder casos positivos)

### Ejemplo 3: Clasificación de Flores (Iris)
- **Características**: Medidas morfológicas
- **Método**: Gaussiana
- **Resultado esperado**: 90-95% accuracy

---

## 💡 Tips y Trucos

### Mejorar el Rendimiento
1. **Más datos**: Siempre ayuda
2. **Feature engineering**: Crea características derivadas
3. **Limpieza**: Elimina outliers extremos
4. **Balance**: Iguala el número de instancias por clase

### Debugging
1. Empieza con dataset pequeño conocido (Iris)
2. Verifica que las métricas sean razonables
3. Inspecciona predicciones individuales
4. Compara con implementaciones conocidas (scikit-learn)

### Productividad
1. Usa `generate_datasets.py` para experimentos rápidos
2. Crea templates de configuración para datasets similares
3. Automatiza con scripts la carga y evaluación

---

## ❓ ¿Más Preguntas?

Si tu pregunta no está aquí:
1. Revisa **README.md** para detalles generales
2. Consulta **TECHNICAL_NOTES.md** para detalles técnicos
3. Ejecuta **test_classifier.py** para verificar funcionamiento
4. Revisa los comentarios en el código fuente

---

**¡Éxito con tu proyecto!** Si encuentras un bug o tienes una sugerencia, documéntalo para mejoras futuras.
