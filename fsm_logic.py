import graphviz

class FiniteStateMachine:
    def __init__(self, states, alphabet, transitions, initial_state, outputs):
        """
        Inicializa la máquina de estados finitos.
        Parámetros:
          - states: lista de estados.
          - alphabet: lista de símbolos de entrada.
          - transitions: diccionario con claves (estado, símbolo) y valor: estado siguiente.
          - outputs: diccionario con claves (estado, símbolo) y valor: símbolo de salida.
          - initial_state: estado inicial.
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
        (lista de estados recorridos, lista de salidas generadas).
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
        Se ajustan las dimensiones y resolución para obtener una imagen de alta calidad.
        """
        dot = graphviz.Digraph(comment='Máquina de Estados Finita')
        dot.attr(rankdir='LR')  # Disposición de izquierda a derecha

        # Ajusta las dimensiones (16x9 pulgadas forzadas) y la resolución (DPI)
        dot.attr(size="16,9!", dpi="150")
        
        for state in self.states:
            if state == self.initial_state:
                dot.node(state, state, color='red', style='filled', fillcolor='#FF5733')
            else:
                dot.node(state, state, color='blue', style='filled', fillcolor='#A0CBE2')

        for (state, inp), next_state in self.transitions.items():
            label = f"{inp}/{self.outputs[(state, inp)]}"
            dot.edge(state, next_state, label=label)

        dot.render('fsm_diagram', view=True, format='png')
