import tkinter as tk
from tkinter import ttk
from gui.styles import COLORS, FONTS
from gui.widgets.components import InfoBox

DATASETS = [
    {
        "name": "Iris Flower Dataset", "icon": "🌸",
        "difficulty": "Principiante", "diff_style": "success",
        "classes": 3, "features": 4, "samples": 150,
        "feature_types": "Solo continuas",
        "best_method": "Gaussiana",
        "url": "UCI ML Repository / sklearn.datasets",
        "color": COLORS["success"], "bg": COLORS["success_light"],
        "description": (
            "El dataset clásico de ML. Clasifica 3 especies de flores iris "
            "(setosa, versicolor, virginica) con largo y ancho de sépalos y pétalos. "
            "Incluido en este proyecto (iris_dataset.csv)."
        ),
        "why_good": (
            "Datos limpios, bien balanceados, variables normalmente distribuidas. "
            "Naïve Bayes alcanza ~95% de accuracy con Gaussiana. "
            "Perfecto como primera prueba del clasificador."
        ),
        "what_to_learn": [
            "Funcionamiento básico del clasificador",
            "Comparar los 4 métodos para variables continuas",
            "Interpretar matriz de confusión multi-clase",
        ],
    },
    {
        "name": "Titanic Survival", "icon": "🚢",
        "difficulty": "Principiante", "diff_style": "success",
        "classes": 2, "features": "6-8", "samples": 891,
        "feature_types": "Mixtas (continuas + discretas)",
        "best_method": "Gaussiana + Laplace",
        "url": "Kaggle.com → kaggle.com/c/titanic",
        "color": COLORS["primary"], "bg": COLORS["primary_light"],
        "description": (
            "Predice si un pasajero del Titanic sobrevivió basándose en "
            "edad, sexo, clase del boleto, tarifa, número de familiares a bordo, etc."
        ),
        "why_good": (
            "Ideal para practicar con variables MIXTAS: continuas (edad, tarifa) "
            "y discretas (sexo, clase). Enseña el manejo de valores faltantes. "
            "Accuracy típico con Naïve Bayes: ~78-82%."
        ),
        "what_to_learn": [
            "Manejo de variables mixtas (continuas + discretas)",
            "Efecto del Laplace Smoothing en variables con muchos nulos",
            "Precisión vs Recall en clasificación binaria",
        ],
    },
    {
        "name": "SMS Spam Collection", "icon": "📱",
        "difficulty": "Intermedio", "diff_style": "warning",
        "classes": 2, "features": "Variable", "samples": 5574,
        "feature_types": "Discretas (frecuencias de palabras)",
        "best_method": "Laplace Smoothing",
        "url": "UCI ML Repository → archive.ics.uci.edu",
        "color": COLORS["ef"], "bg": COLORS["ef_light"],
        "description": (
            "Clasifica SMS como spam o legítimo. El dataset más clásico "
            "para demostrar la fortaleza de Naïve Bayes en clasificación de texto. "
            "5,574 mensajes etiquetados."
        ),
        "why_good": (
            "Naïve Bayes fue diseñado para filtrado de spam. "
            "100% variables discretas. Accuracy > 97%. "
            "Ideal para entender por qué Laplace es crítico cuando aparecen palabras nuevas."
        ),
        "what_to_learn": [
            "Por qué Naïve Bayes es ideal para clasificación de texto",
            "Laplace Smoothing crítico: palabras nuevas → P=0 sin suavizado",
            "Métricas en datos desbalanceados (spam es ~13% del total)",
        ],
    },
    {
        "name": "Wine Quality", "icon": "🍷",
        "difficulty": "Intermedio", "diff_style": "warning",
        "classes": "3-6", "features": 11, "samples": 6497,
        "feature_types": "Solo continuas (distribuciones no normales)",
        "best_method": "KDE o Gaussiana",
        "url": "UCI ML Repository → archive.ics.uci.edu",
        "color": COLORS["error"], "bg": COLORS["error_light"],
        "description": (
            "Predice la calidad de vinos (escala 3-8) con propiedades "
            "fisicoquímicas: acidez, azúcar residual, pH, alcohol, etc. "
            "Disponible para vinos tintos y blancos."
        ),
        "why_good": (
            "Muchas variables tienen distribuciones no normales y sesgadas, "
            "lo que hace KDE más apropiado que Gaussiana. "
            "Demuestra cuándo el método importa. Accuracy típico: 55-65% (problema difícil)."
        ),
        "what_to_learn": [
            "Diferencia práctica entre Gaussiana y KDE en datos no normales",
            "Clasificación multi-clase (hasta 6 categorías)",
            "Cómo interpretar accuracy bajo en problemas inherentemente difíciles",
        ],
    },
    {
        "name": "Heart Disease (Cleveland)", "icon": "❤",
        "difficulty": "Intermedio", "diff_style": "warning",
        "classes": 2, "features": 13, "samples": 303,
        "feature_types": "Mixtas",
        "best_method": "Gaussiana + Laplace",
        "url": "UCI ML Repository → archive.ics.uci.edu",
        "color": COLORS["error"], "bg": "#fff5f5",
        "description": (
            "Predice presencia o ausencia de enfermedad cardíaca con "
            "13 atributos: edad, presión arterial, colesterol, "
            "tipo de dolor de pecho, frecuencia cardíaca máxima y más."
        ),
        "why_good": (
            "Ideal para discutir balance Precisión vs Recall en medicina. "
            "¿Qué es peor: falso positivo (alarma innecesaria) o "
            "falso negativo (no detectar una enfermedad real)? "
            "Accuracy típico: 80-85%."
        ),
        "what_to_learn": [
            "Importancia del Recall en aplicaciones médicas críticas",
            "Análisis ético de errores: ¿cuál es más costoso?",
            "Variables mixtas en contexto de diagnóstico médico",
        ],
    },
    {
        "name": "Mushroom Classification", "icon": "🍄",
        "difficulty": "Principiante", "diff_style": "success",
        "classes": 2, "features": 22, "samples": 8124,
        "feature_types": "Solo discretas (22 variables categóricas)",
        "best_method": "Laplace Smoothing puro",
        "url": "UCI ML Repository → archive.ics.uci.edu",
        "color": COLORS["ew"], "bg": COLORS["ew_light"],
        "description": (
            "Clasifica hongos como comestibles o venenosos. "
            "22 características categóricas: color del sombrero, forma, "
            "olor, textura de laminillas, hábitat, etc."
        ),
        "why_good": (
            "100% variables discretas — demuestra que Naïve Bayes funciona "
            "excelentemente sin necesitar métodos continuos. "
            "Accuracy > 99%. Laplace Smoothing es crítico aquí."
        ),
        "what_to_learn": [
            "Clasificación puramente con variables discretas",
            "Por qué Laplace es crítico con valores no vistos en prueba",
            "Alta accuracy no requiere modelos complejos",
        ],
    },
    {
        "name": "Breast Cancer Wisconsin", "icon": "🔬",
        "difficulty": "Principiante", "diff_style": "success",
        "classes": 2, "features": 30, "samples": 569,
        "feature_types": "Solo continuas",
        "best_method": "Gaussiana",
        "url": "UCI ML / sklearn.datasets.load_breast_cancer()",
        "color": COLORS["kde"], "bg": COLORS["kde_light"],
        "description": (
            "Clasifica tumores como malignos o benignos con 30 características "
            "extraídas de imágenes de biopsias: radio, textura, perímetro, "
            "área, suavidad, etc."
        ),
        "why_good": (
            "Alto accuracy (93-97%) con Gaussiana. Discute el dilema médico: "
            "¿qué es peor, un falso negativo (perder un cáncer) "
            "o un falso positivo (biopsia innecesaria)?"
        ),
        "what_to_learn": [
            "Clasificación binaria con muchas variables continuas (30)",
            "Aplicaciones médicas y ética del error de clasificación",
            "Comparar Precisión vs Recall en contexto real con consecuencias",
        ],
    },
    {
        "name": "Car Evaluation", "icon": "🚗",
        "difficulty": "Principiante", "diff_style": "success",
        "classes": 4, "features": 6, "samples": 1728,
        "feature_types": "Solo discretas (ordinales)",
        "best_method": "Laplace Smoothing",
        "url": "UCI ML Repository → archive.ics.uci.edu",
        "color": COLORS["gaussian"], "bg": COLORS["gaussian_light"],
        "description": (
            "Evalúa aceptabilidad de autos (inaceptable, aceptable, bueno, "
            "muy bueno) con 6 variables: precio de compra, mantenimiento, "
            "número de puertas, capacidad, maletero, seguridad."
        ),
        "why_good": (
            "Dataset sintético perfecto para multi-clase con variables ordinales. "
            "Muestra limitaciones de la suposición de independencia "
            "(precio y mantenimiento están correlacionados). "
            "Accuracy típico: 85-90%."
        ),
        "what_to_learn": [
            "Clasificación multi-clase (4 categorías) con discretas ordinales",
            "Limitaciones de la suposición de independencia de Naïve Bayes",
            "Variables ordinales tratadas como nominales: ¿afecta el resultado?",
        ],
    },
]


class DatasetsTab(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=COLORS["bg_main"], **kw)
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["bg_dark"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="🗃  Datasets Recomendados para Naïve Bayes",
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"],
                 font=FONTS["title"], padx=18, pady=12,
                 anchor="w").pack(fill="x")
        tk.Label(
    hdr,
    text="Selecciona un dataset para ver descripción, "
         "por qué es ideal y qué aprenderás.",
    bg=COLORS["bg_dark"],
    fg=COLORS["text_header"],
    font=FONTS["small"],
    padx=20,
    anchor="w"
).pack(fill="x", pady=(0, 10))

        # Filtros de dificultad
        fbar = tk.Frame(self, bg=COLORS["bg_main"])
        fbar.pack(fill="x", padx=10, pady=6)
        tk.Label(fbar, text="Filtrar por dificultad:",
                 bg=COLORS["bg_main"], fg=COLORS["text_secondary"],
                 font=FONTS["small_bold"]).pack(side="left")
        self._filter = tk.StringVar(value="Todos")
        for level in ["Todos", "Principiante", "Intermedio"]:
            ttk.Radiobutton(fbar, text=level,
                            variable=self._filter, value=level,
                            command=self._apply_filter).pack(side="left", padx=8)

        # Split: lista (izq) + detalle (der) — sin PanedWindow
        body = tk.Frame(self, bg=COLORS["bg_main"])
        body.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Lista izquierda con scroll
        list_outer = tk.Frame(body, bg=COLORS["bg_main"], width=300)
        list_outer.pack(side="left", fill="y")
        list_outer.pack_propagate(False)

        self._list_canvas = tk.Canvas(list_outer, bg=COLORS["bg_main"],
                                      highlightthickness=0, borderwidth=0,
                                      width=296)
        lvsb = ttk.Scrollbar(list_outer, orient="vertical",
                              command=self._list_canvas.yview)
        self._list_inner = tk.Frame(self._list_canvas, bg=COLORS["bg_main"])
        self._list_inner.bind("<Configure>",
                              lambda e: self._list_canvas.configure(
                                  scrollregion=self._list_canvas.bbox("all")))
        self._list_canvas.create_window((0, 0), window=self._list_inner,
                                        anchor="nw")
        self._list_canvas.configure(yscrollcommand=lvsb.set)
        lvsb.pack(side="right", fill="y")
        self._list_canvas.pack(side="left", fill="both", expand=True)
        self._list_canvas.bind("<Button-4>",
                               lambda e: self._list_canvas.yview_scroll(-1, "units"))
        self._list_canvas.bind("<Button-5>",
                               lambda e: self._list_canvas.yview_scroll(1, "units"))

        # Separador vertical
        tk.Frame(body, bg=COLORS["border"], width=1).pack(side="left", fill="y")

        # Detalle derecho con scroll
        detail_outer = tk.Frame(body, bg=COLORS["bg_card"])
        detail_outer.pack(side="right", fill="both", expand=True)

        self._det_canvas = tk.Canvas(detail_outer, bg=COLORS["bg_card"],
                                     highlightthickness=0, borderwidth=0)
        dvsb = ttk.Scrollbar(detail_outer, orient="vertical",
                              command=self._det_canvas.yview)
        self._det_inner = tk.Frame(self._det_canvas, bg=COLORS["bg_card"])
        self._det_inner.bind("<Configure>",
                             lambda e: self._det_canvas.configure(
                                 scrollregion=self._det_canvas.bbox("all")))
        self._det_win = self._det_canvas.create_window(
            (0, 0), window=self._det_inner, anchor="nw")
        self._det_canvas.configure(yscrollcommand=dvsb.set)
        dvsb.pack(side="right", fill="y")
        self._det_canvas.pack(side="left", fill="both", expand=True)
        self._det_canvas.bind("<Configure>",
                              lambda e: self._det_canvas.itemconfig(
                                  self._det_win, width=e.width))
        self._det_canvas.bind("<Button-4>",
                              lambda e: self._det_canvas.yview_scroll(-1, "units"))
        self._det_canvas.bind("<Button-5>",
                              lambda e: self._det_canvas.yview_scroll(1, "units"))

        self._render_list(DATASETS)
        self._show_detail(DATASETS[0])

    def _apply_filter(self):
        f = self._filter.get()
        filtered = DATASETS if f == "Todos" else [
            d for d in DATASETS if d["difficulty"] == f]
        self._render_list(filtered)
        if filtered:
            self._show_detail(filtered[0])

    def _render_list(self, datasets):
        for w in self._list_inner.winfo_children():
            w.destroy()

        diff_colors = {
            "success": (COLORS["success_light"], COLORS["success"]),
            "warning": (COLORS["warning_light"], COLORS["warning"]),
        }

        for ds in datasets:
            card = tk.Frame(self._list_inner, bg=COLORS["bg_card"],
                            relief="solid", bd=1, cursor="hand2")
            card.pack(fill="x", padx=4, pady=3)

            top = tk.Frame(card, bg=ds["bg"])
            top.pack(fill="x")
            tk.Label(top, text=f"{ds['icon']}  {ds['name']}",
                     bg=ds["bg"], fg=ds["color"],
                     font=FONTS["body_bold"],
                     padx=8, pady=6, anchor="w").pack(side="left", fill="x",
                                                       expand=True)
            dbg, dfg = diff_colors.get(ds["diff_style"],
                                        (COLORS["border"],
                                         COLORS["text_secondary"]))
            tk.Label(top, text=ds["difficulty"],
                     bg=dbg, fg=dfg, font=FONTS["small_bold"],
                     padx=6, pady=2).pack(side="right", padx=6, pady=6)

            info = tk.Frame(card, bg=COLORS["bg_card"])
            info.pack(fill="x", padx=8, pady=(3, 6))
            tk.Label(info,
                     text=f"{ds['samples']} instancias · "
                          f"{ds['features']} atrib. · {ds['classes']} clases",
                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                     font=FONTS["small"]).pack(anchor="w")

            click_handler = lambda e, d=ds: self._show_detail(d)
            for w in [card, top, info] + \
                     list(top.winfo_children()) + \
                     list(info.winfo_children()):
                try:
                    w.bind("<Button-1>", click_handler)
                except Exception:
                    pass

    def _show_detail(self, ds):
        for w in self._det_inner.winfo_children():
            w.destroy()
        self._det_canvas.yview_moveto(0)

        f = self._det_inner

        # Header coloreado
        hdr = tk.Frame(f, bg=ds["color"])
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"{ds['icon']}  {ds['name']}",
                 bg=ds["color"], fg="#ffffff", font=FONTS["title"],
                 padx=18, pady=12, anchor="w").pack(fill="x")

        # Barra de meta-datos
        meta = tk.Frame(f, bg=ds["bg"])
        meta.pack(fill="x")
        for lbl, val in [("Instancias", str(ds["samples"])),
                         ("Atributos", str(ds["features"])),
                         ("Clases", str(ds["classes"])),
                         ("Dificultad", ds["difficulty"]),
                         ("Mejor método", ds["best_method"])]:
            cell = tk.Frame(meta, bg=ds["bg"])
            cell.pack(side="left", padx=10, pady=8)
            tk.Label(cell, text=lbl, bg=ds["bg"], fg=ds["color"],
                     font=FONTS["small_bold"]).pack()
            tk.Label(cell, text=val, bg=ds["bg"], fg=COLORS["text"],
                     font=FONTS["body_bold"]).pack()

        P = 14

        # Descripción
        self._det_section(f, "📋 Descripción", ds["description"], P)
        self._det_section(f, "✅ ¿Por qué es ideal para Naïve Bayes?",
                          ds["why_good"], P)

        # Qué aprenderás
        learn_f = tk.Frame(f, bg=COLORS["bg_card"], relief="solid", bd=1)
        learn_f.pack(fill="x", padx=P, pady=4)
        tk.Label(learn_f, text="🎓  ¿Qué aprenderás?",
                 bg=COLORS["primary_light"], fg=COLORS["primary"],
                 font=FONTS["body_bold"],
                 padx=12, pady=6, anchor="w").pack(fill="x")
        for item in ds["what_to_learn"]:
            row = tk.Frame(learn_f, bg=COLORS["bg_card"])
            row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text="▸", bg=COLORS["bg_card"],
                     fg=COLORS["primary"],
                     font=FONTS["body_bold"]).pack(side="left", padx=(0, 6))
            tk.Label(row, text=item, bg=COLORS["bg_card"],
                     fg=COLORS["text"], font=FONTS["small"],
                     wraplength=500, anchor="w",
                     justify="left").pack(side="left")
        tk.Frame(learn_f, bg=COLORS["bg_card"], height=6).pack()

        # Tipos de variables
        InfoBox(f, f"Variables: {ds['feature_types']}",
                type_="info").pack(fill="x", padx=P, pady=4)

        # Fuente
        src_f = tk.Frame(f, bg=COLORS["bg_card"])
        src_f.pack(fill="x", padx=P, pady=(4, 16))
        tk.Label(src_f, text="🔗  Dónde encontrarlo:",
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 font=FONTS["small_bold"]).pack(anchor="w")
        tk.Label(src_f, text=ds["url"],
                 bg=COLORS["bg_card"], fg=COLORS["primary"],
                 font=FONTS["small"]).pack(anchor="w")

    def _det_section(self, parent, title, text, P):
        f = tk.Frame(parent, bg=COLORS["bg_card"], relief="solid", bd=1)
        f.pack(fill="x", padx=P, pady=4)
        tk.Label(f, text=title, bg=COLORS["primary_light"],
                 fg=COLORS["primary"], font=FONTS["body_bold"],
                 padx=12, pady=6, anchor="w").pack(fill="x")
        tk.Label(f, text=text, bg=COLORS["bg_card"],
                 fg=COLORS["text"], font=FONTS["small"],
                 wraplength=520, justify="left",
                 padx=12, pady=8, anchor="nw").pack(fill="x")
