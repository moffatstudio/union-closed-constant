from mpmath import mp, mpf, log, sqrt
mp.dps=30
ln2=log(2)
def h(x):
    x=mpf(x)
    if x<=0 or x>=1: return mpf(0)
    return -(x*log(x)+(1-x)*log(1-x))/ln2
def Lt(u): return log(1/mpf(u))/ln2+(1-mpf(u))/ln2
w=mpf('0.810222'); c=mpf('0.38284'); C=mpf('1.00005'); t0=mpf('0.006')
r=(1-w)/w; L0=Lt(t0)
print("r=(1-w)/w      =",r)
print("Ltilde0        =",L0)
print("2/L0           =",2/L0)
print("second term    =",t0*(L0+1+t0/ln2)/L0)
print("Phi(t0)        =",2/L0+t0*(L0+1+t0/ln2)/L0)
print("h(t0)          =",h(t0))
print("rho            =",(1-t0)/h(t0))
G=(1-c)-C/(2*w)
print("2w             =",2*w)
print("2w(1-c)        =",2*w*(1-c))
print("C/(2w)         =",C/(2*w))
print("G              =",G)
print("G/rho          =",G*h(t0)/(1-t0))
