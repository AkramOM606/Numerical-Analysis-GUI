import numpy as np

def matrice_U(A):
    n = len(A)
    P = np.identity(n)
    U = np.zeros((n, n))
    for k in range(n - 1):
        M = np.identity(n)
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            M[i][k] = -factor
        A = np.dot(M, A)
        P = np.dot(M, P)

    U = A
    return U, P

def matrice_L(A):
    U, M = matrice_U(A)

    return np.linalg.inv(M)

def resolution_LU(A, B):
    U ,M= matrice_U(A)
    L = matrice_L(A)
    y = np.linalg.solve(L, B)
    x = np.linalg.solve(U,y)

    return x