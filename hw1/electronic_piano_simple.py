import numpy as np
import matplotlib.pyplot as plt

def generate_envelope(N, attack=0.1, decay=0.1, sustain=0.7, release=0.2):
    envelope = np.ones(N)
    attack_samples = int(N * attack)
    decay_samples = int(N * decay)
    release_samples = int(N * release)
    sustain_samples = N - attack_samples - decay_samples - release_samples

    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain, decay_samples)
    envelope[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = sustain
    envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)

    return envelope

def generate_piano_tone(freq, duration, Fs=44100, harmonics=[1, 0.5, 0.25, 0.125]):
    N = int(duration * Fs)
    t = np.arange(N) / Fs

    signal = np.zeros(N)
    for i, amp in enumerate(harmonics):
        signal += amp * np.sin(2 * np.pi * freq * (i+1) * t)

    signal = signal / np.max(np.abs(signal))
    envelope = generate_envelope(N)
    signal = signal * envelope * 0.3

    return t, signal

keys = {
    'C': 262, 'D': 294, 'E': 330, 'F': 349, 'G': 392, 'A': 440, 'B': 494,
    'C2': 523, 'D2': 587, 'E2': 659, 'F2': 698, 'G2': 784, 'A2': 880, 'B2': 988
}

print("Simple Electronic Piano (Visualization Version)")
print("Available notes:", list(keys.keys()))

demo_notes = ['C', 'E', 'G', 'C2']
print(f"\nGenerating demo melody: {demo_notes}")

fig, axes = plt.subplots(len(demo_notes), 1, figsize=(12, 10))

for i, note in enumerate(demo_notes):
    t, sig = generate_piano_tone(keys[note], 1.0)

    axes[i].plot(t[:5000], sig[:5000], linewidth=1)
    axes[i].set_title(f'Note: {note} ({keys[note]} Hz) with ADSR envelope and harmonics')
    axes[i].set_ylabel('Amplitude')
    axes[i].grid(True)

    env = generate_envelope(len(sig))
    axes[i].plot(t[:5000], env[:5000] * 0.3, 'r--', linewidth=1.5, alpha=0.7, label='Envelope')
    axes[i].legend()

axes[-1].set_xlabel('Time (s)')

plt.tight_layout()
plt.savefig('piano_output.png', dpi=150)
print(f"\nWaveforms saved as piano_output.png")
print(f"\nEach note includes:")
print(f"  - ADSR envelope (red dashed line)")
print(f"  - 4 harmonics at frequencies: f, 2f, 3f, 4f")
print(f"  - Harmonic amplitudes: 1.0, 0.5, 0.25, 0.125")

plt.show()
