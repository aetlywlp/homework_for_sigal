# HW3 - 信号分析作业

## 作业列表

### 1. 信号幅值域分析
**文件**: `signal_amplitude_analysis.py`

绘制四种信号的概率密度曲线(PDF)和概率分布曲线(CDF)：
- 白噪声信号
- 正弦波信号
- 方波信号
- 三角波信号

```bash
python signal_amplitude_analysis.py
```

---

### 2. 图像直方图均衡
**文件**: `image_histogram_equalization.py`

对光线质量不好的照片进行直方图均衡修正：
- HSV空间亮度通道均衡
- 原图与修正图对比
- RGB和灰度直方图对比

**使用前修改图片路径（第18行）**

```bash
python image_histogram_equalization.py
```

---

### 3. 相关函数性质验证
**文件**: `correlation_properties.py`

验证相关函数六条基本性质：
- a) 自相关函数是偶函数
- b) τ=0时自相关函数最大
- c) 周期信号自相关保持频率，丢失相位
- d) 噪声自相关快速衰减
- e) 同频信号互相关保留相位差
- f) 不同频率信号互不相关

```bash
python correlation_properties.py
```

---

### 4. 回波时差检测
**文件**: `echo_detection.py`

产生带回波信号，用自相关提取回波时差：
- 生成模拟音频信号
- 添加回波（延迟+衰减）
- 自相关函数检测延迟
- 输出WAV音频文件

```bash
python echo_detection.py
```

---

## 依赖库

```bash
pip install numpy matplotlib scipy pillow
```
