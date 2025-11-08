import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def getfigure(win, x0, y0, w, h):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax = fig.add_subplot(111)
    fig.tight_layout()
    return chart, ax

def update_signal():
    global chart1, ax1
    Fs = 44100
    N = 2000
    dt = 1.0 / Fs
    t = np.arange(N) * dt

    F = freq_scale.get()
    A = amp_scale.get()
    P = phase_scale.get()

    y = A * np.sin(2 * np.pi * F * t + P * np.pi / 180)

    ax1.clear()
    ax1.plot(t, y, 'b-', linewidth=1.5)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title(f'Sine Wave: F={F}Hz, A={A:.2f}, Phase={P}deg')
    ax1.grid(True)
    ax1.set_ylim(-1.2, 1.2)
    chart1.draw()

root = tk.Tk()
root.geometry('900x650')
root.config(bg="#ddeeee")
root.wm_title('Sine Wave Generator - Tkinter')

tk.Label(root, text='Frequency (Hz)', bg="#ddeeee").place(x=20, y=20, width=120, height=30)
freq_scale = tk.Scale(root, from_=100, to=2000, orient=tk.HORIZONTAL, command=lambda x: update_signal())
freq_scale.place(x=150, y=10, width=700, height=50)
freq_scale.set(500)

tk.Label(root, text='Amplitude', bg="#ddeeee").place(x=20, y=80, width=120, height=30)
amp_scale = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=lambda x: update_signal())
amp_scale.place(x=150, y=70, width=700, height=50)
amp_scale.set(0.8)

tk.Label(root, text='Phase (deg)', bg="#ddeeee").place(x=20, y=140, width=120, height=30)
phase_scale = tk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL, command=lambda x: update_signal())
phase_scale.place(x=150, y=130, width=700, height=50)
phase_scale.set(0)

chart1, ax1 = getfigure(root, 20, 200, 860, 430)
update_signal()

root.mainloop()
