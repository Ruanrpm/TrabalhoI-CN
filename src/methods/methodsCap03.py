import numpy as np
import time


# ============== MÉTODOS DIRETOS ==============

def gauss_eliminacao(A, b):
    """
    Resolve Ax = b usando Eliminação de Gauss sem pivoteamento.
    Lança exceção se encontrar pivô nulo ou matriz singular.
    Retorna tuple (x, tempo_execucao, info).
    """
    inicio = time.time()
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    
    # Fazer cópias para não alterar originais
    A_work = A.copy()
    b_work = b.copy()

    try:
        # Eliminação (forward elimination)
        for k in range(n - 1):
            if abs(A_work[k, k]) < 1e-15:
                raise ValueError(f"Pivô nulo na linha {k}. Matriz singular ou mal condicionada.")
            for i in range(k + 1, n):
                fator = A_work[i, k] / A_work[k, k]
                A_work[i, k:] = A_work[i, k:] - fator * A_work[k, k:]
                b_work[i] = b_work[i] - fator * b_work[k]

        # Retrosubstituição (back substitution)
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            if abs(A_work[i, i]) < 1e-15:
                raise ValueError(f"Pivô nulo na linha {i}. Matriz singular.")
            x[i] = (b_work[i] - np.dot(A_work[i, i + 1:], x[i + 1:])) / A_work[i, i]

        tempo = time.time() - inicio
        return x, tempo, "OK"
    except Exception as e:
        tempo = time.time() - inicio
        raise


def gauss_pivoteamento_parcial(A, b):
    """
    Resolve Ax = b usando Gauss com Pivoteamento Parcial.
    Busca o maior elemento em cada coluna para melhor estabilidade numérica.
    Retorna tuple (x, tempo_execucao, info).
    """
    inicio = time.time()
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    
    A_work = A.copy()
    b_work = b.copy()

    try:
        # Eliminação com pivoteamento parcial
        for k in range(n - 1):
            # Encontrar linha com maior valor absoluto (pivô)
            max_idx = k + np.argmax(np.abs(A_work[k:, k]))
            
            # Trocar linhas
            A_work[[k, max_idx]] = A_work[[max_idx, k]]
            b_work[[k, max_idx]] = b_work[[max_idx, k]]
            
            if abs(A_work[k, k]) < 1e-15:
                raise ValueError(f"Pivô nulo na linha {k}. Matriz singular.")
            
            # Eliminação
            for i in range(k + 1, n):
                fator = A_work[i, k] / A_work[k, k]
                A_work[i, k:] = A_work[i, k:] - fator * A_work[k, k:]
                b_work[i] = b_work[i] - fator * b_work[k]

        # Retrosubstituição
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            if abs(A_work[i, i]) < 1e-15:
                raise ValueError(f"Pivô nulo na linha {i}. Matriz singular.")
            x[i] = (b_work[i] - np.dot(A_work[i, i + 1:], x[i + 1:])) / A_work[i, i]

        tempo = time.time() - inicio
        return x, tempo, "OK"
    except Exception as e:
        tempo = time.time() - inicio
        raise


def gauss_pivoteamento_completo(A, b):
    """
    Resolve Ax = b usando Gauss com Pivoteamento Completo.
    Busca o maior elemento em toda a matriz para máxima estabilidade.
    Retorna tuple (x, tempo_execucao, info).
    """
    inicio = time.time()
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    
    A_work = A.copy()
    b_work = b.copy()
    permutacoes = list(range(n))  # Rastrear trocas de colunas

    try:
        # Eliminação com pivoteamento completo
        for k in range(n - 1):
            # Encontrar maior elemento em A_work[k:, k:]
            submatriz = np.abs(A_work[k:, k:])
            max_i, max_j = np.unravel_index(np.argmax(submatriz), submatriz.shape)
            max_i += k
            max_j += k
            
            # Trocar linhas
            A_work[[k, max_i]] = A_work[[max_i, k]]
            b_work[[k, max_i]] = b_work[[max_i, k]]
            
            # Trocar colunas
            A_work[:, [k, max_j]] = A_work[:, [max_j, k]]
            permutacoes[k], permutacoes[max_j] = permutacoes[max_j], permutacoes[k]
            
            if abs(A_work[k, k]) < 1e-15:
                raise ValueError(f"Pivô nulo na posição ({k},{k}). Matriz singular.")
            
            # Eliminação
            for i in range(k + 1, n):
                fator = A_work[i, k] / A_work[k, k]
                A_work[i, k:] = A_work[i, k:] - fator * A_work[k, k:]
                b_work[i] = b_work[i] - fator * b_work[k]

        # Retrosubstituição
        x_temp = np.zeros(n)
        for i in range(n - 1, -1, -1):
            if abs(A_work[i, i]) < 1e-15:
                raise ValueError(f"Pivô nulo na linha {i}. Matriz singular.")
            x_temp[i] = (b_work[i] - np.dot(A_work[i, i + 1:], x_temp[i + 1:])) / A_work[i, i]

        # Reordenar solução conforme trocas de colunas
        x = np.zeros(n)
        for i in range(n):
            x[permutacoes[i]] = x_temp[i]

        tempo = time.time() - inicio
        return x, tempo, "OK"
    except Exception as e:
        tempo = time.time() - inicio
        raise


def decomposicao_LU(A, b):
    """
    Resolve Ax=b via decomposição LU (sem pivoteamento).
    Fatora A em L*U onde L é triangular inferior e U é triangular superior.
    Retorna tuple (x, tempo_execucao, info).
    """
    inicio = time.time()
    A = A.astype(float)
    b = b.astype(float)
    n = len(A)
    
    try:
        L = np.eye(n)
        U = A.copy()

        # Decomposição
        for k in range(n - 1):
            if abs(U[k, k]) < 1e-15:
                raise ValueError(f"Pivô nulo na linha {k}. Decomposição LU falhou.")
            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]

        # Ly = b (forward substitution)
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i, :i], y[:i])

        # Ux = y (back substitution)
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            if abs(U[i, i]) < 1e-15:
                raise ValueError(f"Pivô nulo na linha {i}. Matriz singular.")
            x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

        tempo = time.time() - inicio
        return x, tempo, "OK"
    except Exception as e:
        tempo = time.time() - inicio
        raise


def cholesky(A, b):
    """
    Resolve Ax = b via Decomposição de Cholesky.
    A deve ser simétrica e definida positiva.
    Fatora A em L*L^T onde L é triangular inferior.
    Retorna tuple (x, tempo_execucao, info).
    """
    inicio = time.time()
    A = A.astype(float)
    b = b.astype(float)
    n = len(A)
    
    try:
        # Verificar se A é simétrica
        if not np.allclose(A, A.T):
            raise ValueError("Matriz não é simétrica. Cholesky requer matriz simétrica.")
        
        L = np.zeros_like(A)

        # Decomposição de Cholesky
        for i in range(n):
            for j in range(i + 1):
                soma = np.dot(L[i, :j], L[j, :j])
                if i == j:
                    valor = A[i, i] - soma
                    if valor < 1e-15:
                        raise ValueError("Matriz não é definida positiva (diagonal não positiva).")
                    L[i, j] = np.sqrt(valor)
                else:
                    if abs(L[j, j]) < 1e-15:
                        raise ValueError("Matriz não é definida positiva.")
                    L[i, j] = (A[i, j] - soma) / L[j, j]

        # Ly = b (forward substitution)
        y = np.zeros(n)
        for i in range(n):
            y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]

        # L^T x = y (back substitution)
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(L.T[i, i + 1:], x[i + 1:])) / L[i, i]

        tempo = time.time() - inicio
        return x, tempo, "OK"
    except Exception as e:
        tempo = time.time() - inicio
        raise


# ============== MÉTODOS ITERATIVOS ==============

def gauss_jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resolve Ax=b pelo método de Gauss-Jacobi (iterativo).
    Retorna tuple (x, num_iteracoes, historico, tempo_execucao, info, erro_final).
    """
    inicio = time.time()
    A = A.astype(float)
    b = b.astype(float)
    n = len(A)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    historico = []
    erro = None

    try:
        for k in range(max_iter):
            x_new = np.zeros(n)
            for i in range(n):
                if abs(A[i, i]) < 1e-15:
                    raise ValueError(f"Elemento diagonal A[{i},{i}] é nulo. Método de Jacobi não aplicável.")
                s = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i + 1:], x[i + 1:])
                x_new[i] = (b[i] - s) / A[i, i]

            historico.append(x_new.copy())
            erro = np.linalg.norm(x_new - x, ord=np.inf)

            if erro < tol:
                tempo = time.time() - inicio
                return x_new, k + 1, historico, tempo, "Convergiu", erro

            x = x_new

        tempo = time.time() - inicio
        info_msg = f"Não convergiu em {max_iter} iterações. Último erro: {erro:.2e}"
        return x, max_iter, historico, tempo, info_msg, erro
    except Exception as e:
        tempo = time.time() - inicio
        raise


def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resolve Ax=b pelo método de Gauss-Seidel (iterativo).
    Retorna tuple (x, num_iteracoes, historico, tempo_execucao, info, erro_final).
    """
    inicio = time.time()
    A = A.astype(float)
    b = b.astype(float)
    n = len(A)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    historico = []
    erro = None

    try:
        for k in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                if abs(A[i, i]) < 1e-15:
                    raise ValueError(f"Elemento diagonal A[{i},{i}] é nulo. Método de Seidel não aplicável.")
                s1 = np.dot(A[i, :i], x[:i])
                s2 = np.dot(A[i, i + 1:], x_old[i + 1:])
                x[i] = (b[i] - s1 - s2) / A[i, i]

            historico.append(x.copy())
            erro = np.linalg.norm(x - x_old, ord=np.inf)

            if erro < tol:
                tempo = time.time() - inicio
                return x, k + 1, historico, tempo, "Convergiu", erro

        tempo = time.time() - inicio
        info_msg = f"Não convergiu em {max_iter} iterações. Último erro: {erro:.2e}"
        return x, max_iter, historico, tempo, info_msg, erro
    except Exception as e:
        tempo = time.time() - inicio
        raise


# ============== FUNÇÕES DE ENTRADA/SAÍDA ==============

def carregar_matriz_vetor(caminho_matriz, caminho_vetor=None):
    """
    Carrega matriz A de um arquivo e vetor b de outro (ou do mesmo se tiver formato estendido).
    Formato esperado:
    - Se caminho_vetor é None: arquivo contém matriz aumentada [A|b] (A + b em colunas contíguas)
    - Se caminho_vetor é fornecido: matriz em um arquivo, vetor em outro
    
    Retorna (A, b) como arrays numpy.
    """
    try:
        if caminho_vetor is None:
            # Carregar matriz aumentada
            dados = np.loadtxt(caminho_matriz)
            if dados.ndim == 1:
                raise ValueError("Arquivo deve conter matriz 2D ou matriz aumentada.")
            A = dados[:, :-1]
            b = dados[:, -1]
        else:
            # Carregar matriz e vetor separadamente
            A = np.loadtxt(caminho_matriz)
            b = np.loadtxt(caminho_vetor)
            
            if A.ndim != 2:
                raise ValueError("Arquivo de matriz deve conter dados 2D.")
            if b.ndim != 1:
                b = b.flatten()
            
            if len(A) != len(b):
                raise ValueError(f"Tamanho da matriz ({len(A)}) não corresponde ao vetor ({len(b)}).")
        
        if len(A) != len(A[0]):
            raise ValueError("Matriz deve ser quadrada.")
        
        return A.astype(float), b.astype(float)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Arquivo não encontrado: {e}")
    except Exception as e:
        raise ValueError(f"Erro ao carregar dados: {e}")


def validar_matriz_convergencia(A):
    """
    Verifica se a matriz é diagonalmente dominante (suficiente para convergência de métodos iterativos).
    Retorna True se for diagonalmente dominante, False caso contrário.
    """
    n = len(A)
    for i in range(n):
        soma_linha = np.sum(np.abs(A[i, :i])) + np.sum(np.abs(A[i, i+1:]))
        if abs(A[i, i]) < soma_linha:
            return False
    return True
