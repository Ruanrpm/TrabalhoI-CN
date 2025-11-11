import numpy as np

# MÉTODOS DIRETOS

def gauss_eliminacao(A, b):
    """Resolve o sistema Ax = b usando Eliminação de Gauss."""
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)

    # Eliminação
    for k in range(n - 1):
        if A[k, k] == 0:
            raise ValueError("Pivô nulo! Troque as linhas.")
        for i in range(k + 1, n):
            fator = A[i, k] / A[k, k]
            A[i, k:] = A[i, k:] - fator * A[k, k:]
            b[i] = b[i] - fator * b[k]

    # Retrosubstituição
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x


def decomposicao_LU(A, b):
    """Resolve Ax=b via decomposição LU (sem pivoteamento)."""
    A = A.astype(float)
    n = len(A)
    L = np.eye(n)
    U = A.copy()

    # Decomposição
    for k in range(n - 1):
        if U[k, k] == 0:
            raise ValueError("Pivô nulo! Troque as linhas.")
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]

    # Ly = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])

    # Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

    return x


def cholesky(A, b):
    """Resolve Ax = b via Decomposição de Cholesky (A deve ser simétrica e definida positiva)."""
    A = A.astype(float)
    b = b.astype(float)
    n = len(A)
    L = np.zeros_like(A)

    # Decomposição de Cholesky
    for i in range(n):
        for j in range(i + 1):
            soma = np.dot(L[i, :j], L[j, :j])
            if i == j:
                L[i, j] = np.sqrt(A[i, i] - soma)
            else:
                L[i, j] = (A[i, j] - soma) / L[j, j]

    # Ly = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]

    # Lᵀx = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(L.T[i, i + 1:], x[i + 1:])) / L[i, i]

    return x

# MÉTODOS ITERATIVOS

def gauss_jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """Resolve Ax=b pelo método de Gauss-Jacobi."""
    n = len(A)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    historico = []

    for k in range(max_iter):
        x_new = np.zeros(n)
        for i in range(n):
            s = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - s) / A[i, i]

        historico.append(x_new.copy())

        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, k + 1, historico

        x = x_new

    raise ValueError("Método de Jacobi não convergiu em %d iterações" % max_iter)


def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """Resolve Ax=b pelo método de Gauss-Seidel."""
    n = len(A)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    historico = []

    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i + 1:], x_old[i + 1:])
            x[i] = (b[i] - s1 - s2) / A[i, i]

        historico.append(x.copy())

        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            return x, k + 1, historico

    raise ValueError("Método de Gauss-Seidel não convergiu em %d iterações" % max_iter)


A = np.array([[4, 1, 2],
              [3, 5, 1],
              [1, 1, 3]], dtype=float)
b = np.array([4, 7, 3], dtype=float)

xgaus = gauss_eliminacao(A.copy(), b.copy())
x_gauss = tuple(round(float(v), 4) for v in xgaus)
xlu = decomposicao_LU(A.copy(), b.copy())
x_lu = tuple(round(float(v), 4) for v in xlu)
xchol = cholesky(A.copy(), b.copy())
x_cholesky = tuple(round(float(v), 4) for v in xchol)
xjac, it_j, hj = gauss_jacobi(A, b)
x_jacobi = tuple(round(float(v), 4) for v in xjac)
xsaid, it_s, hs = gauss_seidel(A, b)
x_seidel = tuple(round(float(v), 4) for v in xsaid)

print("Gauss:", x_gauss)
print("LU:", x_lu)
print("Cholesky:", x_cholesky)
print("Jacobi:", x_jacobi, "em", it_j, "iterações")
print("Seidel:", x_seidel, "em", it_s, "iterações")
