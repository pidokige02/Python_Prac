import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Issue Inv Assistent")
        self.root.geometry("400x600+0+0")  # 윈도우 크기를 800x600으로 설정

        # Grid 레이아웃 설정
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        # 스타일 설정
        style = ttk.Style()
        style.configure("Blue.TLabel", foreground="blue", font=("Helvetica", 16, "bold"))

        # 제목 라벨
        title_label = ttk.Label(root, text="Issue Inv Assistant", style="Blue.TLabel")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Notebook 생성
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=0, sticky="nsew")

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

        # 오른쪽 프레임 생성
        right_frame = ttk.Frame(root)
        right_frame.grid(row=1, column=1, sticky="ns")

        # 버튼 추가
        button = ttk.Button(right_frame, text="Open Log", command=self.open_log)
        button.pack(padx=10, pady=10, anchor="ne")

        # 버튼 추가
        button = ttk.Button(right_frame, text="Button2")
        button.pack(padx=10, pady=10, anchor="ne")

    def open_log(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Log")
        log_window.geometry("800x600+400+0")

        log_text = tk.Text(log_window, wrap='word')
        log_text.pack(expand=True, fill='both')

        log_text.insert(tk.END, "This is a log message.\nMore log messages can be added here.")

        


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
