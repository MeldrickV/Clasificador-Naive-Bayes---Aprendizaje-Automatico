import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os

# from gui.widgets.components import InfoBox, SectionHeader, MethodCard, Badge, Tooltip, ScrollableFrame
from gui.styles import COLORS, FONTS
from gui.widgets.components import InfoBox, SectionHeader, MethodCard, Badge, Tooltip, ScrollableFrame
from gui.widgets.help_panel import HelpPanel



class ConfigTab(ctk.CTkFrame):
    def __init__(self, parent, app_state: dict, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.app_state = app_state
        self._build()

    def _build(self):
        # Panel izquierdo con scroll - usando CTkScrollableFrame
        left = ctk.CTkScrollableFrame(self, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(8, 4), pady=8)

        # Panel derecho de ayuda (ancho 360)
        right = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"], width=360)
        right.pack(side="right", fill="both", expand=False, padx=(0, 8), pady=8)
        right.pack_propagate(False)

        self.help_panel = HelpPanel(right)
        self.help_panel.pack(fill="both", expand=True)

        # Construir secciones dentro del scrollable frame
        self._build_dataset(left)
        self._build_method(left)
        self._build_params(left)

    # Dataset
    def _build_dataset(self, parent):
        card = self._card(parent)
        SectionHeader(card, "Dataset de Entrenamiento",
                      "Archivo CSV con atributos y columna de clase",
                      icon="", fg_color="#ffffff").pack(
                          fill="x", padx=12, pady=(12, 8))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(0, 4))

        ctk.CTkButton(row, text="Cargar Dataset (.csv)",
                      command=self._load_dataset).pack(side="left")

        self._ds_badge = Badge(row, "Sin cargar", style="gray")
        self._ds_badge.pack(side="left", padx=10)

        self._ds_info = ctk.CTkLabel(card, text="", font=("Segoe UI", 10))
        self._ds_info.pack(anchor="w", padx=12)

        self._col_preview = ctk.CTkLabel(card, text="",
                                         font=("Segoe UI", 10),
                                         wraplength=480, justify="left")
        self._col_preview.pack(anchor="w", padx=12, pady=(0, 4))

        # Separador
        ctk.CTkFrame(card, height=1, fg_color="#e2e8f0").pack(fill="x", padx=12, pady=6)

        obj_row = ctk.CTkFrame(card, fg_color="transparent")
        obj_row.pack(fill="x", padx=12, pady=(0, 12))

        ctk.CTkLabel(obj_row, text="Columna objetivo (clase):",
                     font=("Segoe UI", 10, "bold")).pack(side="left")

        self.target_combo = ctk.CTkComboBox(obj_row, state="readonly", width=260,
                                            variable=self.app_state["target_col"],
                                            values=[])
        self.target_combo.pack(side="left", padx=(10, 0))
        Tooltip(self.target_combo,
                "Columna que contiene las etiquetas de clase (lo que el modelo predice).")

    # Método
    def _build_method(self, parent):
        card = self._card(parent)

        SectionHeader(card, "Método para Variables Continuas",
                      "Cómo estimar la probabilidad de valores numéricos",
                      icon="", fg_color="#ffffff").pack(
                          fill="x", padx=12, pady=(12, 8))

        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=(0, 6))
        grid.grid_columnconfigure((0, 1), weight=1)

        var = self.app_state["cont_method"]

        cards_data = [
            ("gaussian",    "Gaussiana",     "Distribución normal (μ, σ)",
             "#4f46e5", "#ede9fe", ""),
            ("kde",         "KDE",           "Estimación no paramétrica",
             "#0891b2", "#cffafe", ""),
            ("equal_width", "Anchos =",      "Intervalos de igual tamaño",
             "#059669", "#d1fae5", ""),
            ("equal_freq",  "Frecuencias =", "Igual cantidad por intervalo",
             "#d97706", "#fef3c7", "⚖"),
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

    # Parámetros
    def _build_params(self, parent):
        card = self._card(parent)
        SectionHeader(card, "Parámetros de Configuración",
                      "Hiperparámetros del modelo",
                      icon="⚙", fg_color="#ffffff").pack(
                          fill="x", padx=12, pady=(12, 8))

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="x", padx=12, pady=(0, 12))
        body.grid_columnconfigure(1, weight=1)

        # Laplace alpha
        self._param_row(body, 0, "Laplace Alpha (α):",
                        self.app_state["laplace_alpha"], "laplace",
                        "Suavizado para variables discretas. Evita P = 0.")

        # N bins
        self._param_row(body, 1, "N° de Bins:",
                        self.app_state["n_bins"], "nbins",
                        "Intervalos para discretizar variables continuas.")

        # KDE bandwidth
        ctk.CTkLabel(body, text="Bandwidth KDE:", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky="w", pady=5)

        kde_f = ctk.CTkFrame(body, fg_color="transparent")
        kde_f.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=5)

        ctk.CTkComboBox(kde_f, variable=self.app_state["kde_bw"],
                        values=["scott", "silverman"],
                        state="readonly", width=120).pack(side="left")

        bw_help = ctk.CTkLabel(kde_f, text="  ", text_color="#0891b2",
                               cursor="hand2", font=("Segoe UI", 10))
        bw_help.pack(side="left")
        bw_help.bind("<Button-1>",
                     lambda e: self.help_panel.show_param("kde_bw"))

        # Separador
        ctk.CTkFrame(body, height=1, fg_color="#e2e8f0").grid(row=3, column=0, columnspan=2,
                                                               sticky="ew", pady=8)

        ctk.CTkLabel(body, text="División Entrenamiento / Prueba:",
                     font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", pady=5)

        split_f = ctk.CTkFrame(body, fg_color="transparent")
        split_f.grid(row=4, column=1, sticky="ew", padx=(10, 0), pady=5)

        self._split_lbl = ctk.CTkLabel(split_f,
                                       text="70% entrenamiento / 30% prueba",
                                       text_color="#2563eb",
                                       font=("Segoe UI", 10, "bold"))
        self._split_lbl.pack(anchor="w")

        self._slider = ctk.CTkSlider(split_f, from_=10, to=90,
                                     variable=self.app_state["train_pct"],
                                     command=self._upd_split, width=180)
        self._slider.pack(anchor="w", pady=(2, 0))

        help_lbl = ctk.CTkLabel(split_f, text="¿Qué es esto?",
                                text_color="#2563eb", cursor="hand2",
                                font=("Segoe UI", 9))
        help_lbl.pack(anchor="w")
        help_lbl.bind("<Button-1>",
                      lambda e: self.help_panel.show_param("split"))

        # Separador
        ctk.CTkFrame(body, height=1, fg_color="#e2e8f0").grid(row=5, column=0, columnspan=2,
                                                               sticky="ew", pady=6)

        ctk.CTkLabel(body, text="Semilla aleatoria:",
                     font=("Segoe UI", 10)).grid(row=6, column=0, sticky="w", pady=5)

        seed_f = ctk.CTkFrame(body, fg_color="transparent")
        seed_f.grid(row=6, column=1, sticky="w", padx=(10, 0), pady=5)

        ctk.CTkEntry(seed_f, textvariable=self.app_state["seed"],
                     width=100).pack(side="left")
        ctk.CTkLabel(seed_f, text="  (para reproducir resultados)",
                     font=("Segoe UI", 9), text_color="#94a3b8").pack(side="left")

        # Botones de acción
        ctk.CTkFrame(card, height=1, fg_color="#e2e8f0").pack(fill="x", padx=12, pady=8)
        
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=12, pady=(0, 12))
        
        analyze_btn = ctk.CTkButton(
            btn_frame,
            text="ANÁLISIS",
            command=self._on_analyze_click,
            fg_color="#2563eb", hover_color="#1d4ed8"
        )
        analyze_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        ctk.CTkButton(
            btn_frame,
            text="LIMPIAR",
            command=self._on_clear_click,
            fg_color="#e2e8f0", text_color="#2563eb", hover_color="#dbeafe"
        ).pack(side="left", fill="x", expand=True)

    # Helpers
    def _card(self, parent) -> ctk.CTkFrame:
        f = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"])
        f.pack(fill="x", pady=4)
        return f

    def _param_row(self, parent, row, label, var, help_key, tip):
        ctk.CTkLabel(parent, text=label, font=("Segoe UI", 10)).grid(
            row=row, column=0, sticky="w", pady=3)
        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.grid(row=row, column=1, sticky="w", padx=(10, 0), pady=5)

        ctk.CTkEntry(inner, textvariable=var, width=100).pack(side="left")

        hl = ctk.CTkLabel(inner, text=" ", text_color="#2563eb",
                          cursor="hand2", font=("Segoe UI", 10))
        hl.pack(side="left")
        hl.bind("<Button-1>",
                lambda e, k=help_key: self.help_panel.show_param(k))

        ctk.CTkLabel(inner, text=tip, font=("Segoe UI", 9),
                     text_color="#94a3b8").pack(side="left", padx=(6, 0))

    def _upd_split(self, val):
        pct = int(float(val))
        self._split_lbl.configure(text=f"{pct}% entrenamiento  /  {100 - pct}% prueba")

    # Carga dataset
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

            self._ds_badge.configure(text=f"✓ {fname}",
                                     fg_color=COLORS["success_light"],
                                     text_color=COLORS["success"])
            self._ds_info.configure(text=f"{n_rows} instancias  ·  {n_cols} columnas")

            cols = list(df.columns)
            preview = "Columnas: " + ", ".join(
                f"{c}({str(df[c].dtype)[:3]})" for c in cols[:8])
            if len(cols) > 8:
                preview += f" (+{len(cols)-8} más)"
            self._col_preview.configure(text=preview)

            self.target_combo.configure(values=cols)
            self.target_combo.set(cols[-1])
            self.app_state["target_col"].set(cols[-1])

            messagebox.showinfo("Dataset cargado",
                                f"{fname}\n{n_rows} instancias · "
                                f"{n_cols} columnas")
        except Exception as exc:
            messagebox.showerror("Error al cargar dataset", str(exc))

    # VALIDACIÓN Y ANÁLISIS
    def _validate_all(self):
        if self.app_state.get('dataset') is None:
            messagebox.showerror("Error de validación", 
                "Dataset no cargado.\n\nPor favor, carga un archivo CSV primero.")
            return False
        
        target = self.app_state['target_col'].get()
        if not target:
            messagebox.showerror("Error de validación",
                "Columna objetivo no seleccionada.\n\nSelecciona la columna que contiene las etiquetas de clase.")
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
                f"Parámetros inválidos:\n\n{str(e)}")
            return False
        except Exception as e:
            messagebox.showerror("Error de validación",
                f"Error inesperado:\n\n{str(e)}")
            return False
        
        return True

    def _on_analyze_click(self):
        if not self._validate_all():
            return
        messagebox.showinfo("Validación OK",
            "✓ Todos los parámetros son válidos.\n\n"
            "Iniciando análisis en la pestaña Entrenamiento...")
        # Cambiar a la pestaña "Entrenamiento" en el CTkTabview
        tabview = self.master
        if hasattr(tabview, "set"):
            tabview.set("Entrenamiento")
        else:
            # Fallback: buscar en la ventana principal
            root = self.winfo_toplevel()
            if hasattr(root, "_tabview"):
                root._tabview.set("Entrenamiento")

    def _on_clear_click(self):
        if messagebox.askyesno("Limpiar",
            "¿Estás seguro de que deseas limpiar el dataset y resetear los parámetros?"):
            self.app_state['dataset'] = None
            self.app_state['dataset_path'] = None
            self._ds_badge.configure(text="Sin cargar",
                                     fg_color="#e2e8f0",
                                     text_color=COLORS["text_secondary"])
            self._ds_info.configure(text="")
            self._col_preview.configure(text="")
            self.target_combo.configure(values=[])
            self.target_combo.set("")
            messagebox.showinfo("Limpiar", "✓ Dataset y parámetros reseteados.")
