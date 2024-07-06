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

def create_window_on_monitor(monitor_index):
    monitors = get_monitors()
    if monitor_index < 0 or monitor_index >= len(monitors):
        raise ValueError("Invalid monitor index")

    x, y, width, height = monitors[monitor_index]

    root = tk.Tk()
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.title(f"Window on Monitor {monitor_index + 1}")

    label = tk.Label(root, text=f"This is monitor {monitor_index + 1}")
    label.pack(expand=True)

    root.mainloop()

# Example: create a window on the second monitor (index 1)
create_window_on_monitor(0)
