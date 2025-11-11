from metodsCap02 import*

def main():
    intervalo = [prmt[0], prmt[1]]

    with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{'Método':<15}{'Raiz Aproximada':<20}{'Iterações':<15}\n")


    secante(prmt[0], prmt[1], prmt[2], prmt[3])
    newton(prmt[0], prmt[2], prmt[3])
    bissecao(intervalo, prmt[2], prmt[3])
    Mil(prmt[1], prmt[2], prmt[3])
    r_falsi(intervalo, prmt[2], prmt[2], prmt[3])

    escrever_resultados()

if __name__ == "__main__":
    main()
