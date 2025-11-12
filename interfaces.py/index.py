import tkinter as tk
from cap2_tkt import butonCap2OnAction
from cap3_tkt import butonCap3OnAction

janela = tk.Tk()
janela.title("Home")
janela.geometry("400x300")

butonCap2 = tk.Button(janela, text="Capitulo 02", command=lambda: butonCap2OnAction(janela))
butonCap3 = tk.Button(janela, text="Capitulo 03", command=lambda: butonCap3OnAction(janela))

butonCap2.pack(pady=10)
butonCap3.pack(pady=10)

janela.mainloop()