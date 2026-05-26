"""
Widgets reutilizables — versión compatible Linux/Windows/Mac
Sin PanedWindow ni bind_all que causan segfaults.
"""

import tkinter as tk
from tkinter import ttk
from gui.styles import COLORS, FONTS


# ── Tooltip ──────────────────────────────────────────────────
class Tooltip:
    def __init__(self, widget, text: str, delay: int = 700):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._id = None
        self._tw = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._hide)
        widget.bind("<ButtonPress>", self._hide)

    def _schedule(self, event=None):
        self._cancel()
        self._id = self.widget.after(self.delay, self._show)

    def _cancel(self):
        if self._id:
            self.widget.after_cancel(self._id)
            self._id = None

    def _show(self):
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
            self._tw = tk.Toplevel(self.widget)
            self._tw.wm_overrideredirect(True)
            self._tw.wm_geometry(f"+{x}+{y}")
            self._tw.configure(bg="#1e293b")
            tk.Label(self._tw, text=self.text,
                     bg="#1e293b", fg="#f8fafc",
                     font=FONTS["small"],
                     wraplength=280, padx=10, pady=6,
                     justify="left").pack()
        except Exception:
            pass

    def _hide(self, event=None):
        self._cancel()
        if self._tw:
            try:
                self._tw.destroy()
            except Exception:
                pass
            self._tw = None


# ── InfoBox ───────────────────────────────────────────────────
class InfoBox(tk.Frame):
    ICONS = {
        "info":    ("ℹ", COLORS["info"],    COLORS["info_light"]),
        "success": ("✓", COLORS["success"], COLORS["success_light"]),
        "warning": ("⚠", COLORS["warning"], COLORS["warning_light"]),
        "error":   ("✕", COLORS["error"],   COLORS["error_light"]),
        "tip":     ("💡", COLORS["gaussian"], COLORS["gaussian_light"]),
    }

    def __init__(self, parent, text: str, type_: str = "info",
                 title: str = None, **kw):
        icon_char, fg, bg = self.ICONS.get(type_, self.ICONS["info"])
        super().__init__(parent, bg=bg, **kw)

        tk.Label(self, text=icon_char, bg=bg, fg=fg,
                 font=("Segoe UI", 12, "bold")).grid(
                     row=0, column=0, padx=(10, 6), pady=8, sticky="n")

        if title:
            tk.Label(self, text=title, bg=bg, fg=fg,
                     font=FONTS["body_bold"]).grid(
                         row=0, column=1, sticky="w", padx=(0, 10), pady=(8, 2))
            tk.Label(self, text=text, bg=bg, fg=COLORS["text"],
                     font=FONTS["small"], wraplength=460,
                     justify="left", anchor="w").grid(
                         row=1, column=1, sticky="ew",
                         padx=(0, 10), pady=(0, 8))
        else:
            tk.Label(self, text=text, bg=bg, fg=COLORS["text"],
                     font=FONTS["small"], wraplength=480,
                     justify="left", anchor="w").grid(
                         row=0, column=1, sticky="ew",
                         padx=(0, 10), pady=8)
        self.columnconfigure(1, weight=1)


# ── Badge ─────────────────────────────────────────────────────
class Badge(tk.Label):
    STYLES = {
        "primary": (COLORS["primary_light"],  COLORS["primary"]),
        "success": (COLORS["success_light"],  COLORS["success"]),
        "warning": (COLORS["warning_light"],  COLORS["warning"]),
        "error":   (COLORS["error_light"],    COLORS["error"]),
        "info":    (COLORS["info_light"],     COLORS["info"]),
        "gray":    (COLORS["border"],         COLORS["text_secondary"]),
    }

    def __init__(self, parent, text: str, style: str = "primary", **kw):
        bg, fg = self.STYLES.get(style, self.STYLES["gray"])
        super().__init__(parent, text=text, bg=bg, fg=fg,
                         font=FONTS["small_bold"], padx=8, pady=2, **kw)


# ── SectionHeader ─────────────────────────────────────────────
class SectionHeader(tk.Frame):
    def __init__(self, parent, title: str, subtitle: str = None,
                 icon: str = "", bg: str = None, **kw):
        bg = bg or COLORS["bg_main"]
        super().__init__(parent, bg=bg, **kw)

        title_text = f"{icon}  {title}" if icon else title
        tk.Label(self, text=title_text, bg=bg, fg=COLORS["text"],
                 font=FONTS["heading"]).grid(row=0, column=0, sticky="w")

        if subtitle:
            tk.Label(self, text=subtitle, bg=bg,
                     fg=COLORS["text_secondary"],
                     font=FONTS["small"]).grid(row=1, column=0,
                                               sticky="w", pady=(0, 2))

        tk.Frame(self, bg=COLORS["border"], height=1).grid(
            row=2, column=0, sticky="ew", pady=(3, 0))
        self.columnconfigure(0, weight=1)


# ── MethodCard ────────────────────────────────────────────────
class MethodCard(tk.Frame):
    def __init__(self, parent, variable: tk.StringVar, value: str,
                 title: str, short_desc: str, color: str, color_light: str,
                 icon: str = "●", command=None, **kw):
        super().__init__(parent, bg=COLORS["bg_card"],
                         relief="solid", bd=1, **kw)

        self.variable = variable
        self.value = value
        self.color = color
        self.color_light = color_light
        self._command = command

        top = tk.Frame(self, bg=COLORS["bg_card"])
        top.pack(fill="x", padx=10, pady=(8, 3))

        icon_lbl = tk.Label(top, text=icon, bg=color_light, fg=color,
                            font=("Segoe UI", 13), padx=5, pady=1)
        icon_lbl.pack(side="left", padx=(0, 8))

        title_lbl = tk.Label(top, text=title, bg=COLORS["bg_card"],
                             fg=COLORS["text"], font=FONTS["body_bold"])
        title_lbl.pack(side="left", fill="x", expand=True)

        self._radio = ttk.Radiobutton(top, variable=variable,
                                      value=value, command=self._on_select)
        self._radio.pack(side="right")

        desc_lbl = tk.Label(self, text=short_desc, bg=COLORS["bg_card"],
                            fg=COLORS["text_secondary"], font=FONTS["small"],
                            wraplength=200, justify="left", anchor="w")
        desc_lbl.pack(fill="x", padx=12, pady=(0, 8))

        for w in [self, top, icon_lbl, title_lbl, desc_lbl]:
            w.bind("<Button-1>", self._on_click)
            w.config(cursor="hand2")

        variable.trace_add("write", self._sync)
        self._sync()

    def _on_click(self, event=None):
        self.variable.set(self.value)
        self._on_select()

    def _on_select(self):
        self._sync()
        if self._command:
            self._command(self.value)

    def _sync(self, *_):
        selected = self.variable.get() == self.value
        bg = self.color_light if selected else COLORS["bg_card"]
        try:
            self.config(bg=bg,
                        highlightbackground=self.color if selected else COLORS["border"])
            for child in self.winfo_children():
                try:
                    child.config(bg=bg)
                    for subchild in child.winfo_children():
                        try:
                            subchild.config(bg=bg)
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass


# ── MetricCard ────────────────────────────────────────────────
class MetricCard(tk.Frame):
    def __init__(self, parent, label: str, value: str = "—",
                 color: str = None, icon: str = "", **kw):
        color = color or COLORS["primary"]
        super().__init__(parent, bg=COLORS["bg_card"],
                         relief="solid", bd=1, **kw)

        bar = tk.Frame(self, bg=color, height=4)
        bar.pack(fill="x")

        inner = tk.Frame(self, bg=COLORS["bg_card"])
        inner.pack(fill="both", expand=True, padx=10, pady=6)

        lbl_text = f"{icon} {label}".strip()
        tk.Label(inner, text=lbl_text, bg=COLORS["bg_card"],
                 fg=COLORS["text_secondary"],
                 font=FONTS["small"]).pack(anchor="w")

        self._val = tk.Label(
    inner,
    text=value,
    bg=COLORS["bg_card"],
    fg=color
)
        self._val.pack(anchor="w")

    def set_value(self, value: str):
        self._val.config(text=value)


# ── ScrollableFrame (sin bind_all) ────────────────────────────
class ScrollableFrame(tk.Frame):
    """Frame con scroll vertical. Sin bind_all para evitar segfaults."""

    def __init__(self, parent, bg: str = None, **kw):
        bg = bg or COLORS["bg_main"]
        super().__init__(parent, bg=bg, **kw)

        self._canvas = tk.Canvas(self, bg=bg, highlightthickness=0,
                                 borderwidth=0)
        vsb = ttk.Scrollbar(self, orient="vertical",
                             command=self._canvas.yview)
        self.inner = tk.Frame(self._canvas, bg=bg)

        self.inner.bind("<Configure>", self._on_configure)
        self._canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self._canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        # Scroll con rueda — bind solo en canvas (no bind_all)
        self._canvas.bind("<MouseWheel>",     self._on_mousewheel)
        self._canvas.bind("<Button-4>",       self._scroll_up)
        self._canvas.bind("<Button-5>",       self._scroll_down)
        self.inner.bind("<MouseWheel>",       self._on_mousewheel)
        self.inner.bind("<Button-4>",         self._scroll_up)
        self.inner.bind("<Button-5>",         self._scroll_down)

    def _on_configure(self, event=None):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _scroll_up(self, event):
        self._canvas.yview_scroll(-1, "units")

    def _scroll_down(self, event):
        self._canvas.yview_scroll(1, "units")
