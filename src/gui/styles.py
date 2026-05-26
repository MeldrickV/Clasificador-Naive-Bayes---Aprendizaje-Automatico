import customtkinter as ctk

# Colores
COLORS = {
    # ── Fondos ─────────────────────────────
    "bg_main":        ("#f0f4f8", "#0f172a"),
    "bg_card":        ("#ffffff", "#1e293b"),
    "bg_dark":        ("#1e3a5f", "#162033"),
    "bg_sidebar":     ("#162c47", "#0b1628"),
    "bg_header":      ("#0f2035", "#08111f"),
    "bg_input":       ("#f8fafc", "#243447"),
    "bg_code":        ("#1e293b", "#020617"),

    # ── Primarios ──────────────────────────
    "primary":        ("#2563eb", "#3b82f6"),
    "primary_dark":   ("#1d4ed8", "#2563eb"),
    "primary_light":  ("#dbeafe", "#1e3a8a"),

    # ── Estados ────────────────────────────
    "success":        ("#059669", "#10b981"),
    "success_light":  ("#d1fae5", "#064e3b"),

    "warning":        ("#d97706", "#f59e0b"),
    "warning_light":  ("#fef3c7", "#78350f"),

    "error":          ("#dc2626", "#ef4444"),
    "error_light":    ("#fee2e2", "#7f1d1d"),

    "info":           ("#0891b2", "#06b6d4"),
    "info_light":     ("#cffafe", "#164e63"),

    # ── Texto ──────────────────────────────
    "text":           ("#1e293b", "#f8fafc"),
    "text_secondary": ("#64748b", "#94a3b8"),
    "text_light":     ("#94a3b8", "#64748b"),
    "text_white":     ("#f8fafc", "#f8fafc"),
    "text_header":    ("#e2e8f0", "#e2e8f0"),

    # ── Bordes ─────────────────────────────
    "border":         ("#e2e8f0", "#334155"),
    "border_focus":   ("#2563eb", "#3b82f6"),
    "sep":            ("#e2e8f0", "#334155"),

    # ── Métodos ────────────────────────────
    "gaussian":       ("#4f46e5", "#818cf8"),
    "gaussian_light": ("#ede9fe", "#312e81"),

    "kde":            ("#0891b2", "#22d3ee"),
    "kde_light":      ("#cffafe", "#164e63"),

    "ew":             ("#059669", "#34d399"),
    "ew_light":       ("#d1fae5", "#064e3b"),

    "ef":             ("#d97706", "#fbbf24"),
    "ef_light":       ("#fef3c7", "#78350f"),
}

# Fuentes
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


def apply_theme(root):

    ctk.set_default_color_theme("dark_blue")
