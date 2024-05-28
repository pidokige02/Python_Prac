import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Navigation Bar Example")

        # Notebook 생성
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 첫 번째 Pane 생성
        self.pane1 = ttk.Frame(self.notebook)
        self.notebook.add(self.pane1, text='Pane 1')

        # 두 번째 Pane 생성
        self.pane2 = ttk.Frame(self.notebook)
        self.notebook.add(self.pane2, text='Pane 2')

        # 세 번째 Pane 생성
        self.pane3 = ttk.Frame(self.notebook)
        self.notebook.add(self.pane3, text='Pane 3')

        # 첫 번째 Pane 내용
        label1 = ttk.Label(self.pane1, text="This is Pane 1")
        label1.pack(pady=20, padx=20)

        # 두 번째 Pane 내용
        label2 = ttk.Label(self.pane2, text="This is Pane 2")
        label2.pack(pady=20, padx=20)

        # 세 번째 Pane 내용
        label3 = ttk.Label(self.pane3, text="This is Pane 3")
        label3.pack(pady=20, padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
