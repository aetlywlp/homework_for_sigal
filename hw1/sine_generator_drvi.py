import tkinter as tk
import drvi.drviDSP as dsp
import drvi.drviControlls as dr

# 创建主窗口
win = tk.Tk()
win.geometry('1100x670')
win.config(bg="#ddeeee")
win.wm_title('DRVI Sine Wave Generator - Homework')

# DRPlot(win, x0, y0, w, h, title, t1, t2, x1, x2, t, x)
# 参数: 窗口, X, Y, 宽, 高, 标题, 参数1, 参数2, X轴最小值, X轴最大值, Y轴最小值, Y轴最大值
mPlotWave = dr.DRPlot(win, 20, 20, 900, 300, 'Waveform', 0, 0, 0, 0.1, -1.2, 1.2)

# 频率控制（100-2000 Hz）
dr.DRLabel(win, 930, 20, 150, 30, '#003355', '#ffffff', 'Frequency (Hz)')
mKnobFre = dr.DRKnob(win, 930, 50, 150, 150, '#004466', '#222222', '#aaaaaa', '100,2000', 100, 2000, 500)
mEntryFre = dr.DREntryD(win, 950, 210, 110, 30, '#ffffff', '#000000', 500)

# 幅值控制（0-1）
dr.DRLabel(win, 930, 250, 150, 30, '#003355', '#ffffff', 'Amplitude')
mKnobAmp = dr.DRKnob(win, 930, 280, 150, 150, '#004466', '#222222', '#aaaaaa', '0,1', 0, 1, 0.8)
mEntryAmp = dr.DREntryD(win, 950, 440, 110, 30, '#ffffff', '#000000', 0.8)

# 相位控制（0-180度）
dr.DRLabel(win, 930, 480, 150, 30, '#003355', '#ffffff', 'Phase (deg)')
mSliderPha = dr.DRHSlider(win, 20, 350, 900, 40, '#004466', '#222222', '#aaaaaa', 20, 20, 0, 180, 0)
mEntryPha = dr.DREntryD(win, 950, 520, 110, 30, '#ffffff', '#000000', 0)

# 运行按钮
mButton = dr.DRButton(win, 950, 580, 110, 40, '#004466', '#eeee00', 'Run', 101)

# DRGenerator(st, Fs, N, A, F, P)
# 参数: 信号类型, 采样频率, 采样长度, 幅值, 频率, 相位
# st: 0=正弦波, 1=方波, 2=三角波, 3=白噪声
mSignal = dsp.DRGenerator(0, 44100, 4096, 0.8, 500, 0)

# 定义一个包装函数来触发信号生成和显示
def updateWaveform(v=None):
    # 生成信号数据
    mSignal.genData()
    # 获取数据并显示
    t, data = mSignal.t, mSignal.data
    mPlotWave.setValue2D(t, data)

# ========== 直连绑定 ==========
# 按钮 -> 更新波形
mButton.addCallBackSingle(updateWaveform)

# 频率旋钮 -> 信号发生器
mKnobFre.addCallBackSingle(mSignal.setSignalFre)
mKnobFre.addCallBackSingle(mEntryFre.setValueSingle)

# 幅值旋钮 -> 信号发生器
mKnobAmp.addCallBackSingle(mSignal.setSignalAmp)
mKnobAmp.addCallBackSingle(mEntryAmp.setValueSingle)

# 相位滑块 -> 信号发生器
mSliderPha.addCallBackSingle(mSignal.setSignalPha)
mSliderPha.addCallBackSingle(mEntryPha.setValueSingle)

print("="*60)
print("DRVI可调正弦波信号发生器 - 作业")
print("="*60)
print("使用说明：")
print("1. 拖动旋钮调节频率（100-2000Hz）和幅值（0-1）")
print("2. 拖动滑块调节相位（0-180度）")
print("3. 点击'Run'按钮显示波形")
print("="*60)
print(f"初始参数：频率=500Hz, 幅值=0.8, 相位=0度")
print(f"采样频率：44100Hz, 采样点数：4096")
print("="*60)

# 主循环
win.mainloop()

