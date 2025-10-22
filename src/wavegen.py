# src/wavegen.py
import numpy as np

def gerar_onda(frequencia: float,
               duracao: float = 0.1,
               taxa: int = 44100,
               amplitude: float = 0.5,
               fase: float = 0.0) -> np.ndarray:
    """
    Gera uma senoide: y(t) = A * sin(2π f t + fase)
    - frequencia: Hz
    - duracao: segundos
    - taxa: amostras/segundo
    - amplitude: 0..1
    - fase: radianos
    """
    n = int(taxa * duracao)
    t = np.linspace(0, duracao, n, endpoint=False)
    y = amplitude * np.sin(2 * np.pi * frequencia * t + fase)
    return y
