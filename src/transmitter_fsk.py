# src/transmitter_fsk.py
import numpy as np
from src.wavegen import gerar_onda

PREAMBULO = "10101010"  # 8 bits alternando para sincronismo

def text_to_bits(texto: str) -> str:
    """Converte texto para bits (ASCII, 8 bits por caractere)."""
    return ''.join(f'{ord(c):08b}' for c in texto)

def aplicar_fade(y: np.ndarray, n: int = 256) -> np.ndarray:
    """Aplica fade-in/out com janela Hann (suaviza bordas do símbolo)."""
    y = y.copy()
    n = min(n, len(y) // 2)
    if n <= 0:
        return y
    w = np.hanning(2 * n)
    y[:n] *= w[:n]
    y[-n:] *= w[n:]
    return y

def bits_para_audio(bits: str,
                    F0: float = 1000.0,
                    F1: float = 2000.0,
                    SYMBOL: float = 0.1,
                    fs: int = 44100,
                    amp: float = 0.4) -> np.ndarray:
    """
    Concatena um tom por bit:
      - '0' -> F0 Hz
      - '1' -> F1 Hz
    Cada símbolo dura SYMBOL segundos.
    """
    # adiciona o préâmbulo
    bits = PREAMBULO + bits
    chunks = []
    for b in bits:
        f = F1 if b == '1' else F0
        tom = gerar_onda(f, duracao=SYMBOL, taxa=fs, amplitude=amp)
        chunks.append(aplicar_fade(tom, n=256))
    if not chunks:
        return np.array([], dtype=float)
    return np.concatenate(chunks)
