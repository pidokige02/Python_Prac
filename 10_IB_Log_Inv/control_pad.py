import os
import subprocess
import shlex
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from Util.Utils import *
from Util.monitor import *
from configure_data import *
from tkinter import messagebox
from dialog.keylog_player import *



class ControlPad:

    def __init__(self, app):
        self.app = app
        self.right_frame = None
        self.openlog_button = None
        self.savekeyevent_button = None
        self.reset_timestamp_button = None
        self.timestamp_from = None
        self.timestamp_to = None
        self.file_path_keyevent = []
        self.file_path_mainevent = []
        self.keylog_playback_button = None
        self.last_opened_crash_files = []

        self.keylogplayer = KeylogPlayer(self.app.root)


    def layout_ControlPad(self):

        # 오른쪽 프레임 생성
        self.right_frame = ttk.Frame(self.app.root)
        self.right_frame.grid(row=1, column=1, sticky="ns")

        # openlog 버튼 추가
        self.openlog_button = ttk.Button(self.right_frame, text="Open Log", command=self.open_log)
        self.openlog_button.grid(row=0, column=0, padx=1, pady=1, sticky="w")

        # # playback 버튼 추가
        self.keylog_playback_button = ttk.Button(self.right_frame, text="Play Log", command=self.keylog_playback)
        self.keylog_playback_button.grid(row=0, column=1, padx=1, pady=1, sticky="w")

        # Save Key Event 버튼 추가
        self.savekeyevent_button = ttk.Button(self.right_frame, text="Save Log", command=self.save_keyevent_log)
        self.savekeyevent_button.grid(row=1, column=0, padx=1, pady=1, sticky="w")

        # Save Key Event 버튼 추가
        self.reset_timestamp_button = ttk.Button(self.right_frame, text="Reset Time", command=self.reset_timestamp)
        self.reset_timestamp_button.grid(row=1, column=1, padx=1, pady=1, sticky="w")

        ttk.Label(self.right_frame, text="From").grid(row=2, column=0, padx=1, pady=1, sticky="w")
        self.timestamp_from = ttk.Entry(self.right_frame)
        self.timestamp_from.grid(row=3, column=0, padx=1, pady=1, sticky="w")

        ttk.Label(self.right_frame, text="To").grid(row=2, column=1, padx=1, pady=1, sticky="w")
        self.timestamp_to = ttk.Entry(self.right_frame)
        self.timestamp_to.grid(row=3, column=1, padx=1, pady=1, sticky="w")

        # Checkbox 추가
        self.enable_keylog_value = tk.BooleanVar(value=False)
        self.checkbox = ttk.Checkbutton(self.right_frame, text="Enable KBlog", variable=self.enable_keylog_value)
        self.checkbox.grid(row=4, column=0, padx=1, pady=1, sticky="w")

        # # Callback to update label text when checkbox value changes
        self.enable_keylog_value.trace_add("write", self.update_log_window_dimension)


    def update_log_window_dimension(self, *args):

        monitor_info = get_monitors()
        largest_monitor = choose_bigger_monitor(monitor_info)
        x, y, width, height = largest_monitor

        if self.enable_keylog_value.get():
            LOGWIN_DIMENSION = f"{int(width*0.75)}x{int(height*0.65)}+{x}+{y+int(height*0.3)}"        
            self.app.logwin.resize_LogWindow(LOGWIN_DIMENSION)
            KEYEVENTWIN_DIMENSION = f"{int(width*0.25)}x{int(height*0.65)}+{x + int(width*0.75)}+{y+int(height*0.3)}"        
            if not self.app.keyeventwin.keyevent_window:
                self.app.keyeventwin.layout_KeyEventWindow(self.app.notebook, KEYEVENTWIN_DIMENSION)
            else:
                self.app.keyeventwin.resize_KeyEventWindow(KEYEVENTWIN_DIMENSION)
        else:
            LOGWIN_DIMENSION = f"{int(width)}x{int(height*0.65)}+{x}+{y+int(height*0.3)}"        
            print("LOGWIN_DIMENSION", LOGWIN_DIMENSION)
            self.app.logwin.resize_LogWindow(LOGWIN_DIMENSION)
            self.clear_keyeventlog()
            if self.app.keyeventwin.keyevent_window: 
                self.app.keyeventwin.keyevent_window.destroy()
                self.app.keyeventwin.keyevent_window = None


    def clear_eventlog(self):
        self.app.log.clear_eventdata()
        if self.app.keyeventwin.keyevent_window:
            self.app.keyeventwin.clear_highlight()
        self.app.logwin.log_text.config(state=tk.NORMAL)
        self.app.logwin.log_text.delete('1.0', tk.END)
        self.app.logwin.log_text.config(state=tk.DISABLED)


    def clear_keyeventlog(self):
        self.app.log.clear_keyeventdata()
        if self.app.keyeventwin.keyevent_window:
            self.app.keyeventwin.keyevent_text.config(state=tk.NORMAL)
            self.app.keyeventwin.keyevent_text.delete('1.0', tk.END)
            self.app.keyeventwin.keyevent_text.config(state=tk.DISABLED)
            self.app.keyeventwin.last_opened_keyevent_files = []


    def clear_devicelog(self):
        self.app.log.clear_devicedata()
        

    def  clear_crashlog(self):
        self.app.log.clear_crashdata()


    def  clear_overviewlog(self):
        self.app.log.clear_overviewdata()


    def open_mainlog(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*MainLog*.txt")]
        )

        if not file_path:
            print("No file selected or an unknown error occurred.")
            return None


        # 로그 파일 다시 열기 방지
        if self.app.logwin.last_opened_mainevent_files is not None and file_path in self.app.logwin.last_opened_mainevent_files:
            print("Same log files are already open.")
            return file_path

        # below code is commented, As only selected file will be read
        # self.file_path_mainevent = self.sort_filename_order_by_timestamp(file_path, '*MainLog*')
        self.file_path_mainevent = [file_path]

        file_name = os.path.basename(file_path)

        last_exception = None  # last_exception 변수를 초기화

        # 다양한 인코딩 시도
        encodings = ['latin1', 'utf-8', 'cp949']

        file_contents = []

        for idx, file_path in enumerate(self.file_path_mainevent):
            content = None
            for enc in encodings:
                try:
                    with open(file_path, 'r', encoding=enc) as file:
                        lines = file.readlines()

                        if idx >= 1:
                            content = "".join(lines[2:-1]).rstrip("\n")  # 두 번째 및 그 이후 파일에 대해 처음 두 줄과 마지막 한 줄 건너뛰기, line을 모두 합친다음 다지막 개항문제를 제거
                        else:
                            content = "".join(lines[:-1]).rstrip("\n") # 첫 번째 파일에 대해 마지막 한 줄 건너뛰기,line을 모두 합친다음 다지막 개항문제를 제거

                        file_contents.append(content)
                        break
                except Exception as e:
                    last_exception = e

        if file_contents:
            try:
                self.clear_eventlog()
                combined_content = "\n".join(file_contents)
                self.app.logwin.log_text.config(state=tk.NORMAL)
                self.app.logwin.log_text.insert(tk.END, combined_content)
                self.app.logwin.log_text.config(state=tk.DISABLED)

                self.app.log.load_log(self.file_path_mainevent, use_columns_log)
                self.app.log.add_columns_log()
                self.app.log.analyze_log ()
                df_filtered = self.app.log.filter_event()
                self.app.eventWin.update_EventWindow(df_filtered)
                df_filtered = self.app.log.filter_event(events=['S/W version', 'Product'])
                self.app.infoWin.update_InfoWindow(df_filtered)
                self.app.logwin.log_window.title(file_name)  # filename is displayed on the title
                self.app.logwin.last_opened_mainevent_files = self.file_path_mainevent
                return file_path
            except Exception as e:
                print("Failed to read file:\n{e}")
                self.app.logwin.last_opened_mainevent_files = []
                return None
        else:
            print("No Contents. Last exception was:", last_exception)
            self.app.logwin.last_opened_mainevent_files = []
            return None


    def sort_filename_order_by_timestamp(self, file_path, pattern):

        directory_path = get_directory_name(file_path)

        file_paths = find_files(directory_path, pattern)

        encodings = ['latin1', 'utf-8', 'cp949']
        last_exception = None
        sorted_file_paths = []

        for idx, file_path in enumerate(file_paths):

            content = []
            for enc in encodings:
                try:
                    with open(file_path, 'r', encoding=enc) as file:
                        for _ in range(3):  # 처음 3줄만 읽기
                            line = file.readline()
                            if line:
                                content.append(line.strip())
                            else:
                                break

                        # 'Timestamp'가 첫 번째 라인에 있는지 확인
                        header = content[0].split('\t')
                        if 'Timestamp' not in header:
                            print(f"No 'Timestamp' found in the first line of {file_path}. Skipping this file.")
                            break

                        # Timestamp의 인덱스를 찾음
                        timestamp_index = header.index('Timestamp')

                        # 세 번째 라인에서 타임스탬프를 추출
                        timestamp = content[2].split('\t')[timestamp_index]
                        sorted_file_paths.append((timestamp, file_path))
                        break
                except Exception as e:
                    last_exception = e
                    print(f"Failed to read keyevent file:\n{last_exception}")

        # 타임스탬프를 기준으로 파일 경로들을 정렬
        sorted_file_paths.sort()
        return [file_path for _, file_path in sorted_file_paths]


    def open_KB_log(self, file_path):

        self.file_path_keyevent = self.sort_filename_order_by_timestamp(file_path, '*KeyBoardShadow*')

        encodings = ['latin1', 'utf-8', 'cp949']
        last_exception = None

        if self.file_path_keyevent == self.app.keyeventwin.last_opened_keyevent_files:
            print("Same keyevent files are already open.")
            df_filtered = self.app.log.filter_event()  # filter out normal event table
            df_filtered = self.app.log.analyze_keyevent(df_filtered)
            self.app.eventWin.update_EventWindow(df_filtered)
            return

        file_contents = []

        for idx, file_path in enumerate(self.file_path_keyevent):
            content = None
            for enc in encodings:
                try:
                    with open(file_path, 'r', encoding=enc) as file:
                        lines = file.readlines()

                        if idx >= 1:
                            content = "".join(lines[2:-1]).rstrip("\n")  # 두 번째 및 그 이후 파일에 대해 처음 두 줄과 마지막 한 줄 건너뛰기, line을 모두 합친다음 다지막 개항문제를 제거
                        else:
                            content = "".join(lines[:-1]).rstrip("\n") # 첫 번째 파일에 대해 마지막 한 줄 건너뛰기,line을 모두 합친다음 다지막 개항문제를 제거

                        file_contents.append(content)
                        break
                except Exception as e:
                    last_exception = e

        if file_contents:
            self.clear_keyeventlog()
            combined_content = "\n".join(file_contents)
            if self.app.keyeventwin.keyevent_window:
                self.app.keyeventwin.keyevent_text.config(state=tk.NORMAL)
                self.app.keyeventwin.keyevent_text.insert(tk.END, combined_content)
                self.app.keyeventwin.keyevent_text.config(state=tk.DISABLED)
            try:
                if self.app.keyeventwin.keyevent_window:                
                    self.app.keyeventwin.keyevent_window.iconify()
                self.app.log.load_keyevent_log(self.file_path_keyevent, use_columns_keyevent)
                self.app.log.add_columns_keyevent()
                df_filtered = self.app.log.filter_event()  # filter out normal event table
                df_filtered = self.app.log.analyze_keyevent(df_filtered)
                self.app.eventWin.update_EventWindow(df_filtered)
                if self.app.keyeventwin.keyevent_window:                
                    self.app.keyeventwin.last_opened_keyevent_files = self.file_path_keyevent
                    self.app.keyeventwin.keyevent_window.deiconify()
            except Exception as e:
                last_exception = e
                if self.app.keyeventwin.keyevent_window:                
                    self.app.keyeventwin.last_opened_keyevent_files = []
                self.file_path_keyevent = []
                print(f"Failed to read keyevent file:\n{last_exception}")



    def open_device_log(self, file_path):

        file_path_device = replace_filename(file_path, 'Devices_1.txt')
        if file_path_device == self.app.periWin.last_opened_device_file:
            print("Same device file is already open.")
        else:
            try:
                self.clear_devicelog()
                self.app.log.load_device(file_path_device, use_columns_device)
                self.app.periWin.update_PeripheralWindow(self.app.log.df_device)
                self.app.periWin.last_opened_device_file = file_path_device
            except Exception as e:
                last_exception = e
                self.app.periWin.last_opened_device_file = None
                print(f"Failed to read device file:\n{last_exception}")


    def open_log(self):

        file_path = self.open_mainlog()

        if not file_path:
            print("open_mainlog failed.")
            return None
    
        if  self.enable_keylog_value.get():
            self.open_KB_log(file_path)

        self.open_device_log(file_path)

        self.open_crash_log(file_path)

        self.open_overview_log(file_path)

        self.app.keyeventwin.last_opened_keyevent_files = self.file_path_keyevent
        self.reset_timestamp()



    def save_keyevent_log(self):

        try:
            timestamp_from_value = self.timestamp_from.get()
            timestamp_to_value = self.timestamp_to.get()

            # 문자열을 datetime 객체로 변환
            timestamp_from_dt = extract_timestamp(timestamp_from_value)
            timestamp_to_dt = extract_timestamp(timestamp_to_value)

            # 타임스탬프 유효성 검사
            if pd.isna(timestamp_from_dt) or pd.isna(timestamp_to_dt):
                raise ValueError("One or both timestamps are invalid")

            from_lines = self.app.keyeventwin.get_matching_lines(timestamp_from_value)
            to_lines = self.app.keyeventwin.get_matching_lines(timestamp_to_value)
            
            if len(from_lines) == 0 or len(to_lines) == 0:
                raise ValueError("from_lines or to_lines are invalid")

            from_line_number = int(from_lines[0])  # 첫 번째 라인의 번호
            to_line_number = int(to_lines[-1])     # 마지막 라인의 번호

            # 저장할 라인들을 담을 리스트를 초기화합니다.
            lines_to_save = []
            keyevent_text_widget = self.app.keyeventwin.keyevent_text

            # from_line_number부터 to_line_number까지의 라인을 추출하여 리스트에 저장합니다.
            for line_number in range(from_line_number, to_line_number + 1):
                line = keyevent_text_widget.get(f"{line_number}.0", f"{line_number}.end")
                lines_to_save.append(line)

            # get initial file name
            file_path_keyevent_dest = replace_filename(self.file_path_keyevent[0], 'KeyBoardShadow_1_captured.txt')

             # 파일 저장 대화 상자를 열고 파일 경로를 가져옴
            file_path_keyevent_dest = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile="KeyBoardShadow_1_captured.txt"
            )

            if file_path_keyevent_dest and os.path.isdir(os.path.dirname(file_path_keyevent_dest)):
                with open(file_path_keyevent_dest, 'w', encoding='utf-8') as file:
                    for line in lines_to_save:
                        file.write(line + '\n')
                print(f"파일이 성공적으로 저장되었습니다: {file_path_keyevent_dest}")

            else:
                print("Invalid file path selected.")

        except ValueError as e:
            print("Invalid timestamp format:", e)
            messagebox.showerror("Error", f"Invalid timestamp format: {e}")



    def reset_timestamp(self):
        self.timestamp_from.delete(0, tk.END)
        self.timestamp_to.delete(0, tk.END)


    def keylog_playback(self):

        file_path = filedialog.askopenfilename(
        title="Select a KeyBoardShadow log file",
        filetypes=[("Log Files", "*KeyBoardShadow*")])

        if not file_path:  # 파일이 선택되지 않으면 함수 종료
            print("No file is selected")
            return

        file_name = os.path.basename(file_path)
        if "KeyBoardShadow" not in file_name:
            messagebox.showerror("Invalid File", "The selected file does not contain 'KeyBoardShadow' in its name.")
            return        

         # 파일 이름만 추출
        default_ip_address="127.0.0.1"
        default_option="-c 1 -m 2"
        default_command=f"playback.exe -i {file_name} -t {default_ip_address} {default_option}"
        command = self.keylogplayer.show_input_dialog(
            self.right_frame,
            default_command
        )

        if command is None:
            return
        
        # 파일 경로에 큰따옴표 추가하여 명령어 생성
        quoted_file_path = shlex.quote(file_path)        
        final_command = command.replace(f"{file_name}", quoted_file_path)

        print("Jinha", final_command)    
        subprocess.Popen(['start', 'cmd', '/k', final_command], shell=True)


    def open_crash_log(self, file_path):
        # Get the directory name of the provided file path
        directory_path = get_directory_name(file_path)

        # Get the parent directory of the directory path
        parent_directory_path = os.path.dirname(directory_path)

        # Define the CrashDump directory path
        crash_dump_directory_path = os.path.join(parent_directory_path, 'CrashDump')

        pattern = '*CrashDump*'

        file_paths_crash = find_files(crash_dump_directory_path, pattern)

        if file_paths_crash:  
            crash_files_with_timestamps = []
            for file_path in file_paths_crash:
                file_name = os.path.basename(file_path)
                timestamp = extract_timestamp_string_from_filename(file_name)
                if timestamp:
                    crash_files_with_timestamps.append((file_path, timestamp))

            file_paths_crash = [ft[0] for ft in crash_files_with_timestamps]
            timestamps = [ft[1] for ft in crash_files_with_timestamps]

            if file_paths_crash == self.last_opened_crash_files:
                print("Same crash file is already open.")
            else:
                try:
                    self.clear_crashlog()
                    self.app.log.load_crashdata(file_paths_crash, timestamps)
                    self.last_opened_crash_files = file_paths_crash
                except Exception as e:
                    last_exception = e
                    self.last_opened_crash_files = None
                    self.clear_crashlog()
                    print(f"Failed to read crash file:\n{last_exception}")
        else:
            print("No crash file.")
            self.clear_crashlog()
            self.last_opened_crash_files = None


    def open_overview_log(self, file_path):

        file_path_mainlog = self.sort_filename_order_by_timestamp(file_path, '*MainLog*')
        
        if self.app.overviewWin.last_opened_main_log == file_path_mainlog: 
            print("Same overview_log is already open.")
        else:
            self.clear_overviewlog()    
            self.app.log.load_overview(file_path_mainlog)
            self.app.overviewWin.update_Overview_Window(self.app.log.file_timestamp_mapping)

            self.app.overviewWin.last_opened_main_log = file_path_mainlog 

