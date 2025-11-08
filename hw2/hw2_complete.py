"""
作业2完整版: 信号频谱分析器
包含：
1. 标准信号发生器 + FFT频谱分析
2. 窗函数选择
3. 线性/对数谱显示
4. 频谱验证功能
"""
import tkinter as tk
import numpy as np
from scipy.fft import fft, rfft
from scipy import signal as sp_signal
import drvi.drviDSP as dsp
import drvi.drviControlls as dr

# 全局变量
window_type = 0  # 0=矩形窗, 1=汉宁窗, 2=汉明窗, 3=布莱克曼窗
scale_type = 0  # 0=线性, 1=对数

# 创建主窗口
win = tk.Tk()
win.geometry('1100x720')
win.config(bg="#ddeeee")
win.wm_title('作业2: 信号频谱分析器（含窗函数和对数谱）')

# ========== 显示区域 ==========
# 时域波形显示
mPlotWave = dr.DRPlot(win, 20, 20, 900, 300, 'Time Domain', 0, 0, 0, 0.1, -1.2, 1.2)

# 频谱显示
mPlotAmp = dr.DRPlot(win, 20, 330, 900, 300, 'Frequency Spectrum', 0, 0, 0, 5000, 0, 1)

# ========== 窗函数应用 ==========
def apply_window(data, win_type):
    """应用窗函数"""
    N = len(data)
    if win_type == 0:  # 矩形窗
        return data
    elif win_type == 1:  # 汉宁窗
        window = np.hanning(N)
        return data * window
    elif win_type == 2:  # 汉明窗
        window = np.hamming(N)
        return data * window
    elif win_type == 3:  # 布莱克曼窗
        window = np.blackman(N)
        return data * window
    return data

# ========== 信号和频谱更新函数 ==========
def updateSignalAndFFT(v=None):
    global window_type, scale_type

    # 生成信号
    mSignal.genData()
    t, data = mSignal.t, mSignal.data

    # 显示时域波形
    mPlotWave.setValue2D(t, data)

    # 应用窗函数
    windowed_data = apply_window(data, window_type)

    # 计算FFT频谱
    N = len(windowed_data)
    dt = t[1] - t[0] if len(t) > 1 else 1/44100
    Fs = 1 / dt
    df = Fs / N

    # 使用rfft计算频谱
    spectrum = np.fft.rfft(windowed_data)
    A = np.abs(spectrum) / (N / 2)
    A[0] = A[0] / 2  # 直流分量修正

    # 频率轴
    f = np.arange(len(A)) * df

    # 根据显示类型显示频谱
    if scale_type == 0:  # 线性谱
        mPlotAmp.setValue2D(f, A)
        mPlotAmp.setYlim(0, max(A) * 1.2 if max(A) > 0 else 1)
    else:  # 对数谱(dB)
        A_db = 20 * np.log10(A + 1e-10)  # 避免log(0)
        mPlotAmp.setValue2D(f, A_db)
        mPlotAmp.setYlim(-60, max(A_db[A_db > -60]) + 10 if len(A_db[A_db > -60]) > 0 else 10)

    # 频谱验证（仅对正弦波）
    signal_type = mSignal.st
    if signal_type == 0:  # 正弦波
        freq = mSignal.F
        amp = mSignal.A

        # 找到峰值
        search_end = min(int(5000/df), len(A))
        peak_idx = np.argmax(A[1:search_end]) + 1
        peak_freq = f[peak_idx]
        peak_amp = A[peak_idx]

        print(f"\n=== 频谱验证 ===")
        print(f"信号参数: 频率={freq:.1f}Hz, 幅值={amp:.2f}")
        print(f"峰值频率: {peak_freq:.1f}Hz (误差: {abs(peak_freq-freq):.1f}Hz)")
        print(f"峰值幅值: {peak_amp:.3f} (误差: {abs(peak_amp-amp):.3f})")
        print(f"窗函数: {['矩形窗','汉宁窗','汉明窗','布莱克曼窗'][window_type]}")
        print(f"显示模式: {['线性谱','对数谱'][scale_type]}")

# ========== 窗函数选择回调 ==========
def set_window_rect(v):
    global window_type
    window_type = 0
    print("窗函数: 矩形窗")
    updateSignalAndFFT()

def set_window_hanning(v):
    global window_type
    window_type = 1
    print("窗函数: 汉宁窗")
    updateSignalAndFFT()

def set_window_hamming(v):
    global window_type
    window_type = 2
    print("窗函数: 汉明窗")
    updateSignalAndFFT()

def set_window_blackman(v):
    global window_type
    window_type = 3
    print("窗函数: 布莱克曼窗")
    updateSignalAndFFT()

# ========== 显示模式选择回调 ==========
def set_scale_linear(v):
    global scale_type
    scale_type = 0
    print("显示模式: 线性谱")
    updateSignalAndFFT()

def set_scale_log(v):
    global scale_type
    scale_type = 1
    print("显示模式: 对数谱(dB)")
    updateSignalAndFFT()

# ========== 信号类型选择回调 ==========
def set_signal_sine(v):
    mSignal.setSignalType(0)
    print("信号类型: 正弦波")

def set_signal_square(v):
    mSignal.setSignalType(1)
    print("信号类型: 方波")

def set_signal_triangle(v):
    mSignal.setSignalType(2)
    print("信号类型: 三角波")

def set_signal_noise(v):
    mSignal.setSignalType(3)
    print("信号类型: 白噪声")

# ========== 控制面板 ==========
# 信号类型按钮组
dr.DRLabel(win, 930, 20, 150, 30, '#003355', '#ffffff', 'Signal Type')
mBtnSine = dr.DRButton(win, 930, 50, 150, 30, '#004466', '#ffffff', 'Sine', 1)
mBtnSquare = dr.DRButton(win, 930, 85, 150, 30, '#004466', '#ffffff', 'Square', 2)
mBtnTriangle = dr.DRButton(win, 930, 120, 150, 30, '#004466', '#ffffff', 'Triangle', 3)
mBtnNoise = dr.DRButton(win, 930, 155, 150, 30, '#004466', '#ffffff', 'Noise', 4)

# 频率控制
dr.DRLabel(win, 930, 195, 150, 30, '#003355', '#ffffff', 'Freq (Hz)')
mKnobFre = dr.DRKnob(win, 930, 225, 150, 150, '#004466', '#222222', '#aaaaaa', '10,2000', 10, 2000, 100)
mEntryFre = dr.DREntryD(win, 950, 385, 110, 30, '#ffffff', '#000000', 100)

# 幅值控制
dr.DRLabel(win, 930, 425, 150, 30, '#003355', '#ffffff', 'Amplitude')
mKnobAmp = dr.DRKnob(win, 930, 455, 150, 150, '#004466', '#222222', '#aaaaaa', '0,1', 0, 1, 0.8)
mEntryAmp = dr.DREntryD(win, 950, 615, 110, 30, '#ffffff', '#000000', 0.8)

# 运行按钮
mBtnRun = dr.DRButton(win, 930, 655, 150, 50, '#006600', '#ffff00', 'RUN', 100)

# 窗函数选择按钮组
dr.DRLabel(win, 20, 650, 150, 30, '#003355', '#ffffff', 'Window Function')
mBtnWinRect = dr.DRButton(win, 180, 650, 100, 30, '#0066cc', '#ffffff', 'Rect', 10)
mBtnWinHanning = dr.DRButton(win, 285, 650, 100, 30, '#0066cc', '#ffffff', 'Hanning', 11)
mBtnWinHamming = dr.DRButton(win, 390, 650, 100, 30, '#0066cc', '#ffffff', 'Hamming', 12)
mBtnWinBlackman = dr.DRButton(win, 495, 650, 100, 30, '#0066cc', '#ffffff', 'Blackman', 13)

# 显示模式选择按钮
dr.DRLabel(win, 610, 650, 120, 30, '#003355', '#ffffff', 'Scale Type')
mBtnLinear = dr.DRButton(win, 740, 650, 80, 30, '#cc6600', '#ffffff', 'Linear', 20)
mBtnLog = dr.DRButton(win, 825, 650, 80, 30, '#cc6600', '#ffffff', 'Log(dB)', 21)

# ========== 信号发生器 ==========
mSignal = dsp.DRGenerator(0, 44100, 4096, 0.8, 100, 0)

# ========== 绑定事件 ==========
# 运行按钮
mBtnRun.addCallBackSingle(updateSignalAndFFT)

# 信号类型按钮
mBtnSine.addCallBackSingle(set_signal_sine)
mBtnSquare.addCallBackSingle(set_signal_square)
mBtnTriangle.addCallBackSingle(set_signal_triangle)
mBtnNoise.addCallBackSingle(set_signal_noise)

# 频率和幅值控制
mKnobFre.addCallBackSingle(mSignal.setSignalFre)
mKnobFre.addCallBackSingle(mEntryFre.setValueSingle)
mKnobAmp.addCallBackSingle(mSignal.setSignalAmp)
mKnobAmp.addCallBackSingle(mEntryAmp.setValueSingle)

# 窗函数选择按钮
mBtnWinRect.addCallBackSingle(set_window_rect)
mBtnWinHanning.addCallBackSingle(set_window_hanning)
mBtnWinHamming.addCallBackSingle(set_window_hamming)
mBtnWinBlackman.addCallBackSingle(set_window_blackman)

# 显示模式按钮
mBtnLinear.addCallBackSingle(set_scale_linear)
mBtnLog.addCallBackSingle(set_scale_log)

# 打印使用说明
print("="*80)
print("作业2: 信号频谱分析器（完整版）")
print("="*80)
print("功能特性：")
print("1. 标准信号发生器（正弦波/方波/三角波/白噪声）")
print("2. FFT频谱分析")
print("3. 窗函数选择（矩形窗/汉宁窗/汉明窗/布莱克曼窗）")
print("4. 显示模式（线性谱/对数谱dB）")
print("5. 频谱自动验证（对于正弦波）")
print("="*80)
print("使用说明：")
print("1. 选择信号类型（点击Sine/Square/Triangle/Noise按钮）")
print("2. 调节频率（10-2000Hz）和幅值（0-1）")
print("3. 点击'RUN'按钮显示波形和频谱")
print("4. 选择窗函数（Rect/Hanning/Hamming/Blackman）观察频谱变化")
print("5. 切换显示模式（Linear/Log）观察不同显示效果")
print("="*80)
print("验证提示：")
print("- 正弦波: 应在设定频率处有单一峰值")
print("- 方波: 包含奇次谐波（3f, 5f, 7f...）")
print("- 三角波: 包含奇次谐波，但衰减更快")
print("- 白噪声: 频谱应该是平坦的")
print("- 窗函数影响: 非矩形窗会展宽主瓣，但降低旁瓣")
print("="*80)

# 主循环
win.mainloop()
