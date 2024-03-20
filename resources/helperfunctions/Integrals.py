def trapezes(a,b,f,h):
    if(b<a):
        c=a
        a=b
        b=c
    S=0
    for i in range(1,len(f)-1):
        S+=f[i]
    return(h/2 *(f[0]+2*S+f[-1]))

def simpson(a,b,f,h):
        if(b<a):
            c=a
            a=b
            b=c
        S1=0
        S2=0
        for i in range(2,len(f)-2,2):
            S1+=f[i]
        for i in range(1,len(f)-1,2):
            S2+=f[i]
        return(h/6 *(f[0]+2*S1+4*S2+f[-1]))