import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from gui.styles import COLORS, FONTS
from gui.widgets.components import (
    InfoBox, SectionHeader, MethodCard, Badge, Tooltip, ScrollableFrame
)
from gui.widgets.help_panel import HelpPanel


class ConfigTab(tk.Frame):
    def __init__(self, parent, app_state: dict, **kw):
        super().__init__(parent, bg=COLORS["bg_main"], **kw)
        self.app_state = app_state
        self._build()

    def _build(self):
        # Panel izquierdo con scroll
        left = ScrollableFrame(self, bg=COLORS["bg_main"])
        left.pack(side="left", fill="both", expand=True, padx=(8, 4), pady=8)

        # Panel derecho de ayuda - más ancho (360 px)
        right = tk.Frame(self, bg=COLORS["bg_card"], relief="solid", bd=1, width=380)
        right.pack(side="right", fill="both", expand=False, padx=(0, 8), pady=8)
        right.pack_propagate(False)

        self.help_panel = HelpPanel(right)
        self.help_panel.pack(fill="both", expand=True)

        # Construir secciones dentro del frame con scroll
        self._build_dataset(left.inner)
        self._build_method(left.inner)
        self._build_params(left.inner)

    # ── Dataset ───────────────────────────────────
    def _build_dataset(self, parent):
        card = self._card(parent)
        SectionHeader(card, "Dataset de Entrenamiento",
                      "Archivo CSV con atributos y columna de clase",
                      icon="📂", bg=COLORS["bg_card"]).pack(
                          fill="x", padx=12, pady=(12, 8))

        row = tk.Frame(card, bg=COLORS["bg_card"])
        row.pack(fill="x", padx=12, pady=(0, 4))

        ttk.Button(row, text="📂  Cargar Dataset (.csv)",
                   style="Primary.TButton",
                   command=self._load_dataset).pack(side="left")

        self._ds_badge = Badge(row, "Sin cargar", style="gray")
        self._ds_badge.pack(side="left", padx=10)

        self._ds_info = tk.Label(card, text="",
                                 bg=COLORS["bg_card"],
                                 fg=COLORS["text_secondary"],
                                 font=FONTS["small"])
        self._ds_info.pack(anchor="w", padx=12)

        self._col_preview = tk.Label(card, text="",
                                     bg=COLORS["bg_card"],
                                     fg=COLORS["text_secondary"],
                                     font=FONTS["small"],
                                     wraplength=480, justify="left")
        self._col_preview.pack(anchor="w", padx=12, pady=(0, 4))

        ttk.Separator(card).pack(fill="x", padx=12, pady=6)

        obj_row = tk.Frame(card, bg=COLORS["bg_card"])
        obj_row.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(obj_row, text="🎯  Columna objetivo (clase):",
                 bg=COLORS["bg_card"], fg=COLORS["text"],
                 font=FONTS["body_bold"]).pack(side="left")

        self.target_combo = ttk.Combobox(obj_row, state="readonly", width=26,
                                          textvariable=self.app_state["target_col"])
        self.target_combo.pack(side="left", padx=(10, 0))
        Tooltip(self.target_combo,
                "Columna que contiene las etiquetas de clase (lo que el modelo predice).")

    # ── Método ────────────────────────────────────
    def _build_method(self, parent):
        card = self._card(parent)

        SectionHeader(card, "Método para Variables Continuas",
                      "Cómo estimar la probabilidad de valores numéricos",
                      icon="📈", bg=COLORS["bg_card"]).pack(
                          fill="x", padx=12, pady=(12, 8))

        grid = tk.Frame(card, bg=COLORS["bg_card"])
        grid.pack(fill="x", padx=12, pady=(0, 6))
        grid.columnconfigure((0, 1), weight=1)

        var = self.app_state["cont_method"]

        cards_data = [
            ("gaussian",    "Gaussiana",     "Distribución normal (μ, σ)",
             COLORS["gaussian"], COLORS["gaussian_light"], "📊"),
            ("kde",         "KDE",           "Estimación no paramétrica",
             COLORS["kde"],      COLORS["kde_light"],      "〰"),
            ("equal_width", "Anchos =",      "Intervalos de igual tamaño",
             COLORS["ew"],       COLORS["ew_light"],       "📏"),
            ("equal_freq",  "Frecuencias =", "Igual cantidad por intervalo",
             COLORS["ef"],       COLORS["ef_light"],       "⚖"),
        ]

        for idx, (val, title, desc, col, bg, icon) in enumerate(cards_data):
            r, c = divmod(idx, 2)
            mc = MethodCard(grid, var, val, title, desc, col, bg,
                            icon=icon,
                            command=lambda v: self.help_panel.show_method(v))
            mc.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        InfoBox(card,
                "Selecciona una tarjeta → el panel derecho muestra su explicación completa",
                type_="tip").pack(fill="x", padx=12, pady=(0, 12))

    # ── Parámetros ────────────────────────────────
    def _build_params(self, parent):
        card = self._card(parent)
        SectionHeader(card, "Parámetros de Configuración",
                      "Hiperparámetros del modelo",
                      icon="⚙", bg=COLORS["bg_card"]).pack(
                          fill="x", padx=12, pady=(12, 8))

        body = tk.Frame(card, bg=COLORS["bg_card"])
        body.pack(fill="x", padx=12, pady=(0, 12))
        body.columnconfigure(1, weight=1)

        # Laplace alpha
        self._param_row(body, 0, "Laplace Alpha (α):",
                        self.app_state["laplace_alpha"], "laplace",
                        "Suavizado para variables discretas. Evita P = 0.")

        # N bins
        self._param_row(body, 1, "N° de Bins:",
                        self.app_state["n_bins"], "nbins",
                        "Intervalos para discretizar variables continuas.")

        # KDE bandwidth
        tk.Label(body, text="Bandwidth KDE:", bg=COLORS["bg_card"],
                 fg=COLORS["text"], font=FONTS["body"]).grid(
                     row=2, column=0, sticky="w", pady=5)

        kde_f = tk.Frame(body, bg=COLORS["bg_card"])
        kde_f.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=5)

        ttk.Combobox(kde_f, textvariable=self.app_state["kde_bw"],
                     values=["scott", "silverman"],
                     state="readonly", width=12).pack(side="left")

        bw_help = tk.Label(kde_f, text="  ❓",
                           bg=COLORS["bg_card"], fg=COLORS["kde"],
                           cursor="hand2", font=FONTS["body"])
        bw_help.pack(side="left")
        bw_help.bind("<Button-1>",
                     lambda e: self.help_panel.show_param("kde_bw"))

        # Split
        ttk.Separator(body).grid(row=3, column=0, columnspan=2,
                                 sticky="ew", pady=8)

        tk.Label(body, text="División Entrenamiento / Prueba:",
                 bg=COLORS["bg_card"], fg=COLORS["text"],
                 font=FONTS["body"]).grid(row=4, column=0, sticky="w", pady=5)

        split_f = tk.Frame(body, bg=COLORS["bg_card"])
        split_f.grid(row=4, column=1, sticky="ew", padx=(10, 0), pady=5)

        self._split_lbl = tk.Label(split_f,
                                   text="70% entrenamiento / 30% prueba",
                                   bg=COLORS["bg_card"], fg=COLORS["primary"],
                                   font=FONTS["body_bold"])
        self._split_lbl.pack(anchor="w")

        ttk.Scale(split_f, from_=10, to=90,
                  variable=self.app_state["train_pct"],
                  orient="horizontal", length=180,
                  command=self._upd_split).pack(anchor="w", pady=(2, 0))

        help_lbl = tk.Label(split_f, text="❓ ¿Qué es esto?",
                            bg=COLORS["bg_card"], fg=COLORS["primary"],
                            cursor="hand2", font=FONTS["small"])
        help_lbl.pack(anchor="w")
        help_lbl.bind("<Button-1>",
                      lambda e: self.help_panel.show_param("split"))

        # Semilla
        ttk.Separator(body).grid(row=5, column=0, columnspan=2,
                                 sticky="ew", pady=6)

        tk.Label(body, text="Semilla aleatoria:",
                 bg=COLORS["bg_card"], fg=COLORS["text"],
                 font=FONTS["body"]).grid(row=6, column=0, sticky="w", pady=5)

        seed_f = tk.Frame(body, bg=COLORS["bg_card"])
        seed_f.grid(row=6, column=1, sticky="w", padx=(10, 0), pady=5)

        ttk.Entry(seed_f, textvariable=self.app_state["seed"],
                  width=10).pack(side="left")
        tk.Label(seed_f, text="  (para reproducir resultados)",
                 bg=COLORS["bg_card"], fg=COLORS["text_light"],
                 font=FONTS["small"]).pack(side="left")

        # ── Botones de acción ────────
        ttk.Separator(card).pack(fill="x", padx=12, pady=8)
        
        btn_frame = tk.Frame(card, bg=COLORS["bg_card"])
        btn_frame.pack(fill="x", padx=12, pady=(0, 12))
        
        analyze_btn = ttk.Button(
            btn_frame,
            text="▶  ANÁLISIS",
            style="Primary.TButton",
            command=self._on_analyze_click
        )
        analyze_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        ttk.Button(
            btn_frame,
            text="🔄  LIMPIAR",
            style="Secondary.TButton",
            command=self._on_clear_click
        ).pack(side="left", fill="x", expand=True)

    # ── Helpers ───────────────────────────────────
    def _card(self, parent) -> tk.Frame:
        f = tk.Frame(parent, bg=COLORS["bg_card"], relief="solid", bd=1)
        f.pack(fill="x", pady=4)
        return f

    def _param_row(self, parent, row, label, var, help_key, tip):
        tk.Label(parent, text=label, bg=COLORS["bg_card"],
                 fg=COLORS["text"], font=FONTS["body"]).grid(
                     row=row, column=0, sticky="w", pady=3)
        inner = tk.Frame(parent, bg=COLORS["bg_card"])
        inner.grid(row=row, column=1, sticky="w", padx=(10, 0), pady=5)

        ttk.Entry(inner, textvariable=var, width=10).pack(side="left")

        hl = tk.Label(inner, text="  ❓", bg=COLORS["bg_card"],
                      fg=COLORS["primary"], cursor="hand2",
                      font=FONTS["body"])
        hl.pack(side="left")
        hl.bind("<Button-1>",
                lambda e, k=help_key: self.help_panel.show_param(k))

        tk.Label(inner, text=tip, bg=COLORS["bg_card"],
                 fg=COLORS["text_light"],
                 font=FONTS["small"]).pack(side="left", padx=(6, 0))

    def _upd_split(self, val=None):
        pct = int(float(self.app_state["train_pct"].get()))
        self._split_lbl.config(
            text=f"{pct}% entrenamiento  /  {100 - pct}% prueba")

    # ── Carga dataset ─────────────────────────────
    def _load_dataset(self):
        import pandas as pd
        path = filedialog.askopenfilename(
            title="Seleccionar Dataset CSV",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if not path:
            return
        try:
            df = pd.read_csv(path)
            self.app_state["dataset"] = df
            self.app_state["dataset_path"] = path

            fname = os.path.basename(path)
            n_rows, n_cols = df.shape

            self._ds_badge.config(text=f"✓ {fname}",
                                  bg=COLORS["success_light"],
                                  fg=COLORS["success"])
            self._ds_info.config(
                text=f"{n_rows} instancias  ·  {n_cols} columnas")

            cols = list(df.columns)
            preview = "Columnas: " + ", ".join(
                f"{c}({str(df[c].dtype)[:3]})" for c in cols[:8])
            if len(cols) > 8:
                preview += f" (+{len(cols)-8} más)"
            self._col_preview.config(text=preview)

            self.target_combo["values"] = cols
            self.target_combo.current(len(cols) - 1)
            self.app_state["target_col"].set(cols[-1])

            messagebox.showinfo("Dataset cargado",
                                f"{fname}\n{n_rows} instancias · "
                                f"{n_cols} columnas")
        except Exception as exc:
            messagebox.showerror("Error al cargar dataset", str(exc))

    # ── VALIDACIÓN Y ANÁLISIS ────
    def _validate_all(self):
        if self.app_state.get('dataset') is None:
            messagebox.showerror("Error de validación", 
                "❌ Dataset no cargado.\n\nPor favor, carga un archivo CSV primero.")
            return False
        
        target = self.app_state['target_col'].get()
        if not target:
            messagebox.showerror("Error de validación",
                "❌ Columna objetivo no seleccionada.\n\nSelecciona la columna que contiene las etiquetas de clase.")
            return False
        
        try:
            alpha = float(self.app_state['laplace_alpha'].get())
            if alpha <= 0:
                raise ValueError("Laplace Alpha debe ser positivo (>0)")
            
            bins = int(self.app_state['n_bins'].get())
            if not (2 <= bins <= 20):
                raise ValueError("N° de Bins debe estar entre 2 y 20")
            
            train_pct = float(self.app_state['train_pct'].get())
            if not (10 <= train_pct <= 90):
                raise ValueError("% de entrenamiento debe estar entre 10% y 90%")
            
            seed = int(self.app_state['seed'].get())
            if seed < 0:
                raise ValueError("Semilla debe ser no-negativa")
                
        except ValueError as e:
            messagebox.showerror("Error de validación", 
                f"❌ Parámetros inválidos:\n\n{str(e)}")
            return False
        except Exception as e:
            messagebox.showerror("Error de validación",
                f"❌ Error inesperado:\n\n{str(e)}")
            return False
        
        return True

    def _on_analyze_click(self):
        if not self._validate_all():
            return
        messagebox.showinfo("Validación OK", 
            "✓ Todos los parámetros son válidos.\n\n"
            "Iniciando análisis en la pestaña Entrenamiento...")
        notebook = self.master
        notebook.select(1)

    def _on_clear_click(self):
        if messagebox.askyesno("Limpiar", 
            "¿Estás seguro de que deseas limpiar el dataset y resetear los parámetros?"):
            self.app_state['dataset'] = None
            self.app_state['dataset_path'] = None
            self._ds_badge.config(text="Sin cargar", 
                                 bg=COLORS["gray_light"], 
                                 fg=COLORS["gray"])
            self._ds_info.config(text="")
            self._col_preview.config(text="")
            self.target_combo["values"] = []
            self.target_combo.set("")
            messagebox.showinfo("Limpiar", "✓ Dataset y parámetros reseteados.")
