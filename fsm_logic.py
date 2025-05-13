import graphviz

class FiniteStateMachine:
    def __init__(self, states, alphabet, transitions, initial_state, outputs):
        """
        Inicializa la máquina de estados finitos.
        
        Parámetros:
        - states: lista de estados (por ejemplo, ["q0", "q1", ...])
        - alphabet: lista de símbolos de entrada (por ejemplo, ["0", "1"])
        - transitions: diccionario con claves (estado, símbolo) y valor: estado siguiente.
        - outputs: diccionario con claves (estado, símbolo) y valor: símbolo de salida.
        - initial_state: estado inicial (cadena que aparece en states).
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.outputs = outputs
        self.current_state = initial_state

    def process_input(self, input_sequence):
        """
        Procesa una secuencia de entrada (lista de símbolos) y retorna una tupla:
        (lista de estados recorridos, lista de salidas generadas)
        """
        state_history = [self.initial_state]
        output_sequence = []
        for inp in input_sequence:
            key = (self.current_state, inp)
            if key in self.transitions:
                next_state = self.transitions[key]
                output = self.outputs[key]
                state_history.append(next_state)
                output_sequence.append(output)
                self.current_state = next_state
            else:
                raise ValueError(f"Entrada '{inp}' no válida desde el estado '{self.current_state}'")
        return state_history, output_sequence

    def draw_graph(self):
        """
        Dibuja el diagrama de la máquina de estados finitos utilizando Graphviz.
        Se utiliza un grafo dirigido (digraph) para reflejar la direccionalidad de
        las transiciones (de un estado "origen" hacia un estado "destino").
        """
        # Creamos un objeto Digraph de Graphviz.
        dot = graphviz.Digraph(comment='Máquina de Estados Finita')
        dot.attr(rankdir='LR')  # Disposición de izquierda a derecha

        # Agregamos los nodos; diferenciamos el estado inicial usando un color especial.
        for state in self.states:
            if state == self.initial_state:
                dot.node(state, state, color='red', style='filled', fillcolor='#FF5733')
            else:
                dot.node(state, state, color='blue', style='filled', fillcolor='#A0CBE2')

        # Agregamos las aristas dirigidas con sus correspondientes etiquetas.
        for (state, inp), next_state in self.transitions.items():
            label = f"{inp}/{self.outputs[(state, inp)]}"
            dot.edge(state, next_state, label=label)

        # Renderizamos y visualizamos el diagrama.
        # Esto generará un archivo 'fsm_diagram.png' y, dependiendo de tu sistema,
        # se abrirá en el visor de imágenes.
        dot.render('fsm_diagram', view=True, format='png')
