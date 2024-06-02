import tkinter as tk
from tkinter import ttk
from configure_data import *

#pane 에 remarkable event만 표시하는 window 임 
class EventWindow:
    def __init__(self):
        self.pane1 = None
        self.tree = None 


    def layout_EventWindow(self, root):
        # 첫 번째 Pane 생성
        self.pane1 = ttk.Frame(root)
        root.add(self.pane1, text='Event')

        # Treeview 생성
        self.tree = ttk.Treeview(root, columns=treeview_index, show='headings')

        for col_name, col_text in event_columns:
            self.tree.heading(col_name, text=col_text) # 각 열의 제목 설정
            self.tree.column(col_name, width=100)  # 열의 너비를 설정 (옵션)

        # Treeview 패킹
        self.tree.pack(expand=True, fill=tk.BOTH)

        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
      

    def update_EventWindow (self, filtered_df):

        # 기존 데이터를 모두 제거
        for item in self.tree.get_children():
            self.tree.delete(item)

        # DataFrame의 각 행을 Treeview에 삽입
        for index, row in filtered_df.iterrows():
            self.tree.insert("", tk.END, values=(row['Timestamp'], row['Event'], row['Info'], row['line#']))


