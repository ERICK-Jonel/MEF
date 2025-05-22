import tkinter as tk
from fsm_gui import FSMApp

def main():
    root = tk.Tk()
    app = FSMApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


