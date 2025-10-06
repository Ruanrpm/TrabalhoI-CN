import math
import sympy as sp

# Transforma a função do arquivo .txt em uma função que possa ser usada em PY

def cria_funct():
    with open("arq_leitura.txt", "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines() if linha.strip()]

    functFdx = linhas[0]
    functPdx = linhas[1]
    parametros = [float(v) for v in linhas[2:]]

    def FdeX(x):
        return eval(functFdx, {
            "x": x,
            "exp": math.exp,
            "cos": math.cos,
            "sin": math.sin,
            "tan": math.tan,
            "log": math.log,
            "sqrt": math.sqrt
        })
    
    def PdeX(x):
        return eval(functPdx, {
            "x": x,
            "exp": math.exp,
            "cos": math.cos,
            "sin": math.sin,
            "tan": math.tan,
            "log": math.log,
            "sqrt": math.sqrt
        })
    
    x = sp.symbols('x')
    exprF = sp.sympify(functFdx, locals={
        "exp": sp.exp,
        "cos": sp.cos,
        "sin": sp.sin,
        "tan": sp.tan,
        "log": sp.log,
        "sqrt": sp.sqrt
    })
    d_FdeX = sp.diff(exprF, x)

    def dFdeX(x_val):
        return float(d_FdeX.evalf(subs={x: x_val}))


    return FdeX, dFdeX, PdeX, parametros

FdeX, dFdeX, PdeX, prmt = cria_funct()

# Metodo da Bissecção

def bissecao(i , p, it):
    meio = 0
    k = 0
    if(abs(i[1] - i[0]) < p):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Bissecao':<15}{meio:<20f}{k:<15}\n")
        return
    
    while((abs(i[1] - i[0]) > p) and k < it):
        k+=1
        meio = (i[0] + i[1])/2
        finicio = FdeX(i[0])
        fmeio = FdeX(meio)

        if((finicio * fmeio) <= 0):
            i[1] = meio
        else:
            i[0] = meio 

    with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{'Bissecao':<15}{meio:<20f}{k:<15}\n")

# Metodo MIL

def Mil(x0, p, it, k=1):
    if(abs(FdeX(x0)) < p):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'MIL':<15}{x0:<20f}{k:<15}\n")
        return
    
    xn = PdeX(x0)

    if(abs(FdeX(xn)) < p or abs(xn - x0) < p or k >= it):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'MIL':<15}{x0:<20f}{k:<15}\n")
        return
    
    Mil(xn, p, it, k+1)

# Metodo de Newton

def newton(x0, p, it):
    k = 1
    fx = FdeX(x0)
    
    if(abs(fx) > p):
        k = 1
        fxlinha = dFdeX(x0)

        if (fxlinha == 0):
            raise ValueError("Derivada nula! O método de Newton falhou.")

        x1 = x0 - (fx/fxlinha)
        fx = FdeX(x1)

        while(abs(fx) > p and abs(x1 - x0) > p and k <= it):
            k += 1
            x0 = x1
            fx = FdeX(x0)     
            fxlinha = dFdeX(x0)
            x1 = x0 - (fx/fxlinha)
            fx = FdeX(x1)
        raiz = x1

    else:
        raiz = x0

    with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Newton':<15}{abs(raiz):<20f}{k:<15}\n")

# Metodo da secante

def secante(x0, x1, p, it, k=1):
    if(abs(FdeX(x0)) < p):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"A raiz aproximada é: {x0}\n O numero de iterações foi: {k}")
            arquivo.write(f"{'Secante':<15}{x0:<20f}{k:<15}\n")
        return
    
    if(abs(FdeX(x1)) < p or abs(x1 - x0) < p  or k > it):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Secante':<15}{x0:<20f}{k:<15}\n")
        return
    
    x2 = x1 - ((FdeX(x1)*(x1-x0)) / (FdeX(x1)-FdeX(x0)))

    if(abs(FdeX(x2)) < p or abs(x2 - x1) < p or k > it):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Secante':<15}{x0:<20f}{k:<15}\n")
        return
    
    secante(x1, x2, p, it, k+1)

# Metodo regula falsi

def r_falsi(i, p1, p2, it, k=1):
    if(abs(i[1]-i[0]) < p1):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Regula Falsi':<15}{(i[0]+i[1])/2:<20f}{k:<15}\n")
        return
    
    if(abs(FdeX(i[0])) < p2 or abs(FdeX(i[1])) < p2):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Regula Falsi':<15}{i[0]:<20f}{k:<15}\n")
        return
    
    m = FdeX(i[0])
    x = (i[0]*FdeX(i[1]) - i[1]*FdeX(i[0])) / (FdeX(i[1]) - FdeX(i[0]))

    if(abs(FdeX(x)) < p2 or k > it):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Regula Falsi':<15}{x:<20f}{k:<15}\n")
        return
    
    if(m*FdeX(x) > 0):
        i[0] = x
    else:
        i[1] = x
    
    if(abs(i[1] - i[0]) < p1):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Regula Falsi':<15}{i[1]:<20f}{k:<15}\n")
        return
    r_falsi(i[:], p1, p2, it, k+1)

def main():
    intervalo = [prmt[0], prmt[1]]
    with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{'Método':<15}{'Raiz Aproximada':<20}{'Iterações':<15}\n")


    bissecao(intervalo, prmt[2], prmt[3])
    Mil(prmt[1], prmt[2], prmt[3])
    newton(prmt[0], prmt[2], prmt[3])
    secante(prmt[0], prmt[1], prmt[2], prmt[3])
    r_falsi(intervalo, prmt[2], prmt[2], int(prmt[3]))

if __name__ == "__main__":
    main()
