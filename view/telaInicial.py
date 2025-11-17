import tkinter as tk

def CriarTelaInicial(container, mostrar_tela1, mostrar_tela2):
    frame = tk.Frame(container)
    tk.Label(frame, text="Tela Inicial").pack(pady=20)
    tk.Button(frame, text="Metodos cap 02", command=mostrar_tela1).pack(pady=10)
    tk.Button(frame, text="Metodos cap 03", command=mostrar_tela2).pack(pady=10)
    return frame
