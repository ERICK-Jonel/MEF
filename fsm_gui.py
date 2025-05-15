import tkinter as tk
import re
from tkinter import messagebox
from fsm_logic import FiniteStateMachine
from PIL import Image, ImageTk

# --- Editor de código con números de línea y resaltado básico
class CodeEditorWithLineNumbers(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Área de números de línea
        self.linenumbers = tk.Text(self, width=4, padx=4, takefocus=0, border=0,
                                    background="#2B2B2B", foreground="#75715E", state="disabled",
                                    font=("Courier", 12))
        self.linenumbers.pack(side="left", fill="y")
        # Área principal de edición de código
        self.text = tk.Text(self, wrap="none", undo=True, 
                            background="#272822", foreground="#F8F8F2",
                            insertbackground="#F8F8F2", font=("Courier", 12))
        self.text.pack(side="right", fill="both", expand=True)
        # Scrollbar vertical
        self.v_scroll = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=self.v_scroll.set)
        # Vinculación de eventos para actualizar numeración y resaltado
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
        # Pegado personalizado
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
        keywords = ['def', 'class', 'import', 'from', 'as', 'if', 'elif', 'else',
                    'for', 'while', 'try', 'except', 'finally', 'with', 'return',
                    'yield', 'pass', 'break', 'continue', 'and', 'or', 'not', 'in',
                    'is', 'lambda', 'True', 'False', 'None']
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


# --- Clase de la Interfaz Principal ---
class FSMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Estado Finito (MEF)")
        self.root.geometry("900x800")
        self.root.configure(bg="#3C3F41")
        self.root.bind("<Control-r>", lambda event: self.reset_simulation())
        self.root.bind("<Control-R>", lambda event: self.reset_simulation())

        # Sección de simulación (usamos grid para un posicionamiento preciso)
        sim_frame = tk.Frame(root, bg="#3C3F41")
        sim_frame.pack(pady=20, padx=20)

        self.label = tk.Label(sim_frame, text="Ingrese la secuencia binaria (0s y 1s):",
                              font=("Arial", 14, "bold"), bg="#3C3F41", fg="white")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.entry = tk.Entry(sim_frame, font=("Arial", 14), width=40,
                              bg="white", fg="black", relief="flat", bd=5)
        self.entry.grid(row=1, column=0, columnspan=2, pady=10)
        self.entry.bind("<Control-Return>", lambda event: self.run_simulation())

        btn_width = 15  # ancho uniforme para los botones

        self.button_run = tk.Button(sim_frame, text="Ejecutar", command=self.run_simulation,
                                     font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", bd=4,
                                     width=btn_width)
        self.button_run.grid(row=2, column=0, padx=5, pady=5)
        self.button_run.original_bg = "#4CAF50"
        self.button_run.hover_bg = "#66BB6A"
        self.button_run.bind("<Enter>", self.on_enter)
        self.button_run.bind("<Leave>", self.on_leave)

        self.button_graph = tk.Button(sim_frame, text="Ver Digrafo", command=self.show_graph,
                                       font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", bd=4,
                                       width=btn_width)
        self.button_graph.grid(row=2, column=1, padx=5, pady=5)
        self.button_graph.original_bg = "#2196F3"
        self.button_graph.hover_bg = "#42A5F5"
        self.button_graph.bind("<Enter>", self.on_enter)
        self.button_graph.bind("<Leave>", self.on_leave)

        self.button_reset = tk.Button(sim_frame, text="Reiniciar", command=self.reset_simulation,
                                       font=("Arial", 12, "bold"), bg="#f44336", fg="white", relief="flat", bd=4,
                                       width=btn_width)
        self.button_reset.grid(row=3, column=0, padx=5, pady=5)
        self.button_reset.original_bg = "#f44336"
        self.button_reset.hover_bg = "#EF5350"
        self.button_reset.bind("<Enter>", self.on_enter)
        self.button_reset.bind("<Leave>", self.on_leave)

        self.button_copy = tk.Button(sim_frame, text="Copiar Salida", command=self.copy_output,
                                      font=("Arial", 12, "bold"), bg="#009688", fg="white", relief="flat", bd=4,
                                      width=btn_width)
        self.button_copy.grid(row=3, column=1, padx=5, pady=5)
        self.button_copy.original_bg = "#009688"
        self.button_copy.hover_bg = "#26A69A"
        self.button_copy.bind("<Enter>", self.on_enter)
        self.button_copy.bind("<Leave>", self.on_leave)

        self.output_label = tk.Label(sim_frame, text="", font=("Arial", 12),
                                     bg="#3C3F41", fg="white", justify="left")
        self.output_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Editor de código para definir la máquina de estados
        code_frame = tk.Frame(root, bg="#3C3F41")
        code_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.code_editor_label = tk.Label(code_frame, text="Editor de Código (defina su máquina):",
                                          font=("Arial", 14, "bold"), bg="#3C3F41", fg="white")
        self.code_editor_label.pack(pady=5)

        self.code_editor = CodeEditorWithLineNumbers(code_frame, bg="#272822")
        self.code_editor.pack(padx=10, pady=5, fill="both", expand=True)

        self.default_code = """# Máquina para multiplicar por 2 (leer LSB-first)
states = ["q0", "q1"]
alphabet = ["0", "1"]
transitions = {
    ("q0", "0"): "q0",
    ("q0", "1"): "q1",
    ("q1", "0"): "q0",
    ("q1", "1"): "q1"
}
outputs = {
    ("q0", "0"): "0",
    ("q0", "1"): "0",
    ("q1", "0"): "1",
    ("q1", "1"): "1"
}
initial_state = "q0"
"""
        self.code_editor.text.insert("1.0", self.default_code)
        self.highlight_syntax()
        self.button_load_machine = tk.Button(code_frame, text="Cargar Máquina", command=self.load_machine,
                                               font=("Arial", 12, "bold"), bg="#9C27B0", fg="white", relief="flat", bd=4)
        self.button_load_machine.pack(pady=5)

        self.button_reset_default = tk.Button(code_frame, text="Restaurar a Default", command=self.reset_to_default,
                                                font=("Arial", 12, "bold"), bg="#FF9800", fg="white", relief="flat", bd=4)
        self.button_reset_default.pack(pady=5)

        # Configuración inicial de la máquina por defecto (multiplicación por 2)
        states = ["q0", "q1"]
        alphabet = ["0", "1"]
        transitions = {
            ("q0", "0"): "q0", ("q0", "1"): "q1",
            ("q1", "0"): "q0", ("q1", "1"): "q1"
        }
        outputs = {
            ("q0", "0"): "0", ("q0", "1"): "0",
            ("q1", "0"): "1", ("q1", "1"): "1"
        }
        initial_state = "q0"
        self.fsm = FiniteStateMachine(states, alphabet, transitions, initial_state, outputs)
        self.code_editor.text.bind("<KeyRelease>", self.handle_keyrelease)

    def on_enter(self, event):
        event.widget.config(bg=event.widget.hover_bg)

    def on_leave(self, event):
        event.widget.config(bg=event.widget.original_bg)

    def copy_output(self):
        output_text = self.output_label.cget("text")
        if output_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            print("Salida copiada al portapapeles.")
        else:
            print("No hay salida para copiar.")

    def handle_keyrelease(self, event=None):
        self.code_editor._on_change()
        self.highlight_syntax()

    def highlight_syntax(self, event=None):
        text_widget = self.code_editor.text
        text_widget.tag_remove("keyword", "1.0", "end")
        keywords = ["def", "class", "import", "from", "as", "if", "elif", "else",
                    "for", "while", "try", "except", "finally", "with", "return",
                    "yield", "pass", "break", "continue", "and", "or", "not", "in",
                    "is", "lambda", "True", "False", "None"]
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
            messagebox.showerror("Error", "Ingrese solo valores 0 o 1.")
            return
        try:
            state_history, output_sequence = self.fsm.process_input(input_sequence)
            result_text = (
                "RESULTADO DE LA SIMULACIÓN:\n\n" +
                "Entrada: " + " ".join(input_sequence) + "\n\n" +
                "Secuencia de Estados: " + " -> ".join(state_history) + "\n\n" +
                "Secuencia de Salidas: " + " ".join(output_sequence)
            )
            self.output_label.config(text=result_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_simulation(self):
        self.entry.delete(0, tk.END)
        self.output_label.config(text="")
        if self.fsm:
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
                messagebox.showerror("Error",
                                     "El código debe definir: states, alphabet, transitions, outputs, initial_state")
                return
            states = local_vars["states"]
            alphabet = local_vars["alphabet"]
            transitions = local_vars["transitions"]
            outputs = local_vars["outputs"]
            initial_state = local_vars["initial_state"]
            self.fsm = FiniteStateMachine(states, alphabet, transitions, initial_state, outputs)
            messagebox.showinfo("Éxito", "La máquina de estados ha sido cargada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error al cargar la máquina", str(e))

    def reset_to_default(self):
        self.code_editor.text.delete("1.0", tk.END)
        self.code_editor.text.insert("1.0", self.default_code)
        self.highlight_syntax()
        local_vars = {}
        try:
            exec(self.default_code, {}, local_vars)
            required_vars = ["states", "alphabet", "transitions", "outputs", "initial_state"]
            if not all(var in local_vars for var in required_vars):
                messagebox.showerror("Error",
                                     "El código default no define: states, alphabet, transitions, outputs, initial_state")
                return
            states = local_vars["states"]
            alphabet = local_vars["alphabet"]
            transitions = local_vars["transitions"]
            outputs = local_vars["outputs"]
            initial_state = local_vars["initial_state"]
            self.fsm = FiniteStateMachine(states, alphabet, transitions, initial_state, outputs)
            self.reset_simulation()
            messagebox.showinfo("Restaurado", "Se ha restaurado la máquina al estado default.")
        except Exception as e:
            messagebox.showerror("Error al restaurar", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FSMApp(root)
    root.mainloop()
