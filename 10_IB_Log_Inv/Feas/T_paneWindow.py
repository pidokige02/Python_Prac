import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Complex PanedWindow Example")

# 메인 PanedWindow 생성 (수평 방향)
main_paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
main_paned_window.pack(fill=tk.BOTH, expand=True)

# 왼쪽 프레임
left_frame = ttk.Frame(main_paned_window, width=200, height=400, relief=tk.SUNKEN)
main_paned_window.add(left_frame, weight=1)

# 오른쪽 PanedWindow (수직 방향)
right_paned_window = ttk.PanedWindow(main_paned_window, orient=tk.VERTICAL)
main_paned_window.add(right_paned_window, weight=3)

# 오른쪽 상단 프레임
top_right_frame = ttk.Frame(right_paned_window, width=400, height=200, relief=tk.SUNKEN)
right_paned_window.add(top_right_frame, weight=1)

# 오른쪽 하단 PanedWindow (수평 방향)
bottom_right_paned_window = ttk.PanedWindow(right_paned_window, orient=tk.HORIZONTAL)
right_paned_window.add(bottom_right_paned_window, weight=1)

# 오른쪽 하단 좌측 프레임
bottom_left_frame = ttk.Frame(bottom_right_paned_window, width=200, height=200, relief=tk.SUNKEN)
bottom_right_paned_window.add(bottom_left_frame, weight=1)

# 오른쪽 하단 우측 프레임
bottom_right_frame = ttk.Frame(bottom_right_paned_window, width=200, height=200, relief=tk.SUNKEN)
bottom_right_paned_window.add(bottom_right_frame, weight=1)

root.mainloop()
