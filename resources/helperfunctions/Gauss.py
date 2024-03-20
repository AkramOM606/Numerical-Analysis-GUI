# Made By : ADRANE Akram & HARCHA Badr-Eddine

import numpy as np

def triangularisation(A,b):
    n=len(A)
    for k in range(n):
        pivot =A[k][k]

        for i in range(k + 1, n):

            b[i] = b[i] - (((A[i][k]) / pivot) * b[k])

            facteur = A[i][k] / pivot
            for j in range(n):

                A[i][j] = A[i][j] - (facteur * A[k][j])

    return A,b

def verifier_triangularisation(A):
    for i in range(len(A)):
        for j in range(i):
            if A[i][j]!=0:
                return False
    return True

def resoudre_equation_gauss(A,b):
    n=len(b)
    x=np.zeros(n)
    if verifier_triangularisation(A)==False:
        triangularisation(A,b)
    x[n - 1] = b[n - 1] / A[n - 1][n - 1]

    for i in range(n - 2, -1, -1):
        s = b[i]

        for j in range(i + 1, n):
            s = s - A[i][j] * x[j]

        x[i] = s / A[i][i]

    return x