import tkinter as tk
import customtkinter as ctk
import sys, os


from gui.tabs.tab_config   import ConfigTab
from gui.tabs.tab_train    import TrainTab
from gui.tabs.tab_predict  import PredictTab
from gui.tabs.tab_results  import ResultsTab
from gui.tabs.tab_guide    import GuideTab
from gui.tabs.tab_datasets import DatasetsTab
from gui.styles import COLORS


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


def launch_app():
    root = ctk.CTk()
    root.title("Clasificador Naïve Bayes — Aprendizaje Automático")
    root.geometry("1100x720")
    root.minsize(900, 600)

    app = NaiveBayesApp(root)
    app.pack(fill="both", expand=True)
    root.mainloop()


class NaiveBayesApp(ctk.CTkFrame):
    def __init__(self, root: ctk.CTk, **kw):
        super().__init__(root, fg_color="transparent", **kw)
        self.root = root

        self.state = {
	    "dataset": None,
	    "dataset_path": None,
	    "classifier": None,
	    "metrics": None,
	    "y_pred": None,
	    "classes": None,
	    "X_train": None,
	    "X_test": None,
	    "y_train": None,
	    "y_test": None,
	    "predictions": None,
	    "pred_probas": None,

	    "target_col": tk.StringVar(value=""),
	    "cont_method": tk.StringVar(value="gaussian"),


	    "laplace_alpha": tk.StringVar(value="1.0"),
	    "n_bins": tk.StringVar(value="5"),
	    "kde_bw": tk.StringVar(value="scott"),
	    "train_pct": tk.DoubleVar(value=70.0),
	    "seed": tk.StringVar(value="42"),
	}

        self._build()

    def _build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_header"], height=70)
        header.pack(fill="x", side="top", pady=0)
        header.pack_propagate(False)

        # Logo y título
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=16, pady=10)

        ctk.CTkLabel(left, text="", font=("Segoe UI", 24), text_color=COLORS["text_white"]).pack(side="left")
        
        col = ctk.CTkFrame(left, fg_color="transparent")
        col.pack(side="left", padx=8)
        ctk.CTkLabel(col, text="Clasificador Naive Bayes", font=("Segoe UI", 16, "bold"), text_color=COLORS["text_white"]).pack(anchor="w")
        ctk.CTkLabel(col, text="Gaussiana · KDE · Discretización · Laplace Smoothing", font=("Segoe UI", 10), text_color=COLORS["text_secondary"]).pack(anchor="w")

        #Tabview
        self._tabview = ctk.CTkTabview(self, fg_color="transparent")
        self._tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Añadir pestañas
        self._tabview.add("Configuración")
        self._tabview.add("Entrenamiento")
        self._tabview.add("Predicción")
        self._tabview.add("Resultados")
        self._tabview.add("Guía de Uso")
        self._tabview.add("Datasets")

        # Asignar los tabs a cada frame de la tabview
        self.tabs = {
            "Configuración": ConfigTab(self._tabview.tab("Configuración"), self.state),
            "Entrenamiento": TrainTab(self._tabview.tab("Entrenamiento"), self.state),
            "Predicción":   PredictTab(self._tabview.tab("Predicción"), self.state),
            "Resultados":   ResultsTab(self._tabview.tab("Resultados"), self.state),
            "Guía de Uso":  GuideTab(self._tabview.tab("Guía de Uso")),
            "Datasets":     DatasetsTab(self._tabview.tab("Datasets")),
        }
        
        # Mostrar cada tab dentro de su contenedor
        for tab in self.tabs.values():
            tab.pack(fill="both", expand=True)

        # Bind al cambio de pestaña
        self._tabview.configure(command=self._on_tab_change)

        # Status bar
        sb = ctk.CTkFrame(self, height=24, fg_color=COLORS["bg_header"])
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)

        self._status = ctk.CTkLabel(sb,
            text="  ● Listo — Carga un dataset en Configuración para comenzar.",
            anchor="w", font=("Segoe UI", 10), text_color=COLORS["text_secondary"])
        self._status.pack(side="left", fill="x", expand=True, padx=6)

        ctk.CTkLabel(sb, text="v2.0  Naïve Bayes Classifier  ",
                    font=("Segoe UI", 10), text_color="#94a3b8").pack(side="right")

        self.state["target_col"].trace_add("write", self._update_status)

    def _update_status(self, *_):
        if self.state.get("metrics"):
            acc = self.state["metrics"]["accuracy"]
            self._status.configure(
                text=f"  ✓ Modelo entrenado — Accuracy: {acc*100:.2f}%  "
                     f"— Método: {self.state['cont_method'].get()}",
                text_color="#56d4a0")
        elif self.state.get("dataset") is not None:
            n = len(self.state["dataset"])
            self._status.configure(
                text=f"  ● Dataset cargado ({n} instancias) "
                     f"— Ve a Entrenamiento para entrenar.",
                text_color=COLORS["text_secondary"])

    def _on_tab_change(self):
        selected_tab_name = self._tabview.get()

        # Llamar refresh si el tab tiene el método
        tab = self.tabs.get(selected_tab_name)

        if tab and hasattr(tab, "refresh"):
            tab.refresh()

        self._update_status()
