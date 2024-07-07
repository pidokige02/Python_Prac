import tkinter as tk
import win32api

def get_monitors():
    monitors = win32api.EnumDisplayMonitors()
    monitor_info = []
    for monitor in monitors:
        hMonitor, hdcMonitor, lprcMonitor = monitor[0], monitor[1], monitor[2]
        monitor_width = lprcMonitor[2] - lprcMonitor[0]
        monitor_height = lprcMonitor[3] - lprcMonitor[1]
        monitor_info.append((lprcMonitor[0], lprcMonitor[1], monitor_width, monitor_height))
    return monitor_info


def choose_bigger_monitor(monitor_info):
    # 가장 큰 모니터를 찾습니다.
    largest_monitor = max(monitor_info, key=lambda info: info[2] * info[3])
    return largest_monitor

# monitor_info = get_monitors()
# largest_monitor = choose_bigger_monitor(monitor_info)
# x, y, width, height = largest_monitor

# print(f"Largest monitor size: {largest_monitor[2]}x{largest_monitor[3]}")
# print(f"Largest monitor position: ({largest_monitor[0]}, {largest_monitor[1]})")

# root = tk.Tk()
# root.geometry(f"{width}x{height}+{x}+{y}")
# root.title(f"Window on Monitor")
# label = tk.Label(root, text=f"This is monitor ")
# label.pack(expand=True)
# root.mainloop()