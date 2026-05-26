"""
Ventana Principal — versión estable Linux/Windows/Mac
Sin PanedWindow global, sin bind_all.
"""

import tkinter as tk
from tkinter import ttk
import sys, os

from gui.styles import COLORS, FONTS, apply_theme
from gui.tabs.tab_config   import ConfigTab
from gui.tabs.tab_train    import TrainTab
from gui.tabs.tab_predict  import PredictTab
from gui.tabs.tab_results  import ResultsTab
from gui.tabs.tab_guide    import GuideTab
from gui.tabs.tab_datasets import DatasetsTab


def launch_app():
    root = tk.Tk()
    root.title("Clasificador Naïve Bayes — Aprendizaje Automático")
    root.geometry("1100x720")
    root.minsize(900, 600)

    apply_theme(root)

    app = NaiveBayesApp(root)
    app.pack(fill="both", expand=True)
    root.mainloop()


class NaiveBayesApp(tk.Frame):
    def __init__(self, root: tk.Tk, **kw):
        super().__init__(root, bg=COLORS["bg_main"], **kw)
        self.root = root

        self.state = {
            "dataset": None, "dataset_path": None,
            "classifier": None, "metrics": None,
            "y_pred": None, "classes": None,
            "X_train": None, "X_test": None,
            "y_train": None, "y_test": None,
            "predictions": None, "pred_probas": None,
            "target_col":    tk.StringVar(value=""),
            "cont_method":   tk.StringVar(value="gaussian"),
            "laplace_alpha": tk.DoubleVar(value=1.0),
            "n_bins":        tk.IntVar(value=5),
            "kde_bw":        tk.StringVar(value="scott"),
            "train_pct":     tk.DoubleVar(value=70.0),
            "seed":          tk.IntVar(value=42),
        }

        self._build()

    def _build(self):
        # ── Header ────────────────────────────────
        header = tk.Frame(self, bg=COLORS["bg_header"])
        header.pack(fill="x", side="top")

        left = tk.Frame(header, bg=COLORS["bg_header"])
        left.pack(side="left", padx=16, pady=10)

        tk.Label(left, text="🧠", bg=COLORS["bg_header"],
                 fg=COLORS["text_white"],
                 font=("Segoe UI", 20)).pack(side="left")

        col = tk.Frame(left, bg=COLORS["bg_header"])
        col.pack(side="left", padx=8)
        tk.Label(
    col,
    text="Clasificador Naive Bayes",
    bg=COLORS["bg_header"],
    fg=COLORS["text_white"]
).pack(anchor="w")
        tk.Label(col,
                 text="Gaussiana · KDE · Discretización · Laplace Smoothing",
                 bg=COLORS["bg_header"], fg=COLORS["text_light"],
                 font=FONTS["small"], anchor="w").pack(anchor="w")



        # ── Notebook ──────────────────────────────
        self._nb = ttk.Notebook(self)
        self._nb.pack(fill="both", expand=True)

        tabs = [
            ("  ⚙  Configuración  ",  ConfigTab(self._nb,  self.state)),
            ("  ▶  Entrenamiento  ",  TrainTab(self._nb,   self.state)),
            ("  🔮  Predicción     ",  PredictTab(self._nb, self.state)),
            ("  📊  Resultados    ",   ResultsTab(self._nb, self.state)),
            ("  📖  Guía de Uso   ",   GuideTab(self._nb)),
            ("  🗃  Datasets      ",   DatasetsTab(self._nb)),
        ]
        for title, widget in tabs:
            self._nb.add(widget, text=title)

        self._nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

        # ── Status bar ────────────────────────────
        sb = tk.Frame(self, bg=COLORS["bg_dark"], height=24)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)

        self._status = tk.Label(sb,
            text="  ● Listo — Carga un dataset en Configuración para comenzar.",
            bg=COLORS["bg_dark"], fg=COLORS["text_header"],
            font=FONTS["small"], anchor="w")
        self._status.pack(side="left", fill="x", expand=True, padx=6)

        tk.Label(sb, text="v2.0  Naïve Bayes Classifier  ",
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"],
                 font=FONTS["small"]).pack(side="right")

        self.state["target_col"].trace_add("write", self._update_status)

    def _update_status(self, *_):
        if self.state.get("metrics"):
            acc = self.state["metrics"]["accuracy"]
            self._status.config(
                text=f"  ✓ Modelo entrenado — Accuracy: {acc*100:.2f}%  "
                     f"— Método: {self.state['cont_method'].get()}",
                fg="#56d4a0")
        elif self.state.get("dataset") is not None:
            n = len(self.state["dataset"])
            self._status.config(
                text=f"  ● Dataset cargado ({n} instancias) "
                     f"— Ve a Entrenamiento para entrenar.",
                fg=COLORS["text_header"])

    def _on_tab_change(self, event):
        try:
            tab = self._nb.nametowidget(self._nb.select())
            if hasattr(tab, "refresh"):
                tab.refresh()
                self._update_status()
        except Exception:
            pass
