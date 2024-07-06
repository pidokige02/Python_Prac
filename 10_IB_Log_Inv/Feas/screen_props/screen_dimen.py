import tkinter as tk

def get_screen_size():
    root = tk.Tk()
    root.withdraw()  # 창을 표시하지 않음
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

# 화면 크기 출력
width, height = get_screen_size()
print(f"Screen width: {width}")
print(f"Screen height: {height}")
