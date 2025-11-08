import numpy as np
import matplotlib.pyplot as plt

# 设置参数
Fs = 11025  # 采样频率11025Hz
N = 2000  # 采样点数
dt = 1.0 / Fs  # 采样间隔
t = np.arange(N) * dt  # 时间序列

# 生成四个不同频率的正弦波信号
x1 = np.sin(2 * np.pi * 500 * t)  # 500Hz
x2 = np.sin(2 * np.pi * 600 * t)  # 600Hz
x3 = np.sin(2 * np.pi * 700 * t)  # 700Hz
x4 = np.sin(2 * np.pi * 800 * t)  # 800Hz

# 创建2x2的子图布局
fig, ax = plt.subplots(nrows=2, ncols=2)

# 绘制500Hz信号
ax[0][0].plot(t, x1)
ax[0][0].set_title('500Hz Sine Wave')
ax[0][0].set_xlabel('Time (s)')
ax[0][0].set_ylabel('Amplitude')
ax[0][0].grid(True)
ax[0][0].set_xlim(0, 0.02)

# 绘制600Hz信号
ax[0][1].plot(t, x2)
ax[0][1].set_title('600Hz Sine Wave')
ax[0][1].set_xlabel('Time (s)')
ax[0][1].set_ylabel('Amplitude')
ax[0][1].grid(True)
ax[0][1].set_xlim(0, 0.02)

# 绘制700Hz信号
ax[1][0].plot(t, x3)
ax[1][0].set_title('700Hz Sine Wave')
ax[1][0].set_xlabel('Time (s)')
ax[1][0].set_ylabel('Amplitude')
ax[1][0].grid(True)
ax[1][0].set_xlim(0, 0.02)

# 绘制800Hz信号
ax[1][1].plot(t, x4)
ax[1][1].set_title('800Hz Sine Wave')
ax[1][1].set_xlabel('Time (s)')
ax[1][1].set_ylabel('Amplitude')
ax[1][1].grid(True)
ax[1][1].set_xlim(0, 0.02)

# 调整子图间距
plt.tight_layout()

# 显示图形
plt.show()
