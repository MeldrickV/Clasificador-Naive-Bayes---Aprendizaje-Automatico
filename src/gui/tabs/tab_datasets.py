import customtkinter as ctk
from gui.styles import COLORS, FONTS
from gui.widgets.components import InfoBox


DATASETS = [
    {
        "name": "Iris Flower Dataset", "icon": "",
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
        "name": "Titanic Survival", "icon": "",
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
        "name": "SMS Spam Collection", "icon": "",
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
        "name": "Wine Quality", "icon": "",
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
        "name": "Mushroom Classification", "icon": "",
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
        "name": "Breast Cancer Wisconsin", "icon": "",
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
        "name": "Car Evaluation", "icon": "",
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


class DatasetsTab(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color=COLORS["bg_main"], **kw)
        self._build()

    def _build(self):
        # Header
        hdr = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], height=90)
        hdr.pack(fill="x", pady=(0,8))
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="  Datasets Recomendados para Naïve Bayes",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white").pack(anchor="w", padx=18, pady=(12,4))
        ctk.CTkLabel(hdr, text="Selecciona un dataset para ver descripción, por qué es ideal y qué aprenderás.",
                     font=ctk.CTkFont(size=11), text_color="#e2e8f0").pack(anchor="w", padx=20, pady=(0,10))

        # Filtros
        fbar = ctk.CTkFrame(self, fg_color="transparent")
        fbar.pack(fill="x", padx=10, pady=6)
        ctk.CTkLabel(fbar, text="Filtrar por dificultad:",
                     font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
        self._filter = ctk.StringVar(value="Todos")
        for level in ["Todos", "Principiante", "Intermedio"]:
            rb = ctk.CTkRadioButton(fbar, text=level, variable=self._filter,
                                    value=level, command=self._apply_filter)
            rb.pack(side="left", padx=8)

        # Cuerpo principal: dos paneles con CTkScrollableFrame
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=8, pady=(0,8))

        # Panel izquierdo (lista)
        self.left_panel = ctk.CTkScrollableFrame(body, width=280, label_text="Datasets")
        self.left_panel.pack(side="left", fill="both", expand=False)

        # Separador
        sep = ctk.CTkFrame(body, width=1, fg_color="#e2e8f0")
        sep.pack(side="left", fill="y", padx=4)

        # Panel derecho (detalle)
        self.right_panel = ctk.CTkScrollableFrame(body, label_text="Detalle del Dataset")
        self.right_panel.pack(side="right", fill="both", expand=True)

        self._render_list(DATASETS)
        self._show_detail(DATASETS[0])

    def _apply_filter(self):
        f = self._filter.get()
        filtered = DATASETS if f == "Todos" else [d for d in DATASETS if d["difficulty"] == f]
        self._render_list(filtered)
        if filtered:
            self._show_detail(filtered[0])

    def _render_list(self, datasets):
        for w in self.left_panel.winfo_children():
            w.destroy()

        for ds in datasets:
            card = ctk.CTkFrame(self.left_panel, fg_color=ds["bg"], corner_radius=8,
                                border_width=1, border_color=ds["color"])
            card.pack(fill="x", padx=4, pady=3)
            card.bind("<Button-1>", lambda e, d=ds: self._show_detail(d))

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=8, pady=(6,2))
            ctk.CTkLabel(top, text=ds["icon"], font=ctk.CTkFont(size=14)).pack(side="left", padx=(0,6))
            ctk.CTkLabel(top, text=ds["name"], font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=ds["color"]).pack(side="left", fill="x", expand=True)
            diff_bg = "#d1fae5" if ds["diff_style"] == "success" else "#fef3c7"
            diff_fg = "#059669" if ds["diff_style"] == "success" else "#d97706"
            ctk.CTkLabel(top, text=ds["difficulty"], fg_color=diff_bg, text_color=diff_fg,
                         corner_radius=12, padx=6, pady=2,
                         font=ctk.CTkFont(size=10, weight="bold")).pack(side="right")

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(fill="x", padx=8, pady=(0,6))
            ctk.CTkLabel(info, text=f"{ds['samples']} instancias · {ds['features']} atrib. · {ds['classes']} clases",
                         font=ctk.CTkFont(size=10), text_color=COLORS["text_secondary"]).pack(anchor="w")


            for child in [top, info] + top.winfo_children() + info.winfo_children():
                child.bind("<Button-1>", lambda e, d=ds: self._show_detail(d))

    def _show_detail(self, ds):
        for w in self.right_panel.winfo_children():
            w.destroy()

        # Header
        hdr = ctk.CTkFrame(self.right_panel, fg_color=ds["color"], corner_radius=8)
        hdr.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(hdr, text=f"{ds['icon']}  {ds['name']}",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").pack(anchor="w", padx=16, pady=12)

        # Metadatos
        meta = ctk.CTkFrame(self.right_panel, fg_color=ds["bg"], corner_radius=8)
        meta.pack(fill="x", pady=4)
        labels = [("Instancias", str(ds["samples"])), ("Atributos", str(ds["features"])),
                  ("Clases", str(ds["classes"])), ("Dificultad", ds["difficulty"]),
                  ("Mejor método", ds["best_method"])]
        for i, (lbl, val) in enumerate(labels):
            cell = ctk.CTkFrame(meta, fg_color="transparent")
            cell.grid(row=0, column=i, padx=6, pady=8, sticky="nsew")
            ctk.CTkLabel(cell, text=lbl, font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=ds["color"]).pack()
            ctk.CTkLabel(cell, text=val, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#1e293b").pack()
        for i in range(len(labels)):
            meta.grid_columnconfigure(i, weight=1)

        # Descripciones
        self._det_section(self.right_panel, " Descripción", ds["description"])
        self._det_section(self.right_panel, " ¿Por qué es ideal para Naïve Bayes?", ds["why_good"])

        # Qué aprenderás
        learn_frame = ctk.CTkFrame(self.right_panel, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"], corner_radius=8)
        learn_frame.pack(fill="x", pady=4)
        ctk.CTkLabel(learn_frame, text="  ¿Qué aprenderás?",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["primary"],
                     fg_color=COLORS["primary_light"], corner_radius=8).pack(fill="x", ipady=4)
        for item in ds["what_to_learn"]:
            row = ctk.CTkFrame(learn_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text="▸", font=ctk.CTkFont(size=12), text_color=COLORS["primary"]).pack(side="left", padx=(0,6))
            ctk.CTkLabel(row, text=item, font=ctk.CTkFont(size=11), text_color="#1e293b",
                         anchor="w", justify="left").pack(side="left", fill="x", expand=True)
        ctk.CTkFrame(learn_frame, height=6, fg_color="transparent").pack()

        # Tipos de variables
        InfoBox(self.right_panel, f"Variables: {ds['feature_types']}", type_="info").pack(fill="x", pady=4)

        # Fuente
        src_frame = ctk.CTkFrame(self.right_panel, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"], corner_radius=8)
        src_frame.pack(fill="x", pady=4)
        ctk.CTkLabel(src_frame, text="  Dónde encontrarlo:",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color=COLORS["text_secondary"]).pack(anchor="w", padx=12, pady=(6,2))
        ctk.CTkLabel(src_frame, text=ds["url"], font=ctk.CTkFont(size=10), text_color=COLORS["primary"]).pack(anchor="w", padx=12, pady=(0,6))

        self.right_panel._parent_canvas.yview_moveto(0)

    def _det_section(self, parent, title, text):
        frame = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"], corner_radius=8)
        frame.pack(fill="x", pady=4)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=COLORS["primary"], fg_color=COLORS["primary_light"],
                     corner_radius=8).pack(fill="x", ipady=4)
        textbox = ctk.CTkTextbox(frame, height=100, wrap="word", font=ctk.CTkFont(size=11))
        textbox.pack(fill="x", padx=8, pady=8)
        textbox.insert("0.0", text)
        textbox.configure(state="disabled")
