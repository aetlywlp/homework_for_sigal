"""
作业2扩展版: 麦克风/MP3音频频谱分析器
包含：
1. 麦克风实时采集和频谱分析
2. MP3/WAV文件播放和频谱分析
3. 窗函数选择
4. 线性/对数谱显示
"""
import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy.fft import rfft
from scipy import signal as sp_signal
import drvi.drviControlls as dr
import threading
import time

# 全局变量
current_data = None
current_fs = 44100
is_running = False
worker_thread = None
window_type = 0  # 0=矩形窗, 1=汉宁窗, 2=汉明窗, 3=布莱克曼窗
scale_type = 0  # 0=线性, 1=对数

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

# ========== 频谱计算和显示 ==========
def updateSpectrum():
    """更新频谱显示"""
    global current_data, current_fs, window_type, scale_type

    if current_data is None or len(current_data) == 0:
        return

    try:
        # 应用窗函数
        windowed_data = apply_window(current_data, window_type)

        # 计算FFT
        N = len(windowed_data)
        spectrum = np.fft.rfft(windowed_data)
        A = np.abs(spectrum) / (N / 2)
        A[0] = A[0] / 2

        # 频率轴
        df = current_fs / N
        f = np.arange(len(A)) * df

        # 根据scale_type显示
        if scale_type == 0:  # 线性谱
            mPlotAmp.setValue2D(f, A)
            max_val = max(A) if len(A) > 0 else 1
            mPlotAmp.setYlim(0, max_val * 1.2)
        else:  # 对数谱（dB）
            A_db = 20 * np.log10(A + 1e-10)  # 避免log(0)
            mPlotAmp.setValue2D(f, A_db)
            max_db = max(A_db[A_db > -60]) if len(A_db[A_db > -60]) > 0 else 0
            mPlotAmp.setYlim(-60, max_db + 10)

    except Exception as e:
        print(f"频谱计算错误: {e}")

# ========== 麦克风采集线程 ==========
class MicThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True

    def run(self):
        global current_data, current_fs, is_running
        try:
            import pyaudio

            Fs = 44100
            M = 4096
            current_fs = Fs

            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=Fs,
                          input=True, frames_per_buffer=M)

            print("麦克风采集已启动...")

            while self.running and is_running:
                try:
                    data = stream.read(M, exception_on_overflow=False)
                    samples = np.frombuffer(data, np.int16)
                    current_data = samples / 32768.0  # 归一化

                    # 显示波形
                    t = np.arange(len(current_data)) / Fs
                    mPlotWave.setValue2D(t, current_data)
                    mPlotWave.setYlim(-1, 1)

                    # 更新频谱
                    updateSpectrum()

                except Exception as e:
                    print(f"采集错误: {e}")

                time.sleep(0.05)

            stream.stop_stream()
            stream.close()
            p.terminate()
            print("麦克风采集已停止")

        except Exception as e:
            print(f"麦克风初始化错误: {e}")
            print("请确保：1) 已安装pyaudio (pip install pyaudio)  2) 麦克风已连接")

    def stop(self):
        self.running = False

# ========== MP3播放线程 ==========
class MP3Thread(threading.Thread):
    def __init__(self, filepath):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.filepath = filepath

    def run(self):
        global current_data, current_fs, is_running
        try:
            import librosa

            # 加载音频文件
            print(f"加载音频文件: {self.filepath}")
            y, sr = librosa.load(self.filepath, sr=44100, mono=True)
            current_fs = sr

            print(f"音频加载成功: 采样率={sr}Hz, 长度={len(y)/sr:.2f}秒")

            # 播放音频（分段显示）
            chunk_size = 4096
            hop_size = 2048
            total_samples = len(y)
            pos = 0

            while self.running and is_running and pos < total_samples:
                try:
                    # 提取当前片段
                    end_pos = min(pos + chunk_size, total_samples)
                    current_data = y[pos:end_pos]

                    # 显示波形
                    t = np.arange(len(current_data)) / sr
                    mPlotWave.setValue2D(t, current_data)
                    mPlotWave.setYlim(-1, 1)

                    # 更新频谱
                    updateSpectrum()

                    # 移动到下一片段
                    pos += hop_size
                    time.sleep(hop_size / sr)  # 按实际时间播放

                except Exception as e:
                    print(f"播放错误: {e}")
                    break

            print("音频播放完成")

        except Exception as e:
            print(f"MP3播放错误: {e}")
            print("请确保：1) 已安装librosa (pip install librosa)  2) 文件路径正确")

    def stop(self):
        self.running = False

# ========== 控制函数 ==========
def start_mic(v=None):
    """启动麦克风采集"""
    global is_running, worker_thread

    if is_running:
        print("已在运行中，请先停止...")
        return

    is_running = True
    worker_thread = MicThread()
    worker_thread.start()

def start_mp3(v=None):
    """选择并播放MP3文件"""
    global is_running, worker_thread

    if is_running:
        print("请先停止当前采集/播放")
        return

    # 文件选择对话框
    filepath = filedialog.askopenfilename(
        title="选择音频文件",
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg"), ("All Files", "*.*")]
    )

    if not filepath:
        return

    mEntryFile.setValueString(filepath)

    is_running = True
    worker_thread = MP3Thread(filepath)
    worker_thread.start()

def stop_all(v=None):
    """停止采集/播放"""
    global is_running, worker_thread

    is_running = False
    if worker_thread:
        worker_thread.stop()
        worker_thread = None

    print("已停止")

# ========== 窗函数选择 ==========
def set_window_rect(v):
    global window_type
    window_type = 0
    print("窗函数: 矩形窗")
    if current_data is not None:
        updateSpectrum()

def set_window_hanning(v):
    global window_type
    window_type = 1
    print("窗函数: 汉宁窗")
    if current_data is not None:
        updateSpectrum()

def set_window_hamming(v):
    global window_type
    window_type = 2
    print("窗函数: 汉明窗")
    if current_data is not None:
        updateSpectrum()

def set_window_blackman(v):
    global window_type
    window_type = 3
    print("窗函数: 布莱克曼窗")
    if current_data is not None:
        updateSpectrum()

# ========== 显示模式选择 ==========
def set_scale_linear(v):
    global scale_type
    scale_type = 0
    print("显示模式: 线性谱")
    if current_data is not None:
        updateSpectrum()

def set_scale_log(v):
    global scale_type
    scale_type = 1
    print("显示模式: 对数谱(dB)")
    if current_data is not None:
        updateSpectrum()

# ========== 创建GUI界面 ==========
win = tk.Tk()
win.geometry('1100x720')
win.config(bg="#ddeeee")
win.wm_title('作业2扩展版: 麦克风/MP3音频频谱分析器')

# 波形显示
mPlotWave = dr.DRPlot(win, 20, 20, 900, 300, 'Time Domain', 0, 0, 0, 0.1, -1, 1)

# 频谱显示
mPlotAmp = dr.DRPlot(win, 20, 330, 900, 300, 'Frequency Spectrum', 0, 0, 0, 5000, 0, 1)

# ========== 控制面板 ==========
# 控制按钮
dr.DRLabel(win, 930, 20, 150, 30, '#003355', '#ffffff', 'Control')
mBtnMic = dr.DRButton(win, 930, 50, 150, 40, '#006600', '#ffffff', 'Mic Start', 1)
mBtnMP3 = dr.DRButton(win, 930, 100, 150, 40, '#0066cc', '#ffffff', 'Open Audio', 2)
mBtnStop = dr.DRButton(win, 930, 150, 150, 40, '#cc0000', '#ffffff', 'Stop', 3)

# 文件路径显示
mEntryFile = dr.DREntryT(win, 20, 650, 600, 30, '#ffffff', '#000000', '')

# 窗函数选择
dr.DRLabel(win, 930, 200, 150, 30, '#003355', '#ffffff', 'Window Func')
mBtnWinRect = dr.DRButton(win, 930, 230, 150, 30, '#0066cc', '#ffffff', 'Rect', 10)
mBtnWinHanning = dr.DRButton(win, 930, 265, 150, 30, '#0066cc', '#ffffff', 'Hanning', 11)
mBtnWinHamming = dr.DRButton(win, 930, 300, 150, 30, '#0066cc', '#ffffff', 'Hamming', 12)
mBtnWinBlackman = dr.DRButton(win, 930, 335, 150, 30, '#0066cc', '#ffffff', 'Blackman', 13)

# 谱类型选择
dr.DRLabel(win, 930, 375, 150, 30, '#003355', '#ffffff', 'Scale Type')
mBtnLinear = dr.DRButton(win, 930, 405, 150, 40, '#cc6600', '#ffffff', 'Linear', 20)
mBtnLog = dr.DRButton(win, 930, 450, 150, 40, '#cc6600', '#ffffff', 'Log(dB)', 21)

# ========== 绑定事件 ==========
mBtnMic.addCallBackSingle(start_mic)
mBtnMP3.addCallBackSingle(start_mp3)
mBtnStop.addCallBackSingle(stop_all)

mBtnWinRect.addCallBackSingle(set_window_rect)
mBtnWinHanning.addCallBackSingle(set_window_hanning)
mBtnWinHamming.addCallBackSingle(set_window_hamming)
mBtnWinBlackman.addCallBackSingle(set_window_blackman)

mBtnLinear.addCallBackSingle(set_scale_linear)
mBtnLog.addCallBackSingle(set_scale_log)

# 打印使用说明
print("="*80)
print("作业2扩展版: 麦克风/MP3音频频谱分析器")
print("="*80)
print("功能特性：")
print("1. 麦克风实时采集和频谱分析")
print("2. MP3/WAV/FLAC音频文件播放和频谱分析")
print("3. 窗函数选择（矩形窗/汉宁窗/汉明窗/布莱克曼窗）")
print("4. 显示模式（线性谱/对数谱dB）")
print("="*80)
print("使用说明：")
print("1. 点击'Mic Start'开始麦克风采集（需要pyaudio）")
print("2. 点击'Open Audio'选择并播放音频文件（需要librosa）")
print("3. 点击'Stop'停止当前采集/播放")
print("4. 选择窗函数观察频谱变化")
print("5. 切换显示模式（Linear/Log）")
print("="*80)
print("依赖库安装：")
print("pip install pyaudio      # 麦克风采集")
print("pip install librosa      # 音频文件加载")
print("="*80)
print("注意事项：")
print("- 麦克风采集需要连接麦克风设备")
print("- 支持MP3/WAV/FLAC/OGG等格式音频文件")
print("- 可以播放音乐并实时观察频谱变化")
print("="*80)

# 主循环
win.mainloop()

# 确保退出时停止所有线程
is_running = False
if worker_thread:
    worker_thread.stop()
