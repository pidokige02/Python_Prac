import tkinter as tk
from tkinter import ttk
from configure_data import *


class InfoWindow:
    def __init__(self):
        self.pane1 = None
        self.text  = None 


    def layout_InfoWindow(self, root):
        self.pane1 = ttk.Frame(root)
        root.add(self.pane1, text='Info')

        # Text 위젯 생성
        self.text = tk.Text(self.pane1, wrap='word', state='disabled')  # Text 위젯을 disabled 상태로 생성


        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(self.pane1, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        # Text 위젯과 스크롤바를 grid로 배치
        self.text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # grid 레이아웃을 사용하여 크기 조정
        self.pane1.grid_rowconfigure(0, weight=1)
        self.pane1.grid_columnconfigure(0, weight=1)        
   
   
    def update_InfoWindow (self, filtered_df):

        # Text 위젯의 텍스트를 지우고 (임시로 'normal' 상태로 변경하여) 새로운 텍스트를 삽입
        self.text.config(state='normal')
        self.text.delete('1.0', tk.END)  # 기존 텍스트 삭제
        
        for index, row in filtered_df.iterrows():
            info_text = f"Timestamp: {row['Timestamp']}\nEvent: {row['Event']}\nInfo: {row['Info']}\nLine#: {row['line#']}\n\n"
            self.text.insert(tk.END, info_text)  # 새로운 텍스트 삽입

        self.text.config(state='disabled')  # 다시 Text 위젯을 disabled 상태로 변경
