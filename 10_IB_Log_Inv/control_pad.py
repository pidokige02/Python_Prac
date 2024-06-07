import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from configure_data import *
from Utils import *
from configure_data import *



class ControlPad:

    def __init__(self, app):
        self.app = app
        self.right_frame = None
        self.openlog_button = None 
        self.button = None
        # self.checkbuttons = []
        # self.checkbox_vars = []


    def layout_ControlPad(self):

        # 오른쪽 프레임 생성
        self.right_frame = ttk.Frame(self.app.root)
        self.right_frame.grid(row=1, column=1, sticky="ns")

        # openlog 버튼 추가
        self.openlog_button = ttk.Button(self.right_frame, text="Open Log", command=self.open_log)
        self.openlog_button.pack(padx=10, pady=10, anchor="ne")

        # 버튼 추가
        self.button = ttk.Button(self.right_frame, text="Filter", command=self.open_log)
        self.button.pack(padx=10, pady=10, anchor="ne")

        # # Checkbuttons 추가
        # for option, (pattern, is_active, info_idx) in evant_table_map.items():
        #     if is_active:  # is_active가 True인 항목만 추가
        #         var = tk.BooleanVar(value=is_active)
        #         chk = ttk.Checkbutton(self.right_frame, text=option, variable=var)
        #         chk.pack(padx=10, pady=2, anchor="ne")
        #         self.checkbuttons.append(chk)
        #         self.checkbox_vars.append(var)


    def open_log(self):
        # 파일 선택 대화 상자 열기
        file_path = filedialog.askopenfilename()

        if file_path:

            self.app.logwin.layout_LogWindow(self.app.root, LOGWIN_DIMENSION)

            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    
                    self.app.logwin.log_text.insert(tk.END, content)

                    self.app.log.load_log(file_path, use_columns_log)
                    self.app.log.add_columns()
                    self.app.log.analyze_log ()
                    filtered_df = self.app.log.filter_event()
                    self.app.eventWin.update_EventWindow(filtered_df)
                    filtered_df = self.app.log.filter_event("S/W version")
                    self.app.infoWin.update_InfoWindow(filtered_df)

            except Exception as e:
                self.app.logwin.log_text.insert(tk.END, f"Failed to read file:\n{e}")


            file_path_keyevent = replace_filename(file_path, 'KeyBoardShadow_1.txt')
            self.app.keyeventwin.layout_KeyEventWindow(self.app.root, KEYEVENTWIN_DIMENSION)
            try:
                with open(file_path_keyevent, 'r') as file:
                    content = file.read()
                    self.app.keyeventwin.keyevent_text.insert(tk.END, content)
            except Exception as e:
                self.app.keyeventwin.keyevent_text.insert(tk.END, f"Failed to read file:\n{e}")


            file_path_device = replace_filename(file_path, 'Devices_1.txt')
            try:
                with open(file_path_device, 'r') as file:
                    self.app.log.load_device(file_path_device, use_columns_device)
                    self.app.periWin.update_PeripheralWindow(self.app.log.df_device)
            except Exception as e:
                print(f"Failed to read file:\n{e}")


        # 포커스 및 이벤트 관리
        self.app.root.bind_all("<FocusIn>", self.app.on_focus_in)


    def filter_log(self):
        # Checkbutton의 상태를 읽어 evant_table_map의 활성 상태 업데이트
        # for option, var in zip(evant_table_map.keys(), self.checkbox_vars):
        #     evant_table_map[option][1] = var.get()
        print("JINHA")