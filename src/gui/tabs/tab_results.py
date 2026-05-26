import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import customtkinter as ctk

from gui.styles import COLORS, FONTS
from gui.widgets.components import SectionHeader, MetricCard, Badge


class ResultsTab(ctk.CTkFrame):
    def __init__(self, parent, app_state: dict, **kw):
        super().__init__(parent, fg_color=COLORS["bg_main"], **kw)
        self.app_state = app_state
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

        # Contenedor principal con scroll usando CTkScrollableFrame
        self._scroll_frame = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_main"])
        self._scroll_frame.pack(fill="both", expand=True, padx=10, pady=8)

        self._placeholder()

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

        # Matriz de confusión
        self._section(self._scroll_frame, "Matriz de Confusión", icon="")
        cm_card = self._card(self._scroll_frame)
        cm_card.pack(fill="x", padx=4, pady=(4,12))
        self._draw_confusion_matrix(cm_card, metrics['confusion_matrix'], classes)

        # Tabla por clase
        self._section(self._scroll_frame, "Métricas por Clase", icon="")
        tbl_card = self._card(self._scroll_frame)
        tbl_card.pack(fill="x", padx=4, pady=(4,12))
        self._draw_class_table(tbl_card, metrics, classes)


    #  MATRIZ DE CONFUSIÓN VISUAL

    def _draw_confusion_matrix(self, parent, cm: np.ndarray, classes):
        n = len(classes)
        cm_max = cm.max() if cm.max() > 0 else 1
    
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.pack(padx=18, pady=18)
    
        title_row = ctk.CTkFrame(wrap, fg_color="transparent")
        title_row.pack()
    
        ctk.CTkLabel(
            title_row,
            text="Predicción",
            font=FONTS["small_bold"],
            text_color=self._resolve_color(COLORS["text_secondary"])
        ).grid(row=0, column=1, columnspan=n, pady=(0,6))
    
        grid = ctk.CTkFrame(
            wrap,
            fg_color=self._resolve_color(COLORS["bg_card"])
        )
        grid.pack()
    
        # esquina
        ctk.CTkLabel(
            grid,
            text="Real ↓\nPred →",
            width=90,
            height=60,
            corner_radius=8,
            fg_color=self._resolve_color(COLORS["primary_light"]),
            font=FONTS["small_bold"]
        ).grid(row=0, column=0, padx=4, pady=4)
    
        # headers columnas
        for j, cls in enumerate(classes):
            ctk.CTkLabel(
                grid,
                text=str(cls),
                width=90,
                height=40,
                corner_radius=8,
                fg_color=self._resolve_color(COLORS["bg_sidebar"]),
                font=FONTS["small_bold"]
            ).grid(row=0, column=j+1, padx=4, pady=4)
    
        for i, row_cls in enumerate(classes):
    
            # header fila
            ctk.CTkLabel(
                grid,
                text=str(row_cls),
                width=90,
                height=70,
                corner_radius=8,
                fg_color=self._resolve_color(COLORS["bg_sidebar"]),
                font=FONTS["small_bold"]
            ).grid(row=i+1, column=0, padx=4, pady=4)
    
            for j in range(n):
    
                val = cm[i, j]
                intensity = val / cm_max
    
                if i == j:
                    bg = self._lerp_hex(
                        COLORS["success_light"],
                        COLORS["success"],
                        intensity
                    )
                    fg = "#ffffff" if intensity > 0.55 else "#111827"
                else:
                    bg = self._lerp_hex(
                        COLORS["error_light"],
                        "#ffffff",
                        1 - intensity
                    )
                    fg = self._resolve_color(COLORS["text"])
    
                total_row = cm[i].sum()
                pct = (val / total_row * 100) if total_row else 0
    
                cell = ctk.CTkFrame(
                    grid,
                    width=90,
                    height=70,
                    corner_radius=10,
                    fg_color=bg
                )
                cell.grid(row=i+1, column=j+1, padx=4, pady=4)
                cell.grid_propagate(False)
    
                ctk.CTkLabel(
                    cell,
                    text=str(val),
                    font=("Segoe UI", 18, "bold"),
                    text_color=fg
                ).pack(pady=(10,0))
    
                ctk.CTkLabel(
                    cell,
                    text=f"{pct:.1f}%",
                    font=FONTS["small"],
                    text_color=fg
                ).pack()
    
    
    def _resolve_color(self, color):
        if isinstance(color, (tuple, list)):
            modo = ctk.get_appearance_mode()
            return color[1] if modo == "Dark" else color[0]
        return color
    
    def _lerp_hex(self, c1, c2, t: float) -> str:
        t = max(0.0, min(1.0, t))
    
        c1 = self._resolve_color(c1)
        c2 = self._resolve_color(c2)
    
        def parse(c):
            c = c.lstrip("#")
            return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
    
        r1, g1, b1 = parse(c1)
        r2, g2, b2 = parse(c2)
    
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
    
        return f"#{r:02x}{g:02x}{b:02x}"


    #  TABLA DE MÉTRICAS POR CLASE

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
    
            card = ctk.CTkFrame(
                parent,
                fg_color=self._resolve_color(COLORS["bg_sidebar"]),
                corner_radius=14
            )
            card.pack(fill="x", padx=12, pady=8)
    
            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=12, pady=(10,4))
    
            ctk.CTkLabel(
                top,
                text=f"Clase: {cls}",
                font=FONTS["body_bold"]
            ).pack(side="left")
    
            Badge(
                top,
                badge,
                style="success" if f >= 0.75 else
                      "warning" if f >= 0.5 else
                      "error"
            ).pack(side="right")
    
            body = ctk.CTkFrame(card, fg_color="transparent")
            body.pack(fill="x", padx=12, pady=(0,12))
    
            data = [
                ("Precisión", p),
                ("Recall", r),
                ("F1", f)
            ]
    
            for label, val in data:
    
                row = ctk.CTkFrame(body, fg_color="transparent")
                row.pack(fill="x", pady=3)
    
                ctk.CTkLabel(
                    row,
                    text=label,
                    width=90,
                    anchor="w"
                ).pack(side="left")
    
                bar = ctk.CTkProgressBar(
                    row,
                    progress_color=self._resolve_color(color)
                )
                bar.pack(side="left", fill="x", expand=True, padx=8)
                bar.set(val)
    
                ctk.CTkLabel(
                    row,
                    text=f"{val*100:.1f}%"
                ).pack(side="right")
    
            ctk.CTkLabel(
                card,
                text=f"Soporte: {sup} instancias",
                font=FONTS["small"],
                text_color=self._resolve_color(COLORS["text_secondary"])
            ).pack(anchor="e", padx=12, pady=(0,10))


    def _section(self, parent, title: str, icon: str = ""):
        from gui.widgets.components import SectionHeader
        SectionHeader(parent, title, icon=icon,
                      fg_color=COLORS["bg_main"]).pack(
                          fill="x", padx=4, pady=(10, 2))

    def _card(self, parent) -> ctk.CTkFrame:
        return ctk.CTkFrame(parent,
                            fg_color=COLORS["bg_card"],
                            border_width=1,
                            border_color=COLORS["border"])

    def _export(self):
        metrics = self.app_state.get("metrics")
        if not metrics:
            messagebox.showinfo("Sin resultados", "Entrena el modelo primero.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
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
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
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
