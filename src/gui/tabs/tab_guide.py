import tkinter as tk
from tkinter import ttk
from gui.styles import COLORS, FONTS
from gui.widgets.components import InfoBox

GUIDE_SECTIONS = [
    {
        "id": "naive_bayes", "title": "¿Qué es Naïve Bayes?", "icon": "🧠",
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
        "id": "workflow", "title": "Flujo de Trabajo", "icon": "🔄",
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
        "id": "methods", "title": "Métodos para Variables Continuas", "icon": "📈",
        "content": [
            ("intro",
             "Las variables numéricas no tienen valores fijos, así que no se puede "
             "calcular P(x=5.3|Clase) directamente. Se usan estrategias para estimarla:"),
            ("method_block", {
                "name": "📊 Distribución Gaussiana",
                "color": COLORS["gaussian"], "bg": COLORS["gaussian_light"],
                "formula": "P(x|C) = (1/√2πσ²) × e^(−(x−μ)²/2σ²)",
                "desc": "Asume distribución normal. Calcula μ y σ por clase durante el entrenamiento.",
                "when": "✅ Cuando los datos son aproximadamente normales. Primera opción a probar.",
            }),
            ("method_block", {
                "name": "〰 KDE — Kernel Density Estimation",
                "color": COLORS["kde"], "bg": COLORS["kde_light"],
                "formula": "P(x|C) ≈ (1/nh) × Σ K((x − xⱼ)/h)",
                "desc": "No asume distribución. Coloca una 'campana' sobre cada punto de entrenamiento y las suma.",
                "when": "✅ Distribuciones complejas, multimodales o asimétricas.",
            }),
            ("method_block", {
                "name": "📏 Discretización — Anchos Iguales",
                "color": COLORS["ew"], "bg": COLORS["ew_light"],
                "formula": "Ancho = (máx − mín) / n_bins",
                "desc": "Divide el rango en n intervalos del mismo tamaño. Trata cada intervalo como categoría.",
                "when": "✅ Datos sin outliers extremos, distribución relativamente uniforme.",
            }),
            ("method_block", {
                "name": "⚖ Discretización — Frecuencias Iguales",
                "color": COLORS["ef"], "bg": COLORS["ef_light"],
                "formula": "Cada bin ≈ n_muestras / n_bins instancias",
                "desc": "Coloca cortes en percentiles equidistantes. Bins con igual cantidad de datos.",
                "when": "✅ Distribuciones muy sesgadas o con muchos outliers.",
            }),
        ],
    },
    {
        "id": "discrete", "title": "Variables Discretas y Laplace", "icon": "🔤",
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
        "id": "metrics", "title": "Métricas de Evaluación", "icon": "📊",
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
        "id": "confusion", "title": "Matriz de Confusión", "icon": "🗂",
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
        "id": "dataset_format", "title": "Formato del Dataset", "icon": "📁",
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
    {
        "id": "tips", "title": "Tips y Buenas Prácticas", "icon": "💡",
        "content": [
            ("list_title", "Selección del método:"),
            ("list", [
                "Empieza con Gaussiana — es rápido y buen baseline",
                "Si el accuracy es bajo, prueba KDE (más flexible)",
                "Con muchos outliers → usa Discretización",
                "Compara los 4 métodos para encontrar el mejor para tus datos",
            ]),
            ("list_title", "Escala de accuracy:"),
            ("list", [
                "Accuracy > 90% → Excelente",
                "Accuracy 75-90% → Bueno",
                "Accuracy 60-75% → Aceptable",
                "Accuracy < 60% → Revisa los datos o cambia el método",
            ]),
            ("list_title", "Mejora de resultados:"),
            ("list", [
                "Más datos → siempre mejora el modelo",
                "Limpia el dataset: elimina duplicados y outliers extremos",
                "Clases desbalanceadas → usa F1 en lugar de Accuracy",
                "Prueba diferentes valores de n_bins (3, 5, 10) con discretización",
            ]),
            ("tip",
             "Un modelo 100% en entrenamiento pero malo en prueba "
             "indica sobreajuste. Con Naïve Bayes esto es poco común."),
        ],
    },
]


class GuideTab(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=COLORS["bg_main"], **kw)
        self._current = None
        self._build()

    def _build(self):
        # Sidebar izquierda + contenido derecho con pack
        sidebar = tk.Frame(self, bg=COLORS["bg_sidebar"], width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        content_outer = tk.Frame(self, bg=COLORS["bg_main"])
        content_outer.pack(side="right", fill="both", expand=True)

        # Canvas + scrollbar para el contenido
        self._canvas = tk.Canvas(content_outer, bg=COLORS["bg_main"],
                                 highlightthickness=0, borderwidth=0)
        vsb = ttk.Scrollbar(content_outer, orient="vertical",
                             command=self._canvas.yview)
        self._inner = tk.Frame(self._canvas, bg=COLORS["bg_main"])
        self._inner.bind("<Configure>",
                         lambda e: self._canvas.configure(
                             scrollregion=self._canvas.bbox("all")))
        self._win_id = self._canvas.create_window(
            (0, 0), window=self._inner, anchor="nw")
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        # Scroll con rueda del mouse (Linux: Button-4/5)
        self._canvas.bind("<Button-4>",
                          lambda e: self._canvas.yview_scroll(-1, "units"))
        self._canvas.bind("<Button-5>",
                          lambda e: self._canvas.yview_scroll(1, "units"))
        self._canvas.bind("<MouseWheel>",
                          lambda e: self._canvas.yview_scroll(
                              int(-1 * e.delta / 120), "units"))
        # Ajustar ancho del inner frame al canvas
        self._canvas.bind("<Configure>", self._on_canvas_resize)

        self._show_section(GUIDE_SECTIONS[0]["id"])

    def _on_canvas_resize(self, event):
        self._canvas.itemconfig(self._win_id, width=event.width)

    def _build_sidebar(self, parent):
        tk.Label(parent, text="📖  GUÍA DE USO",
                 bg=COLORS["bg_sidebar"], fg=COLORS["text_white"],
                 font=FONTS["small_bold"],
                 padx=14, pady=12, anchor="w").pack(fill="x")
        tk.Frame(parent, bg=COLORS["primary"], height=2).pack(fill="x")

        self._nav_btns = {}
        for sec in GUIDE_SECTIONS:
            btn = tk.Label(parent,
                           text=f"  {sec['icon']}  {sec['title']}",
                           bg=COLORS["bg_sidebar"],
                           fg=COLORS["text_header"],
                           font=FONTS["small"],
                           anchor="w", cursor="hand2",
                           wraplength=180, justify="left",
                           padx=6, pady=7)
            btn.pack(fill="x")
            sid = sec["id"]
            btn.bind("<Button-1>", lambda e, s=sid: self._show_section(s))
            btn.bind("<Enter>",
                     lambda e, b=btn: b.config(bg=COLORS["primary_dark"],
                                               fg="#ffffff"))
            btn.bind("<Leave>",
                     lambda e, b=btn, s=sec["id"]:
                     b.config(bg=COLORS["primary"] if self._current == s
                              else COLORS["bg_sidebar"],
                              fg="#ffffff" if self._current == s
                              else COLORS["text_header"]))
            self._nav_btns[sid] = btn

    def _show_section(self, sid: str):
        # Deseleccionar anterior
        if self._current and self._current in self._nav_btns:
            self._nav_btns[self._current].config(
                bg=COLORS["bg_sidebar"], fg=COLORS["text_header"])
        self._current = sid
        if sid in self._nav_btns:
            self._nav_btns[sid].config(
                bg=COLORS["primary"], fg="#ffffff")

        sec = next((s for s in GUIDE_SECTIONS if s["id"] == sid), None)
        if not sec:
            return

        # Limpiar contenido
        for w in self._inner.winfo_children():
            w.destroy()

        f = self._inner

        # Header de sección
        hdr = tk.Frame(f, bg=COLORS["bg_dark"])
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"{sec['icon']}  {sec['title']}",
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"],
                 font=FONTS["title"], padx=20, pady=12,
                 anchor="w").pack(fill="x")

        # Renderizar ítems
        for item_type, content in sec["content"]:
            self._render(f, item_type, content)

        tk.Frame(f, bg=COLORS["bg_main"], height=30).pack()
        # Volver al inicio
        self._canvas.yview_moveto(0)

    def _render(self, parent, itype: str, content):
        P = 16

        if itype == "intro":
            card = tk.Frame(parent, bg=COLORS["bg_card"], relief="solid", bd=1)
            card.pack(fill="x", padx=P, pady=(6, 4))
            tk.Label(card, text=content, bg=COLORS["bg_card"],
                     fg=COLORS["text"], font=FONTS["body"],
                     wraplength=680, justify="left",
                     padx=14, pady=12, anchor="w").pack(fill="x")

        elif itype == "formula_title":
            tk.Label(parent, text=f"  {content}",
                     bg=COLORS["bg_main"], fg=COLORS["text_secondary"],
                     font=FONTS["small_bold"]).pack(
                         anchor="w", padx=P, pady=(8, 2))

        elif itype == "formula":
            ff = tk.Frame(parent, bg=COLORS["bg_code"])
            ff.pack(fill="x", padx=P, pady=(0, 8))
            tk.Label(ff, text=content, bg=COLORS["bg_code"],
                     fg="#a8d8ff", font=FONTS["mono"],
                     padx=14, pady=8,
                     justify="left", anchor="w").pack(fill="x")

        elif itype == "diagram":
            df = tk.Frame(parent, bg="#1a2744", relief="solid", bd=1)
            df.pack(fill="x", padx=P, pady=(0, 10))
            tk.Label(df, text=content, bg="#1a2744", fg="#b8d4ff",
                     font=("Courier New", 9),
                     padx=14, pady=8,
                     justify="left", anchor="w").pack(fill="x")

        elif itype == "list_title":
            tk.Label(parent, text=f"  {content}",
                     bg=COLORS["bg_main"], fg=COLORS["text"],
                     font=FONTS["body_bold"]).pack(
                         anchor="w", padx=P, pady=(8, 2))

        elif itype == "list":
            lf = tk.Frame(parent, bg=COLORS["bg_card"], relief="solid", bd=1)
            lf.pack(fill="x", padx=P, pady=(0, 8))
            for item in content:
                row = tk.Frame(lf, bg=COLORS["bg_card"])
                row.pack(fill="x", padx=10, pady=2)
                tk.Label(row, text="▸", bg=COLORS["bg_card"],
                         fg=COLORS["primary"],
                         font=FONTS["body_bold"]).pack(side="left",
                                                       padx=(0, 6))
                tk.Label(row, text=item, bg=COLORS["bg_card"],
                         fg=COLORS["text"], font=FONTS["small"],
                         wraplength=650, justify="left",
                         anchor="w").pack(side="left", fill="x", expand=True)
            tk.Frame(lf, bg=COLORS["bg_card"], height=4).pack()

        elif itype == "tip":
            InfoBox(parent, content, type_="tip",
                    title="Consejo").pack(fill="x", padx=P, pady=(0, 8))

        elif itype == "warning":
            InfoBox(parent, content, type_="warning").pack(
                fill="x", padx=P, pady=(0, 8))

        elif itype == "steps":
            for step_title, step_desc in content:
                sf = tk.Frame(parent, bg=COLORS["bg_card"],
                              relief="solid", bd=1)
                sf.pack(fill="x", padx=P, pady=3)
                tk.Label(sf, text=step_title, bg=COLORS["primary_light"],
                         fg=COLORS["primary"], font=FONTS["body_bold"],
                         padx=12, pady=5, anchor="w").pack(fill="x")
                tk.Label(sf, text=step_desc, bg=COLORS["bg_card"],
                         fg=COLORS["text"], font=FONTS["small"],
                         wraplength=670, justify="left",
                         padx=12, pady=6, anchor="w").pack(fill="x")

        elif itype == "method_block":
            d = content
            mf = tk.Frame(parent, bg=d["bg"], relief="solid", bd=1)
            mf.pack(fill="x", padx=P, pady=5)
            tk.Label(mf, text=d["name"], bg=d["color"], fg="#ffffff",
                     font=FONTS["body_bold"],
                     padx=12, pady=6, anchor="w").pack(fill="x")
            body = tk.Frame(mf, bg=d["bg"])
            body.pack(fill="x", padx=12, pady=6)
            cf = tk.Frame(body, bg=COLORS["bg_code"])
            cf.pack(fill="x", pady=(0, 6))
            tk.Label(cf, text=d["formula"], bg=COLORS["bg_code"],
                     fg="#a8d8ff", font=FONTS["mono"],
                     padx=8, pady=4, anchor="w").pack(fill="x")
            tk.Label(body, text=d["desc"], bg=d["bg"],
                     fg=COLORS["text"], font=FONTS["small"],
                     wraplength=660, justify="left",
                     anchor="w").pack(anchor="w", pady=(0, 4))
            wf = tk.Frame(body, bg=COLORS["success_light"])
            wf.pack(fill="x")
            tk.Label(wf, text=d["when"], bg=COLORS["success_light"],
                     fg=COLORS["success"], font=FONTS["small"],
                     padx=8, pady=4, anchor="w",
                     wraplength=660).pack(fill="x")

        elif itype == "metric_block":
            d = content
            mf = tk.Frame(parent, bg=COLORS["bg_card"],
                          relief="solid", bd=1)
            mf.pack(fill="x", padx=P, pady=4)
            tk.Label(mf, text=d["name"], bg=COLORS["primary_light"],
                     fg=COLORS["primary"], font=FONTS["body_bold"],
                     padx=12, pady=6, anchor="w").pack(fill="x")
            body = tk.Frame(mf, bg=COLORS["bg_card"])
            body.pack(fill="x", padx=12, pady=6)
            cf = tk.Frame(body, bg=COLORS["bg_code"])
            cf.pack(fill="x", pady=(0, 6))
            tk.Label(cf, text=d["formula"], bg=COLORS["bg_code"],
                     fg="#a8d8ff", font=FONTS["mono"],
                     padx=8, pady=4, anchor="w").pack(fill="x")
            tk.Label(body, text=d["desc"], bg=COLORS["bg_card"],
                     fg=COLORS["text"], font=FONTS["small"],
                     wraplength=660, justify="left",
                     anchor="w").pack(anchor="w", pady=(0, 4))
            ef = tk.Frame(body, bg=COLORS["info_light"])
            ef.pack(fill="x")
            tk.Label(ef, text=f"Ejemplo: {d['example']}",
                     bg=COLORS["info_light"], fg=COLORS["info"],
                     font=FONTS["small"], padx=8, pady=4,
                     anchor="w").pack(fill="x")
