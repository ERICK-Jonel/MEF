# config.py
# Configuración global y estilos para la aplicación MEF

# Colores y fuentes generales
BACKGROUND_COLOR = "#3C3F41"    # Fondo principal de la ventana
DEFAULT_FONT = ("Arial", 12)
CODE_EDITOR_FONT = ("Courier", 12)  # Fuente para el editor de código

# Estilos para el editor de código
CODE_EDITOR_BG = "#272822"      # Fondo del editor de código
CODE_EDITOR_FG = "#F8F8F2"      # Color del texto del editor

# Estilos para la numeración de líneas
LINE_NUMBER_BG = "#2B2B2B"      # Fondo de la numeración
LINE_NUMBER_FG = "#75715E"      # Color de la numeración

# Color para resaltar palabras clave
KEYWORD_COLOR = "#66d9ef"

# Configuración de layout para el editor de código
# Este diccionario se pasará a pack() para el widget del editor.
CODE_EDITOR_PACK_OPTIONS = {
    "side": "right",
    "fill": "both",
    "expand": True
}

# Configuración de layout para el scrollbar
SCROLLBAR_PACK_OPTIONS = {
    "side": "right",
    "fill": "y"
}

# Opciones para botones (ejemplos)
BUTTON_RUN_BG = "#4CAF50"
BUTTON_RUN_HOVER_BG = "#66BB6A"
BUTTON_GRAPH_BG = "#2196F3"
BUTTON_GRAPH_HOVER_BG = "#42A5F5"
BUTTON_RESET_BG = "#f44336"
BUTTON_RESET_HOVER_BG = "#EF5350"
BUTTON_COPY_BG = "#009688"
BUTTON_COPY_HOVER_BG = "#26A69A"

# Configuración para Graphviz (para la representación del diagrama de la máquina)
NODE_INITIAL_COLOR = "#FF5733"
NODE_OTHER_COLOR = "#A0CBE2"
EDGE_COLOR = "#BBBBBB"
GRAPH_TITLE_COLOR = "black"
GRAPHVIZ_FORMAT = "png"
GRAPHVIZ_OUTPUT_FILENAME = "fsm_diagram"

# Función para aplicar bindings comunes al widget de texto del editor.
def apply_text_editor_bindings(widget, instance):
    """
    Aplica bindings comunes al widget de texto del editor.
    Se espera que 'instance' disponga de los siguientes métodos:
      - _on_change
      - select_all
      - undo (o edit_undo)
      - redo (o edit_redo)
      - custom_paste
    """
    widget.bind("<<Change>>", instance._on_change)
    widget.bind("<Configure>", instance._on_change)
    widget.bind("<KeyRelease>", instance._on_change)
    widget.bind("<Control-a>", instance.select_all)
    widget.bind("<Control-A>", instance.select_all)
    widget.bind("<Control-z>", lambda event: instance.undo() or "break")
    widget.bind("<Control-Z>", lambda event: instance.undo() or "break")
    widget.bind("<Control-y>", lambda event: instance.redo() or "break")
    widget.bind("<Control-Y>", lambda event: instance.redo() or "break")
    widget.bind("<Control-v>", instance.custom_paste)
    widget.bind("<Control-V>", instance.custom_paste)
