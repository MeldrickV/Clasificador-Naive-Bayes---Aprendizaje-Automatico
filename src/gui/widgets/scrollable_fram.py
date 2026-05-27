import customtkinter as ctk

class ScrollableFrame(ctk.CTkScrollableFrame):
    """
    CTkScrollableFrame con soporte nativo para scroll con rueda del mouse
    sobre cualquier parte del contenido.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._enable_mousewheel_scroll()

    def _enable_mousewheel_scroll(self):
        """Vincula la rueda del mouse al canvas interno."""
        canvas = self._parent_canvas

        def on_mousewheel(event):
            # Detecta dirección del scroll según SO
            if event.num == 4:      # Linux arriba
                delta = -1
            elif event.num == 5:    # Linux abajo
                delta = 1
            else:                   # Windows / macOS
                delta = -1 * (event.delta // abs(event.delta)) if event.delta != 0 else 0
            canvas.yview_scroll(delta, "units")
            return "break"  # Evita que el evento se propague

        # Vincular eventos al canvas
        canvas.bind("<MouseWheel>", on_mousewheel, add=True)
        canvas.bind("<Button-4>", on_mousewheel, add=True)
        canvas.bind("<Button-5>", on_mousewheel, add=True)

        # También forzar que el canvas capture el foco
        canvas.focus_set()

        # Propagar eventos a todos los widgets hijos (para que funcione incluso sobre gráficos)
        def bind_recursive(widget):
            widget.bind("<MouseWheel>", on_mousewheel, add=True)
            widget.bind("<Button-4>", on_mousewheel, add=True)
            widget.bind("<Button-5>", on_mousewheel, add=True)
            for child in widget.winfo_children():
                bind_recursive(child)

        bind_recursive(self)
