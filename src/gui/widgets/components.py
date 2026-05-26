import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from gui.styles import COLORS, FONTS


# Tooltip
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
            self._tw.configure(fg_color="#1e293b")
            tk.Label(self._tw, text=self.text,
                     fg_color="#1e293b", text_color="#f8fafc",
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


# InfoBox
class InfoBox(ctk.CTkFrame):
    ICONS = {
        "info":    ("ℹ", COLORS["info"],    COLORS["info_light"]),
        "success": ("✓", COLORS["success"], COLORS["success_light"]),
        "warning": ("⚠", COLORS["warning"], COLORS["warning_light"]),
        "error":   ("✕", COLORS["error"],   COLORS["error_light"]),
        "tip":     ("", COLORS["gaussian"], COLORS["gaussian_light"]),
    }

    def __init__(self, parent, text: str, type_: str = "info",
                 title: str = None, **kw):
        icon_char, fg, bg = self.ICONS.get(type_, self.ICONS["info"])
        super().__init__(parent, fg_color=bg, **kw)

        # Icono
        ctk.CTkLabel(self, text=icon_char, text_color=fg,
                     font=("Segoe UI", 12, "bold")).grid(
                         row=0, column=0, padx=(10, 6), pady=8, sticky="n")

        if title:
            ctk.CTkLabel(self, text=title, text_color=fg,
                         font=FONTS["body_bold"]).grid(
                             row=0, column=1, sticky="w", padx=(0, 10), pady=(8, 2))
            ctk.CTkLabel(self, text=text, text_color=COLORS["text"],
                         font=FONTS["small"], wraplength=460,
                         justify="left").grid(
                             row=1, column=1, sticky="ew",
                             padx=(0, 10), pady=(0, 8))
        else:
            ctk.CTkLabel(self, text=text, text_color=COLORS["text"],
                         font=FONTS["small"], wraplength=480,
                         justify="left").grid(
                             row=0, column=1, sticky="ew",
                             padx=(0, 10), pady=8)
        self.grid_columnconfigure(1, weight=1)


# Badge
class Badge(ctk.CTkLabel):
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
        super().__init__(parent, text=text, fg_color=bg, text_color=fg,
                         font=FONTS["small_bold"], corner_radius=10,
                         padx=8, pady=2, **kw)


# SectionHeader
class SectionHeader(ctk.CTkFrame):
    def __init__(self, parent, title: str, subtitle: str = None,
                 icon: str = "", bg: str = None, **kw):

        if "fg_color" not in kw:
            kw["fg_color"] = bg or COLORS["bg_main"]

        super().__init__(parent, **kw)

        title_text = f"{icon}  {title}" if icon else title

        ctk.CTkLabel(
            self,
            text=title_text,
            text_color=COLORS["text"],
            font=FONTS["heading"]
        ).grid(row=0, column=0, sticky="w")

        if subtitle:
            ctk.CTkLabel(
                self,
                text=subtitle,
                text_color=COLORS["text_secondary"],
                font=FONTS["small"]
            ).grid(row=1, column=0, sticky="w", pady=(0, 2))

        ctk.CTkFrame(
            self,
            height=1,
            fg_color=COLORS["border"]
        ).grid(row=2, column=0, sticky="ew", pady=(3, 0))

        self.grid_columnconfigure(0, weight=1)

# MethodCard
class MethodCard(ctk.CTkFrame):
    def __init__(self, parent, variable: tk.StringVar, value: str,
                 title: str, short_desc: str, color: str, color_light: str,
                 icon: str = "●", command=None, **kw):
        super().__init__(parent, fg_color=COLORS["bg_card"],
                         border_width=1, border_color=COLORS["border"], **kw)

        self.variable = variable
        self.value = value
        self.color = color
        self.color_light = color_light
        self._command = command

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(8, 3))

        icon_lbl = ctk.CTkLabel(top, text=icon, text_color=color,
                                font=("Segoe UI", 13), width=30)
        icon_lbl.pack(side="left", padx=(0, 8))

        title_lbl = ctk.CTkLabel(top, text=title, text_color=COLORS["text"],
                                 font=FONTS["body_bold"])
        title_lbl.pack(side="left", fill="x", expand=True)

        self._radio = ctk.CTkRadioButton(top, variable=variable,
                                         value=value, command=self._on_select,
                                         text="", fg_color=color)
        self._radio.pack(side="right")

        desc_lbl = ctk.CTkLabel(self, text=short_desc, text_color=COLORS["text_secondary"],
                                font=FONTS["small"], wraplength=200, justify="left")
        desc_lbl.pack(fill="x", padx=12, pady=(0, 8))

        for w in [self, top, icon_lbl, title_lbl, desc_lbl]:
            w.bind("<Button-1>", self._on_click)
            w.configure(cursor="hand2")

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
        border_color = self.color if selected else COLORS["border"]
        self.configure(fg_color=bg, border_color=border_color)
        # El radiobutton ya se actualiza solo por variable


# MetricCard
class MetricCard(ctk.CTkFrame):
    def __init__(self, parent, label: str, value: str = "—",
                 color: str = None, icon: str = "", **kw):
        color = color or COLORS["primary"]
        super().__init__(parent, fg_color=COLORS["bg_card"],
                         border_width=1, border_color=COLORS["border"], **kw)

        # Barra superior de color
        bar = ctk.CTkFrame(self, fg_color=color, height=4)
        bar.pack(fill="x")

        inner = ctk.CTkFrame(self, fg_color=COLORS["bg_card"])
        inner.pack(fill="both", expand=True, padx=10, pady=6)

        lbl_text = f"{icon} {label}".strip()
        ctk.CTkLabel(inner, text=lbl_text, text_color=COLORS["text_secondary"],
                     font=FONTS["small"]).pack(anchor="w")

        self._val = ctk.CTkLabel(inner, text=value, text_color=color,
                                 font=FONTS["body_bold"])
        self._val.pack(anchor="w")

    def set_value(self, value: str):
        self._val.configure(text=value)


# ScrollableFrame
class ScrollableFrame(ctk.CTkScrollableFrame):
    """Frame con scroll vertical usando CustomTkinter."""
    def __init__(self, parent, bg: str = None, **kw):
        bg = bg or COLORS["bg_main"]
        super().__init__(parent, fg_color=bg, **kw)
        self.inner = self  # Para compatibilidad con código antiguo
