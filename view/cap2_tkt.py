import tkinter as tk

def criarTelaCap2(container, voltarTelaInicial):
    frame = tk.Frame(container)
    tk.Label(frame, text="Capitulo 02").pack(pady=20)
    tk.Button(frame, text="Voltar", command=voltarTelaInicial).pack(pady=10)
    return frame
    