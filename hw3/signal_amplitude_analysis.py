# -*- coding: utf-8 -*-
"""
信号的幅值域分析
绘制白噪声信号、正弦波信号、方波信号和三角波信号的概率密度曲线和概率分布曲线
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 基本参数设置
Fs = 44100  # 采样频率
N = 4096    # 采样点数
t = np.arange(N) * (1.0 / Fs)  # 时间向量
f0 = 50     # 信号频率

# 生成四种信号
# 1. 白噪声信号
noise_signal = 0.8 * np.random.randn(N)

# 2. 正弦波信号
sine_signal = 0.8 * np.sin(2 * np.pi * f0 * t)

# 3. 方波信号
square_signal = 0.8 * sig.square(2 * np.pi * f0 * t)

# 4. 三角波信号
triangle_signal = 0.8 * sig.sawtooth(2 * np.pi * f0 * t, width=0.5)

# 概率密度和概率分布计算函数
def calculate_pdf_cdf(signal_data, M=50, x_range=(-1, 1)):
    """
    计算信号的概率密度函数(PDF)和累积分布函数(CDF)

    参数:
        signal_data: 输入信号数据
        M: 直方图的分组数
        x_range: 幅值范围

    返回:
        x: 幅值坐标
        pdf: 概率密度函数
        cdf: 累积分布函数
    """
    x = np.linspace(x_range[0], x_range[1], num=M)

    # 计算直方图
    hist, bin_edges = np.histogram(signal_data, bins=x)

    # 计算概率密度函数 (归一化)
    dx = x[1] - x[0]  # 幅值间隔
    pdf = hist / (len(signal_data) * dx)  # 归一化为概率密度
    pdf = np.append(pdf, pdf[-1])  # 保持与x长度一致

    # 计算累积分布函数
    cdf = np.cumsum(pdf) * dx

    return x, pdf, cdf

# 计算四种信号的PDF和CDF
M = 100  # 分组数，增加分辨率
x_noise, pdf_noise, cdf_noise = calculate_pdf_cdf(noise_signal, M)
x_sine, pdf_sine, cdf_sine = calculate_pdf_cdf(sine_signal, M)
x_square, pdf_square, cdf_square = calculate_pdf_cdf(square_signal, M)
x_triangle, pdf_triangle, cdf_triangle = calculate_pdf_cdf(triangle_signal, M)

# 创建图形
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(15, 12))

# 信号名称
signal_names = ['白噪声信号', '正弦波信号', '方波信号', '三角波信号']
signals = [noise_signal, sine_signal, square_signal, triangle_signal]
x_vals = [x_noise, x_sine, x_square, x_triangle]
pdfs = [pdf_noise, pdf_sine, pdf_square, pdf_triangle]
cdfs = [cdf_noise, cdf_sine, cdf_square, cdf_triangle]

# 绘制每种信号
for i in range(4):
    # 时域波形
    axes[i, 0].plot(t[:500], signals[i][:500], 'b-', linewidth=0.8)
    axes[i, 0].set_title(f'{signal_names[i]} - 时域波形')
    axes[i, 0].set_xlabel('时间 (s)')
    axes[i, 0].set_ylabel('幅值')
    axes[i, 0].grid(True, alpha=0.3)
    axes[i, 0].set_xlim([0, t[499]])

    # 概率密度曲线
    axes[i, 1].plot(x_vals[i], pdfs[i], 'r-', linewidth=1.5)
    axes[i, 1].set_title(f'{signal_names[i]} - 概率密度曲线 (PDF)')
    axes[i, 1].set_xlabel('幅值')
    axes[i, 1].set_ylabel('概率密度')
    axes[i, 1].grid(True, alpha=0.3)
    axes[i, 1].set_xlim([-1, 1])

    # 概率分布曲线 (累积分布函数)
    axes[i, 2].plot(x_vals[i], cdfs[i], 'g-', linewidth=1.5)
    axes[i, 2].set_title(f'{signal_names[i]} - 概率分布曲线 (CDF)')
    axes[i, 2].set_xlabel('幅值')
    axes[i, 2].set_ylabel('累积概率')
    axes[i, 2].grid(True, alpha=0.3)
    axes[i, 2].set_xlim([-1, 1])
    axes[i, 2].set_ylim([0, 1.1])

plt.suptitle('信号的幅值域分析', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.subplots_adjust(top=0.95)

# 保存图形
plt.savefig('signal_amplitude_analysis.png', dpi=150, bbox_inches='tight')
print("图形已保存为 signal_amplitude_analysis.png")

plt.show()
