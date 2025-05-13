# config.py
# Configuración global y estilos para la aplicación

# Colores
BACKGROUND_COLOR = "#3C3F41"        # Fondo principal de la ventana
CODE_EDITOR_BG = "#272822"           # Fondo del editor de código
CODE_EDITOR_FG = "#F8F8F2"           # Color de texto del editor
LINE_NUMBER_BG = "#2B2B2B"           # Fondo de la numeración
LINE_NUMBER_FG = "#75715E"           # Color de la numeración
KEYWORD_COLOR = "#66d9ef"            # Color para palabras clave en el editor

# Colores para el grafo
NODE_INITIAL_COLOR = "#FF5733"       # Color para el estado inicial
NODE_OTHER_COLOR = "#A0CBE2"         # Color para los demás nodos
EDGE_COLOR = "#BBBBBB"               # Color de las aristas
LABEL_COLOR = "white"                # Color de las etiquetas en nodos
GRAPH_TITLE_COLOR = "black"          # Color del título del gráfico

# Fuentes
DEFAULT_FONT = ("Arial", 12)
MONO_FONT = ("Courier", 12)

# Configuración para el layout del grafo (usado en el método draw_graph)
GRAPH_SIZES = {
    "small": (10, 8),
    "medium": (12, 10),
    "large": (16, 12)
}
SPRING_LAYOUT_PARAMS = {
    "small": {"k": 1.5, "iterations": 100},
    "medium": {"k": 2.0, "iterations": 100},
    "large": {"k": 2.5, "iterations": 100}
}
