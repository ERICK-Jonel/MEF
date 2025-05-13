import tkinter as tk
import re
import networkx as nx
import matplotlib.pyplot as plt
# Variable global para referenciar el Tk principal
APP_ROOT = None
# --- Funciones personalizadas de mensajes ---
def custom_showerror(parent, title, message):
    win = tk.Toplevel(parent)
    win.configure(bg="#3C3F41")
    win.title(title)
    win.geometry("400x150")
    label = tk.Label(win, text=message, font=("Arial", 12), bg="#3C3F41", fg="white", wraplength=380)
    label.pack(pady=20, padx=10)
    button = tk.Button(win, text="Ok", command=win.destroy, font=("Arial", 12), bg="#FF9800", fg="white")
    button.pack(pady=10)
    # Cierre con ESC
    win.bind("<Escape>", lambda event: win.destroy())
    win.grab_set()
    win.transient(parent)
    win.wait_window(win)
def custom_showinfo(parent, title, message):
    win = tk.Toplevel(parent)
    win.configure(bg="#3C3F41")
    win.title(title)
    win.geometry("400x150")
    label = tk.Label(win, text=message, font=("Arial", 12), bg="#3C3F41", fg="white", wraplength=380)
    label.pack(pady=20, padx=10)
    button = tk.Button(win, text="Ok", command=win.destroy, font=("Arial", 12), bg="#66BB6A", fg="white")
    button.pack(pady=10)
    # Cierre con ESC
    win.bind("<Escape>", lambda event: win.destroy())
    win.grab_set()
    win.transient(parent)
    win.wait_window(win)
# --- Editor de código con números de línea y resaltado básico ---
class CodeEditorWithLineNumbers(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        # Área de números de línea
        self.linenumbers = tk.Text(self, width=4, padx=4, takefocus=0, border=0,
                                   background="#2B2B2B", foreground="#75715E", state="disabled",
                                   font=("Courier", 12))
        self.linenumbers.pack(side="left", fill="y")
        # Área principal de edición
        self.text = tk.Text(self, wrap="none", undo=True, background="#272822", foreground="#F8F8F2",
                            insertbackground="#F8F8F2", font=("Courier", 12))
        self.text.pack(side="right", fill="both", expand=True)
        # Scroll vertical
        self.v_scroll = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=self.v_scroll.set)
        # Vinculación de eventos: actualiza números de línea y resalta sintaxis
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        self.text.bind("<KeyRelease>", self._on_change)
        # Atajos de teclado
        self.text.bind("<Control-a>", self.select_all)
        self.text.bind("<Control-A>", self.select_all)
        self.text.bind("<Control-z>", lambda event: self.text.edit_undo() or "break")
        self.text.bind("<Control-Z>", lambda event: self.text.edit_undo() or "break")
        self.text.bind("<Control-y>", lambda event: self.text.edit_redo() or "break")
        self.text.bind("<Control-Y>", lambda event: self.text.edit_redo() or "break")
        # Pegado personalizado: si hay selección, reemplaza el contenido
        self.text.bind("<Control-v>", self.custom_paste)
        self.text.bind("<Control-V>", self.custom_paste)
        self._update_line_numbers()
        self.setup_highlight_tags()
    def setup_highlight_tags(self):
        self.text.tag_configure("keyword", foreground="#66d9ef")
    def select_all(self, event):
        self.text.tag_add("sel", "1.0", "end")
        return "break"
    def custom_paste(self, event):
        try:
            sel_start = self.text.index("sel.first")
            sel_end = self.text.index("sel.last")
            self.text.delete(sel_start, sel_end)
            self.text.insert(sel_start, self.text.clipboard_get())
        except tk.TclError:
            self.text.event_generate("<<Paste>>")
        return "break"
    def _on_change(self, event=None):
        self._update_line_numbers()
        self.highlight_syntax()
    def _update_line_numbers(self):
        self.linenumbers.config(state="normal")
        self.linenumbers.delete("1.0", "end")
        line_count = int(self.text.index("end-1c").split(".")[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        self.linenumbers.insert("1.0", line_numbers_string)
        self.linenumbers.config(state="disabled")
    def highlight_syntax(self, event=None):
        self.text.tag_remove("keyword", "1.0", "end")
        keywords = ["def", "class", "import", "from", "as", "if", "elif", "else", 
                    "for", "while", "try", "except", "finally", "with", "return", 
                    "yield", "pass", "break", "continue", "and", "or", "not", "in", "is", 
                    "lambda", "True", "False", "None"]
        for kw in keywords:
            start_index = "1.0"
            while True:
                pos = self.text.search(r'\b' + re.escape(kw) + r'\b', start_index, stopindex="end", regexp=True)
                if not pos:
                    break
                end_pos = f"{pos}+{len(kw)}c"
                self.text.tag_add("keyword", pos, end_pos)
                start_index = end_pos
        self.text.tag_configure("keyword", foreground="#66d9ef")
# --- Máquina de Estados Finita ---
class FiniteStateMachine:
    def __init__(self, states, alphabet, transitions, initial_state, outputs):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.outputs = outputs
        self.current_state = initial_state
    def process_input(self, input_sequence):
        state_history = [self.initial_state]
        output_sequence = []
        for inp in input_sequence:
            if (self.current_state, inp) in self.transitions:
                next_state = self.transitions[(self.current_state, inp)]
                output = self.outputs[(self.current_state, inp)]
                state_history.append(next_state)
                output_sequence.append(output)
                self.current_state = next_state
            else:
                custom_showerror(APP_ROOT, "Error", f"Entrada '{inp}' no válida desde el estado '{self.current_state}'")
                return [], []
        return state_history, output_sequence
    def draw_graph(self):
        """Genera un grafo (diagrama no dirigido) de la máquina de estados.
           Se ajustan dinámicamente el tamaño de la figura y el parámetro 'k' según el número de nodos.
        """
        # Usamos un grafo no dirigido
        G = nx.Graph()
        for state in self.states:
            G.add_node(state)
        for (state, inp), next_state in self.transitions.items():
            label = f"{inp}/{self.outputs[(state, inp)]}"
            G.add_edge(state, next_state, label=label)
        # Ajuste de parámetros según el número de nodos
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
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3500, edgecolors="black", linewidths=2)
        nx.draw_networkx_edges(G, pos, edge_color="#BBBBBB", width=2, connectionstyle="arc3, rad=0.1")
        nx.draw_networkx_labels(G, pos, font_size=14, font_color="white", font_weight='bold')
        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_color="black")
        plt.title("Máquina de Estado Finito (Grafo)", fontsize=18, fontweight='bold', color="black")
        plt.axis("off")
        plt.tight_layout()
        plt.show()
# --- Interfaz Principal (FSMApp) ---
class FSMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Estado Finito")
        self.root.geometry("900x800")
        self.root.configure(bg="#3C3F41")
        # Vinculamos Control+R para reiniciar
        self.root.bind("<Control-r>", lambda event: self.reset_simulation())
        self.root.bind("<Control-R>", lambda event: self.reset_simulation())
        # Sección de simulación
        sim_frame = tk.Frame(root, bg="#3C3F41")
        sim_frame.pack(pady=10)
        self.label = tk.Label(sim_frame, text="Ingrese la secuencia binaria (0s y 1s):", 
                              font=("Arial", 12), bg="#3C3F41", fg="white")
        self.label.pack(pady=5)
        self.entry = tk.Entry(sim_frame, font=("Arial", 12), width=40)
        self.entry.pack(pady=5)
        self.entry.bind("<Control-Return>", lambda event: self.run_simulation())
        self.button_run = tk.Button(sim_frame, text="Ejecutar", command=self.run_simulation,
                                      font=("Arial", 12), bg="#4CAF50", fg="white")
        self.button_run.pack(pady=5)
        self.button_graph = tk.Button(sim_frame, text="Ver Grafo", command=self.show_graph,
                                      font=("Arial", 12), bg="#2196F3", fg="white")
        self.button_graph.pack(pady=5)
        self.button_reset = tk.Button(sim_frame, text="Reiniciar", command=self.reset_simulation,
                                      font=("Arial", 12), bg="#f44336", fg="white")
        self.button_reset.pack(pady=5)
        self.output_label = tk.Label(sim_frame, text="", font=("Arial", 12), bg="#3C3F41", fg="white", justify="left")
        self.output_label.pack(pady=10)
        # Editor de código
        code_frame = tk.Frame(root, bg="#3C3F41")
        code_frame.pack(pady=10, fill="both", expand=True)
        self.code_editor_label = tk.Label(code_frame, 
            text="Editor de Código (defina su máquina de estados):", font=("Arial", 12),
            bg="#3C3F41", fg="white")
        self.code_editor_label.pack(pady=5)
        self.code_editor = CodeEditorWithLineNumbers(code_frame)
        self.code_editor.pack(padx=10, pady=5, fill="both", expand=True)
        self.default_code = """# Ejemplo: Chequeadora de Paridad
states = ["q0", "q1"]
alphabet = ["0", "1"]
transitions = {
    ("q0", "0"): "q0",
    ("q0", "1"): "q1",
    ("q1", "0"): "q1",
    ("q1", "1"): "q0"
}
outputs = {
    ("q0", "0"): "0",
    ("q0", "1"): "1",
    ("q1", "0"): "1",
    ("q1", "1"): "0"
}
initial_state = "q0"
"""
        self.code_editor.text.insert("1.0", self.default_code)
        self.highlight_syntax()  # Resaltado inicial
        
        self.button_load_machine = tk.Button(code_frame, text="Cargar Máquina", command=self.load_machine,
                                               font=("Arial", 12), bg="#9C27B0", fg="white")
        self.button_load_machine.pack(pady=5)
        
        self.button_reset_default = tk.Button(code_frame, text="Restaurar a Default", command=self.reset_to_default,
                                               font=("Arial", 12), bg="#FF9800", fg="white")
        self.button_reset_default.pack(pady=5)
        # Máquina por defecto
        states = ["q0", "q1"]
        alphabet = ["0", "1"]
        transitions = {
            ("q0", "0"): "q0", ("q0", "1"): "q1",
            ("q1", "0"): "q1", ("q1", "1"): "q0"
        }
        outputs = {
            ("q0", "0"): "0", ("q0", "1"): "1",
            ("q1", "0"): "1", ("q1", "1"): "0"
        }
        initial_state = "q0"
        self.fsm = FiniteStateMachine(states, alphabet, transitions, initial_state, outputs)
        # Vincular actualización de resaltado
        self.code_editor.text.bind("<KeyRelease>", self.handle_keyrelease)
    def handle_keyrelease(self, event=None):
        self.code_editor._on_change()
        self.highlight_syntax()
    def highlight_syntax(self, event=None):
        text_widget = self.code_editor.text
        text_widget.tag_remove("keyword", "1.0", "end")
        keywords = ["def", "class", "import", "from", "as", "if", "elif", "else", 
                    "for", "while", "try", "except", "finally", "with", "return", 
                    "yield", "pass", "break", "continue", "and", "or", "not", "in", "is",
                    "lambda", "True", "False", "None"]
        for kw in keywords:
            start_index = "1.0"
            while True:
                pos = text_widget.search(r'\b' + re.escape(kw) + r'\b', start_index, stopindex="end", regexp=True)
                if not pos:
                    break
                end_pos = f"{pos}+{len(kw)}c"
                text_widget.tag_add("keyword", pos, end_pos)
                start_index = end_pos
        text_widget.tag_configure("keyword", foreground="#66d9ef")
    def run_simulation(self):
        input_sequence = list(self.entry.get().strip())
        if not all(inp in ["0", "1"] for inp in input_sequence):
            custom_showerror(self.root, "Error", "Ingrese solo valores 0 o 1.")
            return
        states, outputs = self.fsm.process_input(input_sequence)
        if states:
            result_text = (
                "RESULTADO DE LA SIMULACIÓN:\n\n" +
                "Entrada: " + ' '.join(input_sequence) + "\n\n" +
                "Secuencia de Estados: " + " -> ".join(states) + "\n\n" +
                "Secuencia de Salidas: " + ' '.join(outputs)
            )
            self.output_label.config(text=result_text)
    def reset_simulation(self):
        self.entry.delete(0, tk.END)
        self.output_label.config(text="")
        self.fsm.current_state = self.fsm.initial_state
    def show_graph(self):
        self.fsm.draw_graph()
    def load_machine(self):
        code_str = self.code_editor.text.get("1.0", tk.END)
        local_vars = {}
        try:
            exec(code_str, {}, local_vars)
            required_vars = ["states", "alphabet", "transitions", "outputs", "initial_state"]
            if not all(var in local_vars for var in required_vars):
                custom_showerror(self.root, "Error", "El código debe definir: states, alphabet, transitions, outputs, initial_state")
                return
            states = local_vars["states"]
            alphabet = local_vars["alphabet"]
            transitions = local_vars["transitions"]
            outputs = local_vars["outputs"]
            initial_state = local_vars["initial_state"]
            self.fsm = FiniteStateMachine(states, alphabet, transitions, initial_state, outputs)
            custom_showinfo(self.root, "Éxito", "La máquina de estados ha sido cargada exitosamente.")
        except Exception as e:
            custom_showerror(self.root, "Error al cargar la máquina", str(e))
    def reset_to_default(self):
        """Restaura el editor y la máquina a su contenido por defecto."""
        self.code_editor.text.delete("1.0", tk.END)
        self.code_editor.text.insert("1.0", self.default_code)
        self.highlight_syntax()
        local_vars = {}
        try:
            exec(self.default_code, {}, local_vars)
            required_vars = ["states", "alphabet", "transitions", "outputs", "initial_state"]
            if not all(var in local_vars for var in required_vars):
                custom_showerror(self.root, "Error", "El código default no define: states, alphabet, transitions, outputs, initial_state")
                return
            states = local_vars["states"]
            alphabet = local_vars["alphabet"]
            transitions = local_vars["transitions"]
            outputs = local_vars["outputs"]
            initial_state = local_vars["initial_state"]
            self.fsm = FiniteStateMachine(states, alphabet, transitions, initial_state, outputs)
            self.reset_simulation()
            custom_showinfo(self.root, "Restaurado", "Se ha restaurado la máquina al estado default.")
        except Exception as e:
            custom_showerror(self.root, "Error al restaurar", str(e))
if __name__ == "__main__":
    root = tk.Tk()
    APP_ROOT = root  # Asigna el Tk principal a la variable global
    app = FSMApp(root)
    root.mainloop()
