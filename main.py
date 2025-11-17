from methods.metodsCap02 import*
import tkinter as tk
from view.telaInicial import CriarTelaInicial
from view.cap2_tkt import criarTelaCap2
from view.cap3_tkt import criarTelaCap3 

def mostrar_tela(frame):
    frame.tkraise()

janela = tk.Tk()
janela.title("Calculus Numerical Methods")
janela.geometry("400x300")

container = tk.Frame(janela)
container.pack(fill="both", expand=True)

tela_inicial = CriarTelaInicial(container, 
                                  lambda: mostrar_tela(tela1), 
                                  lambda: mostrar_tela(tela2))

tela1 = criarTelaCap2(container, lambda: mostrar_tela(tela_inicial))
tela2 = criarTelaCap3(container, lambda: mostrar_tela(tela_inicial))

for frame in (tela_inicial, tela1, tela2):
    frame.place(relheight=1, relwidth=1)

mostrar_tela(tela_inicial)
janela.mainloop()

# def main():
#     intervalo = [prmt[0], prmt[1]]

#     with open("arquivos/arq_escrita.txt", "a", encoding="utf-8") as arquivo:
#         arquivo.write(f"{'Método':<15}{'Raiz Aproximada':<20}{'Iterações':<15}\n")


#     secante(prmt[0], prmt[1], prmt[2], prmt[3])
#     newton(prmt[0], prmt[2], prmt[3])
#     bissecao(intervalo, prmt[2], prmt[3])
#     Mil(prmt[1], prmt[2], prmt[3])
#     r_falsi(intervalo, prmt[2], prmt[2], prmt[3])

#     escrever_resultados()

# if __name__ == "__main__":
#     main()
