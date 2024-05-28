import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Viewer")
        self.root.geometry("800x600")

        # 파일 선택 버튼
        self.open_button = tk.Button(self.root, text="Open Log", command=self.open_log)
        self.open_button.pack(pady=10)

    def open_log(self):
        # 파일 선택 대화 상자 열기
        file_path = filedialog.askopenfilename()

        if file_path:
            log_window = tk.Toplevel(self.root)
            log_window.title("Log")
            log_window.geometry("800x600")

            # 프레임
            frame = tk.Frame(log_window)
            frame.pack(expand=True, fill='both')

            # 텍스트 위젯
            log_text = tk.Text(frame, wrap='word')
            log_text.pack(side=tk.LEFT, expand=True, fill='both')

            # 파일 읽기 및 내용 삽입
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    log_text.insert(tk.END, content)
            except Exception as e:
                log_text.insert(tk.END, f"Failed to read file:\n{e}")

            # 수직 스크롤 막대
            vscroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=log_text.yview)
            vscroll.pack(side=tk.RIGHT, fill=tk.Y)
            log_text.config(yscrollcommand=vscroll.set)

            # 수평 스크롤 막대
            hscroll = tk.Scrollbar(log_window, orient=tk.HORIZONTAL, command=log_text.xview)
            hscroll.pack(side=tk.BOTTOM, fill=tk.X)
            log_text.config(xscrollcommand=hscroll.set)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()