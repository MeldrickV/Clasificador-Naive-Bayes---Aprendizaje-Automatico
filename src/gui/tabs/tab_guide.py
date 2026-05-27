import customtkinter as ctk
from gui.styles import COLORS, FONTS
from gui.widgets.components import InfoBox

GUIDE_SECTIONS = [
    {
        "id": "naive_bayes", "title": "¿Qué es Naïve Bayes?", "icon": "",
        "content": [
            ("intro",
             "El clasificador Naïve Bayes es uno de los algoritmos más simples y "
             "efectivos del aprendizaje automático. Se basa en el Teorema de Bayes "
             "con una suposición 'ingenua' (naive): asume que todos los atributos "
             "son independientes entre sí dada la clase."),
            ("formula_title", "Teorema de Bayes"),
            ("formula", "P(Clase | X) = P(X | Clase) × P(Clase) / P(X)"),
            ("list_title", "Componentes:"),
            ("list", [
                "P(Clase | X) → Probabilidad posterior: ¿qué tan probable es la clase dado X?",
                "P(X | Clase) → Verosimilitud: ¿qué tan probable es ver X en esa clase?",
                "P(Clase) → A priori: frecuencia de la clase en los datos de entrenamiento",
                "P(X) → Constante de normalización (se cancela al comparar clases)",
            ]),
            ("tip",
             "Aunque la suposición de independencia rara vez se cumple, "
             "el algoritmo funciona sorprendentemente bien en la práctica."),
        ],
    },
    {
        "id": "workflow", "title": "Flujo de Trabajo", "icon": "",
        "content": [
            ("intro", "Sigue estos 5 pasos para clasificar con el modelo:"),
            ("steps", [
                ("1. Configuración",
                 "Carga tu dataset CSV. Selecciona la columna objetivo y "
                 "configura el método y parámetros."),
                ("2. Entrenamiento",
                 "El modelo aprende las probabilidades de cada clase a partir "
                 "del subconjunto de entrenamiento."),
                ("3. Evaluación automática",
                 "Se evalúa con el subconjunto de prueba (nunca visto) y se "
                 "calculan las métricas de rendimiento."),
                ("4. Predicción",
                 "Carga nuevas instancias sin etiqueta para clasificarlas "
                 "con el modelo entrenado."),
                ("5. Resultados",
                 "Visualiza la matriz de confusión, métricas detalladas "
                 "y exporta el reporte."),
            ]),
        ],
    },
    {
        "id": "methods", "title": "Métodos para Variables Continuas", "icon": "",
        "content": [
            ("intro",
             "Las variables numéricas no tienen valores fijos, así que no se puede "
             "calcular P(x=5.3|Clase) directamente. Se usan estrategias para estimarla:"),
            ("method_block", {
                "name": " Distribución Gaussiana",
                "color": COLORS["gaussian"], "bg": COLORS["gaussian_light"],
                "formula": "P(x|C) = (1/√2πσ²) × e^(−(x−μ)²/2σ²)",
                "desc": "Asume distribución normal. Calcula μ y σ por clase durante el entrenamiento.",
                "when": " Cuando los datos son aproximadamente normales. Primera opción a probar.",
            }),
            ("method_block", {
                "name": "〰 KDE — Kernel Density Estimation",
                "color": COLORS["kde"], "bg": COLORS["kde_light"],
                "formula": "P(x|C) ≈ (1/nh) × Σ K((x − xⱼ)/h)",
                "desc": "No asume distribución. Coloca una 'campana' sobre cada punto de entrenamiento y las suma.",
                "when": " Distribuciones complejas, multimodales o asimétricas.",
            }),
            ("method_block", {
                "name": " Discretización — Anchos Iguales",
                "color": COLORS["ew"], "bg": COLORS["ew_light"],
                "formula": "Ancho = (máx − mín) / n_bins",
                "desc": "Divide el rango en n intervalos del mismo tamaño. Trata cada intervalo como categoría.",
                "when": " Datos sin outliers extremos, distribución relativamente uniforme.",
            }),
            ("method_block", {
                "name": "⚖ Discretización — Frecuencias Iguales",
                "color": COLORS["ef"], "bg": COLORS["ef_light"],
                "formula": "Cada bin ≈ n_muestras / n_bins instancias",
                "desc": "Coloca cortes en percentiles equidistantes. Bins con igual cantidad de datos.",
                "when": " Distribuciones muy sesgadas o con muchos outliers.",
            }),
        ],
    },
    {
        "id": "discrete", "title": "Variables Discretas y Laplace", "icon": "",
        "content": [
            ("intro",
             "Las variables categóricas se manejan calculando frecuencias de cada valor por clase."),
            ("formula_title", "Sin Suavizado"),
            ("formula", "P(x=valor | Clase) = count(valor, Clase) / count(Clase)"),
            ("warning",
             "⚠ PROBLEMA: Si un valor no aparece en entrenamiento, P = 0, "
             "lo que anula toda la multiplicación de probabilidades."),
            ("formula_title", "Con Laplace Smoothing (solución)"),
            ("formula", "P(x|C) = (count(x,C) + α) / (count(C) + α × n_valores)"),
            ("list_title", "Valores de Alpha (α):"),
            ("list", [
                "α = 0.0 → Sin suavizado. Puede producir P = 0",
                "α = 1.0 → Laplace estándar. Recomendado ✓",
                "α > 1.0 → Mayor suavizado para datasets pequeños",
            ]),
        ],
    },
    {
        "id": "validation", "title": "Validación — Simple Split", "icon": "✂",
        "content": [
            ("intro",
             "Para evaluar la generalización del modelo, el dataset se divide en "
             "entrenamiento (el modelo aprende aquí) y prueba (evaluación honesta):"),
            ("diagram",
             "Dataset completo (100%)\n"
             "┌────────────────────────────┬───────────┐\n"
             "│   Entrenamiento (ej. 70%)  │ Prueba    │\n"
             "│   El modelo aprende aquí   │ Evaluación│\n"
             "│   (no se usa en evaluación)│ honesta   │\n"
             "└────────────────────────────┴───────────┘"),
            ("list_title", "Reglas clave:"),
            ("list", [
                "Los datos de PRUEBA nunca participan en el entrenamiento",
                "70-80% entrenamiento es el balance más común",
                "La semilla aleatoria garantiza reproducibilidad",
                "Con pocos datos (<200) usa 60% de entrenamiento",
            ]),
            ("tip",
             "El accuracy en entrenamiento siempre es mayor al de prueba. "
             "Lo importante es el rendimiento en el conjunto de prueba."),
        ],
    },
    {
        "id": "metrics", "title": "Métricas de Evaluación", "icon": "",
        "content": [
            ("intro",
             "Las métricas miden la calidad del clasificador. Cada una captura un "
             "aspecto diferente del rendimiento:"),
            ("metric_block", {
                "name": "Accuracy (Exactitud Global)",
                "formula": "Accuracy = (TP + TN) / Total",
                "desc": "Porcentaje de predicciones correctas. Simple pero engañoso con clases desbalanceadas.",
                "example": "90 de 100 predicciones correctas → Accuracy = 90%",
            }),
            ("metric_block", {
                "name": "Precisión (Precision)",
                "formula": "Precision = TP / (TP + FP)",
                "desc": "De las predichas como clase X, ¿cuántas realmente lo son? Alta precisión = pocas falsas alarmas.",
                "example": "Predijo 20 spam, 18 eran spam → Precisión = 90%",
            }),
            ("metric_block", {
                "name": "Recall (Exhaustividad)",
                "formula": "Recall = TP / (TP + FN)",
                "desc": "De las instancias reales de clase X, ¿cuántas detectó? Alto recall = pocas perdidas.",
                "example": "Había 25 spam, detectó 20 → Recall = 80%",
            }),
            ("metric_block", {
                "name": "F1-Score",
                "formula": "F1 = 2 × (Precision × Recall) / (Precision + Recall)",
                "desc": "Media armónica entre Precisión y Recall. La métrica más balanceada.",
                "example": "Precisión=90%, Recall=80% → F1 = 84.7%",
            }),
            ("list_title", "¿Qué métrica priorizar?"),
            ("list", [
                "Clases balanceadas → Accuracy o F1",
                "Evitar falsas alarmas (spam) → Alta Precisión",
                "No perder casos (diagnóstico médico) → Alto Recall",
                "Caso general → F1-Score",
            ]),
        ],
    },
    {
        "id": "confusion", "title": "Matriz de Confusión", "icon": "",
        "content": [
            ("intro",
             "Muestra cuántas predicciones fueron correctas e incorrectas, "
             "y qué clases se confunden entre sí."),
            ("diagram",
             "              Predicho A   Predicho B\n"
             "  Real A    [    85    ] [    15    ]  ← 15 errores\n"
             "  Real B    [    10    ] [    90    ]  ← 10 errores\n"
             "               ↑              ↑\n"
             "           correcto         correcto"),
            ("list_title", "Interpretación:"),
            ("list", [
                "Diagonal (verde en la app) → Predicciones correctas",
                "Fuera de diagonal (rojo) → Errores de clasificación",
                "Fila = clase real · Columna = clase predicha",
                "Muchos errores en una fila → el modelo confunde esa clase",
            ]),
            ("tip",
             "Si el modelo confunde clase A con B frecuentemente, puede que ambas "
             "clases sean difíciles de separar con los atributos disponibles."),
        ],
    },
    {
        "id": "dataset_format", "title": "Formato del Dataset", "icon": "",
        "content": [
            ("intro",
             "El dataset debe ser un archivo CSV con encabezados en la primera fila:"),
            ("formula_title", "Formato requerido"),
            ("formula",
             "atributo1,atributo2,atributo3,clase\n"
             "5.1,3.5,alto,setosa\n"
             "6.4,3.2,bajo,versicolor"),
            ("list_title", "Reglas:"),
            ("list", [
                "Primera fila: nombres de columnas (sin espacios recomendado)",
                "Una columna para la clase objetivo (seleccionable en Configuración)",
                "Números → tratados como variables continuas automáticamente",
                "Texto o enteros con <20 valores únicos → tratados como discretas",
                "Valores faltantes (NaN) → ignorados automáticamente",
            ]),
            ("list_title", "Para clasificar nuevas instancias (pestaña Predicción):"),
            ("list", [
                "Mismo formato CSV pero SIN la columna de clase",
                "Mismos nombres de columnas que el dataset de entrenamiento",
                "Puede contener 1 o más instancias",
            ]),
        ],
    },
    
]


class GuideTab(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color=COLORS["bg_main"], **kw)
        self._current = None
        self._build()

    def _build(self):
        # Sidebar izquierda
        sidebar = ctk.CTkFrame(self, fg_color=COLORS["bg_sidebar"], width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        # Contenedor derecho con scroll usando CTkScrollableFrame
        self._scroll_frame = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_main"])
        self._scroll_frame.pack(side="right", fill="both", expand=True)
        self._inner = self._scroll_frame

        self._show_section(GUIDE_SECTIONS[0]["id"])

    def _build_sidebar(self, parent):
        ctk.CTkLabel(parent, text="  GUÍA DE USO",
                     font=FONTS["small_bold"],
                     text_color=COLORS["text_white"],
                     anchor="w").pack(fill="x", padx=14, pady=12)
        ctk.CTkFrame(parent, height=2, fg_color=COLORS["primary"]).pack(fill="x")

        self._nav_btns = {}
        for sec in GUIDE_SECTIONS:
            btn = ctk.CTkLabel(parent,
                               text=f"  {sec['icon']}  {sec['title']}",
                               font=FONTS["small"],
                               text_color=COLORS["text_header"],
                               anchor="w", cursor="hand2",
                               wraplength=180, justify="left")
            btn.pack(fill="x", padx=6, pady=4)
            sid = sec["id"]
            btn.bind("<Button-1>", lambda e, s=sid: self._show_section(s))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(fg_color=COLORS["primary_dark"], text_color="#ffffff"))
            btn.bind("<Leave>", lambda e, b=btn, s=sid:
                     b.configure(fg_color=COLORS["primary"] if self._current == s else "transparent",
                                 text_color="#ffffff" if self._current == s else COLORS["text_header"]))
            self._nav_btns[sid] = btn

    def _show_section(self, sid: str):
        # Actualizar estilo de botones
        for s, btn in self._nav_btns.items():
            if s == sid:
                btn.configure(fg_color=COLORS["primary"], text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["text_header"])

        sec = next((s for s in GUIDE_SECTIONS if s["id"] == sid), None)
        if not sec:
            return

        # Limpiar contenido
        for w in self._inner.winfo_children():
            w.destroy()

        # Header de sección
        hdr = ctk.CTkFrame(self._inner, fg_color=COLORS["bg_dark"])
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=f"{sec['icon']}  {sec['title']}",
                     font=FONTS["title"], text_color=COLORS["text_white"],
                     anchor="w").pack(fill="x", padx=20, pady=12)

        # Renderizar contenido
        for item_type, content in sec["content"]:
            self._render(self._inner, item_type, content)

        ctk.CTkFrame(self._inner, height=30).pack()

    def _render(self, parent, itype: str, content):
        P = 16

        if itype == "intro":
            card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", padx=P, pady=(6, 4))
            ctk.CTkLabel(card, text=content, text_color=COLORS["text"],
                         font=FONTS["body"], wraplength=680, justify="left",
                         padx=14, pady=12, anchor="w").pack(fill="x")

        elif itype == "formula_title":
            ctk.CTkLabel(parent, text=f"  {content}",
                         text_color=COLORS["text_secondary"],
                         font=FONTS["small_bold"]).pack(
                             anchor="w", padx=P, pady=(8, 2))

        elif itype == "formula":
            ff = ctk.CTkFrame(parent, fg_color=COLORS["bg_code"])
            ff.pack(fill="x", padx=P, pady=(0, 8))
            ctk.CTkLabel(ff, text=content, text_color="#a8d8ff",
                         font=FONTS["mono"], padx=14, pady=8,
                         justify="left", anchor="w").pack(fill="x")

        elif itype == "diagram":
            df = ctk.CTkFrame(parent, fg_color="#1a2744", border_width=1, border_color=COLORS["border"])
            df.pack(fill="x", padx=P, pady=(0, 10))
            ctk.CTkLabel(df, text=content, text_color="#b8d4ff",
                         font=("Courier New", 9), padx=14, pady=8,
                         justify="left", anchor="w").pack(fill="x")

        elif itype == "list_title":
            ctk.CTkLabel(parent, text=f"  {content}",
                         text_color=COLORS["text"],
                         font=FONTS["body_bold"]).pack(
                             anchor="w", padx=P, pady=(8, 2))

        elif itype == "list":
            lf = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"])
            lf.pack(fill="x", padx=P, pady=(0, 8))
            for item in content:
                row = ctk.CTkFrame(lf, fg_color=COLORS["bg_card"])
                row.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(row, text="▸", text_color=COLORS["primary"],
                             font=FONTS["body_bold"]).pack(side="left", padx=(0, 6))
                ctk.CTkLabel(row, text=item, text_color=COLORS["text"],
                             font=FONTS["small"], wraplength=650, justify="left",
                             anchor="w").pack(side="left", fill="x", expand=True)
            ctk.CTkFrame(lf, height=4, fg_color=COLORS["bg_card"]).pack()

        elif itype == "tip":
            InfoBox(parent, content, type_="tip", title="Consejo").pack(fill="x", padx=P, pady=(0, 8))

        elif itype == "warning":
            InfoBox(parent, content, type_="warning").pack(fill="x", padx=P, pady=(0, 8))

        elif itype == "steps":
            for step_title, step_desc in content:
                sf = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"])
                sf.pack(fill="x", padx=P, pady=3)
                ctk.CTkLabel(sf, text=step_title, fg_color=COLORS["primary_light"],
                             text_color=COLORS["primary"], font=FONTS["body_bold"],
                             padx=12, pady=5, anchor="w").pack(fill="x")
                ctk.CTkLabel(sf, text=step_desc, text_color=COLORS["text"],
                             font=FONTS["small"], wraplength=670, justify="left",
                             padx=12, pady=6, anchor="w").pack(fill="x")

        elif itype == "method_block":
            d = content
            mf = ctk.CTkFrame(parent, fg_color=d["bg"], border_width=1, border_color=COLORS["border"])
            mf.pack(fill="x", padx=P, pady=5)
            ctk.CTkLabel(mf, text=d["name"], fg_color=d["color"], text_color="#ffffff",
                         font=FONTS["body_bold"], padx=12, pady=6, anchor="w").pack(fill="x")
            body = ctk.CTkFrame(mf, fg_color=d["bg"])
            body.pack(fill="x", padx=12, pady=6)
            cf = ctk.CTkFrame(body, fg_color=COLORS["bg_code"])
            cf.pack(fill="x", pady=(0, 6))
            ctk.CTkLabel(cf, text=d["formula"], text_color="#a8d8ff",
                         font=FONTS["mono"], padx=8, pady=4, anchor="w").pack(fill="x")
            ctk.CTkLabel(body, text=d["desc"], text_color=COLORS["text"],
                         font=FONTS["small"], wraplength=660, justify="left",
                         anchor="w").pack(anchor="w", pady=(0, 4))
            wf = ctk.CTkFrame(body, fg_color=COLORS["success_light"])
            wf.pack(fill="x")
            ctk.CTkLabel(wf, text=d["when"], text_color=COLORS["success"],
                         font=FONTS["small"], padx=8, pady=4, anchor="w",
                         wraplength=660).pack(fill="x")

        elif itype == "metric_block":
            d = content
            mf = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"])
            mf.pack(fill="x", padx=P, pady=4)
            ctk.CTkLabel(mf, text=d["name"], fg_color=COLORS["primary_light"],
                         text_color=COLORS["primary"], font=FONTS["body_bold"],
                         padx=12, pady=6, anchor="w").pack(fill="x")
            body = ctk.CTkFrame(mf, fg_color=COLORS["bg_card"])
            body.pack(fill="x", padx=12, pady=6)
            cf = ctk.CTkFrame(body, fg_color=COLORS["bg_code"])
            cf.pack(fill="x", pady=(0, 6))
            ctk.CTkLabel(cf, text=d["formula"], text_color="#a8d8ff",
                         font=FONTS["mono"], padx=8, pady=4, anchor="w").pack(fill="x")
            ctk.CTkLabel(body, text=d["desc"], text_color=COLORS["text"],
                         font=FONTS["small"], wraplength=660, justify="left",
                         anchor="w").pack(anchor="w", pady=(0, 4))
            ef = ctk.CTkFrame(body, fg_color=COLORS["info_light"])
            ef.pack(fill="x")
            ctk.CTkLabel(ef, text=f"Ejemplo: {d['example']}",
                         text_color=COLORS["info"], font=FONTS["small"],
                         padx=8, pady=4, anchor="w").pack(fill="x")
