import tkinter as tk
from tkinter import font
from Util.Utils import *


class CrashWindow:
    def __init__(self):
        self.crash_window = None
        self.current_font_size = 10     # 기본 폰트 크기
        self.text_font = None
        self.crash_text = None

        self.log_window = None          # mutual 참조룰 위함
        self.keyevent_window = None     # mutual 참조룰 위함
        self.event_pane_window = None          # mutual 참조룰 위함

        self.log_instance = None
        self.timestamp_list = []        # List to store timestamps string


    def set_event_pane (self, event_pane):
        self.event_pane_window = event_pane


    def set_keyevent_window (self, key_log_win):
        self.keyevent_window = key_log_win


    def set_log_window (self, log_win):
        self.log_window = log_win


    def set_log_instance (self, log):
        self.log_instance = log


    def layout_CrashWindow(self, root, dimension):

        self.crash_window = tk.Toplevel(root)
        self.crash_window.title("crash")
        self.crash_window.geometry(dimension)
        
        # 닫기 버튼 비활성화
        self.crash_window.protocol("WM_DELETE_WINDOW", self.disable_close_button)

        # 창을 항상 최상위로 설정
        self.crash_window.attributes("-topmost", True)        

        frame = tk.Frame(self.crash_window)
        frame.pack(expand=True, fill='both')

         # 텍스트 위젯  wrap='none' 은 line 이 긴 경우에 다음줄로 넘기지 않는다
        self.crash_text = tk.Text(frame, wrap='none')
        self.crash_text.grid(row=0, column=0, sticky="nsew")

        # 기본 폰트 설정
        self.text_font = font.Font(family="Helvetica", size=self.current_font_size)
        self.crash_text.configure(font=self.text_font)

        # 수직 스크롤 막대
        vscroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=lambda *args: self.on_vertical_scroll(*args) or self.crash_text.yview(*args))
        vscroll.grid(row=0, column=1, sticky="ns")
        self.crash_text.config(yscrollcommand=vscroll.set)

        # 수평 스크롤 막대
        hscroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.crash_text.xview)
        hscroll.grid(row=1, column=0, sticky="ew")
        self.crash_text.config(xscrollcommand=hscroll.set)

        # 프레임 크기 조정
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

         # 마우스 휠 이벤트 바인딩
        self.crash_text.bind("<Control-MouseWheel>", self.on_mouse_wheel)

        # Bind click event
        self.crash_text.bind("<Button-1>", self.on_click)
        self.crash_text.tag_configure("highlight", background="yellow")


    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.current_font_size += 1  # 폰트 크기 증가
        else:
            self.current_font_size -= 1  # 폰트 크기 감소
        self.text_font.configure(size=self.current_font_size)
        self.crash_text.configure(font=self.text_font)


    def on_vertical_scroll(self, *args):
        self.log_text.yview(*args)


    def disable_close_button(self):
        pass  # 아무 동작도 하지 않음


    def on_click(self, event):
        # Get the line number where the click occurred
        line_index = int(self.crash_text.index(f"@{event.x},{event.y}").split('.')[0]) - 1

        print("line_index", line_index)

        # Initialize timestamp_str with a default value
        timestamp_str = None

        # Get the timestamp for the selected line
        if 0 <= line_index < len(self.timestamp_list):
            timestamp_str = self.timestamp_list[line_index]
            print("Timestamp:", timestamp_str)
        else:
            print("Invalid line index")

        if timestamp_str is not None:
            print("on_click", timestamp_str)
            keyevent_index = self.log_instance.locate_keyevent(timestamp_str)
            if keyevent_index is not None:  # line_index가 None이 아닌지 확인
                self.keyevent_window.scroll_to_line(keyevent_index)
            else:
                print ("keyevent_index not valid")
                
            logevent_index = self.log_instance.locate_logevent(timestamp_str)
            if logevent_index is not None:  # line_index가 None이 아닌지 확인
                self.log_window.scroll_to_line(logevent_index)
            else:
                print ("logevent_index not valid")


        else:
            print("No valid timestamp found")

        # Remove previous highlights
        self.crash_text.tag_remove("highlight", "1.0", tk.END)

        # Highlight the selected line
        self.crash_text.tag_add("highlight", f"{line_index+1}.0", f"{line_index+1}.end")


    def update_crash_window(self, first_lines_with_timestamps):

        self.crash_text.config(state=tk.NORMAL)  # Allow text editing
        self.crash_text.delete("1.0", tk.END)    # Clear existing content
        self.timestamp_list = []  # Clear the previous timestamps
        
        for (file_name, timestamp), first_line in first_lines_with_timestamps.items():
            entry = f"{timestamp}\t : {first_line}\n"
            self.crash_text.insert(tk.END, entry)
            self.timestamp_list.append(timestamp)  # Store the timestamp
        
        self.crash_text.config(state=tk.DISABLED)  # Disable text editing        