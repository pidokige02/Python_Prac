import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from Utils import *
from log import *
from event_win import *
from log_win import *
from keyevent_win import *
from log import *
from configure_data import *


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

        # # 첫 번째 Pane 생성
        self.eventWin = EventWindow()
        self.eventWin.layout_EventWindow(self.notebook)

        # 두 번째 Pane 생성
        self.pane2 = ttk.Frame(self.notebook)
        self.notebook.add(self.pane2, text='Pane 2')

        # 세 번째 Pane 생성
        self.pane3 = ttk.Frame(self.notebook)
        self.notebook.add(self.pane3, text='Pane 3')


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

        #log window creation
        self.logwin = LogWindow() 

        # keyevent window creation
        self.keyeventwin =  KeyEventWindow ()

        # log object creation for log analysis 
        self.log = Log()


    def on_vertical_scroll(self, *args):
        print(f"Scrolled to: {args}")


    def open_log(self):
        # 파일 선택 대화 상자 열기
        file_path = filedialog.askopenfilename()

        if file_path:

            self.logwin.layout_LogWindow(self.root, LOGWIN_DIMENSION)

            file_path_keyevent = replace_filename(file_path, 'KeyBoardShadow_1.txt')

            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    
                    self.logwin.log_text.insert(tk.END, content)

                    self.log.load_log(file_path, use_columns)
                    self.log.add_columns()
                    self.log.analyze_log ()
                    self.log.filter_log()
                    self.eventWin.update_EventWindow(self.log.filtered_df)

            except Exception as e:
                self.logwin.log_text.insert(tk.END, f"Failed to read file:\n{e}")

            self.keyeventwin.layout_KeyEventWindow(self.root, KEYEVENTWIN_DIMENSION)

            try:
                with open(file_path_keyevent, 'r') as file:
                    content = file.read()
                    self.keyeventwin.keyevent_text.insert(tk.END, content)
            except Exception as e:
                self.keyeventwin.keyevent_text.insert(tk.END, f"Failed to read file:\n{e}")


        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
