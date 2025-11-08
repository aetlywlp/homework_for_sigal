import os
import sys

# 设置库路径以避免Qt库冲突 - 需要在加载Qt之前重新启动进程
conda_lib_path = '/home/aetly/miniconda3/envs/homework_for_signal/lib'
current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')

# 如果LD_LIBRARY_PATH还没有设置conda路径，则重新执行程序
if conda_lib_path not in current_ld_path:
    if current_ld_path:
        os.environ['LD_LIBRARY_PATH'] = f"{conda_lib_path}:{current_ld_path}"
    else:
        os.environ['LD_LIBRARY_PATH'] = conda_lib_path
    # 重新执行当前程序
    os.execv(sys.executable, [sys.executable] + sys.argv)

import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

def setFigure(win, x0, y0, w, h):
    wdi = QWidget(win)
    wdi.setGeometry(x0, y0, w, h)
    wdi.setStyleSheet('background-color: #dddddd;')
    lay = QVBoxLayout(wdi)
    lay.setContentsMargins(2, 2, 2, 2)
    fig = Figure()
    canvas = FigureCanvasQTAgg(fig)
    lay.addWidget(canvas)
    return fig, canvas

def update_signal():
    Fs = 44100
    N = 2000
    dt = 1.0 / Fs
    t = np.arange(N) * dt

    F = freq_slider.value()
    A = amp_slider.value() / 100.0
    P = phase_slider.value()

    y = A * np.sin(2 * np.pi * F * t + P * np.pi / 180)

    mFig.clear()
    ax = mFig.add_subplot(111)
    ax.plot(t, y, 'b-', linewidth=1.5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Sine Wave: F={F}Hz, A={A:.2f}, Phase={P}deg')
    ax.grid(True)
    ax.set_ylim(-1.2, 1.2)
    mCanvas.draw()

    freq_label.setText(f'Frequency: {F} Hz')
    amp_label.setText(f'Amplitude: {A:.2f}')
    phase_label.setText(f'Phase: {P} deg')

app = QApplication(sys.argv)
app.setStyle("Fusion")
win = QWidget()
win.setWindowTitle('Sine Wave Generator - PyQt5')
win.resize(900, 650)
win.setStyleSheet("background-color: #ddeeee;")

freq_label = QLabel('Frequency: 500 Hz', win)
freq_label.setGeometry(20, 10, 200, 30)
freq_slider = QSlider(Qt.Horizontal, win)
freq_slider.setGeometry(230, 10, 650, 30)
freq_slider.setMinimum(100)
freq_slider.setMaximum(2000)
freq_slider.setValue(500)
freq_slider.valueChanged.connect(update_signal)

amp_label = QLabel('Amplitude: 0.80', win)
amp_label.setGeometry(20, 50, 200, 30)
amp_slider = QSlider(Qt.Horizontal, win)
amp_slider.setGeometry(230, 50, 650, 30)
amp_slider.setMinimum(0)
amp_slider.setMaximum(100)
amp_slider.setValue(80)
amp_slider.valueChanged.connect(update_signal)

phase_label = QLabel('Phase: 0 deg', win)
phase_label.setGeometry(20, 90, 200, 30)
phase_slider = QSlider(Qt.Horizontal, win)
phase_slider.setGeometry(230, 90, 650, 30)
phase_slider.setMinimum(0)
phase_slider.setMaximum(180)
phase_slider.setValue(0)
phase_slider.valueChanged.connect(update_signal)

mFig, mCanvas = setFigure(win, 20, 140, 860, 490)
update_signal()

win.show()
sys.exit(app.exec_())
