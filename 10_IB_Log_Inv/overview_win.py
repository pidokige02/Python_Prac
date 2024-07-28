import os
import tkinter as tk
from tkinter import ttk
from configure_data import *
from datetime import datetime
from Util.Utils import *


class OverviewWindow:
    def __init__(self):
        self.pane1 = None
        self.tree = None 

        self.log_window = None          # mutual 참조룰 위함
        self.keyevent_window = None     # mutual 참조룰 위함
        self.log_instance = None


    def layout_Overview_Window(self, root):
        self.pane1 = ttk.Frame(root)
        root.add(self.pane1, text='Overview')

        # Treeview 생성
        self.tree = ttk.Treeview(self.pane1, columns=treeview_index, show='headings')  # panel 을 parent 로 하여 TreeView 를 만든다.

        for col_name, col_text, col_witdh  in overview_columns:
            self.tree.heading(col_name, text=col_text) # 각 열의 제목 설정
            self.tree.column(col_name, width=col_witdh)  # 열의 너비를 설정 (옵션)

        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(self.pane1, orient="vertical", command=self.tree.yview) # scroll bar 도 panel 을 parent 로 만든다.
        self.tree.configure(yscroll=scrollbar.set)

        # Treeview와 스크롤바를 grid로 배치
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # grid 레이아웃을 사용하여 크기 조정
        self.pane1.grid_rowconfigure(0, weight=1)
        self.pane1.grid_columnconfigure(0, weight=1)
        
        # TreeviewSelect 이벤트 바인딩
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Ctrl+C 키 이벤트 바인딩
        self.tree.bind("<Control-c>", self.on_copy)


    def set_keyevent_window (self, key_log_win):
        self.keyevent_window = key_log_win


    def set_log_window (self, log_win):
        self.log_window = log_win


    def set_log_instance (self, log):
        self.log_instance = log


    def update_Overview_Window (self, file_timestamp_mapping):

        # 기존 데이터를 모두 제거
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Dictionary to keep track of files without crash events
        displayed_files = {}

        # Iterate over the file_timestamp_mapping list and insert each record into the Treeview
        for data in file_timestamp_mapping:
            file_path = data.get('file_path', '')
            from_timestamp = data.get('from_timestamp', '')
            to_timestamp = data.get('to_timestamp', '')
            crash_timestamp = data.get('crash_timestamp', '')
            crash_event = data.get('Crash', '')

            
            # get file_name from file_path
            if file_path:
               file_name = os.path.basename(file_path)    
            # Format the timestamps
            if from_timestamp:
                from_timestamp = from_timestamp.strftime('%Y-%m-%d %H:%M:%S')
            if to_timestamp:
                to_timestamp = to_timestamp.strftime('%Y-%m-%d %H:%M:%S')
            if crash_timestamp:
                crash_timestamp = crash_timestamp.strftime('%Y-%m-%d %H:%M:%S')

            # Find the start of the module information
            module_start_index = crash_event.find('in module')
            
            if module_start_index != -1:
                # Extract the substring starting from 'in module'
                module_info = crash_event[module_start_index:].strip()
            else:
                module_info = crash_event

            # Insert the row into the Treeview if there is a crash event
            if crash_event:
                self.tree.insert("", tk.END, values=(file_name, from_timestamp, to_timestamp, module_info, crash_timestamp))
                displayed_files[file_name] = True
            else:
                # If there is no crash event, check if the file has already been displayed
                if file_name not in displayed_files:
                    self.tree.insert("", tk.END, values=(file_name, from_timestamp, to_timestamp, crash_event, crash_timestamp))
                    displayed_files[file_name] = True


    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']

            if len(values) > 4 and values[4]:  # crash_timestamp이 리스트에 있는지 및 값이 있는지 확인
                crash_timestamp = values[4]  # crash_timestamp이 Treeview의 5번째 열에 있다고 가정
                self.find_closest_events(crash_timestamp)
            else:
                print("crash_timestamp is not available or empty")


    def find_closest_events(self, crash_timestamp_str):

        crash_timestam = extract_simpler_timestamp(crash_timestamp_str)

        is_timestamp_within_range = self.log_instance.check_specific_crash_timestamp(crash_timestam, self.log_window.last_opened_mainevent_files[0])

        if is_timestamp_within_range :
            keyevent_index = self.log_instance.locate_keyevent(crash_timestamp_str)
            if keyevent_index is not None:  # line_index가 None이 아닌지 확인
                self.keyevent_window.scroll_to_line(keyevent_index)
            else:
                print ("keyevent_index not valid")
                
            logevent_index = self.log_instance.locate_logevent(crash_timestamp_str)
            if logevent_index is not None:  # line_index가 None이 아닌지 확인
                self.log_window.scroll_to_line(logevent_index)
            else:
                print ("logevent_index not valid")

        else:
            print("No valid timestamp found")


    def on_copy(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            clipboard_data = "\t".join(str(v) for v in values)
            self.copy_to_clipboard(clipboard_data)


    def copy_to_clipboard(self, text):
        root = self.pane1.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # 클립보드에 복사된 내용을 업데이트

    
