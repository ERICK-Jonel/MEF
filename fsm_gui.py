import tkinter as tk
import re
from tkinter import messagebox
from fsm_logic import FiniteStateMachine  # Lógica de la máquina de estados finitos (MEF)
from PIL import Image, ImageTk

###############################################################################
#                           COMPONENTE EDITOR                                  #
###############################################################################
class CodeEditorWithLineNumbers(tk.Frame):
    """
    Editor de código integrado con numeración de líneas y resaltado básico.
    
    Este componente crea:
      - Un área para la numeración de líneas.
      - Un área de texto para el código.
      - Un scrollbar vertical asociado.
      - Bindings para actualizar la numeración y el resaltado de sintaxis.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Área de numeración de líneas
        self.linenumbers = tk.Text(
            self,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            background="#2B2B2B",  # Fondo para la numeración
            foreground="#75715E",  # Color de la numeración
            state="disabled",
            font=("Courier", 12)
        )
        self.linenumbers.pack(side="left", fill="y")
        # Área principal de edición de código
        self.text = tk.Text(
            self,
            wrap="none",
            undo=True,
            background="#272822",  # Fondo del editor
            foreground="#F8F8F2",  # Color del texto
            insertbackground="#F8F8F2",  # Color del cursor
            font=("Courier", 12)
        )
        self.text.pack(side="right", fill="both", expand=True)
        # Scrollbar vertical
        self.v_scroll = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=self.v_scroll.set)
        # Bindings para actualizar numeración y resaltado
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
        self.text.bind("<Control-v>", self.custom_paste)
        self.text.bind("<Control-V>", self.custom_paste)
        
        # Inicia la actualización de la numeración y el resaltado
        self._update_line_numbers()
        self.setup_highlight_tags()
    
    def setup_highlight_tags(self):
        """Configura el tag para el resaltado de palabras clave."""
        self.text.tag_configure("keyword", foreground="#66d9ef")
    
    def select_all(self, event):
        """Selecciona todo el contenido del editor."""
        self.text.tag_add("sel", "1.0", "end")
        return "break"
    
    def custom_paste(self, event):
        """Realiza un pegado personalizado (sustituye la selección con el contenido del portapapeles)."""
        try:
            sel_start = self.text.index("sel.first")
            sel_end = self.text.index("sel.last")
            self.text.delete(sel_start, sel_end)
            self.text.insert(sel_start, self.text.clipboard_get())
        except tk.TclError:
            self.text.event_generate("<<Paste>>")
        return "break"
    
    def _on_change(self, event=None):
        """Callback que se ejecuta al detectar cambios: actualiza numeración y resaltado."""
        self._update_line_numbers()
        self.highlight_syntax()
    
    def _update_line_numbers(self):
        """Actualiza la numeración de líneas según el contenido actual del editor."""
        self.linenumbers.config(state="normal")
        self.linenumbers.delete("1.0", "end")
        line_count = int(self.text.index("end-1c").split(".")[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        self.linenumbers.insert("1.0", line_numbers_string)
        self.linenumbers.config(state="disabled")
    
    def highlight_syntax(self, event=None):
        """
        Elimina los tags de resaltado y aplica nuevamente el resaltado a
        cada palabra clave definida.
        """
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

###############################################################################
#                        INTERFAZ PRINCIPAL (FSMApp)                         #
###############################################################################
class FSMApp:
    """
    Interfaz principal del simulador de Máquina de Estado Finito (MEF).
    
    Esta clase se encarga de:
      - Configurar la ventana principal (tamaño, fondo, atajos generales).
      - Crear y organizar los widgets de la interfaz: entrada, botones, salida y el editor.
      - Conectar la lógica de la FSM (definida en fsm_logic.py) con la interacción del usuario.
    """
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Simulador de Máquina de Estado Finito (MEF)")
        self.root.geometry("1200x900")
        self.root.minsize(1200, 900)
        self.root.configure(bg="#3C3F41")
        self.root.bind("<Control-r>", lambda event: self.reset_simulation())
        self.root.bind("<Control-R>", lambda event: self.reset_simulation())
        
        # --- Sección de Simulación ---
        sim_frame = tk.Frame(root, bg="#3C3F41")
        sim_frame.pack(pady=20, padx=10)
        
        # Etiqueta para indicar la entrada
        self.label = tk.Label(sim_frame,
                              text="Ingrese la secuencia:",
                              font=("Arial", 14, "bold"),
                              bg="#3C3F41", fg="white")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campo de entrada para la secuencia (no se restringe a "0" o "1")
        self.entry = tk.Entry(sim_frame,
                              font=("Arial", 14),
                              width=40,
                              bg="white", fg="black",
                              relief="flat", bd=5)
        self.entry.grid(row=1, column=0, columnspan=2, pady=10)
        self.entry.bind("<Control-Return>", lambda event: self.run_simulation())
        btn_width = 15
        
        # Botón "Ejecutar" para simular el procesamiento de la entrada
        self.button_run = tk.Button(sim_frame, text="Ejecutar",
                                    command=self.run_simulation,
                                    font=("Arial", 12, "bold"),
                                    bg="#4CAF50", fg="white",
                                    relief="flat", bd=4, width=btn_width)
        self.button_run.grid(row=2, column=0, padx=5, pady=5)
        self.button_run.original_bg = "#4CAF50"
        self.button_run.hover_bg = "#66BB6A"
        self.button_run.bind("<Enter>", self.on_enter)
        self.button_run.bind("<Leave>", self.on_leave)
        
        # Botón "Ver Digrafo" para generar el diagrama de estados
        self.button_graph = tk.Button(sim_frame, text="Ver Digrafo",
                                      command=self.show_graph,
                                      font=("Arial", 12, "bold"),
                                      bg="#2196F3", fg="white",
                                      relief="flat", bd=4, width=btn_width)
        self.button_graph.grid(row=2, column=1, padx=5, pady=5)
        self.button_graph.original_bg = "#2196F3"
        self.button_graph.hover_bg = "#42A5F5"
        self.button_graph.bind("<Enter>", self.on_enter)
        self.button_graph.bind("<Leave>", self.on_leave)
        
        # Botón "Reiniciar" para reiniciar la simulación
        self.button_reset = tk.Button(sim_frame, text="Reiniciar",
                                      command=self.reset_simulation,
                                      font=("Arial", 12, "bold"),
                                      bg="#f44336", fg="white",
                                      relief="flat", bd=4, width=btn_width)
        self.button_reset.grid(row=3, column=0, padx=5, pady=5)
        self.button_reset.original_bg = "#f44336"
        self.button_reset.hover_bg = "#EF5350"
        self.button_reset.bind("<Enter>", self.on_enter)
        self.button_reset.bind("<Leave>", self.on_leave)
        
        # Botón "Copiar Salida" para copiar el resultado
        self.button_copy = tk.Button(sim_frame, text="Copiar Salida",
                                     command=self.copy_output,
                                     font=("Arial", 12, "bold"),
                                     bg="#009688", fg="white",
                                     relief="flat", bd=4, width=btn_width)
        self.button_copy.grid(row=3, column=1, padx=5, pady=5)
        self.button_copy.original_bg = "#009688"
        self.button_copy.hover_bg = "#26A69A"
        self.button_copy.bind("<Enter>", self.on_enter)
        self.button_copy.bind("<Leave>", self.on_leave)
        
        # Etiqueta para mostrar la salida del simulador
        self.output_label = tk.Label(sim_frame, text="",
                                     font=("Arial", 12),
                                     bg="#3C3F41", fg="white", justify="left")
        self.output_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # --- Sección del Editor de Código ---
        code_frame = tk.Frame(root, bg="#3C3F41")
        code_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Etiqueta descriptiva del editor
        self.code_editor_label = tk.Label(code_frame,
                                        text="Editor de Código (defina su máquina):",
                                        font=("Arial", 14, "bold"),
                                        bg="#3C3F41", fg="white")
        self.code_editor_label.pack(pady=5)
        
        # Instancia del editor integrado
        self.code_editor = CodeEditorWithLineNumbers(code_frame, bg="#272822")
        self.code_editor.pack(padx=5, pady=5, anchor="n")
        
        # Código default para la máquina de estados (Ejercicio 1)
        self.default_code = """# ejercicio de ejemplo
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
    ("q1", "0"): "0",
    ("q1", "1"): "1"
}

initial_state = "q0"
"""
        self.code_editor.text.insert("1.0", self.default_code)
        self.highlight_syntax()
        
        # Botón para cargar la máquina definida en el editor
        self.button_load_machine = tk.Button(code_frame, text="Cargar Máquina",
                                            command=self.load_machine,
                                            font=("Arial", 12, "bold"),
                                            bg="#9C27B0", fg="white",
                                            relief="flat", bd=4)
        self.button_load_machine.pack(pady=5)
        
        # Botón para restaurar el código a default
        self.button_reset_default = tk.Button(code_frame, text="Restaurar a Default",
                                            command=self.reset_to_default,
                                            font=("Arial", 12, "bold"),
                                            bg="#FF9800", fg="white",
                                            relief="flat", bd=4)
        self.button_reset_default.pack(pady=5)
        
        ############################################################################
        #      Integración de la Lógica de la Máquina de Estados Finitos (MEF)       #
        #  Aquí se crea la instancia de la FSM usando parámetros default            #
        ############################################################################
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
        self.fsm = FiniteStateMachine(states, alphabet, transitions, initial_state, outputs)
        
        # Bind para actualizar el editor al soltar una tecla.
        self.code_editor.text.bind("<KeyRelease>", self.handle_keyrelease)
    
    # ---------------------- Métodos de la Interfaz General ----------------------
    def on_enter(self, event):
        """Cambia el fondo del widget al pasar el mouse (hover)."""
        event.widget.config(bg=event.widget.hover_bg)
    
    def on_leave(self, event):
        """Restaura el fondo original del widget al salir el mouse."""
        event.widget.config(bg=event.widget.original_bg)
    
    def copy_output(self):
        """Copia el contenido de la salida al portapapeles."""
        output_text = self.output_label.cget("text")
        if output_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            print("Salida copiada al portapapeles.")
        else:
            print("No hay salida para copiar.")
    
    def handle_keyrelease(self, event=None):
        """Actualiza la numeración y el resaltado en el editor al soltar una tecla."""
        self.code_editor._on_change()
        self.highlight_syntax()
    
    def highlight_syntax(self, event=None):
        """Aplica el resaltado de sintaxis en el editor de código."""
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
    
    # ---------------------- Métodos de Integración con la FSM ----------------------
    def run_simulation(self):
        """
        Lee la secuencia de entrada del Entry, la procesa mediante la FSM,
        y muestra la secuencia de estados y salidas resultante.
        
        *Modificación:* Se remueve la validación estricta de "0" y "1" para permitir
        ingresar cualquier símbolo del alfabeto definido.
        """
        # Se obtiene la entrada sin aplicar strip() para preservar espacios finales.
        input_sequence = list(self.entry.get())
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
        """
        Reinicia la simulación:
          - Borra el contenido del Entry.
          - Limpia la salida.
          - Restablece el estado inicial de la FSM.
        """
        self.entry.delete(0, tk.END)
        self.output_label.config(text="")
        if self.fsm:
            self.fsm.current_state = self.fsm.initial_state
    
    def show_graph(self):
        """
        Invoca el método draw_graph() de la FSM para generar y visualizar
        el diagrama de estados.
        """
        self.fsm.draw_graph()
    
    def load_machine(self):
        """
        Carga una definición de máquina de estados a partir del código introducido
        en el editor de código mediante exec(), siempre que se definan:
          states, alphabet, transitions, outputs, initial_state.
        """
        code_str = self.code_editor.text.get("1.0", tk.END)
        local_vars = {}
        try:
            exec(code_str, {}, local_vars)
            required_vars = ["states", "alphabet", "transitions", "outputs", "initial_state"]
            if not all(var in local_vars for var in required_vars):
                messagebox.showerror("Error", "El código debe definir: states, alphabet, transitions, outputs, initial_state")
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
        """
        Restaura el código del editor a la definición default y actualiza la FSM con dicha definición.
        """
        self.code_editor.text.delete("1.0", tk.END)
        self.code_editor.text.insert("1.0", self.default_code)
        self.highlight_syntax()
        local_vars = {}
        try:
            exec(self.default_code, {}, local_vars)
            required_vars = ["states", "alphabet", "transitions", "outputs", "initial_state"]
            if not all(var in local_vars for var in required_vars):
                messagebox.showerror("Error", "El código default no define: states, alphabet, transitions, outputs, initial_state")
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

###############################################################################
#                    BLOQUE DE EJECUCIÓN PRINCIPAL (MAIN)                   #
###############################################################################
if __name__ == "__main__":
    root = tk.Tk()
    app = FSMApp(root)
    root.mainloop()
