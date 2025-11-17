# -*- coding: utf-8 -*-
"""
带回波信号的自相关分析
产生一个带回波的信号，用自相关函数提取回波的时差
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def doCorr(Fs, N, x1, y1, st=1):
    """
    计算两个信号的相关函数

    参数:
        Fs: 采样频率
        N: 信号长度
        x1: 信号1
        y1: 信号2
        st: 0-原始相关, 1-无偏估计校正

    返回:
        tt: 时间轴
        cc: 相关函数值
    """
    x = x1[:N]
    y = y1[:N]
    dt = 1.0 / Fs
    cc = np.correlate(x, y, 'full')
    NN = len(cc)
    tt = np.arange(NN) * dt - N * dt
    if st == 0:
        return tt, cc
    # 无偏估计校正
    W = np.append(1 + np.arange(N), N - np.arange(N - 1))
    cc1 = cc / W
    return tt, cc1


def generate_test_signal(Fs, duration):
    """
    生成测试音频信号（模拟语音/音乐信号）

    参数:
        Fs: 采样频率
        duration: 信号时长（秒）

    返回:
        signal: 生成的信号
    """
    N = int(Fs * duration)
    t = np.arange(N) / Fs

    # 生成复合信号（模拟音频）
    signal = np.zeros(N)

    # 添加多个频率成分
    freqs = [220, 440, 880, 1760]  # A音符的各倍频
    for i, f in enumerate(freqs):
        amplitude = 0.5 / (i + 1)  # 高次谐波衰减
        signal += amplitude * np.sin(2 * np.pi * f * t)

    # 添加包络（模拟实际音频的起伏）
    envelope = np.exp(-t * 2) * (1 - np.exp(-t * 50))
    signal = signal * envelope

    # 归一化
    signal = signal / np.max(np.abs(signal)) * 0.8

    return signal


def add_echo(signal, Fs, delay_time, echo_amplitude):
    """
    给信号添加回波

    参数:
        signal: 原始信号
        Fs: 采样频率
        delay_time: 回波延迟时间（秒）
        echo_amplitude: 回波幅度（相对于原信号）

    返回:
        echo_signal: 带回波的信号
    """
    delay_samples = int(delay_time * Fs)
    N = len(signal)

    # 扩展信号长度以容纳回波
    echo_signal = np.zeros(N + delay_samples)
    echo_signal[:N] = signal

    # 添加回波（延迟+衰减的副本）
    echo_signal[delay_samples:delay_samples + N] += echo_amplitude * signal

    return echo_signal


def find_echo_delay(signal, Fs):
    """
    使用自相关函数检测回波延迟

    参数:
        signal: 带回波的信号
        Fs: 采样频率

    返回:
        delay_time: 检测到的回波延迟时间
        tt: 时间轴
        Rxx: 自相关函数
    """
    N = len(signal)
    tt, Rxx = doCorr(Fs, N, signal, signal, 0)

    # 只分析正半轴（τ > 0）
    center_idx = N - 1
    Rxx_positive = Rxx[center_idx:]
    tt_positive = tt[center_idx:]

    # 寻找第一个显著峰值（排除τ=0的主峰）
    # 设置搜索起点，跳过主峰附近
    min_delay_samples = int(0.01 * Fs)  # 至少10ms的延迟

    # 在主峰之后寻找次峰
    search_start = min_delay_samples
    if search_start < len(Rxx_positive):
        peak_idx = search_start + np.argmax(Rxx_positive[search_start:])
        delay_time = tt_positive[peak_idx]
    else:
        delay_time = 0
        peak_idx = 0

    return delay_time, tt, Rxx, peak_idx


# ===== 主程序 =====

# 参数设置
Fs = 44100  # 采样频率
signal_duration = 0.5  # 原始信号时长（秒）

# 回波参数
echo_delay = 0.15  # 回波延迟时间（秒）
echo_amplitude = 0.6  # 回波幅度（相对于原信号）

print("===== 带回波信号的自相关分析 =====")
print(f"采样频率: {Fs} Hz")
print(f"信号时长: {signal_duration} 秒")
print(f"设定回波延迟: {echo_delay * 1000:.1f} ms")
print(f"设定回波幅度: {echo_amplitude}")

# 生成原始信号
print("\n正在生成测试信号...")
original_signal = generate_test_signal(Fs, signal_duration)

# 添加回波
print("正在添加回波...")
signal_with_echo = add_echo(original_signal, Fs, echo_delay, echo_amplitude)

# 使用自相关函数检测回波延迟
print("正在进行自相关分析...")
detected_delay, tt_corr, Rxx, peak_idx = find_echo_delay(signal_with_echo, Fs)

print(f"\n检测到的回波延迟: {detected_delay * 1000:.2f} ms")
print(f"设定的回波延迟: {echo_delay * 1000:.1f} ms")
print(f"误差: {abs(detected_delay - echo_delay) * 1000:.2f} ms")

# 绘图
fig, axes = plt.subplots(4, 1, figsize=(12, 14))

# 1. 原始信号
t_orig = np.arange(len(original_signal)) / Fs
axes[0].plot(t_orig * 1000, original_signal, 'b-', linewidth=0.8)
axes[0].set_title('原始信号（无回波）', fontsize=12)
axes[0].set_xlabel('时间 (ms)')
axes[0].set_ylabel('幅值')
axes[0].grid(True, alpha=0.3)
axes[0].set_xlim([0, t_orig[-1] * 1000])

# 2. 带回波的信号
t_echo = np.arange(len(signal_with_echo)) / Fs
axes[1].plot(t_echo * 1000, signal_with_echo, 'r-', linewidth=0.8)
axes[1].axvline(x=echo_delay * 1000, color='g', linestyle='--', linewidth=2,
                label=f'回波起始位置 ({echo_delay * 1000:.1f} ms)')
axes[1].set_title('带回波的信号', fontsize=12)
axes[1].set_xlabel('时间 (ms)')
axes[1].set_ylabel('幅值')
axes[1].legend(loc='upper right')
axes[1].grid(True, alpha=0.3)
axes[1].set_xlim([0, t_echo[-1] * 1000])

# 3. 自相关函数（完整）
axes[2].plot(tt_corr * 1000, Rxx, 'b-', linewidth=0.8)
axes[2].axvline(x=0, color='k', linestyle='--', alpha=0.5, label='τ=0 (主峰)')
axes[2].axvline(x=detected_delay * 1000, color='r', linestyle='--', linewidth=2,
                label=f'检测到的回波延迟 ({detected_delay * 1000:.2f} ms)')
axes[2].set_title('带回波信号的自相关函数', fontsize=12)
axes[2].set_xlabel('τ (ms)')
axes[2].set_ylabel('Rxx(τ)')
axes[2].legend(loc='upper right')
axes[2].grid(True, alpha=0.3)

# 4. 自相关函数（放大正半轴，突出回波峰值）
center_idx = len(signal_with_echo) - 1
Rxx_positive = Rxx[center_idx:]
tt_positive = tt_corr[center_idx:]

# 显示范围：0到2倍回波延迟
max_show_time = min(2.5 * echo_delay, tt_positive[-1])
show_samples = int(max_show_time * Fs)
show_samples = min(show_samples, len(tt_positive))

axes[3].plot(tt_positive[:show_samples] * 1000, Rxx_positive[:show_samples], 'b-', linewidth=1.5)
axes[3].axvline(x=detected_delay * 1000, color='r', linestyle='--', linewidth=2,
                label=f'检测到的回波: {detected_delay * 1000:.2f} ms')
axes[3].axvline(x=echo_delay * 1000, color='g', linestyle=':', linewidth=2,
                label=f'实际回波: {echo_delay * 1000:.1f} ms')

# 标记峰值点
if peak_idx < show_samples:
    axes[3].plot(tt_positive[peak_idx] * 1000, Rxx_positive[peak_idx], 'ro', markersize=10,
                 label='回波峰值')

axes[3].set_title('自相关函数（正半轴放大，显示回波峰值）', fontsize=12)
axes[3].set_xlabel('τ (ms)')
axes[3].set_ylabel('Rxx(τ)')
axes[3].legend(loc='upper right')
axes[3].grid(True, alpha=0.3)
axes[3].set_xlim([0, max_show_time * 1000])

# 添加文本说明
textstr = f'回波延迟检测结果:\n设定值: {echo_delay * 1000:.1f} ms\n检测值: {detected_delay * 1000:.2f} ms\n误差: {abs(detected_delay - echo_delay) * 1000:.2f} ms'
axes[3].text(0.02, 0.98, textstr, transform=axes[3].transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.suptitle('带回波信号的自相关分析 - 回波时差提取', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.subplots_adjust(top=0.95)

# 保存图形
plt.savefig('echo_detection.png', dpi=150, bbox_inches='tight')
print(f"\n图形已保存为 echo_detection.png")

# 保存带回波的音频信号为WAV文件
output_wav = 'signal_with_echo.wav'
# 归一化并转换为16位整数
signal_normalized = signal_with_echo / np.max(np.abs(signal_with_echo))
signal_int16 = (signal_normalized * 32767).astype(np.int16)
wavfile.write(output_wav, Fs, signal_int16)
print(f"带回波的音频信号已保存为 {output_wav}")

plt.show()

print("\n分析完成！")
print("自相关函数中，除了τ=0处的主峰外，")
print(f"在τ={detected_delay * 1000:.2f}ms处出现次峰，对应回波延迟时间。")
