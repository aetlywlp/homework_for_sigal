import numpy as np
import matplotlib.pyplot as plt

def sin_wave(Fs, N, A, F, P):
    t = np.arange(N) / Fs
    y = A * np.sin(2 * np.pi * F * t + P * np.pi / 180)
    return t, y

def square_wave(Fs, N, A, F, P, duty=0.5):
    t = np.arange(N) / Fs
    phase = 2 * np.pi * F * t + P * np.pi / 180
    y = A * np.sign(np.sin(phase))
    return t, y

def triangle_wave(Fs, N, A, F, P):
    t = np.arange(N) / Fs
    phase = (F * t + P / 360) % 1
    y = A * (4 * np.abs(phase - 0.5) - 1)
    return t, y

def sawtooth_wave(Fs, N, A, F, P):
    t = np.arange(N) / Fs
    phase = (F * t + P / 360) % 1
    y = A * (2 * phase - 1)
    return t, y

def white_noise(Fs, N, A):
    t = np.arange(N) / Fs
    y = A * 0.333 * np.random.randn(N)
    return t, y

Fs = 44100
N = 4096
A = 1.0
F = 100
P = 0

fig, axes = plt.subplots(5, 1, figsize=(12, 10))

t1, y1 = sin_wave(Fs, N, A, F, P)
axes[0].plot(t1[:1000], y1[:1000], 'b-', linewidth=1.5)
axes[0].set_title(f'Sine Wave - Frequency: {F} Hz, Amplitude: {A}')
axes[0].set_ylabel('Amplitude')
axes[0].grid(True)

t2, y2 = square_wave(Fs, N, A, F, P, 0.5)
axes[1].plot(t2[:1000], y2[:1000], 'r-', linewidth=1.5)
axes[1].set_title(f'Square Wave - Frequency: {F} Hz, Amplitude: {A}')
axes[1].set_ylabel('Amplitude')
axes[1].grid(True)

t3, y3 = triangle_wave(Fs, N, A, F, P)
axes[2].plot(t3[:1000], y3[:1000], 'g-', linewidth=1.5)
axes[2].set_title(f'Triangle Wave - Frequency: {F} Hz, Amplitude: {A}')
axes[2].set_ylabel('Amplitude')
axes[2].grid(True)

t4, y4 = sawtooth_wave(Fs, N, A, F, P)
axes[3].plot(t4[:1000], y4[:1000], 'm-', linewidth=1.5)
axes[3].set_title(f'Sawtooth Wave - Frequency: {F} Hz, Amplitude: {A}')
axes[3].set_ylabel('Amplitude')
axes[3].grid(True)

t5, y5 = white_noise(Fs, N, A)
axes[4].plot(t5[:1000], y5[:1000], 'k-', linewidth=0.8)
axes[4].set_title(f'White Noise - Amplitude: {A}')
axes[4].set_ylabel('Amplitude')
axes[4].set_xlabel('Time (s)')
axes[4].grid(True)

plt.tight_layout()
plt.savefig('signal_output.png', dpi=150)
print("Signal generator created 5 waveforms, image saved as signal_output.png")

plt.show()

print("\nSignal Parameters:")
print(f"Sampling rate: {Fs} Hz")
print(f"Number of samples: {N}")
print(f"Amplitude: {A}")
print(f"Frequency: {F} Hz")
