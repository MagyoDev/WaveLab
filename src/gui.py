# src/gui.py
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd

from src.wavegen import gerar_onda
from src.transmitter_fsk import text_to_bits, bits_para_audio
from src.decoder_fsk import (
    record_seconds,
    decode_bits_from_audio_v2,
    bits_to_text,
    strip_preamble
)
from src.visualizer import plot_time, plot_fft, dominant_freq

FS_DEFAULT = 44100

class WaveLabGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WaveLab — FSK Toolkit")
        self.geometry("520x360")

        pad = {'padx': 8, 'pady': 6}
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, **pad)

        ttk.Label(frm, text="Mensagem a transmitir:").grid(row=0, column=0, sticky="w")
        self.msg_var = tk.StringVar(value="")
        ttk.Entry(frm, textvariable=self.msg_var, width=40).grid(row=0, column=1, columnspan=2, sticky="we")

        ttk.Label(frm, text="F0 (Hz) bit 0:").grid(row=1, column=0, sticky="w")
        self.f0_var = tk.StringVar(value="1000")
        ttk.Entry(frm, textvariable=self.f0_var, width=10).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="F1 (Hz) bit 1:").grid(row=2, column=0, sticky="w")
        self.f1_var = tk.StringVar(value="2000")
        ttk.Entry(frm, textvariable=self.f1_var, width=10).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="SYMBOL (s):").grid(row=3, column=0, sticky="w")
        self.sym_var = tk.StringVar(value="0.10")
        ttk.Entry(frm, textvariable=self.sym_var, width=10).grid(row=3, column=1, sticky="w")

        ttk.Label(frm, text="FS (Hz):").grid(row=4, column=0, sticky="w")
        self.fs_var = tk.StringVar(value=str(FS_DEFAULT))
        ttk.Entry(frm, textvariable=self.fs_var, width=10).grid(row=4, column=1, sticky="w")

        btnfrm = ttk.Frame(frm)
        btnfrm.grid(row=5, column=0, columnspan=3, sticky="we", pady=10)
        ttk.Button(btnfrm, text="Transmitir (FSK)", command=self.on_tx).grid(row=0, column=0, padx=5)
        ttk.Button(btnfrm, text="Visualizar (tempo)", command=self.on_view_time).grid(row=0, column=1, padx=5)
        ttk.Button(btnfrm, text="Visualizar (FFT)", command=self.on_view_fft).grid(row=0, column=2, padx=5)
        ttk.Button(btnfrm, text="Decodificar do microfone", command=self.on_rx).grid(row=0, column=3, padx=5)

        self.status = tk.StringVar(value="Pronto.")
        ttk.Label(frm, textvariable=self.status).grid(row=6, column=0, columnspan=3, sticky="w")

        for c in range(3):
            frm.grid_columnconfigure(c, weight=1)

        self._last_audio = np.array([], dtype=float)

    def get_params(self):
        try:
            f0 = float(self.f0_var.get())
            f1 = float(self.f1_var.get())
            sym = float(self.sym_var.get())
            fs = int(float(self.fs_var.get()))
            if sym <= 0 or fs < 8000:
                raise ValueError
            return f0, f1, sym, fs
        except Exception:
            messagebox.showerror("Erro", "Parâmetros inválidos. Verifique F0, F1, SYMBOL e FS.")
            raise

    def on_tx(self):
        def _tx():
            try:
                msg = self.msg_var.get()
                f0, f1, sym, fs = self.get_params()
                bits = text_to_bits(msg)
                audio = bits_para_audio(bits, F0=f0, F1=f1, SYMBOL=sym, fs=fs, amp=0.4)
                self._last_audio = audio
                self.status.set(f"TX {len(bits)} bits | duração ~ {len(audio)/fs:.2f}s")
                sd.play(audio, fs); sd.wait()
                self.status.set("Transmissão concluída.")
            except Exception as e:
                self.status.set(f"Erro TX: {e}")
        threading.Thread(target=_tx, daemon=True).start()

    def on_view_time(self):
        if self._last_audio.size == 0:
            messagebox.showinfo("Info", "Transmita algo primeiro (gera áudio) para visualizar.")
            return
        f0, f1, sym, fs = self.get_params()
        plot_time(self._last_audio, fs, title="FSK no tempo")

    def on_view_fft(self):
        if self._last_audio.size == 0:
            messagebox.showinfo("Info", "Transmita algo primeiro (gera áudio) para visualizar.")
            return
        f0, f1, sym, fs = self.get_params()
        plot_fft(self._last_audio, fs, title="FSK — Espectro (FFT)")
        dom = dominant_freq(self._last_audio, fs)
        self.status.set(f"Frequência dominante ≈ {dom:.1f} Hz")

    def on_rx(self):
        def _rx():
            try:
                f0, f1, sym, fs = self.get_params()
                msg_len = max(1, len(self.msg_var.get()))
                seconds = msg_len*8*sym + 0.8
                y = record_seconds(seconds=seconds, fs=fs)
                bits = decode_bits_from_audio_v2(y, fs=fs, F0=f0, F1=f1, SYMBOL=sym)
                bits_sem = strip_preamble(bits, preamble="10101010")
                text = bits_to_text(bits_sem)
                self.status.set(f"RX: bits={len(bits)} | texto='{text}'")
                messagebox.showinfo("Recepção",
                    f"Bits (primeiros 64): {bits[:64]}\nBits sem pré-âmbulo: {bits_sem[:64]}\n\nTexto:\n{text}")
            except Exception as e:
                self.status.set(f"Erro RX: {e}")
        threading.Thread(target=_rx, daemon=True).start()

def main():
    app = WaveLabGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
