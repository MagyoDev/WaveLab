# src/decoder_fsk.py
import numpy as np
import sounddevice as sd
from scipy.signal import butter, filtfilt

def bits_to_text(bits: str) -> str:
    out = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        out.append(chr(int(byte, 2)))
    return ''.join(out)

def goertzel_power(sig, fs, freq):
    """Detector Goertzel simples (potência na freq)"""
    N = len(sig)
    if N == 0:
        return 0.0
    w = 2 * np.pi * freq / fs
    cosw = np.cos(w)
    s_prev = s_prev2 = 0.0
    for x in sig:
        s = x + 2 * cosw * s_prev - s_prev2
        s_prev2, s_prev = s_prev, s
    power = s_prev2**2 + s_prev**2 - 2 * cosw * s_prev * s_prev2
    return power / max(N, 1)

def decode_bits_from_audio(y, fs, F0=1000.0, F1=2000.0, SYMBOL=0.1):
    samples_per_symbol = int(SYMBOL * fs)
    if samples_per_symbol <= 0:
        raise ValueError("SYMBOL muito pequeno para a taxa de amostragem.")
    n_symbols = len(y) // samples_per_symbol
    bits = []
    for k in range(n_symbols):
        seg = y[k*samples_per_symbol:(k+1)*samples_per_symbol]
        if len(seg) > 4:
            seg = seg * np.hanning(len(seg))
        p0 = goertzel_power(seg, fs, F0)
        p1 = goertzel_power(seg, fs, F1)
        bits.append('1' if p1 > p0 else '0')
    return ''.join(bits)

def record_seconds(seconds=3.0, fs=44100):
    print(f"[RX] Gravando {seconds:.1f}s @ {fs} Hz...")
    audio = sd.rec(int(seconds*fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    return audio[:, 0]

# ---------- Versão v2 com filtro e limiar adaptativo ----------
def _butter_bandpass(low, high, fs, order=4):
    nyq = fs / 2
    b, a = butter(order, [low/nyq, high/nyq], btype='band')
    return b, a

def _filtrar_banda(y, fs, low, high):
    b, a = _butter_bandpass(low, high, fs)
    return filtfilt(b, a, y)

def decode_bits_from_audio_v2(y, fs, F0=1000.0, F1=2000.0, SYMBOL=0.1,
                              bw_hz=220, ratio_hi=0.58, ratio_lo=0.42):
    """Decodificação mais robusta com filtro passa-banda e limiar adaptativo."""
    if len(y) == 0:
        return ""
    y = y / np.max(np.abs(y)) if np.max(np.abs(y)) > 0 else y
    samples = int(SYMBOL * fs)
    bits = []
    for i in range(0, len(y), samples):
        seg = y[i:i+samples]
        if len(seg) < samples: break
        seg0 = _filtrar_banda(seg, fs, max(50, F0-bw_hz), F0+bw_hz)
        seg1 = _filtrar_banda(seg, fs, max(50, F1-bw_hz), F1+bw_hz)
        p0, p1 = np.mean(seg0**2), np.mean(seg1**2)
        ratio = p1 / (p0 + p1 + 1e-12)
        if ratio > ratio_hi:
            bits.append('1')
        elif ratio < ratio_lo:
            bits.append('0')
        else:
            bits.append(bits[-1] if bits else '0')
    return ''.join(bits)

def strip_preamble(bits: str, preamble="10101010"):
    """Remove a primeira ocorrência do pré-âmbulo no fluxo de bits."""
    idx = bits.find(preamble)
    if idx == -1:
        return bits
    return bits[idx+len(preamble):]
