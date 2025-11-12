import tkinter as tk

def butonCap2OnAction(home):
    home.withdraw()
    janela = tk.Toplevel()
    janela.title("Capitulo 02")
    janela.geometry("400x300")
    tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)