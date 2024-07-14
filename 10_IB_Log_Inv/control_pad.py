import os
import subprocess
import shlex
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from Util.Utils import *
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
        self.keylog_playback_button = None
        self.last_opened_log_file = None
        self.last_opened_keyevent_file = []
        self.last_opened_device_file = None
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


    def clear_eventlog(self):
        self.app.log.clear_eventdata()
        self.app.logwin.log_text.config(state=tk.NORMAL)
        self.app.logwin.log_text.delete('1.0', tk.END)
        self.app.logwin.log_text.config(state=tk.DISABLED)


    def clear_keyeventlog(self):
        self.app.log.clear_keyeventdata()
        self.app.keyeventwin.keyevent_text.config(state=tk.NORMAL)
        self.app.keyeventwin.keyevent_text.delete('1.0', tk.END)
        self.app.keyeventwin.keyevent_text.config(state=tk.DISABLED)


    def clear_devicelog(self):
        self.app.log.clear_devicedata()


    def open_mainlog(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*MainLog*.txt")]
        )

        if not file_path:
            print("No file selected or an unknown error occurred.")
            return None

        # 로그 파일 다시 열기 방지
        if file_path == self.last_opened_log_file and self.last_opened_log_file is not None:
            print("Same log file is already open.")
            return None

        last_exception = None  # last_exception 변수를 초기화

        # 다양한 인코딩 시도
        encodings = ['latin1', 'utf-8', 'cp949']
        content = None
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as file:
                    content = file.read()
                break
            except Exception as e:
                last_exception = e

        if content:
            try:
                self.clear_eventlog()
                self.app.logwin.log_text.config(state=tk.NORMAL)
                self.app.logwin.log_text.insert(tk.END, content)
                self.app.logwin.log_text.config(state=tk.DISABLED)
                self.app.log.load_log(file_path, use_columns_log)
                self.app.log.add_columns_log()
                self.app.log.analyze_log ()
                filtered_df = self.app.log.filter_event()
                self.app.eventWin.update_EventWindow(filtered_df)
                filtered_df = self.app.log.filter_event(events=['S/W version', 'Product'])
                self.app.infoWin.update_InfoWindow(filtered_df)
                self.last_opened_log_file = file_path
                return file_path
            except Exception as e:
                print("Failed to read file:\n{e}")
                self.last_opened_log_file = None
                return None
        else:
            print("No Contents. Last exception was:", last_exception)
            self.last_opened_log_file = None
            return None


    def sort_filename_order_by_timestamp(self, file_path):

        directory_path = get_directory_name(file_path)
        pattern = '*KeyBoardShadow*'

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

                        if 'Timestamp' not in content[0]:
                            print(f"No 'Timestamp' found in the first line of {file_path}. Skipping this file.")
                            break                        # 유효한 파일로 추가

                        timestamp = content[2].split('\t')[0]
                        sorted_file_paths.append((timestamp, file_path))
                        break
                except Exception as e:
                    last_exception = e
                    print(f"Failed to read keyevent file:\n{last_exception}")

        # 타임스탬프를 기준으로 파일 경로들을 정렬
        sorted_file_paths.sort()
        return [file_path for _, file_path in sorted_file_paths]


    def open_KB_log(self, file_path):

        self.file_path_keyevent = self.sort_filename_order_by_timestamp(file_path)

        encodings = ['latin1', 'utf-8', 'cp949']
        last_exception = None

        if self.file_path_keyevent == self.last_opened_keyevent_file:
            print("Same keyevent files are already open.")
            filtered_df = self.app.log.filter_event()  # filter out normal event table
            filtered_df = self.app.log.analyze_keyevent(filtered_df)
            self.app.eventWin.update_EventWindow(filtered_df)
            return

        self.sort_filename_order_by_timestamp(file_path)

        file_contents = []

        for idx, file_path in enumerate(self.file_path_keyevent):
            content = None
            for enc in encodings:
                try:
                    with open(file_path, 'r', encoding=enc) as file:
                        lines = file.readlines()

                        if idx >= 1:
                            content = "".join(lines[2:-2]).rstrip("\n")  # 두 번째 및 그 이후 파일에 대해 처음 두 줄과 마지막 두 줄 건너뛰기, line을 모두 합친다음 다지막 개항문제를 제거
                        else:
                            content = "".join(lines[:-2]).rstrip("\n") # 첫 번째 파일에 대해 마지막 두 줄 건너뛰기,line을 모두 합친다음 다지막 개항문제를 제거

                        file_contents.append(content)
                        break
                except Exception as e:
                    last_exception = e

        if file_contents:
            self.clear_keyeventlog()
            combined_content = "\n".join(file_contents)
            self.app.keyeventwin.keyevent_text.config(state=tk.NORMAL)
            self.app.keyeventwin.keyevent_text.insert(tk.END, combined_content)
            self.app.keyeventwin.keyevent_text.config(state=tk.DISABLED)
            try:
                self.app.keyeventwin.keyevent_window.iconify()
                self.app.log.load_keyevent_log(self.file_path_keyevent, use_columns_keyevent)
                self.app.log.add_columns_keyevent()
                filtered_df = self.app.log.filter_event()  # filter out normal event table
                filtered_df = self.app.log.analyze_keyevent(filtered_df)
                self.app.eventWin.update_EventWindow(filtered_df)
                self.last_opened_keyevent_file = self.file_path_keyevent
                self.app.keyeventwin.keyevent_window.deiconify()
            except Exception as e:
                last_exception = e
                self.last_opened_keyevent_file = []
                self.file_path_keyevent = []
                print(f"Failed to read keyevent file:\n{last_exception}")



    def open_device_log(self, file_path):

        file_path_device = replace_filename(file_path, 'Devices_1.txt')
        if file_path_device == self.last_opened_device_file:
            print("Same device file is already open.")
        else:
            try:
                self.clear_devicelog()
                self.app.log.load_device(file_path_device, use_columns_device)
                self.app.periWin.update_PeripheralWindow(self.app.log.df_device)
                self.last_opened_device_file = file_path_device
            except Exception as e:
                last_exception = e
                self.last_opened_device_file = None
                print(f"Failed to read device file:\n{last_exception}")


    def open_log(self):

        file_path = self.open_mainlog()

        if not file_path:
            print("open_mainlog failed.")
            return None

        self.open_KB_log(file_path)

        self.open_device_log(file_path)

        self.last_opened_keyevent_file = self.file_path_keyevent
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
