# src/visualizer.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window

def plot_time(y, fs, title="Sinal no tempo"):
    t = np.arange(len(y)) / fs
    plt.figure(figsize=(10, 4))
    plt.plot(t, y, linewidth=1.5)
    plt.title(title)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_fft(y, fs, title="Espectro (FFT)"):
    if len(y) == 0:
        return
    w = get_window('hann', len(y))
    Y = np.fft.rfft(y * w)
    f = np.fft.rfftfreq(len(y), d=1/fs)
    mag = 20 * np.log10(np.maximum(np.abs(Y), 1e-12))
    plt.figure(figsize=(10, 4))
    plt.plot(f, mag, linewidth=1.0)
    plt.title(title)
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def dominant_freq(y, fs):
    if len(y) == 0:
        return 0.0
    Y = np.fft.rfft(y * np.hanning(len(y)))
    f = np.fft.rfftfreq(len(y), d=1/fs)
    idx = np.argmax(np.abs(Y))
    return float(f[idx])
