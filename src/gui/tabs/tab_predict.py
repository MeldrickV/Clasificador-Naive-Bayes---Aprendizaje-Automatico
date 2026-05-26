import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

from gui.styles import COLORS, FONTS
from gui.widgets.components import SectionHeader, InfoBox, Badge



class PredictTab(ctk.CTkFrame):
    def __init__(self, parent, app_state: dict, **kw):
        super().__init__(parent, fg_color=COLORS["bg_main"], **kw)
        self.app_state = app_state
        self._instances = None
        self._build()

    def _build(self):
        # Cargar archivo
        load_card = self._card(self)
        load_card.pack(fill="x", padx=10, pady=(10, 0))

        SectionHeader(load_card, "Cargar Instancias a Clasificar",
                      "Archivo CSV con los mismos atributos del dataset (sin la columna de clase)",
                      icon="", fg_color=COLORS["bg_card"]).pack(
                          fill="x", padx=14, pady=(12, 8))

        row = ctk.CTkFrame(load_card, fg_color=COLORS["bg_card"])
        row.pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkButton(row, text="    Cargar instancias (.csv)",
                      command=self._load_instances,
                      fg_color=COLORS["primary"],
                      hover_color=COLORS["primary_dark"]).pack(side="left")

        self._inst_badge = Badge(row, "Sin cargar", style="gray")
        self._inst_badge.pack(side="left", padx=10)

        self._inst_info = ctk.CTkLabel(load_card, text="",
                                       font=FONTS["small"],
                                       text_color=COLORS["text_secondary"])
        self._inst_info.pack(anchor="w", padx=14, pady=(0, 4))

        InfoBox(load_card,
                "El archivo no debe incluir la columna de clase. Solo las características.",
                type_="info").pack(fill="x", padx=14, pady=(0, 12))

        # Botón clasificar
        btn_row = ctk.CTkFrame(self, fg_color=COLORS["bg_main"])
        btn_row.pack(fill="x", padx=10, pady=8)

        ctk.CTkButton(btn_row, text="   Clasificar Instancias",
                      command=self._classify,
                      fg_color=COLORS["success"],
                      hover_color="#047857").pack(side="left")

        # Resultados
        res_card = self._card(self)
        res_card.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        SectionHeader(res_card, "Resultados de Clasificación",
                      "Clase predicha y probabilidades por instancia",
                      icon="", fg_color=COLORS["bg_card"]).pack(
                          fill="x", padx=14, pady=(12, 6))

        # Tabla de resultados con scrollbar
        table_outer = ctk.CTkFrame(res_card, fg_color=COLORS["bg_card"])
        table_outer.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        from tkinter import ttk
        self._results_tree = ttk.Treeview(table_outer,
                                          show="headings",
                                          selectmode="browse")
        vsb = ttk.Scrollbar(table_outer, orient="vertical",
                            command=self._results_tree.yview)
        hsb = ttk.Scrollbar(table_outer, orient="horizontal",
                            command=self._results_tree.xview)
        self._results_tree.configure(yscrollcommand=vsb.set,
                                     xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self._results_tree.pack(fill="both", expand=True)

        # Colores alternativos de filas
        # Elegir colores reales según el modo actual
        bg_card = COLORS["bg_card"]
        if isinstance(bg_card, (list, tuple)):
            modo = ctk.get_appearance_mode()
            bg_card = bg_card[1] if modo == "Dark" else bg_card[0]
        
        even_bg = "#172554" if ctk.get_appearance_mode() == "Dark" else "#f8fafc"
        
        # Colores alternativos de filas
        self._results_tree.tag_configure("even", background=even_bg)
        self._results_tree.tag_configure("odd", background=bg_card)

        # Botón exportar
        ctk.CTkButton(res_card, text="  Exportar resultados (.csv)",
                      command=self._export,
                      fg_color=COLORS["primary"],
                      hover_color=COLORS["primary_dark"]).pack(padx=14, pady=(0, 14),
                                                                anchor="e")


    def _load_instances(self):
        import pandas as pd

        if self.app_state.get("classifier") is None:
            messagebox.showerror("Sin modelo",
                                 "Entrena el modelo antes de cargar instancias.")
            return

        path = filedialog.askopenfilename(
            title="Cargar instancias CSV",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if not path:
            return

        try:
            df = pd.read_csv(path)
            clf = self.app_state["classifier"]
            feat_cols = clf.feature_names_

            missing = set(feat_cols) - set(df.columns)
            if missing:
                messagebox.showerror("Columnas faltantes",
                                     f"Faltan columnas: {', '.join(missing)}")
                return

            self._instances = df[feat_cols]
            fname = os.path.basename(path)
            self._inst_badge.configure(text=f"✓ {fname}",
                                       fg_color=COLORS["success_light"],
                                       text_color=COLORS["success"])
            self._inst_info.configure(text=f"{len(df)} instancias  ·  {len(feat_cols)} atributos")

        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _classify(self):
        if self.app_state.get("classifier") is None:
            messagebox.showerror("Sin modelo", "Primero entrena el modelo.")
            return
        if self._instances is None:
            messagebox.showerror("Sin instancias", "Primero carga un archivo de instancias.")
            return

        clf = self.app_state["classifier"]
        preds = clf.predict(self._instances)
        probas = clf.predict_proba(self._instances)

        # Construir columnas
        cols = ["#"] + list(self._instances.columns) + ["Clase Predicha"] + \
               [f"P({c})" for c in clf.classes_]

        self._results_tree["columns"] = cols
        for c in cols:
            width = 80 if c.startswith("P(") else (120 if c == "Clase Predicha" else 70)
            self._results_tree.heading(c, text=c)
            self._results_tree.column(c, width=width, anchor="center", minwidth=60)

        # Limpiar
        for row in self._results_tree.get_children():
            self._results_tree.delete(row)

        # Insertar filas
        for i, (pred, proba_row) in enumerate(zip(preds, probas)):
            vals = [i+1] + list(self._instances.iloc[i]) + [pred] + [f"{p:.3f}" for p in proba_row]
            tag = "even" if i % 2 == 0 else "odd"
            self._results_tree.insert("", "end", values=vals, tags=(tag,))

        self.app_state["predictions"] = preds
        self.app_state["pred_probas"] = probas

    def _export(self):
        import pandas as pd

        if not self._results_tree.get_children():
            messagebox.showinfo("Sin resultados", "Clasifica instancias primero.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")])
        if not path:
            return

        rows = [self._results_tree.item(row)["values"]
                for row in self._results_tree.get_children()]
        cols = self._results_tree["columns"]
        pd.DataFrame(rows, columns=cols).to_csv(path, index=False)
        messagebox.showinfo("Guardado", f"Resultados exportados a:\n{path}")

    def _card(self, parent) -> ctk.CTkFrame:
        return ctk.CTkFrame(parent,
                            fg_color=COLORS["bg_card"],
                            border_width=1,
                            border_color=COLORS["border"])
