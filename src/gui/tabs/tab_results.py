"""
Pestaña 4 — Resultados
=======================
Muestra la matriz de confusión visual, métricas detalladas y exportación.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np

from gui.styles import COLORS, FONTS
from gui.widgets.components import SectionHeader, MetricCard, Badge


class ResultsTab(tk.Frame):

    def __init__(self, parent, app_state: dict, **kw):
        super().__init__(parent, bg=COLORS["bg_main"], **kw)
        self.app_state = app_state
        self._build()

    def _build(self):
        # ── Botones de acción ──────────────────────
        top = tk.Frame(self, bg=COLORS["bg_main"])
        top.pack(fill="x", padx=10, pady=(10, 0))

        ttk.Button(top, text="🔄  Actualizar Resultados",
                   style="Primary.TButton",
                   command=self.refresh).pack(side="left", padx=(0, 4))

        ttk.Button(top, text="💾  Exportar Reporte (TXT)",
                   style="Secondary.TButton",
                   command=self._export).pack(side="left", padx=4)

        ttk.Button(top, text="📊  Exportar CSV",
                   style="Secondary.TButton",
                   command=self._export_csv).pack(side="left", padx=4)

        self._model_badge = Badge(top, "Sin modelo", style="gray")
        self._model_badge.pack(side="left", padx=8)

        # ── Contenedor con scroll ──────────────────
        outer = tk.Frame(self, bg=COLORS["bg_main"])
        outer.pack(fill="both", expand=True, padx=10, pady=8)

        canvas = tk.Canvas(outer, bg=COLORS["bg_main"], highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self._scroll_frame = tk.Frame(canvas, bg=COLORS["bg_main"])
        self._scroll_frame.bind("<Configure>",
                                lambda e: canvas.configure(
                                    scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Configurar scroll con rueda del mouse
        self._canvas = canvas  # guardar referencia

        def _on_mousewheel(event):
            self._canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _on_mousewheel_linux(event):
            self._canvas.yview_scroll(-1 if event.num==4 else 1, "units")

        self._canvas.bind("<MouseWheel>", _on_mousewheel)
        self._canvas.bind("<Button-4>", _on_mousewheel_linux)
        self._canvas.bind("<Button-5>", _on_mousewheel_linux)

        self._placeholder()

    def _placeholder(self):
        for w in self._scroll_frame.winfo_children():
            w.destroy()
        tk.Label(self._scroll_frame,
                 text="🏁  Entrena el modelo para ver los resultados aquí",
                 bg=COLORS["bg_main"], fg=COLORS["text_secondary"],
                 font=FONTS["body"]).pack(pady=60)

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
        self._model_badge.config(
            text=f"✓ Método: {meth}",
            bg=COLORS["primary_light"], fg=COLORS["primary"])

        # ── 1. Tarjetas de métricas globales ───────
        self._section(self._scroll_frame, "Métricas Globales", icon="🎯")

        cards_frame = tk.Frame(self._scroll_frame, bg=COLORS["bg_main"])
        cards_frame.pack(fill="x", padx=4, pady=(4, 12))

        metrics_data = [
            ("Accuracy",     metrics['accuracy'],           COLORS["primary"],  "🎯"),
            ("Precisión\nMacro", metrics['precision_macro'], COLORS["gaussian"], "🔬"),
            ("Recall\nMacro",    metrics['recall_macro'],    COLORS["kde"],      "🔎"),
            ("F1-Score\nMacro",  metrics['f1_macro'],        COLORS["ew"],       "⚖"),
            ("Precisión\nWeighted", metrics['precision_weighted'], COLORS["ef"], "📐"),
            ("F1\nWeighted",     metrics['f1_weighted'],    COLORS["info"],      "📊"),
        ]
        for label, val, color, icon in metrics_data:
            c = MetricCard(cards_frame, label,
                           value=f"{val*100:.2f}%",
                           color=color, icon=icon)
            c.pack(side="left", padx=3, pady=3, fill="x", expand=True)

        # ── 2. Matriz de confusión ─────────────────
        self._section(self._scroll_frame, "Matriz de Confusión", icon="🗂")

        cm_card = self._card(self._scroll_frame)
        cm_card.pack(fill="x", padx=4, pady=(4, 12))
        self._draw_confusion_matrix(cm_card,
                                    metrics['confusion_matrix'], classes)

        # ── 3. Tabla de métricas por clase ─────────
        self._section(self._scroll_frame, "Métricas por Clase", icon="📊")

        tbl_card = self._card(self._scroll_frame)
        tbl_card.pack(fill="x", padx=4, pady=(4, 12))
        self._draw_class_table(tbl_card, metrics, classes)

    # ──────────────────────────────────────────────
    #  MATRIZ DE CONFUSIÓN VISUAL
    # ──────────────────────────────────────────────
    def _draw_confusion_matrix(self, parent, cm: np.ndarray, classes):
        n = len(classes)
        cell_w = max(70, min(100, 600 // (n + 1)))
        container = tk.Frame(parent, bg=COLORS["bg_card"])
        container.pack(padx=14, pady=14)

        tk.Label(container, text="Predicho →",
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 font=FONTS["small_bold"]).grid(row=0, column=1, columnspan=n)

        tk.Label(container, text="R\ne\na\nl\n↓",
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 font=FONTS["small_bold"],
                 justify="center").grid(row=2, column=0, padx=(0, 6))

        for j, cls in enumerate(classes):
            tk.Label(container, text=str(cls)[:10],
                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                     font=FONTS["small_bold"],
                     width=int(cell_w/8)).grid(row=1, column=j+1, pady=(0, 3))

        cm_max = cm.max() if cm.max() > 0 else 1
        for i, row_cls in enumerate(classes):
            tk.Label(container, text=str(row_cls)[:12],
                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                     font=FONTS["small_bold"],
                     anchor="e", width=12).grid(row=i+2, column=0, padx=(0, 6))
            for j in range(n):
                val = cm[i, j]
                intensity = val / cm_max
                if i == j:
                    bg_hex = self._lerp_hex(COLORS["success_light"],
                                            COLORS["success"], intensity)
                    fg_hex = "#ffffff" if intensity > 0.5 else COLORS["text"]
                else:
                    bg_hex = self._lerp_hex("#ffffff",
                                            COLORS["error_light"], intensity)
                    fg_hex = COLORS["error"] if intensity > 0 else COLORS["text_light"]
                cell = tk.Label(container, text=str(val),
                                bg=bg_hex, fg=fg_hex,
                                font=FONTS["body_bold"],
                                width=int(cell_w/8), height=2,
                                relief="flat",
                                highlightbackground=COLORS["border"],
                                highlightthickness=1)
                cell.grid(row=i+2, column=j+1, padx=1, pady=1)

        legend = tk.Frame(parent, bg=COLORS["bg_card"])
        legend.pack(padx=14, pady=(0, 10), anchor="w")
        tk.Label(legend, text="■", bg=COLORS["bg_card"],
                 fg=COLORS["success"], font=FONTS["body"]).pack(side="left")
        tk.Label(legend, text=" Correcto  ",
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 font=FONTS["small"]).pack(side="left")
        tk.Label(legend, text="■", bg=COLORS["bg_card"],
                 fg=COLORS["error"], font=FONTS["body"]).pack(side="left")
        tk.Label(legend, text=" Error",
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 font=FONTS["small"]).pack(side="left")

    def _lerp_hex(self, c1: str, c2: str, t: float) -> str:
        t = max(0.0, min(1.0, t))
        def parse(c):
            c = c.lstrip("#")
            return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
        r1, g1, b1 = parse(c1)
        r2, g2, b2 = parse(c2)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ──────────────────────────────────────────────
    #  TABLA DE MÉTRICAS POR CLASE
    # ──────────────────────────────────────────────
    def _draw_class_table(self, parent, metrics: dict, classes):
        tree = ttk.Treeview(parent, columns=("clase", "prec", "recall",
                                              "f1", "support"),
                            show="headings", height=len(classes)+2)
        tree.heading("clase",   text="Clase")
        tree.heading("prec",    text="Precisión")
        tree.heading("recall",  text="Recall")
        tree.heading("f1",      text="F1-Score")
        tree.heading("support", text="Soporte")
        for col in ("clase", "prec", "recall", "f1", "support"):
            w = 180 if col == "clase" else 100
            tree.column(col, width=w, anchor="center")

        cm = metrics["confusion_matrix"]
        tree.tag_configure("high", foreground=COLORS["success"])
        tree.tag_configure("med",  foreground=COLORS["warning"])
        tree.tag_configure("low",  foreground=COLORS["error"])
        tree.tag_configure("total", foreground=COLORS["primary"],
                           font=FONTS["body_bold"])

        for i, cls in enumerate(classes):
            p = metrics["precision"][cls]
            r = metrics["recall"][cls]
            f = metrics["f1_score"][cls]
            sup = cm[i].sum()
            tag = "high" if f >= 0.75 else ("med" if f >= 0.5 else "low")
            tree.insert("", "end",
                        values=(cls,
                                f"{p:.4f} ({p*100:.1f}%)",
                                f"{r:.4f} ({r*100:.1f}%)",
                                f"{f:.4f} ({f*100:.1f}%)",
                                sup),
                        tags=(tag,))

        tree.insert("", "end",
                    values=("MACRO",
                            f"{metrics['precision_macro']:.4f} ({metrics['precision_macro']*100:.1f}%)",
                            f"{metrics['recall_macro']:.4f} ({metrics['recall_macro']*100:.1f}%)",
                            f"{metrics['f1_macro']:.4f} ({metrics['f1_macro']*100:.1f}%)",
                            cm.sum()),
                    tags=("total",))
        tree.pack(fill="x", padx=14, pady=14)

    # ──────────────────────────────────────────────
    def _section(self, parent, title: str, icon: str = ""):
        from gui.widgets.components import SectionHeader
        SectionHeader(parent, title, icon=icon,
                      bg=COLORS["bg_main"]).pack(
                          fill="x", padx=4, pady=(10, 2))

    def _card(self, parent) -> tk.Frame:
        return tk.Frame(parent, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1)

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
