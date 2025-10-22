# WaveLab

**WaveLab** é uma ferramenta experimental para visualização e transmissão de sinais analógicos e digitais simples, com foco em **modulação FSK (Frequency Shift Keying)**.
O projeto permite gerar, visualizar, transmitir e decodificar mensagens em forma de som.

---

## Funcionalidades

* **Geração de ondas analógicas** (senoides) com frequências configuráveis.
* **Transmissão FSK**: converte texto em sinais sonoros binários (0 e 1) usando duas frequências distintas.
* **Visualização no tempo e frequência** (FFT) para análise de sinais.
* **Decodificação via microfone**: recebe sinais FSK e reconstrói o texto original.
* **Interface gráfica (Tkinter)** para controle dos parâmetros e execução das funções.

---

## Estrutura do Projeto

```
WaveLab/
├── src/
├── main.py
│   ├── gui.py
│   ├── wavegen.py
│   ├── transmitter_fsk.py
│   ├── decoder_fsk.py
│   ├── visualizer.py
└── requirements.txt
```

---

## Requisitos

* Python 3.10 ou superior
* Bibliotecas:

  * `numpy`
  * `matplotlib`
  * `sounddevice`
  * `tkinter` (nativa no Python)

Instalação rápida:

```bash
pip install numpy matplotlib sounddevice
```

---

## Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/WaveLab.git
   cd WaveLab
   ```

2. Execute a aplicação:

   ```bash
   python main.py
   ```

---

## Uso

1. Digite uma mensagem na interface.
2. Configure as frequências (`F0` e `F1`), o tempo por símbolo (`SYMBOL`) e a taxa de amostragem (`FS`).
3. Clique em **Transmitir (FSK)** para gerar e tocar o som.
4. Use **Visualizar (tempo)** ou **Visualizar (FFT)** para analisar o sinal.
5. Use **Decodificar do microfone** para receber sinais sonoros e converter novamente em texto.

---

## Conceitos Principais

* **Amplitude:** intensidade do sinal.
* **Frequência:** número de ciclos por segundo (Hz).
* **FS (Sampling Rate):** quantas amostras por segundo o computador captura.
* **FSK:** modulação que representa bits (0 e 1) com frequências diferentes.

---

## Licença

Este projeto é distribuído sob a licença MIT.
Você é livre para usar, modificar e distribuir com os devidos créditos.