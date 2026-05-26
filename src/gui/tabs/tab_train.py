import threading
import numpy as np
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from gui.styles import COLORS, FONTS
from gui.widgets.components import SectionHeader, MetricCard, Badge


class TrainTab(ctk.CTkFrame):
    """Pestaña de entrenamiento del clasificador."""

    def __init__(self, parent, app_state: dict, **kw):
        super().__init__(parent, fg_color=COLORS["bg_main"], **kw)
        self.app_state = app_state
        self._build()

    def _build(self):
        # Encabezado de acción
        action_bar = ctk.CTkFrame(self, fg_color=COLORS["bg_card"],
                                  border_width=1, border_color=COLORS["border"])
        action_bar.pack(fill="x", padx=10, pady=(10, 0))

        inner = ctk.CTkFrame(action_bar, fg_color=COLORS["bg_card"])
        inner.pack(fill="x", padx=16, pady=12)

        self._train_btn = ctk.CTkButton(inner, text="    Entrenar Modelo",
                                        command=self._start_training,
                                        fg_color=COLORS["success"],
                                        hover_color="#047857")
        self._train_btn.pack(side="left")

        self._status_badge = Badge(inner, "Sin entrenar", style="gray")
        self._status_badge.pack(side="left", padx=14)

        self._progress = ctk.CTkProgressBar(inner, width=200, mode="indeterminate")
        self._progress.pack(side="left")
        self._progress.set(0)

        # Tarjetas de métricas
        metrics_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_main"])
        metrics_frame.pack(fill="x", padx=10, pady=8)

        self._m_acc = MetricCard(metrics_frame, "Accuracy", icon="",
                                 color=COLORS["primary"])
        self._m_acc.pack(side="left", padx=4, pady=4, fill="x", expand=True)

        self._m_prec = MetricCard(metrics_frame, "Precisión", icon="",
                                  color=COLORS["gaussian"])
        self._m_prec.pack(side="left", padx=4, pady=4, fill="x", expand=True)

        self._m_rec = MetricCard(metrics_frame, "Recall", icon="",
                                 color=COLORS["kde"])
        self._m_rec.pack(side="left", padx=4, pady=4, fill="x", expand=True)

        self._m_f1 = MetricCard(metrics_frame, "F1-Score", icon="⚖",
                                color=COLORS["ew"])
        self._m_f1.pack(side="left", padx=4, pady=4, fill="x", expand=True)

        # Log de entrenamiento
        log_card = ctk.CTkFrame(self, fg_color=COLORS["bg_card"],
                                border_width=1, border_color=COLORS["border"])
        log_card.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        SectionHeader(log_card, "Log de Entrenamiento",
                      "Salida detallada del proceso",
                      icon="",
                      fg_color=COLORS["bg_card"]).pack(fill="x", padx=14, pady=(12, 6))


        # Texto del log
        log_outer = ctk.CTkFrame(log_card, fg_color=COLORS["bg_code"])
        log_outer.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        
        # Elegir color según modo actual
        bg_code = COLORS["bg_code"]
        if isinstance(bg_code, (list, tuple)):
            modo = ctk.get_appearance_mode()
            bg_code = bg_code[1] if modo == "Dark" else bg_code[0]
            
        self.log_text = tk.Text(
            log_outer,
            bg=bg_code,
            fg="#a8d8a8",
            insertbackground="#ffffff",
            font=FONTS["mono"],
            relief="flat",
            padx=10,
            pady=8,
            wrap="word",
            cursor="arrow",
            state="disabled"
        )
        
        scrollbar = ctk.CTkScrollbar(
            log_outer,
            orientation="vertical",
            command=self.log_text.yview
        )
        
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.log_text.pack(fill="both", expand=True)
            
        
        # Colores de texto en el log
        self.log_text.tag_configure("ok", foreground="#56d4a0")
        self.log_text.tag_configure("info", foreground="#7ec8e3")
        self.log_text.tag_configure("warn", foreground="#f7c35f")
        self.log_text.tag_configure("error", foreground="#f75454")
        self.log_text.tag_configure("header", foreground="#ffffff",
                                    font=FONTS["mono_bold"])
        self.log_text.tag_configure("dim", foreground="#4a5568")


    def _start_training(self):
        if self.app_state.get("dataset") is None:
            messagebox.showerror("Sin dataset",
                                 "Ve a la pestaña 'Configuración' y carga un dataset primero.")
            return

        if not self.app_state["target_col"].get():
            messagebox.showerror("Sin columna objetivo",
                                 "Selecciona la columna objetivo en 'Configuración'.")
            return

        self._clear_log()
        self._set_status("Entrenando…", "warning")
        self._progress.start()

        thread = threading.Thread(target=self._run_training, daemon=True)
        thread.start()

    def _run_training(self):
        import pandas as pd
        from core.classifier import NaiveBayesClassifier
        from core.evaluation import ModelEvaluator

        try:
            ds = self.app_state["dataset"].copy()
            tgt = self.app_state["target_col"].get()
            meth = self.app_state["cont_method"].get()
            alpha = float(self.app_state["laplace_alpha"].get())
            nbins = int(self.app_state["n_bins"].get())
            bw = self.app_state["kde_bw"].get()
            pct = float(self.app_state["train_pct"].get()) / 100
            seed = int(self.app_state["seed"].get())

            X = ds.drop(columns=[tgt])
            y = ds[tgt]

            np.random.seed(seed)
            idx = np.random.permutation(len(X))
            n_train = int(len(X) * pct)
            tr_idx, ts_idx = idx[:n_train], idx[n_train:]

            X_train = X.iloc[tr_idx].reset_index(drop=True)
            X_test = X.iloc[ts_idx].reset_index(drop=True)
            y_train = y.iloc[tr_idx].reset_index(drop=True)
            y_test = y.iloc[ts_idx].reset_index(drop=True)

            self.app_state["X_train"] = X_train
            self.app_state["X_test"] = X_test
            self.app_state["y_train"] = y_train
            self.app_state["y_test"] = y_test

            method_names = {
                "gaussian": "Distribución Gaussiana",
                "kde": "KDE (Kernel Density Estimation)",
                "equal_width": "Discretización — Anchos Iguales",
                "equal_freq": "Discretización — Frecuencias Iguales",
            }

            self._log("═" * 56, "dim")
            self._log("  CLASIFICADOR NAÏVE BAYES", "header")
            self._log("═" * 56, "dim")

            self._log(f"\n  Dataset: {self.app_state.get('dataset_path', '—')}", "info")
            self._log(f"  Clase objetivo: {tgt}", "info")
            self._log(f"  Método: {method_names.get(meth, meth)}", "info")
            self._log(f"  Laplace α: {alpha}  |  Bins: {nbins}  |  KDE bw: {bw}", "info")
            self._log(f"✂   Split: {int(pct*100)}% / {int((1-pct)*100)}%  |  Semilla: {seed}\n", "info")

            self._log("─" * 40, "dim")
            self._log(f"  Entrenamiento: {len(X_train)} instancias", "ok")
            self._log(f"  Prueba:        {len(X_test)} instancias", "ok")
            classes = sorted(y.unique())
            self._log(f"  Clases ({len(classes)}): {', '.join(map(str, classes))}\n", "ok")

            self._log("─" * 40, "dim")
            self._log("  Tipos de variables identificados:", "info")

            clf = NaiveBayesClassifier(
                continuous_method=meth,
                laplace_alpha=alpha,
                n_bins=nbins,
                kde_bandwidth=bw)
            clf.fit(X_train, y_train)

            for feat, ftype in clf.feature_types_.items():
                icon = "" if ftype == "continuous" else ""
                self._log(f"    {icon}  {feat}: {ftype}", "dim")

            self.app_state["classifier"] = clf

            self._log("\n  Evaluando en conjunto de prueba…", "info")
            y_pred = clf.predict(X_test)
            metrics = ModelEvaluator.evaluate(y_test.values, y_pred, clf.classes_)
            self.app_state["metrics"] = metrics
            self.app_state["y_pred"] = y_pred
            self.app_state["classes"] = clf.classes_

            self._log("\n─" * 40, "dim")
            self._log("  MÉTRICAS DE EVALUACIÓN", "header")
            self._log("─" * 40, "dim")
            self._log(f"  Accuracy:   {metrics['accuracy']:.4f}  ({metrics['accuracy']*100:.2f}%)", "ok")
            self._log(f"  Precisión:  {metrics['precision_macro']:.4f}  (macro)", "ok")
            self._log(f"  Recall:     {metrics['recall_macro']:.4f}  (macro)", "ok")
            self._log(f"  F1-Score:   {metrics['f1_macro']:.4f}  (macro)\n", "ok")

            self._log("─" * 40, "dim")
            self._log("  POR CLASE:", "info")
            fmt = f"  {{:<20}} {{:>8}} {{:>8}} {{:>8}}"
            self._log(fmt.format("Clase", "Prec.", "Recall", "F1"), "dim")
            for cls in clf.classes_:
                p = metrics['precision'][cls]
                r = metrics['recall'][cls]
                f = metrics['f1_score'][cls]
                self._log(fmt.format(str(cls)[:20], f"{p:.3f}", f"{r:.3f}", f"{f:.3f}"), "ok")

            self._log("\n  Entrenamiento completado correctamente.", "ok")
            self._log("═" * 56 + "\n", "dim")

            self.after(0, self._update_metric_cards, metrics)
            self.after(0, self._set_status, "✓ Modelo entrenado", "success")
            self.after(0, self._progress.stop)

        except Exception as exc:
            import traceback
            self._log(f"\n  ERROR: {exc}", "error")
            self._log(traceback.format_exc(), "error")
            self.after(0, self._set_status, "Error", "error")
            self.after(0, self._progress.stop)


    def _log(self, msg: str, tag: str = ""):
        def _do():
            self.log_text.config(state="normal")
            if tag:
                self.log_text.insert("end", msg + "\n", tag)
            else:
                self.log_text.insert("end", msg + "\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
        self.after(0, _do)

    def _clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def _set_status(self, text: str, style: str):
        self._status_badge.configure(text=text,
                                     fg_color=Badge.STYLES[style][0],
                                     text_color=Badge.STYLES[style][1])

    def _update_metric_cards(self, metrics: dict):
        self._m_acc.set_value(f"{metrics['accuracy']*100:.1f}%")
        self._m_prec.set_value(f"{metrics['precision_macro']*100:.1f}%")
        self._m_rec.set_value(f"{metrics['recall_macro']*100:.1f}%")
        self._m_f1.set_value(f"{metrics['f1_macro']*100:.1f}%")
