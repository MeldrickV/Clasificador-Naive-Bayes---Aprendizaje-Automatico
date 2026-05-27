import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from gui.styles import COLORS, FONTS
from gui.widgets.components import SectionHeader, MetricCard, Badge


class ResultsTab(ctk.CTkFrame):
    def __init__(self, parent, app_state: dict, **kw):
        super().__init__(parent, fg_color=COLORS["bg_main"], **kw)
        self.app_state = app_state
        self._kde_canvas = None
        self._build()

    def _build(self):
        # Botones de acción
        top = ctk.CTkFrame(self, fg_color=COLORS["bg_main"])
        top.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkButton(top, text="  Actualizar Resultados", command=self.refresh,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=(0,4))
        ctk.CTkButton(top, text="  Exportar Reporte (TXT)", command=self._export,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=4)
        ctk.CTkButton(top, text="  Exportar CSV", command=self._export_csv,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=4)

        self._model_badge = Badge(top, "Sin modelo", style="gray")
        self._model_badge.pack(side="left", padx=8)

        # Contenedor principal con scroll
        self._scroll_frame = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_main"])
        self._scroll_frame.pack(fill="both", expand=True, padx=10, pady=8)

        # Habilitar scroll con rueda del mouse (suave)
        self._enable_smooth_scroll(self._scroll_frame)

        self._placeholder()

    def _enable_smooth_scroll(self, scrollable_frame):
        """Habilita el scroll con la rueda del mouse en un CTkScrollableFrame."""
        canvas = scrollable_frame._parent_canvas

        def on_mousewheel(event):
            if event.num == 4:      # Linux arriba
                delta = -1
            elif event.num == 5:    # Linux abajo
                delta = 1
            else:                   # Windows / macOS
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

    def _placeholder(self):
        for w in self._scroll_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(self._scroll_frame,
                     text="  Entrena el modelo para ver los resultados aquí",
                     font=FONTS["body"], text_color=COLORS["text_secondary"]).pack(pady=60)

    def refresh(self):
        metrics = self.app_state.get("metrics")
        classes = self.app_state.get("classes")
        if metrics is None or classes is None:
            messagebox.showinfo("Sin resultados", "Entrena el modelo primero.")
            return

        for w in self._scroll_frame.winfo_children():
            w.destroy()

        method_map = {
            "gaussian":    "Gaussiana",
            "kde":         "KDE",
            "equal_width": "Discret. Anchos Iguales",
            "equal_freq":  "Discret. Frecuencias Iguales",
        }
        meth = method_map.get(self.app_state["cont_method"].get(), "—")
        self._model_badge.configure(text=f"✓ Método: {meth}",
                                    fg_color=COLORS["primary_light"], text_color=COLORS["primary"])

        # Métricas globales
        self._section(self._scroll_frame, "Métricas Globales", icon="")
        cards_frame = ctk.CTkFrame(self._scroll_frame, fg_color=COLORS["bg_main"])
        cards_frame.pack(fill="x", padx=4, pady=(4,12))
        metrics_data = [
            ("Accuracy", metrics['accuracy'], COLORS["primary"], ""),
            ("Precisión\nMacro", metrics['precision_macro'], COLORS["gaussian"], ""),
            ("Recall\nMacro", metrics['recall_macro'], COLORS["kde"], ""),
            ("F1-Score\nMacro", metrics['f1_macro'], COLORS["ew"], "⚖"),
            ("Precisión\nWeighted", metrics['precision_weighted'], COLORS["ef"], ""),
            ("F1\nWeighted", metrics['f1_weighted'], COLORS["info"], ""),
        ]
        for label, val, color, icon in metrics_data:
            c = MetricCard(cards_frame, label, value=f"{val*100:.2f}%", color=color, icon=icon)
            c.pack(side="left", padx=3, pady=3, fill="x", expand=True)

        # Matriz de confusión (heatmap)
        self._section(self._scroll_frame, "Matriz de Confusión", icon="")
        cm_card = self._card(self._scroll_frame)
        cm_card.pack(fill="x", padx=4, pady=(4,12))
        self._draw_confusion_matrix_heatmap(cm_card, metrics['confusion_matrix'], classes)

        # Visualización KDE si aplica (con histograma)
        if self.app_state["cont_method"].get() == "kde" and self.app_state.get("classifier") is not None:
            self._section(self._scroll_frame, "Visualización KDE + Histograma", icon="〰")
            kde_card = self._card(self._scroll_frame)
            kde_card.pack(fill="x", padx=4, pady=(4,12))
            self._build_kde_visualization(kde_card)

        # Tabla por clase
        self._section(self._scroll_frame, "Métricas por Clase", icon="")
        tbl_card = self._card(self._scroll_frame)
        tbl_card.pack(fill="x", padx=4, pady=(4,12))
        self._draw_class_table(tbl_card, metrics, classes)

    # --------------------------------------------------------------
    # Matriz de confusión con heatmap
    # --------------------------------------------------------------
    def _draw_confusion_matrix_heatmap(self, parent, cm: np.ndarray, classes):
        for w in parent.winfo_children():
            w.destroy()

        modo = ctk.get_appearance_mode()
        bg_color = "#f8fafc" if modo == "Light" else "#1e293b"
        text_color = "#1e293b" if modo == "Light" else "#f8fafc"

        fig, ax = plt.subplots(figsize=(6, 4.5))
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        im = ax.imshow(cm, cmap='Blues', interpolation='nearest')
        ax.set_xticks(np.arange(len(classes)))
        ax.set_yticks(np.arange(len(classes)))
        ax.set_xticklabels(classes, color=text_color)
        ax.set_yticklabels(classes, color=text_color)
        ax.set_xlabel("Predicción", color=text_color, fontsize=10)
        ax.set_ylabel("Valor Real", color=text_color, fontsize=10)

        for i in range(len(classes)):
            for j in range(len(classes)):
                val = cm[i, j]
                color = "white" if val > cm.max() / 2 else text_color
                ax.text(j, i, str(val), ha='center', va='center', color=color, fontsize=10)

        cbar = fig.colorbar(im, ax=ax, shrink=0.8)
        cbar.ax.yaxis.label.set_color(text_color)
        cbar.ax.tick_params(color=text_color, labelcolor=text_color)

        ax.set_title("Matriz de Confusión", color=text_color, fontsize=12)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Evitar que matplotlib capture el scroll
        widget.unbind("<MouseWheel>")
        widget.unbind("<Button-4>")
        widget.unbind("<Button-5>")

        def propagate(event):
            self._scroll_frame._parent_canvas.event_generate(
                event.type,
                delta=getattr(event, 'delta', 0),
                num=getattr(event, 'num', 0),
                x=event.x, y=event.y
            )
            return "break"

        widget.bind("<MouseWheel>", propagate, add=True)
        widget.bind("<Button-4>", propagate, add=True)
        widget.bind("<Button-5>", propagate, add=True)

    # --------------------------------------------------------------
    # Visualización KDE con histograma
    # --------------------------------------------------------------
    def _build_kde_visualization(self, parent):
        clf = self.app_state["classifier"]
        X_train = self.app_state.get("X_train")
        y_train = self.app_state.get("y_train")
        if X_train is None or y_train is None:
            ctk.CTkLabel(parent, text="No hay datos de entrenamiento para visualizar KDE.",
                         font=FONTS["small"], text_color=COLORS["warning"]).pack(padx=12, pady=12)
            return

        # Filtrar atributos continuos (los que tienen KDE entrenado)
        continuous_features = [f for f in clf.feature_names_ if f in clf.kde_models_]
        if not continuous_features:
            ctk.CTkLabel(parent, text="No hay variables continuas con KDE en este modelo.",
                         font=FONTS["small"], text_color=COLORS["warning"]).pack(padx=12, pady=12)
            return

        # Selector de atributo y clase
        control_frame = ctk.CTkFrame(parent, fg_color="transparent")
        control_frame.pack(fill="x", padx=12, pady=(12,6))

        ctk.CTkLabel(control_frame, text="Atributo:", font=FONTS["small_bold"]).pack(side="left", padx=(0,8))
        self._kde_feature_var = ctk.StringVar(value=continuous_features[0])
        feature_combo = ctk.CTkComboBox(control_frame, variable=self._kde_feature_var,
                                        values=continuous_features, state="readonly", width=180)
        feature_combo.pack(side="left", padx=(0,16))

        ctk.CTkLabel(control_frame, text="Clase:", font=FONTS["small_bold"]).pack(side="left", padx=(0,8))
        self._kde_class_var = ctk.StringVar(value=str(clf.classes_[0]))
        class_combo = ctk.CTkComboBox(control_frame, variable=self._kde_class_var,
                                      values=[str(c) for c in clf.classes_], state="readonly", width=120)
        class_combo.pack(side="left")

        ctk.CTkButton(control_frame, text="Actualizar gráfico", command=lambda: self._update_kde_plot(parent),
                      fg_color=COLORS["primary"], width=120).pack(side="left", padx=16)

        self._kde_plot_frame = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"])
        self._kde_plot_frame.pack(fill="both", expand=True, padx=12, pady=(0,12))

        self._update_kde_plot(parent)

    def _update_kde_plot(self, parent_frame):
        clf = self.app_state["classifier"]
        X_train = self.app_state.get("X_train")
        y_train = self.app_state.get("y_train")
        if X_train is None or y_train is None:
            return

        feature = self._kde_feature_var.get()
        class_val = self._kde_class_var.get()
        # Convertir tipo de clase si es numérico
        try:
            class_val = type(clf.classes_[0])(class_val)
        except:
            pass

        # Verificar que exista KDE para esa feature y clase
        if feature not in clf.kde_models_ or class_val not in clf.kde_models_[feature]:
            for w in self._kde_plot_frame.winfo_children():
                w.destroy()
            ctk.CTkLabel(self._kde_plot_frame, text="No hay KDE entrenado para esta combinación.",
                         font=FONTS["small"], text_color=COLORS["warning"]).pack(padx=12, pady=12)
            return

        # Obtener datos reales de entrenamiento para esa clase
        class_mask = (y_train == class_val)
        data = X_train.loc[class_mask, feature].dropna().values
        if len(data) == 0:
            for w in self._kde_plot_frame.winfo_children():
                w.destroy()
            ctk.CTkLabel(self._kde_plot_frame, text=f"No hay datos de entrenamiento para la clase {class_val} en '{feature}'.",
                         font=FONTS["small"], text_color=COLORS["warning"]).pack(padx=12, pady=12)
            return

        # KDE
        kde = clf.kde_models_[feature][class_val]
        x_min, x_max = data.min(), data.max()
        margin = (x_max - x_min) * 0.1
        x = np.linspace(x_min - margin, x_max + margin, 200)
        y = kde.evaluate(x)

        # Modo claro/oscuro
        modo = ctk.get_appearance_mode()
        bg_color = "#f8fafc" if modo == "Light" else "#1e293b"
        text_color = "#1e293b" if modo == "Light" else "#f8fafc"
        kde_color = COLORS["kde"][1] if modo == "Dark" else COLORS["kde"][0]
        hist_color = COLORS["primary"][1] if modo == "Dark" else COLORS["primary"][0]

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        # Histograma de los datos reales (normalizado a densidad)
        ax.hist(data, bins='auto', density=True, alpha=0.5, color=hist_color, edgecolor=text_color, label='Datos reales')

        # Curva KDE
        ax.plot(x, y, color=kde_color, linewidth=2.5, label='Estimación KDE')
        ax.fill_between(x, y, alpha=0.2, color=kde_color)

        ax.set_xlabel(feature, color=text_color)
        ax.set_ylabel("Densidad", color=text_color)
        ax.set_title(f"Distribución de '{feature}' para clase {class_val}", color=text_color)
        ax.tick_params(colors=text_color)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['left'].set_color(text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(loc='best', framealpha=0.5, facecolor=bg_color, edgecolor=text_color)

        # Integrar en tkinter
        for w in self._kde_plot_frame.winfo_children():
            w.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self._kde_plot_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=5, pady=5)

        # Propagar scroll al canvas principal
        widget.unbind("<MouseWheel>")
        widget.unbind("<Button-4>")
        widget.unbind("<Button-5>")

        def propagate(event):
            self._scroll_frame._parent_canvas.event_generate(
                event.type,
                delta=getattr(event, 'delta', 0),
                num=getattr(event, 'num', 0),
                x=event.x, y=event.y
            )
            return "break"

        widget.bind("<MouseWheel>", propagate, add=True)
        widget.bind("<Button-4>", propagate, add=True)
        widget.bind("<Button-5>", propagate, add=True)

    # --------------------------------------------------------------
    # Tabla por clase
    # --------------------------------------------------------------
    def _draw_class_table(self, parent, metrics, classes):
        cm = metrics["confusion_matrix"]
        for i, cls in enumerate(classes):
            p = metrics["precision"][cls]
            r = metrics["recall"][cls]
            f = metrics["f1_score"][cls]
            sup = cm[i].sum()

            if f >= 0.75:
                color = COLORS["success"]
                badge = "Excelente"
            elif f >= 0.5:
                color = COLORS["warning"]
                badge = "Regular"
            else:
                color = COLORS["error"]
                badge = "Bajo"

            card = ctk.CTkFrame(parent, fg_color=self._resolve_color(COLORS["bg_sidebar"]), corner_radius=14)
            card.pack(fill="x", padx=12, pady=8)

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=12, pady=(10,4))
            ctk.CTkLabel(top, text=f"Clase: {cls}", font=FONTS["body_bold"]).pack(side="left")
            Badge(top, badge, style="success" if f >= 0.75 else "warning" if f >= 0.5 else "error").pack(side="right")

            body = ctk.CTkFrame(card, fg_color="transparent")
            body.pack(fill="x", padx=12, pady=(0,12))

            for label, val in [("Precisión", p), ("Recall", r), ("F1", f)]:
                row = ctk.CTkFrame(body, fg_color="transparent")
                row.pack(fill="x", pady=3)
                ctk.CTkLabel(row, text=label, width=90, anchor="w").pack(side="left")
                bar = ctk.CTkProgressBar(row, progress_color=self._resolve_color(color))
                bar.pack(side="left", fill="x", expand=True, padx=8)
                bar.set(val)
                ctk.CTkLabel(row, text=f"{val*100:.1f}%").pack(side="right")

            ctk.CTkLabel(card, text=f"Soporte: {sup} instancias",
                         font=FONTS["small"], text_color=self._resolve_color(COLORS["text_secondary"])
                         ).pack(anchor="e", padx=12, pady=(0,10))

    # --------------------------------------------------------------
    # Auxiliares
    # --------------------------------------------------------------
    def _section(self, parent, title: str, icon: str = ""):
        from gui.widgets.components import SectionHeader
        SectionHeader(parent, title, icon=icon, fg_color=COLORS["bg_main"]).pack(fill="x", padx=4, pady=(10, 2))

    def _card(self, parent) -> ctk.CTkFrame:
        return ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], border_width=1, border_color=COLORS["border"])

    def _resolve_color(self, color):
        if isinstance(color, (tuple, list)):
            modo = ctk.get_appearance_mode()
            return color[1] if modo == "Dark" else color[0]
        return color

    # --------------------------------------------------------------
    # Exportaciones (sin cambios)
    # --------------------------------------------------------------
    def _export(self):
        metrics = self.app_state.get("metrics")
        if not metrics:
            messagebox.showinfo("Sin resultados", "Entrena el modelo primero.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if not path:
            return
        classes = self.app_state["classes"]
        lines = []
        lines.append("REPORTE DE EVALUACIÓN — NAÏVE BAYES")
        lines.append("=" * 60)
        lines.append(f"Accuracy:           {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        lines.append(f"Precisión Macro:    {metrics['precision_macro']:.4f}")
        lines.append(f"Recall Macro:       {metrics['recall_macro']:.4f}")
        lines.append(f"F1-Score Macro:     {metrics['f1_macro']:.4f}")
        lines.append(f"Precisión Weighted: {metrics['precision_weighted']:.4f}")
        lines.append(f"F1 Weighted:        {metrics['f1_weighted']:.4f}")
        lines.append("\nMATRIZ DE CONFUSIÓN:")
        cm = metrics["confusion_matrix"]
        header = f"{'':>16}" + "".join(f"{str(c)[:10]:>12}" for c in classes)
        lines.append(header)
        for i, cls in enumerate(classes):
            row_str = f"{str(cls)[:16]:>16}" + "".join(f"{cm[i,j]:>12}" for j in range(len(classes)))
            lines.append(row_str)
        lines.append("\nMÉTRICAS POR CLASE:")
        lines.append(f"{'Clase':<20} {'Precisión':>10} {'Recall':>10} {'F1':>10}")
        for cls in classes:
            p = metrics["precision"][cls]
            r = metrics["recall"][cls]
            f = metrics["f1_score"][cls]
            lines.append(f"{str(cls):<20} {p:>10.4f} {r:>10.4f} {f:>10.4f}")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        messagebox.showinfo("Guardado", f"Reporte exportado a:\n{path}")

    def _export_csv(self):
        import csv
        metrics = self.app_state.get("metrics")
        if not metrics:
            messagebox.showinfo("Sin resultados", "Entrena el modelo primero.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if not path:
            return
        try:
            classes = self.app_state["classes"]
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["MÉTRICAS DE EVALUACIÓN - CLASIFICADOR NAÏVE BAYES"])
                writer.writerow([])
                writer.writerow(["MÉTRICAS GLOBALES"])
                writer.writerow(["Métrica", "Valor", "Porcentaje"])
                writer.writerow(["Accuracy", metrics['accuracy'], f"{metrics['accuracy']*100:.2f}%"])
                writer.writerow(["Precisión Macro", metrics['precision_macro'], f"{metrics['precision_macro']*100:.2f}%"])
                writer.writerow(["Recall Macro", metrics['recall_macro'], f"{metrics['recall_macro']*100:.2f}%"])
                writer.writerow(["F1-Score Macro", metrics['f1_macro'], f"{metrics['f1_macro']*100:.2f}%"])
                writer.writerow(["Precisión Weighted", metrics['precision_weighted'], f"{metrics['precision_weighted']*100:.2f}%"])
                writer.writerow(["F1 Weighted", metrics['f1_weighted'], f"{metrics['f1_weighted']*100:.2f}%"])
                writer.writerow([])
                writer.writerow(["MÉTRICAS POR CLASE"])
                writer.writerow(["Clase", "Precisión", "Recall", "F1-Score", "Soporte"])
                cm = metrics["confusion_matrix"]
                for i, cls in enumerate(classes):
                    p = metrics["precision"][cls]
                    r = metrics["recall"][cls]
                    f = metrics["f1_score"][cls]
                    sup = cm[i].sum()
                    writer.writerow([cls, f"{p:.4f}", f"{r:.4f}", f"{f:.4f}", sup])
                writer.writerow([])
                writer.writerow(["MATRIZ DE CONFUSIÓN"])
                header = ["Predicho →"] + [str(c) for c in classes]
                writer.writerow(header)
                for i, cls in enumerate(classes):
                    row = [str(cls)] + [cm[i, j] for j in range(len(classes))]
                    writer.writerow(row)
            messagebox.showinfo("Guardado", f"Métricas exportadas a:\n{path}")
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo guardar el archivo:\n{str(e)}")
