import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from configure_data import *
from Utils import *
from configure_data import *
from tkinter import messagebox




class ControlPad:

    def __init__(self, app):
        self.app = app
        self.right_frame = None
        self.openlog_button = None
        self.savekeyevent_button = None
        self.reset_timestamp_button = None
        self.timestamp_from = None
        self.timestamp_to = None
        self.file_path_keyevent = None
        self.address = None
        self.keylog_playback_button = None


    def layout_ControlPad(self):

        # 오른쪽 프레임 생성
        self.right_frame = ttk.Frame(self.app.root)
        self.right_frame.grid(row=1, column=1, sticky="ns")

        # openlog 버튼 추가
        self.openlog_button = ttk.Button(self.right_frame, text="Open Log", command=self.open_log)
        self.openlog_button.grid(row=0, column=0, padx=1, pady=1, sticky="w")

        # Save Key Event 버튼 추가
        self.savekeyevent_button = ttk.Button(self.right_frame, text="Save Key Event", command=self.save_keyevent_log)
        self.savekeyevent_button.grid(row=1, column=0, padx=1, pady=1, sticky="w")

        # Save Key Event 버튼 추가
        self.reset_timestamp_button = ttk.Button(self.right_frame, text="Reset Time", command=self.reset_timestamp)
        self.reset_timestamp_button.grid(row=1, column=1, padx=1, pady=1, sticky="w")

        ttk.Label(self.right_frame, text="From (YYYY-MM-DD HH:MM:SS.ssssss)").grid(row=2, column=0, padx=1, pady=1, sticky="w")
        self.timestamp_from = ttk.Entry(self.right_frame)
        self.timestamp_from.grid(row=3, column=0, padx=1, pady=1, sticky="w")

        ttk.Label(self.right_frame, text="To (YYYY-MM-DD HH:MM:SS.ssssss)").grid(row=4, column=0, padx=1, pady=1, sticky="w")
        self.timestamp_to = ttk.Entry(self.right_frame)
        self.timestamp_to.grid(row=5, column=0, padx=1, pady=1, sticky="w")

        ttk.Label(self.right_frame, text="Address").grid(row=6, column=0, padx=1, pady=1, sticky="w")
        self.address = ttk.Entry(self.right_frame)
        self.address.grid(row=7, column=0, padx=1, pady=1, sticky="w")

        self.keylog_playback_button = ttk.Button(self.right_frame, text="Playback", command=self.keylog_playback)
        self.keylog_playback_button.grid(row=7, column=1, padx=1, pady=1, sticky="w")


    def open_log(self):
        # 파일 선택 대화 상자 열기
        file_path = filedialog.askopenfilename()

        if file_path:
            self.app.log.clear_data()
            self.app.logwin.log_text.delete('1.0', tk.END)
            self.app.keyeventwin.keyevent_text.delete('1.0', tk.END)

        # 다양한 인코딩 시도
            encodings = ['utf-8', 'cp949', 'latin1']
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
                    self.app.logwin.log_text.insert(tk.END, content)

                    self.app.log.load_log(file_path, use_columns_log)
                    self.app.log.add_columns_log()
                    self.app.log.analyze_log ()
                    filtered_df = self.app.log.filter_event()
                    self.app.eventWin.update_EventWindow(filtered_df)
                    filtered_df = self.app.log.filter_event(events=['S/W version', 'Product'])
                    self.app.infoWin.update_InfoWindow(filtered_df)

                except Exception as e:
                    self.app.logwin.log_text.insert(tk.END, f"Failed to read file:\n{e}")


            self.file_path_keyevent = replace_filename(file_path, 'KeyBoardShadow_1.txt')
            content = None
            for enc in encodings:
                try:
                    with open(self.file_path_keyevent, 'r', encoding=enc) as file:
                        content = file.read()
                    break
                except Exception as e:
                    last_exception = e

            if content:
                self.app.keyeventwin.keyevent_text.insert(tk.END, content)

                try:
                    self.app.log.load_keyevent_log(self.file_path_keyevent, use_columns_keyevent)
                    self.app.log.add_columns_keyevent()
                    filtered_df = self.app.log.filter_event()  # filter out normal event table

                    filtered_df = self.app.log.analyze_keyevent(filtered_df)
                    self.app.eventWin.update_EventWindow(filtered_df)

                except Exception as e:
                    self.app.keyeventwin.keyevent_text.insert(tk.END, f"Failed to read file:\n{e}")


            file_path_device = replace_filename(file_path, 'Devices_1.txt')
            for enc in encodings:
                try:
                    self.app.log.load_device(file_path_device, use_columns_device)
                    self.app.periWin.update_PeripheralWindow(self.app.log.df_device)
                except Exception as e:
                    last_exception = e
                    print(f"Failed to read device file:\n{last_exception}")


        else:
            self.app.logwin.log_text.insert(tk.END, f"Failed to read file:\n{last_exception}")



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

            print("save_keyevent_log is initiated!!!")

            # CSV 파일 읽기
            try:
                df = pd.read_csv(self.file_path_keyevent, sep='\t', dtype=str, low_memory=False, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(self.file_path_keyevent, sep='\t', dtype=str, low_memory=False, encoding='latin1')

            # 타임스탬프 열의 값을 datetime 객체로 변환하여 새로운 열에 저장
            df['Timestamp_dt'] = df['Timestamp'].apply(extract_timestamp)

            # 주어진 타임스탬프 범위에 있는 행들만 필터링
            filtered_df = df[(df['Timestamp_dt'] >= timestamp_from_dt) & (df['Timestamp_dt'] <= timestamp_to_dt)]

            encodings = ['utf-8', 'cp949', 'latin1']
            lines = None
            last_exception = None

            # 처음 두 줄을 가져오기
            for enc in encodings:
                try:
                    with open(self.file_path_keyevent, 'r',encoding=enc) as source_file:
                        lines = source_file.readlines()
                    break
                except Exception as e:
                    last_exception = e

            if lines:
                header_lines = lines[:2]
            else:
                print("No lines were read. Last exception was:", last_exception)

            # 새로운 CSV 파일에 처음 두 줄을 쓰기
            file_path_keyevent_dest = replace_filename(self.file_path_keyevent, 'KeyBoardShadow_1_captured.txt')

             # 파일 저장 대화 상자를 열고 파일 경로를 가져옴
            file_path_keyevent_dest = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile="KeyBoardShadow_1_captured.txt"
            )

            with open(file_path_keyevent_dest, 'w', encoding='utf-8') as dest_file:
                dest_file.writelines(header_lines)

                # 필터링된 행들을 추가 모드로 쓰기
                filtered_df.to_csv(dest_file, sep='\t', index=False, header=False, mode='a', columns=df.columns.drop('Timestamp_dt'), lineterminator='\n')

            print("save_keyevent_log is completed!!!")

        except ValueError as e:
            print("Invalid timestamp format:", e)
            messagebox.showerror("Error", f"Invalid timestamp format: {e}")






    def reset_timestamp(self):
        self.timestamp_from.delete(0, tk.END)
        self.timestamp_to.delete(0, tk.END)


    def keylog_playback(self):
        file_path = filedialog.askopenfilename()
