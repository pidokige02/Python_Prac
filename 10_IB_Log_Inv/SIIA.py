import tkinter as tk
from tkinter import ttk
import datetime

from Util.Utils import *
from Util.monitor import *
from event_win import *
from info_win import *
from peripheral_win import *
from log_win import *
from keyevent_win import *
from overview_win import *
from log import *
from configure_data import *
from control_pad import *
import build_info  # 빌드 타임스탬프를 포함한 파일


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Issue Inv Assistent")
        monitor_info = get_monitors()
        largest_monitor = choose_bigger_monitor(monitor_info)
        x, y, width, height = largest_monitor
        print("MONITOR_DIMENSION", f"{width}x{height}+{x}+{y}")

        # height/4의 결과를 정수로 변환
        MAINWIN_DIMENSION = f"{width}x{int(height*0.25)}+{x}+{y}"        
        print("MAINWIN_DIMENSION", MAINWIN_DIMENSION)
        self.root.geometry(MAINWIN_DIMENSION)  # 윈도우 크기를  가장 큰 window 에 맞추어서 설정 height 는 window 의 1/4 로

        # Grid 레이아웃 설정
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        # 스타일 설정
        style = ttk.Style()
        style.configure("Blue.TLabel", foreground="blue", font=("Helvetica", 16, "bold"))

        # 제목 라벨
        title_label = ttk.Label(root, text=f"Issue Inv Assistant (ver 1) build {build_info.BUILD_TIMESTAMP}", style="Blue.TLabel")           
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Notebook 생성
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=0, sticky="nsew")

        # control pad 생성
        self.controlpad = ControlPad(self)
        self.controlpad.layout_ControlPad()

        #log window creation
        self.logwin = LogWindow()
        self.keyeventwin =  KeyEventWindow ()
        LOGWIN_DIMENSION = None
        KEYEVENTWIN_DIMENSION = None

        if self.controlpad.enable_keylog_value.get():
            LOGWIN_DIMENSION = f"{int(width*0.75)}x{int(height*0.65)}+{x}+{y+int(height*0.3)}"        
            print("LOGWIN_DIMENSION", LOGWIN_DIMENSION)
            self.logwin.layout_LogWindow(self.notebook, LOGWIN_DIMENSION)

            # keyevent window creation
            KEYEVENTWIN_DIMENSION = f"{int(width*0.25)}x{int(height*0.65)}+{x + int(width*0.75)}+{y+int(height*0.3)}"        
            print("KEYEVENTWIN_DIMENSION", KEYEVENTWIN_DIMENSION)
            self.keyeventwin.layout_KeyEventWindow(self.notebook, KEYEVENTWIN_DIMENSION)
        else:
            LOGWIN_DIMENSION = f"{int(width)}x{int(height*0.65)}+{x}+{y+int(height*0.3)}"        
            print("LOGWIN_DIMENSION", LOGWIN_DIMENSION)
            self.logwin.layout_LogWindow(self.notebook, LOGWIN_DIMENSION)

        # for mutual data exchange
        self.logwin.set_keyevent_window(self.keyeventwin)
        self.keyeventwin.set_log_window(self.logwin)

        # # 첫 번째 Pane EventWindow 생성
        self.eventWin = EventWindow(self.logwin, self.keyeventwin)
        self.eventWin.layout_EventWindow(self.notebook)

        # 두 번째 Pane OverviewWindow 생성
        self.overviewWin = OverviewWindow()   
        self.overviewWin.layout_Overview_Window(self.notebook)
        self.overviewWin.set_keyevent_window(self.keyeventwin)
        self.overviewWin.set_log_window(self.logwin)


        # 세 번째 Pane InfoWindow 생성
        self.infoWin = InfoWindow()
        self.infoWin.layout_InfoWindow(self.notebook)

        # 네 번째 Pane peripheral_win 생성
        self.periWin  = PeripheralWindow()
        self.periWin.layout_PeripheralWindow(self.notebook)

        # log object creation for log analysis
        self.log = Log()
        self.logwin.set_log_instance (self.log)
        self.overviewWin.set_log_instance(self.log)

        # # 포커스 및 이벤트 관리
        self.root.bind_all("<FocusIn>", self.on_focus_in)
        # main window 에 focus 가 오면 log window 와 key log window 도 같이 activate 되도록 함.

        # Bind Unmap and Map events to handle minimize and restore
        self.root.bind("<Unmap>", self.on_minimize)
        self.root.bind("<Map>", self.on_restore)


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


    def on_minimize(self, event):
        if str(event.widget) == str(self.root):
            self.logwin.log_window.withdraw()
            if self.keyeventwin.keyevent_window:
                self.keyeventwin.keyevent_window.withdraw()

    def on_restore(self, event):
        if str(event.widget) == str(self.root):
            self.logwin.log_window.deiconify()
            if self.keyeventwin.keyevent_window: 
                self.keyeventwin.keyevent_window.deiconify() 


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
