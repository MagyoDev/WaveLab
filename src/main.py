# src/main.py
import sounddevice as sd
from src.transmitter_fsk import text_to_bits, bits_para_audio

def tocar(y, fs=44100):
    if y.size == 0:
        return
    sd.play(y, fs)
    sd.wait()

def main():
    mensagem = "OI"              # troque aqui o texto que quer transmitir
    F0 = 1000.0                  # bit 0
    F1 = 2000.0                  # bit 1
    SYMBOL = 0.10                # 100 ms por bit (~10 bps)
    FS = 44100

    bits = text_to_bits(mensagem)
    print("Mensagem:", mensagem)
    print("Bits:", bits)

    audio = bits_para_audio(bits, F0=F0, F1=F1, SYMBOL=SYMBOL, fs=FS, amp=0.4)
    print("Amostras geradas:", audio.shape[0], f"({len(bits)} bits, ~{len(audio)/FS:.2f}s)")
    tocar(audio, fs=FS)

if __name__ == "__main__":
    main()
