import numpy as np

def definie_positive(A):
    valeur_propre=np.linalg.eigvals(A)
    return np.all(valeur_propre>0)

def symetrique(A):
    At=np.transpose(A)
    if np.array_equal(A,At):
        return True
    return False

def matric_L_Lt(A):
    n = len(A)
    l = np.zeros((n, n))
    l[0][0] = A[0][0] ** (1 / 2)

    for i in range(1, n):
        l[i][0] = A[i][0] / l[0][0]

    for i in range(1, n):
        somme1 = 0
        for k in range(0, i):
            somme1 = somme1 + (l[i][k] ** 2)

        l[i][i] = (A[i][i] - somme1) ** (1 / 2)

        for j in range(i + 1, n):
            somme2 = 0
            for k in range(0, i):
                somme2 += l[j][k] * l[i][k]

            l[j][i] = (A[j][i] - somme2) / l[i][i]

    return l,np.transpose(l)

def resolution_choleski(A,B):
    if not definie_positive(A):
        return "E"
    if not symetrique(A):
        return "E"
    n=len(A)
    L,Lt=matric_L_Lt(A)
    y = np.zeros(n)
    x = np.zeros(n)
    y = np.linalg.solve(L, B)
    x = np.linalg.solve(Lt,y)
    return x