import networkx as nx
import matplotlib.pyplot as plt

class FiniteStateMachine:
    def __init__(self, states, alphabet, transitions, initial_state, outputs):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.outputs = outputs
        self.current_state = initial_state

    def process_input(self, input_sequence):
        """
        Procesa la secuencia de entrada (lista de '0' y '1') y devuelve una tupla:
        (lista de estados visitados, lista de salidas generadas)
        
        En este ejemplo (multiplicación por 2 usando LSB-first), si al
        finalizar la entrada el estado es "q1" (carry=1), se agrega un dígito extra "1".
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
                # Para mantener el mismo funcionamiento (en el simulador original se
                # mostraba una ventana emergente), aquí lanzamos una excepción.
                raise ValueError(f"Entrada '{inp}' no válida desde el estado '{self.current_state}'")
        # Post-procesamiento: si al finalizar la entrada el estado es "q1" (carry=1),
        # se agregará un dígito extra "1" – este comportamiento es útil, por ejemplo,
        # para la máquina de multiplicar por 2.
        if self.current_state == "q1":
            output_sequence.append("1")
        return state_history, output_sequence

    def draw_graph(self):
        """
        Dibuja un grafo (diagrama no dirigido) que representa la máquina de estados.
        Se ajusta el tamaño de la figura y el parámetro 'k' del layout según la
        cantidad de nodos.
        """
        G = nx.Graph()
        for state in self.states:
            G.add_node(state)
        for (state, inp), next_state in self.transitions.items():
            label = f"{inp}/{self.outputs[(state, inp)]}"
            G.add_edge(state, next_state, label=label)
        
        n_nodes = len(G.nodes())
        if n_nodes < 10:
            fig_size = (10, 8)
            k_val = 1.5
        elif n_nodes < 20:
            fig_size = (12, 10)
            k_val = 2.0
        else:
            fig_size = (16, 12)
            k_val = 2.5

        plt.figure(figsize=fig_size)
        pos = nx.spring_layout(G, seed=42, k=k_val, iterations=100)
        node_colors = ["#FF5733" if state == self.initial_state else "#A0CBE2" for state in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3500,
                               edgecolors="black", linewidths=2)
        nx.draw_networkx_edges(G, pos, edge_color="#BBBBBB", width=2,
                               connectionstyle="arc3, rad=0.1")
        nx.draw_networkx_labels(G, pos, font_size=14, font_color="white", font_weight="bold")
        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                     font_size=12, font_color="black")
        plt.title("Máquina de Estado Finito (Grafo)", fontsize=18, fontweight="bold", color="black")
        plt.axis("off")
        plt.tight_layout()
        plt.show()
