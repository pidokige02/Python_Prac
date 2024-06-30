import tkinter as tk
from tkinter import ttk

from Utils import *
from event_win import *
from info_win import *
from peripheral_win import *
from log_win import *
from keyevent_win import *
from log import *
from configure_data import *
from control_pad import *


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
        self.logwin.layout_LogWindow(root, LOGWIN_DIMENSION)

        # keyevent window creation
        self.keyeventwin =  KeyEventWindow ()
        self.keyeventwin.layout_KeyEventWindow(root, KEYEVENTWIN_DIMENSION)

        # for mutual data exchange
        self.logwin.set_keyevent_window(self.keyeventwin)
        self.keyeventwin.set_log_window(self.logwin)


        # # 첫 번째 Pane EventWindow 생성
        self.eventWin = EventWindow(self.logwin, self.keyeventwin)
        self.eventWin.layout_EventWindow(self.notebook)

        # 두 번째 Pane InfoWindow 생성
        self.infoWin = InfoWindow()
        self.infoWin.layout_InfoWindow(self.notebook)

        # 세 번째 Pane peripheral_win 생성
        self.periWin  = PeripheralWindow()
        self.periWin.layout_PeripheralWindow(self.notebook)

        # control pad 생성
        self.controlpad = ControlPad(self)
        self.controlpad.layout_ControlPad()

        # log object creation for log analysis
        self.log = Log()
        self.logwin.set_log_instance (self.log)

        # # 포커스 및 이벤트 관리
        self.root.bind_all("<FocusIn>", self.on_focus_in)



    def on_vertical_scroll(self, *args):
        print(f"Scrolled to: {args}")


    def on_focus_in(self, event):
        # 포커스 변경 시 처리할 로직
        widget = self.root.focus_get()

        if self.logwin.log_text == widget:
            pass
            # print("Log window is focused", self.logwin.log_text)
        elif self.keyeventwin.keyevent_text == widget:
            pass
            # print("KeyEvent window is focused", self.keyeventwin.keyevent_text)
        elif self.eventWin.tree == widget:
            # print("Event window is focused", self.eventWin.tree)
            pass
        elif self.infoWin.text == widget:
            # print("infoWin window is focused", self.infoWin.text)
            pass
        elif self.periWin.tree == widget:
            # print("periWin window is focused", self.periWin.tree)
            pass
        else:
            # print("Other window is focused", widget, widget.winfo_name(), widget.winfo_class())
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
