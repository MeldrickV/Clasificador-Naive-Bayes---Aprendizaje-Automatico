import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd

from gui.styles import COLORS, FONTS
from gui.widgets.components import SectionHeader, InfoBox, Badge


class PredictTab(ctk.CTkFrame):
    def __init__(self, parent, app_state: dict, **kw):
        super().__init__(parent, fg_color=COLORS["bg_main"], **kw)
        self.app_state = app_state
        self._instances = None
        self._build()

    def _build(self):
        # Panel de carga
        load_card = self._card(self)
        load_card.pack(fill="x", padx=10, pady=(10, 0))

        SectionHeader(load_card, "Cargar Instancias a Clasificar",
                      "Archivo CSV con los mismos atributos del dataset (puede incluir o no la columna de clase)",
                      icon="", fg_color=COLORS["bg_card"]).pack(fill="x", padx=14, pady=(12, 8))

        row = ctk.CTkFrame(load_card, fg_color=COLORS["bg_card"])
        row.pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkButton(row, text="    Cargar archivo CSV",
                      command=self._load_instances,
                      fg_color=COLORS["primary"],
                      hover_color=COLORS["primary_dark"]).pack(side="left", padx=(0, 4))

        ctk.CTkButton(row, text="    Usar dataset de entrenamiento",
                      command=self._use_training_dataset,
                      fg_color=COLORS["info"],
                      hover_color=COLORS["info"][1] if isinstance(COLORS["info"], tuple) else COLORS["info"]).pack(side="left")

        self._inst_badge = Badge(row, "Sin cargar", style="gray")
        self._inst_badge.pack(side="left", padx=10)

        self._inst_info = ctk.CTkLabel(load_card, text="",
                                       font=FONTS["small"],
                                       text_color=COLORS["text_secondary"])
        self._inst_info.pack(anchor="w", padx=14, pady=(0, 4))

        InfoBox(load_card,
                "El archivo puede incluir la columna de clase (será ignorada) o solo las características.\n"
                "Usa el botón 'Usar dataset de entrenamiento' para cargar directamente el mismo dataset que usaste para entrenar.",
                type_="tip").pack(fill="x", padx=14, pady=(0, 12))

        # Botones de acción
        btn_row = ctk.CTkFrame(self, fg_color=COLORS["bg_main"])
        btn_row.pack(fill="x", padx=10, pady=8)

        self._classify_btn = ctk.CTkButton(btn_row, text="   Clasificar Instancias",
                                           command=self._classify,
                                           fg_color=COLORS["success"],
                                           hover_color="#047857", state="disabled")
        self._classify_btn.pack(side="left", padx=(0, 4))

        self._clear_btn = ctk.CTkButton(btn_row, text="   Limpiar Resultados",
                                        command=self._clear_results,
                                        fg_color=COLORS["warning"],
                                        hover_color="#b45309", state="disabled")
        self._clear_btn.pack(side="left", padx=4)

        # Panel de resultados (con scroll)
        res_card = self._card(self)
        res_card.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        SectionHeader(res_card, "Resultados de Clasificación",
                      "Clase predicha y probabilidades por instancia",
                      icon="", fg_color=COLORS["bg_card"]).pack(fill="x", padx=14, pady=(12, 6))

        self._results_container = ctk.CTkScrollableFrame(res_card, fg_color=COLORS["bg_card"])
        self._results_container.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Panel de resumen
        self._summary_frame = ctk.CTkFrame(self._results_container, fg_color=COLORS["bg_card"],
                                           border_width=1, border_color=COLORS["border"])
        self._summary_frame.pack(fill="x", pady=(0, 12))
        self._build_summary_panel()

        # Tabla
        self._build_table()
        self._enable_mousewheel_scroll(self._results_container)

    def _use_training_dataset(self):
        """Carga directamente el dataset de entrenamiento (ignorando la columna de clase)."""
        if self.app_state.get("dataset") is None:
            messagebox.showerror("Sin dataset", "Primero carga un dataset en la pestaña Configuración.")
            return

        clf = self.app_state.get("classifier")
        if clf is None:
            messagebox.showerror("Sin modelo", "Entrena el modelo antes de predecir.")
            return

        df = self.app_state["dataset"].copy()
        target_col = self.app_state["target_col"].get()

        if target_col not in df.columns:
            messagebox.showerror("Error", f"La columna objetivo '{target_col}' no se encuentra en el dataset.")
            return

        X = df.drop(columns=[target_col])

        expected_cols = set(clf.feature_names_)
        actual_cols = set(X.columns)
        if actual_cols != expected_cols:
            missing = expected_cols - actual_cols
            extra = actual_cols - expected_cols
            error_msg = ""
            if missing:
                error_msg += f"Faltan columnas: {', '.join(missing)}\n"
            if extra:
                error_msg += f"Sobran columnas: {', '.join(extra)}\n"
            messagebox.showerror("Columnas incorrectas", error_msg)
            return

        self._instances = X
        self._inst_badge.configure(text="✓ Dataset de entrenamiento (sin clase)",
                                   fg_color=COLORS["success_light"],
                                   text_color=COLORS["success"])
        self._inst_info.configure(text=f"{len(X)} instancias  ·  {len(X.columns)} atributos (clase eliminada)")
        self._classify_btn.configure(state="normal")

    def _load_instances(self):
        if self.app_state.get("classifier") is None:
            messagebox.showerror("Sin modelo", "Entrena el modelo antes de cargar instancias.")
            return

        path = filedialog.askopenfilename(
            title="Cargar archivo CSV (puede incluir o no la columna de clase)",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if not path:
            return

        try:
            df = pd.read_csv(path)
            clf = self.app_state["classifier"]
            target_col = self.app_state["target_col"].get()

            if target_col in df.columns:
                df = df.drop(columns=[target_col])
                messagebox.showinfo("Columna de clase ignorada",
                                    f"El archivo contenía la columna '{target_col}', que ha sido eliminada automáticamente.\n"
                                    "Se usarán el resto de columnas para la predicción.")

            expected_cols = set(clf.feature_names_)
            actual_cols = set(df.columns)
            if actual_cols != expected_cols:
                missing = expected_cols - actual_cols
                extra = actual_cols - expected_cols
                error = ""
                if missing:
                    error += f"Faltan columnas: {', '.join(missing)}\n"
                if extra:
                    error += f"Sobran columnas: {', '.join(extra)}\n"
                messagebox.showerror("Columnas incorrectas", error)
                return

            self._instances = df[clf.feature_names_]
            fname = os.path.basename(path)
            self._inst_badge.configure(text=f"✓ {fname}",
                                       fg_color=COLORS["success_light"],
                                       text_color=COLORS["success"])
            self._inst_info.configure(text=f"{len(df)} instancias  ·  {len(df.columns)} atributos")
            self._classify_btn.configure(state="normal")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _build_summary_panel(self):
        for w in self._summary_frame.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self._summary_frame, fg_color=COLORS["bg_sidebar"])
        header.pack(fill="x")
        ctk.CTkLabel(header, text="📊 Resumen de Predicciones",
                     font=FONTS["small_bold"], text_color=COLORS["text_white"]).pack(anchor="w", padx=10, pady=5)

        self._summary_content = ctk.CTkFrame(self._summary_frame, fg_color="transparent")
        self._summary_content.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(self._summary_content, text="Aún no hay resultados.",
                     font=FONTS["small"], text_color=COLORS["text_secondary"]).pack(pady=10)

    def _build_table(self):
        from tkinter import ttk
        table_frame = ctk.CTkFrame(self._results_container, fg_color=COLORS["bg_card"])
        table_frame.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")

        self._results_tree = ttk.Treeview(table_frame, show="headings", selectmode="browse",
                                          yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=self._results_tree.yview)
        hsb.config(command=self._results_tree.xview)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self._results_tree.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("default")
        modo = ctk.get_appearance_mode()
        bg_tree = "#f8fafc" if modo == "Light" else "#1e293b"
        fg_tree = "#1e293b" if modo == "Light" else "#f8fafc"
        heading_bg = "#e2e8f0" if modo == "Light" else "#334155"
        heading_fg = "#1e293b" if modo == "Light" else "#f8fafc"
        selected_bg = "#3b82f6" if modo == "Light" else "#2563eb"

        style.configure("Treeview", background=bg_tree, foreground=fg_tree,
                        fieldbackground=bg_tree, font=FONTS["small"], rowheight=28)
        style.configure("Treeview.Heading", background=heading_bg, foreground=heading_fg,
                        font=FONTS["small_bold"], relief="flat")
        style.map("Treeview", background=[("selected", selected_bg)])

        self._results_tree.tag_configure("even", background="#f1f5f9" if modo == "Light" else "#0f172a")
        self._results_tree.tag_configure("odd", background=bg_tree)
        self._enable_treeview_mousewheel(self._results_tree)

    def _enable_treeview_mousewheel(self, treeview):
        def on_mousewheel(event):
            if event.num == 4:
                treeview.yview_scroll(-1, "units")
            elif event.num == 5:
                treeview.yview_scroll(1, "units")
            else:
                delta = -1 * (event.delta // abs(event.delta)) if event.delta != 0 else 0
                treeview.yview_scroll(delta, "units")
            return "break"
        treeview.bind("<MouseWheel>", on_mousewheel, add=True)
        treeview.bind("<Button-4>", on_mousewheel, add=True)
        treeview.bind("<Button-5>", on_mousewheel, add=True)

    def _enable_mousewheel_scroll(self, scrollable_frame):
        canvas = scrollable_frame._parent_canvas
        def on_mousewheel(event):
            if event.num == 4:
                delta = -1
            elif event.num == 5:
                delta = 1
            else:
                delta = -1 * (event.delta // abs(event.delta)) if event.delta != 0 else 0
            canvas.yview_scroll(delta, "units")
            return "break"
        canvas.bind("<MouseWheel>", on_mousewheel, add=True)
        canvas.bind("<Button-4>", on_mousewheel, add=True)
        canvas.bind("<Button-5>", on_mousewheel, add=True)
        canvas.focus_set()

        def bind_recursive(widget):
            widget.bind("<MouseWheel>", on_mousewheel, add=True)
            widget.bind("<Button-4>", on_mousewheel, add=True)
            widget.bind("<Button-5>", on_mousewheel, add=True)
            for child in widget.winfo_children():
                bind_recursive(child)
        bind_recursive(scrollable_frame)

    def _classify(self):
        if self.app_state.get("classifier") is None or self._instances is None:
            return

        clf = self.app_state["classifier"]
        preds = clf.predict(self._instances)
        probas = clf.predict_proba(self._instances)

        cols = ["#"] + list(self._instances.columns) + ["Clase Predicha"] + [f"P({c})" for c in clf.classes_]

        self._results_tree["columns"] = cols
        for c in cols:
            width = 80 if c.startswith("P(") else (140 if c == "Clase Predicha" else 70)
            anchor = "center" if c == "#" or c.startswith("P(") else "w"
            self._results_tree.heading(c, text=c)
            self._results_tree.column(c, width=width, anchor=anchor, minwidth=60)

        for row in self._results_tree.get_children():
            self._results_tree.delete(row)

        for i, (pred, proba_row) in enumerate(zip(preds, probas)):
            values = [i+1] + list(self._instances.iloc[i]) + [pred] + [f"{p:.4f}" for p in proba_row]
            tag = "even" if i % 2 == 0 else "odd"
            self._results_tree.insert("", "end", values=values, tags=(tag,))

        self.app_state["predictions"] = preds
        self.app_state["pred_probas"] = probas
        self._update_summary(preds, clf.classes_)
        self._clear_btn.configure(state="normal")

    def _update_summary(self, predictions, classes):
        from collections import Counter
        for w in self._summary_content.winfo_children():
            w.destroy()
        total = len(predictions)
        counts = Counter(predictions)
        total_frame = ctk.CTkFrame(self._summary_content, fg_color="transparent")
        total_frame.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(total_frame, text="Total de instancias:", font=FONTS["body_bold"]).pack(side="left")
        ctk.CTkLabel(total_frame, text=str(total), font=FONTS["body_bold"],
                     text_color=COLORS["primary"]).pack(side="left", padx=(8,0))

        ctk.CTkLabel(self._summary_content, text="Distribución por clase:", font=FONTS["small_bold"],
                     anchor="w").pack(fill="x", pady=(0, 4))
        for cls in classes:
            count = counts.get(cls, 0)
            pct = (count / total * 100) if total > 0 else 0
            row = ctk.CTkFrame(self._summary_content, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=str(cls), width=100, anchor="w").pack(side="left")
            bar = ctk.CTkProgressBar(row, width=200, progress_color=COLORS["success"])
            bar.pack(side="left", padx=8)
            bar.set(pct / 100)
            ctk.CTkLabel(row, text=f"{count} ({pct:.1f}%)", width=80).pack(side="right")

    def _clear_results(self):
        for row in self._results_tree.get_children():
            self._results_tree.delete(row)
        self._build_summary_panel()
        self._clear_btn.configure(state="disabled")
        self.app_state["predictions"] = None
        self.app_state["pred_probas"] = None

    def _card(self, parent) -> ctk.CTkFrame:
        return ctk.CTkFrame(parent,
                            fg_color=COLORS["bg_card"],
                            border_width=1,
                            border_color=COLORS["border"])
