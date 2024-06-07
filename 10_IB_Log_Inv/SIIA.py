import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from Utils import *
from log import *
from event_win import *
from info_win import *
from peripheral_win import *
from log_win import *
from keyevent_win import *
from log import *
from configure_data import *


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Issue Inv Assistent")
        self.root.geometry(MAINWIN_DIMENSION)  # 윈도우 크기를 800x600으로 설정

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

        #log window creation
        self.logwin = LogWindow() 

        # keyevent window creation
        self.keyeventwin =  KeyEventWindow ()

        # # 첫 번째 Pane EventWindow 생성
        self.eventWin = EventWindow(self.logwin)
        self.eventWin.layout_EventWindow(self.notebook)

        # 두 번째 Pane InfoWindow 생성
        self.infoWin = InfoWindow()
        self.infoWin.layout_InfoWindow(self.notebook)

        # 세 번째 Pane peripheral_win 생성
        self.periWin  = PeripheralWindow()
        self.periWin.layout_PeripheralWindow(self.notebook)

        # 오른쪽 프레임 생성
        right_frame = ttk.Frame(root)
        right_frame.grid(row=1, column=1, sticky="ns")

        # 버튼 추가
        button = ttk.Button(right_frame, text="Open Log", command=self.open_log)
        button.pack(padx=10, pady=10, anchor="ne")

        # 버튼 추가
        button = ttk.Button(right_frame, text="Button2")
        button.pack(padx=10, pady=10, anchor="ne")

        # log object creation for log analysis 
        self.log = Log()


    def on_vertical_scroll(self, *args):
        print(f"Scrolled to: {args}")


    def open_log(self):
        # 파일 선택 대화 상자 열기
        file_path = filedialog.askopenfilename()

        if file_path:

            self.logwin.layout_LogWindow(self.root, LOGWIN_DIMENSION)

            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    
                    self.logwin.log_text.insert(tk.END, content)

                    self.log.load_log(file_path, use_columns_log)
                    self.log.add_columns()
                    self.log.analyze_log ()
                    filtered_df = self.log.filter_event()
                    self.eventWin.update_EventWindow(filtered_df)
                    filtered_df = self.log.filter_event("S/W version")
                    self.infoWin.update_InfoWindow(filtered_df)

            except Exception as e:
                self.logwin.log_text.insert(tk.END, f"Failed to read file:\n{e}")


            file_path_keyevent = replace_filename(file_path, 'KeyBoardShadow_1.txt')
            self.keyeventwin.layout_KeyEventWindow(self.root, KEYEVENTWIN_DIMENSION)
            try:
                with open(file_path_keyevent, 'r') as file:
                    content = file.read()
                    self.keyeventwin.keyevent_text.insert(tk.END, content)
            except Exception as e:
                self.keyeventwin.keyevent_text.insert(tk.END, f"Failed to read file:\n{e}")


            file_path_device = replace_filename(file_path, 'Devices_1.txt')
            try:
                with open(file_path_device, 'r') as file:
                    self.log.load_device(file_path_device, use_columns_device)
                    self.periWin.update_PeripheralWindow(self.log.df_device)
            except Exception as e:
                print(f"Failed to read file:\n{e}")


        # 포커스 및 이벤트 관리
        self.root.bind_all("<FocusIn>", self.on_focus_in)
        
    def on_focus_in(self, event):
        # 포커스 변경 시 처리할 로직
        if self.logwin.log_text == self.root.focus_get():
            print("Log window is focused")
        elif self.keyeventwin.keyevent_text == self.root.focus_get():
            print("KeyEvent window is focused")
        elif self.eventWin.tree == self.root.focus_get():
            print("Event window is focused")
        elif self.infoWin.text == self.root.focus_get():
            print("infoWin window is focused")
        elif self.periWin.tree == self.root.focus_get():
            print("periWin window is focused")
        else: 
            print("other window is focused")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
