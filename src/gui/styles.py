import tkinter as tk
from tkinter import ttk

COLORS = {
    "bg_main":        "#f0f4f8",
    "bg_card":        "#ffffff",
    "bg_dark":        "#1e3a5f",
    "bg_sidebar":     "#162c47",
    "bg_header":      "#0f2035",
    "bg_input":       "#f8fafc",
    "bg_code":        "#1e293b",
    "primary":        "#2563eb",
    "primary_dark":   "#1d4ed8",
    "primary_light":  "#dbeafe",
    "success":        "#059669",
    "success_light":  "#d1fae5",
    "warning":        "#d97706",
    "warning_light":  "#fef3c7",
    "error":          "#dc2626",
    "error_light":    "#fee2e2",
    "info":           "#0891b2",
    "info_light":     "#cffafe",
    "text":           "#1e293b",
    "text_secondary": "#64748b",
    "text_light":     "#94a3b8",
    "text_white":     "#f8fafc",
    "text_header":    "#e2e8f0",
    "border":         "#e2e8f0",
    "border_focus":   "#2563eb",
    "gaussian":       "#4f46e5",
    "gaussian_light": "#ede9fe",
    "kde":            "#0891b2",
    "kde_light":      "#cffafe",
    "ew":             "#059669",
    "ew_light":       "#d1fae5",
    "ef":             "#d97706",
    "ef_light":       "#fef3c7",
    "sep":            "#e2e8f0",
}

FONTS = {
    "title":       ("Segoe UI", 16, "bold"),
    "subtitle":    ("Segoe UI", 12, "bold"),
    "heading":     ("Segoe UI", 11, "bold"),
    "body":        ("Segoe UI", 10),
    "body_bold":   ("Segoe UI", 10, "bold"),
    "small":       ("Segoe UI", 9),
    "small_bold":  ("Segoe UI", 9, "bold"),
    "mono":        ("Courier New", 9),
    "mono_bold":   ("Courier New", 10, "bold"),
    "button":      ("Segoe UI", 10, "bold"),
}

PAD = {"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24}


def apply_theme(root: tk.Tk):
    style = ttk.Style(root)

    # Elegir tema base disponible
    available = style.theme_names()
    for preferred in ("clam", "alt", "default"):
        if preferred in available:
            style.theme_use(preferred)
            break

    style.configure("TFrame",       background=COLORS["bg_main"])
    style.configure("Card.TFrame",  background=COLORS["bg_card"])
    style.configure("Dark.TFrame",  background=COLORS["bg_dark"])

    style.configure("TLabel",
                    background=COLORS["bg_main"],
                    foreground=COLORS["text"],
                    font=FONTS["body"])

    style.configure("TLabelframe",
                    background=COLORS["bg_card"],
                    bordercolor=COLORS["border"],
                    relief="groove")
    style.configure("TLabelframe.Label",
                    background=COLORS["bg_card"],
                    foreground=COLORS["primary"],
                    font=FONTS["body_bold"])

    style.configure("TNotebook",
                    background=COLORS["bg_main"],
                    borderwidth=0)
    style.configure("TNotebook.Tab",
                    background="#d1d9e6",
                    foreground=COLORS["text_secondary"],
                    font=FONTS["body_bold"],
                    padding=[12, 7])
    style.map("TNotebook.Tab",
              background=[("selected", COLORS["bg_card"]),
                          ("active",   COLORS["primary_light"])],
              foreground=[("selected", COLORS["primary"]),
                          ("active",   COLORS["primary"])])

    style.configure("Primary.TButton",
                    background=COLORS["primary"],
                    foreground="#ffffff",
                    font=FONTS["button"],
                    relief="flat",
                    padding=(14, 7))
    style.map("Primary.TButton",
              background=[("active", COLORS["primary_dark"]),
                          ("pressed", COLORS["primary_dark"])],
              foreground=[("active", "#ffffff")])

    style.configure("Success.TButton",
                    background=COLORS["success"],
                    foreground="#ffffff",
                    font=FONTS["button"],
                    relief="flat",
                    padding=(14, 7))
    style.map("Success.TButton",
              background=[("active", "#047857"), ("pressed", "#047857")],
              foreground=[("active", "#ffffff")])

    style.configure("Secondary.TButton",
                    background="#e2e8f0",
                    foreground=COLORS["primary"],
                    font=FONTS["button"],
                    relief="flat",
                    padding=(12, 6))
    style.map("Secondary.TButton",
              background=[("active", COLORS["primary_light"])])

    style.configure("TEntry",
                    fieldbackground=COLORS["bg_input"],
                    foreground=COLORS["text"],
                    relief="solid",
                    borderwidth=1)

    style.configure("TCombobox",
                    fieldbackground=COLORS["bg_input"],
                    foreground=COLORS["text"],
                    relief="solid")

    style.configure("TScale",
                    background=COLORS["bg_card"],
                    troughcolor="#d1d9e6",
                    sliderlength=18)

    style.configure("TRadiobutton",
                    background=COLORS["bg_card"],
                    foreground=COLORS["text"],
                    font=FONTS["body"])
    style.map("TRadiobutton",
              background=[("active", COLORS["bg_card"])])

    style.configure("TSeparator", background=COLORS["sep"])

    style.configure("TScrollbar",
                    background=COLORS["border"],
                    troughcolor=COLORS["bg_main"],
                    relief="flat",
                    borderwidth=0)

    style.configure("TProgressbar",
                    troughcolor=COLORS["border"],
                    background=COLORS["primary"],
                    borderwidth=0,
                    thickness=6)

    style.configure("Treeview",
                    background=COLORS["bg_card"],
                    fieldbackground=COLORS["bg_card"],
                    foreground=COLORS["text"],
                    rowheight=26,
                    font=FONTS["small"])
    style.configure("Treeview.Heading",
                    background=COLORS["primary_light"],
                    foreground=COLORS["primary"],
                    font=FONTS["small_bold"],
                    relief="flat")
    style.map("Treeview",
              background=[("selected", COLORS["primary_light"])],
              foreground=[("selected", COLORS["primary"])])
