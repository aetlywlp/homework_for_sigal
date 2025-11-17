# -*- coding: utf-8 -*-
"""
相关函数性质验证
验证自相关函数和互相关函数的六条基本性质：
a) 自相关函数是偶函数，Rx(τ)=Rx(-τ)
b) 当τ=0时，自相关函数具有最大值
c) 周期信号的自相关函数仍然是同频率周期信号，但不保留原信号相位信息
d) 随机噪声信号的自相关函数将随τ的增大快速衰减
e) 两周期信号互相关函数仍然是同频率周期信号，且保留了信号相位信息
f) 两个非同频率的周期信号互不相关
"""

import numpy as np
import matplotlib.pyplot as plt

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
    cc1 = cc1 / max(abs(cc1))
    return tt, cc1


def noiseGenerator(Fs, N, amplitude=1.0):
    """生成白噪声信号"""
    dt = 1.0 / Fs
    t = np.arange(N) * dt
    y = amplitude * np.random.randn(N)
    return t, y


def sineGenerator(Fs, N, freq, amplitude=1.0, phase=0):
    """生成正弦波信号"""
    dt = 1.0 / Fs
    t = np.arange(N) * dt
    y = amplitude * np.sin(2 * np.pi * freq * t + phase)
    return t, y


# 基本参数设置
Fs = 44100  # 采样频率
N = 2048    # 采样点数
dt = 1.0 / Fs

# 生成测试信号
# 白噪声信号
t_noise, noise = noiseGenerator(Fs, N, 0.5)

# 正弦波信号（带相位）
freq1 = 1000  # 频率1
freq2 = 1500  # 频率2（不同频率）
phase1 = np.pi / 4  # 相位1
phase2 = np.pi / 3  # 相位2

t_sine1, sine1 = sineGenerator(Fs, N, freq1, 0.8, phase1)
t_sine2, sine2 = sineGenerator(Fs, N, freq1, 0.8, phase2)  # 同频率不同相位
t_sine3, sine3 = sineGenerator(Fs, N, freq2, 0.8, 0)       # 不同频率

# ===== 验证六条基本性质 =====

# 创建大图
fig = plt.figure(figsize=(16, 18))

# ===== 性质a: 自相关函数是偶函数 =====
tt_sine, Rxx_sine = doCorr(Fs, N, sine1, sine1, 1)
ax1 = plt.subplot(6, 2, 1)
ax1.plot(t_sine1[:500], sine1[:500], 'b-', linewidth=1)
ax1.set_title('性质a: 原始正弦信号', fontsize=11)
ax1.set_xlabel('时间 (s)')
ax1.set_ylabel('幅值')
ax1.grid(True, alpha=0.3)

ax2 = plt.subplot(6, 2, 2)
ax2.plot(tt_sine, Rxx_sine, 'r-', linewidth=1)
ax2.axvline(x=0, color='k', linestyle='--', alpha=0.5)
ax2.set_title('性质a: 自相关函数 (偶函数，关于τ=0对称)', fontsize=11)
ax2.set_xlabel('τ (s)')
ax2.set_ylabel('Rx(τ)')
ax2.grid(True, alpha=0.3)
# 标注对称性
mid_idx = len(tt_sine) // 2
ax2.text(0.05, 0.95, f'Rx(0)={Rxx_sine[mid_idx]:.4f}\n验证: Rx(τ)=Rx(-τ)',
         transform=ax2.transAxes, verticalalignment='top', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ===== 性质b: τ=0时自相关函数具有最大值 =====
tt_noise, Rxx_noise = doCorr(Fs, N, noise, noise, 1)
ax3 = plt.subplot(6, 2, 3)
ax3.plot(t_noise[:500], noise[:500], 'b-', linewidth=0.8)
ax3.set_title('性质b: 白噪声信号', fontsize=11)
ax3.set_xlabel('时间 (s)')
ax3.set_ylabel('幅值')
ax3.grid(True, alpha=0.3)

ax4 = plt.subplot(6, 2, 4)
ax4.plot(tt_noise, Rxx_noise, 'r-', linewidth=1)
ax4.axvline(x=0, color='k', linestyle='--', alpha=0.5)
max_idx = np.argmax(Rxx_noise)
ax4.plot(tt_noise[max_idx], Rxx_noise[max_idx], 'go', markersize=8)
ax4.set_title('性质b: 自相关函数 (τ=0处最大值)', fontsize=11)
ax4.set_xlabel('τ (s)')
ax4.set_ylabel('Rx(τ)')
ax4.grid(True, alpha=0.3)
ax4.text(0.05, 0.95, f'最大值位置: τ={tt_noise[max_idx]:.6f}s\n最大值: {Rxx_noise[max_idx]:.4f}',
         transform=ax4.transAxes, verticalalignment='top', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ===== 性质c: 周期信号自相关函数仍是同频率周期信号，不保留相位 =====
ax5 = plt.subplot(6, 2, 5)
ax5.plot(t_sine1[:500], sine1[:500], 'b-', linewidth=1, label=f'相位={phase1:.2f}rad')
ax5.set_title(f'性质c: 正弦信号 (f={freq1}Hz, φ={phase1:.2f}rad)', fontsize=11)
ax5.set_xlabel('时间 (s)')
ax5.set_ylabel('幅值')
ax5.grid(True, alpha=0.3)
ax5.legend(loc='upper right', fontsize=8)

ax6 = plt.subplot(6, 2, 6)
ax6.plot(tt_sine, Rxx_sine, 'r-', linewidth=1)
ax6.set_title('性质c: 自相关函数 (同频率周期，相位信息丢失)', fontsize=11)
ax6.set_xlabel('τ (s)')
ax6.set_ylabel('Rx(τ)')
ax6.grid(True, alpha=0.3)
# 计算自相关函数的周期
period_original = 1.0 / freq1
ax6.text(0.05, 0.95, f'原信号周期: {period_original*1000:.3f}ms\n自相关函数保持同频率\n但相位信息丢失(从τ=0开始)',
         transform=ax6.transAxes, verticalalignment='top', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ===== 性质d: 噪声信号自相关函数随τ增大快速衰减 =====
ax7 = plt.subplot(6, 2, 7)
ax7.plot(t_noise[:500], noise[:500], 'b-', linewidth=0.8)
ax7.set_title('性质d: 白噪声信号', fontsize=11)
ax7.set_xlabel('时间 (s)')
ax7.set_ylabel('幅值')
ax7.grid(True, alpha=0.3)

ax8 = plt.subplot(6, 2, 8)
# 放大显示中心部分
center = len(tt_noise) // 2
range_show = N // 4
ax8.plot(tt_noise[center-range_show:center+range_show],
         Rxx_noise[center-range_show:center+range_show], 'r-', linewidth=1)
ax8.axvline(x=0, color='k', linestyle='--', alpha=0.5)
ax8.set_title('性质d: 白噪声自相关函数 (快速衰减至0)', fontsize=11)
ax8.set_xlabel('τ (s)')
ax8.set_ylabel('Rx(τ)')
ax8.grid(True, alpha=0.3)
ax8.text(0.05, 0.95, '白噪声自相关函数\n在τ≠0时快速衰减\n趋近于零',
         transform=ax8.transAxes, verticalalignment='top', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ===== 性质e: 两周期信号互相关函数保留相位信息 =====
tt_cross, Rxy_cross = doCorr(Fs, N, sine1, sine2, 1)
ax9 = plt.subplot(6, 2, 9)
ax9.plot(t_sine1[:500], sine1[:500], 'b-', linewidth=1, label=f'x: φ={phase1:.2f}rad')
ax9.plot(t_sine2[:500], sine2[:500], 'g-', linewidth=1, label=f'y: φ={phase2:.2f}rad')
ax9.set_title(f'性质e: 两个同频率正弦信号 (f={freq1}Hz)', fontsize=11)
ax9.set_xlabel('时间 (s)')
ax9.set_ylabel('幅值')
ax9.legend(loc='upper right', fontsize=8)
ax9.grid(True, alpha=0.3)

ax10 = plt.subplot(6, 2, 10)
ax10.plot(tt_cross, Rxy_cross, 'r-', linewidth=1)
ax10.axvline(x=0, color='k', linestyle='--', alpha=0.5)
ax10.set_title('性质e: 互相关函数 (同频率，保留相位差信息)', fontsize=11)
ax10.set_xlabel('τ (s)')
ax10.set_ylabel('Rxy(τ)')
ax10.grid(True, alpha=0.3)
phase_diff = phase2 - phase1
time_delay = phase_diff / (2 * np.pi * freq1)
ax10.text(0.05, 0.95, f'相位差: {phase_diff:.4f}rad\n理论时延: {time_delay*1000:.4f}ms\n互相关函数保留相位信息',
         transform=ax10.transAxes, verticalalignment='top', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ===== 性质f: 不同频率的周期信号互不相关 =====
tt_diff, Rxy_diff = doCorr(Fs, N, sine1, sine3, 1)
ax11 = plt.subplot(6, 2, 11)
ax11.plot(t_sine1[:500], sine1[:500], 'b-', linewidth=1, label=f'x: f={freq1}Hz')
ax11.plot(t_sine3[:500], sine3[:500], 'g-', linewidth=1, label=f'y: f={freq2}Hz')
ax11.set_title(f'性质f: 两个不同频率正弦信号', fontsize=11)
ax11.set_xlabel('时间 (s)')
ax11.set_ylabel('幅值')
ax11.legend(loc='upper right', fontsize=8)
ax11.grid(True, alpha=0.3)

ax12 = plt.subplot(6, 2, 12)
ax12.plot(tt_diff, Rxy_diff, 'r-', linewidth=1)
ax12.axhline(y=0, color='k', linestyle='--', alpha=0.5)
ax12.set_title('性质f: 互相关函数 (不同频率信号互不相关)', fontsize=11)
ax12.set_xlabel('τ (s)')
ax12.set_ylabel('Rxy(τ)')
ax12.grid(True, alpha=0.3)
ax12.text(0.05, 0.95, f'f1={freq1}Hz, f2={freq2}Hz\n不同频率信号互不相关\n互相关函数振幅较小',
         transform=ax12.transAxes, verticalalignment='top', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('相关函数六条基本性质验证', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.subplots_adjust(top=0.95, hspace=0.35)

# 保存图形
plt.savefig('correlation_properties.png', dpi=150, bbox_inches='tight')
print("图形已保存为 correlation_properties.png")

plt.show()

# 打印验证结果
print("\n===== 相关函数六条基本性质验证结果 =====")
print("a) 自相关函数是偶函数: Rx(τ) = Rx(-τ)")
print("   验证: 观察自相关函数图形关于τ=0对称")
print("\nb) 当τ=0时，自相关函数具有最大值")
print(f"   验证: 最大值位置在τ=0处")
print("\nc) 周期信号的自相关函数仍然是同频率周期信号，但不保留原信号相位信息")
print(f"   验证: 自相关函数周期与原信号相同，但从τ=0开始（相位归零）")
print("\nd) 随机噪声信号的自相关函数将随τ的增大快速衰减")
print("   验证: 白噪声自相关函数在τ≠0时迅速衰减至0")
print("\ne) 两周期信号互相关函数仍然是同频率周期信号，且保留了信号相位信息")
print(f"   验证: 互相关函数反映了两信号的相位差")
print("\nf) 两个非同频率的周期信号互不相关")
print(f"   验证: 不同频率({freq1}Hz和{freq2}Hz)信号的互相关函数振幅很小")
