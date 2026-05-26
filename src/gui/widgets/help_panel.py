"""
Panel de Ayuda Contextual — versión estable Linux/Windows/Mac
"""

import tkinter as tk
from tkinter import ttk
from gui.styles import COLORS, FONTS

METHOD_HELP = {
    "gaussian": {
        "title":   "Distribución Gaussiana (Normal)",
        "icon":    "📊",
        "color":   COLORS["gaussian"],
        "bg":      COLORS["gaussian_light"],
        "formula": "P(xᵢ|C) = (1/√2πσ²) × e^(−(xᵢ−μ)²/2σ²)",
        "what":    "Modela cada variable continua como si siguiera una distribución normal (campana de Gauss). Calcula la media (μ) y desviación estándar (σ) de cada variable por clase.",
        "how":     "1. Calcula μ y σ de cada atributo por clase.\n2. Al clasificar, evalúa la densidad de probabilidad usando la fórmula gaussiana.\n3. Multiplica las probabilidades de todos los atributos.",
        "when":    "Cuando los datos siguen distribución aproximadamente normal. Primera opción recomendada.",
        "pros":    ["⚡ Muy rápido", "📉 Requiere pocos datos", "🔢 Simple de interpretar"],
        "cons":    ["⚠ Asume normalidad", "❌ Mal con distribuciones bimodales"],
    },
    "kde": {
        "title":   "KDE — Kernel Density Estimation",
        "icon":    "〰",
        "color":   COLORS["kde"],
        "bg":      COLORS["kde_light"],
        "formula": "P(x|C) ≈ (1/nh) × Σ K((x − xⱼ)/h)",
        "what":    "Estimación no paramétrica. Coloca una 'función kernel' (campana pequeña) sobre cada punto de entrenamiento y las suma para obtener la densidad.",
        "how":     "1. Guarda todos los puntos de entrenamiento por clase.\n2. Al clasificar, suma la contribución de puntos cercanos.\n3. El bandwidth (h) controla la suavidad de la curva.",
        "when":    "Cuando los datos tienen distribuciones complejas, multimodales o asimétricas.",
        "pros":    ["🎯 No asume distribución", "〰 Captura formas complejas"],
        "cons":    ["🐢 Más lento", "💾 Necesita más datos", "⚙ Sensible al bandwidth"],
    },
    "equal_width": {
        "title":   "Discretización — Anchos Iguales",
        "icon":    "📏",
        "color":   COLORS["ew"],
        "bg":      COLORS["ew_light"],
        "formula": "Ancho = (máx − mín) / n_bins",
        "what":    "Divide el rango total de valores en intervalos del mismo tamaño. Luego trata cada intervalo como categoría discreta con Laplace smoothing.",
        "how":     "1. Calcula mín y máx del atributo.\n2. Divide el rango en n intervalos iguales.\n3. Asigna cada valor al bin correspondiente.\n4. Calcula P(bin|clase) con Laplace smoothing.",
        "when":    "Datos sin muchos outliers y distribución relativamente uniforme.",
        "pros":    ["📖 Fácil de interpretar", "⚡ Rápido"],
        "cons":    ["⚠ Sensible a outliers", "📊 Bins pueden quedar vacíos"],
    },
    "equal_freq": {
        "title":   "Discretización — Frecuencias Iguales",
        "icon":    "⚖",
        "color":   COLORS["ef"],
        "bg":      COLORS["ef_light"],
        "formula": "Cada bin ≈ n_muestras / n_bins instancias",
        "what":    "Coloca los cortes en percentiles equidistantes. Cada intervalo tiene aproximadamente el mismo número de instancias, aunque los anchos sean distintos.",
        "how":     "1. Ordena los valores del atributo.\n2. Coloca cortes en percentiles equidistantes.\n3. Cada bin tiene ~igual cantidad de puntos.\n4. Calcula P(bin|clase) con Laplace smoothing.",
        "when":    "Distribuciones muy sesgadas o con muchos outliers.",
        "pros":    ["⚖ Bins balanceados", "🛡 Robusto a outliers"],
        "cons":    ["📐 Bins de ancho variable", "🔍 Menos intuitivo"],
    },
}

PARAM_HELP = {
    "laplace": {
        "title": "Laplace Smoothing (Alpha)",
        "icon":  "🔢", "color": COLORS["primary"],
        "text":  "Evita probabilidades = 0 cuando un valor no aparece en entrenamiento.\n\n• α = 0.0 → sin suavizado (puede dar P=0)\n• α = 1.0 → Laplace estándar (recomendado) ✓\n• α > 1.0 → más suavizado / mayor generalización\n\nFórmula: P(x|C) = (count + α) / (total + α × n_valores)",
    },
    "nbins": {
        "title": "Número de Bins",
        "icon":  "📊", "color": COLORS["primary"],
        "text":  "Cuántos intervalos se crean al discretizar variables continuas.\n\n• 3-4 bins → Muy general, pierde información\n• 5-10 bins → Balance recomendado ✓\n• 10+ bins → Más detalle, riesgo de sobreajuste\n\nRegla: √n donde n = número de instancias.",
    },
    "kde_bw": {
        "title": "Bandwidth de KDE",
        "icon":  "〰", "color": COLORS["kde"],
        "text":  "Controla la suavidad de la curva KDE.\n\n• scott → h = n^(−1/(d+4)) × σ  (recomendado ✓)\n• silverman → similar, más conservador\n\nBandwidth pequeño → curva detallada (puede sobreajustar)\nBandwidth grande → curva suave (puede perder detalle)",
    },
    "split": {
        "title": "División Entrenamiento / Prueba",
        "icon":  "✂", "color": COLORS["primary"],
        "text":  "Porcentaje del dataset para entrenar vs evaluar.\n\n• 60% → Más evaluación, menos entrenamiento\n• 70-80% → Balance recomendado ✓\n• 90% → Modelo más potente, evaluación menos confiable\n\nLos datos de prueba NUNCA participan en el entrenamiento.",
    },
}


class HelpPanel(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=COLORS["bg_card"], **kw)
        self._placeholder()

    def _placeholder(self):
        self._clear()
        tk.Label(self,
                 text="💡\n\nSelecciona un\nmétodo para ver\nsu explicación",
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 font=FONTS["body"], justify="center").pack(expand=True, pady=40)

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_method(self, key: str):
        d = METHOD_HELP.get(key)
        if not d:
            self._placeholder(); return
        self._clear()

        # Header
        hdr = tk.Frame(self, bg=d["color"])
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"{d['icon']}  {d['title']}",
                 bg=d["color"], fg="#ffffff", font=FONTS["subtitle"],
                 padx=12, pady=10, anchor="w").pack(fill="x")

        # Cuerpo con scroll
        canvas = tk.Canvas(self, bg=COLORS["bg_card"],
                           highlightthickness=0, borderwidth=0)
        vsb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=COLORS["bg_card"])
        inner.bind("<Configure>",
                   lambda e: canvas.configure(
                       scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        p = 10

        def sec(title):
            tk.Label(inner, text=title, bg=COLORS["bg_card"],
                     fg=COLORS["text_secondary"],
                     font=FONTS["small_bold"]).pack(anchor="w", padx=p,
                                                    pady=(8, 1))
            tk.Frame(inner, bg=COLORS["border"],
                     height=1).pack(fill="x", padx=p, pady=(0, 4))

        sec("📐 Fórmula")
        code_f = tk.Frame(inner, bg=COLORS["bg_code"])
        code_f.pack(fill="x", padx=p, pady=(0, 8))
        tk.Label(code_f, text=d["formula"], bg=COLORS["bg_code"],
                 fg="#a8d8ff", font=FONTS["mono"],
                 padx=8, pady=5, anchor="w").pack(fill="x")

        sec("🔍 ¿Qué hace?")
        tk.Label(inner, text=d["what"], bg=COLORS["bg_card"],
                 fg=COLORS["text"], font=FONTS["small"],
                 wraplength=350, justify="left",
                 anchor="w").pack(fill="x", padx=p, pady=(0, 8))

        sec("⚙ ¿Cómo funciona?")
        tk.Label(inner, text=d["how"], bg=COLORS["bg_card"],
                 fg=COLORS["text"], font=FONTS["small"],
                 wraplength=350, justify="left",
                 anchor="w").pack(fill="x", padx=p, pady=(0, 8))

        sec("🎯 ¿Cuándo usarlo?")
        wf = tk.Frame(inner, bg=COLORS["info_light"])
        wf.pack(fill="x", padx=p, pady=(0, 8))
        tk.Label(wf, text=d["when"], bg=COLORS["info_light"],
                 fg=COLORS["text"], font=FONTS["small"],
                 wraplength=350, justify="left",
                 padx=8, pady=6).pack(anchor="w")

        sec("✅ Ventajas")
        for pro in d["pros"]:
            tk.Label(inner, text=pro, bg=COLORS["bg_card"],
                     fg=COLORS["success"],
                     font=FONTS["small"]).pack(anchor="w", padx=p, pady=1)

        sec("⚠ Limitaciones")
        for con in d["cons"]:
            tk.Label(inner, text=con, bg=COLORS["bg_card"],
                     fg=COLORS["warning"],
                     font=FONTS["small"]).pack(anchor="w", padx=p, pady=1)

        tk.Frame(inner, bg=COLORS["bg_card"], height=12).pack()

    def show_param(self, key: str):
        d = PARAM_HELP.get(key)
        if not d:
            return
        self._clear()
        hdr = tk.Frame(self, bg=d["color"])
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"{d['icon']}  {d['title']}",
                 bg=d["color"], fg="#ffffff", font=FONTS["subtitle"],
                 padx=12, pady=10, anchor="w").pack(fill="x")
        body = tk.Frame(self, bg=COLORS["bg_card"])
        body.pack(fill="both", expand=True, padx=12, pady=12)
        tk.Label(body, text=d["text"], bg=COLORS["bg_card"],
                 fg=COLORS["text"], font=FONTS["small"],
                 wraplength=350, justify="left",
                 anchor="nw").pack(fill="x")
