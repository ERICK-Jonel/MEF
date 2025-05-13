# config.py
# Configuración global y estilos para la aplicación MEF

# Colores y estilos para la interfaz general
BACKGROUND_COLOR = "#3C3F41"        # Fondo principal de la ventana
DEFAULT_FONT = ("Arial", 12)

# Estilos para el editor de código
CODE_EDITOR_BG = "#272822"           # Fondo del editor de código
CODE_EDITOR_FG = "#F8F8F2"           # Color de texto del editor
LINE_NUMBER_BG = "#2B2B2B"           # Fondo de la numeración
LINE_NUMBER_FG = "#75715E"           # Color de la numeración
KEYWORD_COLOR = "#66d9ef"            # Color para palabras clave

# Configuración para la representación gráfica de la máquina (Graphviz)
# Estos parámetros se usarán en el método draw_graph() de fsm_logic.py
NODE_INITIAL_COLOR = "#FF5733"       # Color para el estado inicial
NODE_OTHER_COLOR = "#A0CBE2"         # Color para los demás nodos
EDGE_COLOR = "#BBBBBB"               # Color de las aristas del digraph
GRAPH_TITLE_COLOR = "black"          # Color del título del gráfico (si se usa en el layout)

# Parámetros para Graphviz
GRAPHVIZ_FORMAT = "png"              # Formato de la imagen resultante (png, pdf, etc.)
GRAPHVIZ_OUTPUT_FILENAME = "fsm_diagram"  # Nombre base del archivo generado
