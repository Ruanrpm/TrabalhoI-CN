import math
import sympy as sp

resultados = {
    "Secante": [],
    "Newton": [],
    "Bissecao": [],
    "MIL": [],
    "Regula Falsi": []
}

def escrever_resultados():
    metodos = list(resultados.keys())
    max_iters = max(len(v) for v in resultados.values())

    with open("arq_escrita.txt", "a", encoding="utf-8") as arq:
        arq.write("Método:       " + "".join(f"{m:<20}" for m in metodos) + "\n")

        for i in range(max_iters):
            linha_raiz = "Raiz:         "
            linha_it = "Iteração:     "
            for m in metodos:
                if i < len(resultados[m]):
                    raiz, it = resultados[m][i]
                    if(raiz == 'Inf'):
                        linha_raiz += f"{'Inf':<20}"
                    else:
                        linha_raiz += f"{raiz:<20.6f}"
                    linha_it += f"{it:<20}"
                else:
                    linha_raiz += f"{'':<20}"
                    linha_it += f"{'':<20}"
            arq.write(linha_raiz + "\n")
            arq.write(linha_it + "\n\n")


# Transforma a função do arquivo .txt em uma função que possa ser usada em PY

def cria_funct():
    with open("arq_leitura.txt", "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines() if linha.strip()]

    functFdx = linhas[0]
    parametros = [float(v) for v in linhas[1:]]

    def FdeX(x):
        try:
            return eval(functFdx, {
                "x": x,
                "exp": math.exp,
                "cos": math.cos,
                "sin": math.sin,
                "tan": math.tan,
                "log": math.log,
                "sqrt": math.sqrt
            })
        except OverflowError:
            return float('inf') 
    
    def PdeX(x):
        return x - FdeX(x)
    
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

# Metodo da secante

def secante(x0, x1, p, it, k=1):

    if(abs(FdeX(x0)) < p):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo: 
            resultados["Secante"].append((x0, k))
            arquivo.write(f"{'Secante':<15}{x0:<20f}{k:<15}\n")
        return
    
    if(abs(FdeX(x1)) < p or abs(x1 - x0) < p  or k > it):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            resultados["Secante"].append((x0, k))
            arquivo.write(f"{'Secante':<15}{x0:<20f}{k:<15}\n")
        return
    
    x2 = x1 - ((FdeX(x1)*(x1-x0)) / (FdeX(x1)-FdeX(x0)))

    if(abs(FdeX(x2)) < p or abs(x2 - x1) < p or k > it):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            resultados["Secante"].append((x0, k))
            arquivo.write(f"{'Secante':<15}{x0:<20f}{k:<15}\n")
        return
    
    resultados["Secante"].append(((x1+x2)/2, k))    
    secante(x1, x2, p, it, k+1)

# Metodo de Newton

def newton(x0, p, it):
    fx = FdeX(x0)
    
    if(abs(fx) > p):
        k = 1
        fxlinha = dFdeX(x0)

        if (fxlinha == 0):
            raise ValueError("Derivada nula! O método de Newton falhou.")

        x1 = x0 - (fx/fxlinha)
        fx = FdeX(x1)

        while(abs(fx) > p and abs(x1 - x0) > p and k <= it):
            x0 = x1
            fx = FdeX(x0)     
            fxlinha = dFdeX(x0)
            x1 = x0 - (fx/fxlinha)
            fx = FdeX(x1)
            resultados["Newton"].append((x1, k))
            k += 1
        raiz = x1

    else:
        raiz = x0
        resultados["MIL"].append((raiz, k))

    with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{'Newton':<15}{raiz:<20f}{k:<15}\n")


# Metodo da Bissecção

def bissecao(i , p, it):
    meio = 0
    k = 0
    if(abs(i[1] - i[0]) < p):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            resultados["Bissecao"].append((meio, k))
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
        resultados["Bissecao"].append((meio, k))


    with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{'Bissecao':<15}{meio:<20f}{k:<15}\n")

# Metodo MIL

def Mil(x0, p, it, k=1):
    if(abs(FdeX(x0)) < p):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            resultados["MIL"].append((x0, k))
            arquivo.write(f"{'MIL':<15}{x0:<20f}{k:<15}\n")
        return
    
    if(FdeX(x0) == float('inf')):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            resultados["MIL"].append(("Inf", k))
            arquivo.write(f"{'MIL':<15}{'Inf':<20}{k:<15}\n")
        return
    
    xn = PdeX(x0)

    if(abs(FdeX(xn)) < p or abs(xn - x0) < p or k >= it):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            resultados["MIL"].append((xn, k))
            arquivo.write(f"{'MIL':<15}{xn:<20f}{k:<15}\n")
        return
    elif(FdeX(xn) == float('inf')):
        with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
            resultados["MIL"].append(('Inf', k))
            arquivo.write(f"{'MIL':<15}{'Inf':<20}{k:<15}\n")
        return
    
    resultados["MIL"].append((xn, k))
    Mil(xn, p, it, k+1)

# Metodo regula falsi

def r_falsi(i, p1, p2, it):
    k = 1
    while (True):

        if(abs(i[0] - i[1]) < p1):
            with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
                resultados["Regula Falsi"].append((i[1], k))
                arquivo.write(f"{'Regula Falsi':<15}{i[1]:<20f}{k:<15}\n\n")
            return 

        if(abs(FdeX(i[0])) < p2 or abs(FdeX(i[1])) < p2):
            with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
                resultados["Regula Falsi"].append((i[0], k))
                arquivo.write(f"{'Regula Falsi':<15}{i[0]:<20f}{k:<15}\n\n")
            return 

        m = FdeX(i[0])
        x = (i[0]*FdeX(i[1]) - i[1]*m) / (FdeX(i[1]) - m)
        
        if(abs(FdeX(x)) < p2 or k > it):
            with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
                resultados["Regula Falsi"].append((i[x], k))
                arquivo.write(f"{'Regula Falsi':<15}{x:<20f}{k:<15}\n\n")
            return
         
        if(m*FdeX(x) > 0):
            i[0] = x
        else:
            i[1] = x

        if(abs(i[1] - i[0]) < p1):
            with open("arq_escrita.txt", "a", encoding="utf-8") as arquivo:
                resultados["Regula Falsi"].append(((i[1]+i[0])/2, k))
                arquivo.write(f"{'Regula Falsi':<15}{((i[1]+i[0])/2):<20f}{k:<15}\n\n")
            return 
        
        resultados["Regula Falsi"].append(((i[1]+i[0])/2, k))
        k = k + 1



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
