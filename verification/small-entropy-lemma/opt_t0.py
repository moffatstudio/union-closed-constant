from mpmath import mp, mpf, log, sqrt, findroot
mp.dps=40
w=mpf('0.810222'); c=mpf('0.38284'); C=mpf('1.00005')
ln2=log(2); r=(1-w)/w
def h(x):
    x=mpf(x)
    if x<=0 or x>=1: return mpf(0)
    return -(x*log(x)+(1-x)*log(1-x))/ln2
def Lt(u): return log(1/u)/ln2 + (1-u)/ln2
def Phi(t0):
    L0=Lt(t0)
    return 2/L0 + t0*(L0+1+t0/ln2)/L0
# largest t0 with Phi(t0)<=r
t0=findroot(lambda t: Phi(t)-r, mpf('0.006'))
print("t0* =",t0, " Phi=",Phi(t0), " r=",r, " Ltilde0=",Lt(t0))
G=(1-c)-C/(2*w)
eps0=G*h(t0)/(1-t0)
print("h(t0)=",h(t0))
print("G=",G)
print("eps0 =",eps0)
# safe rounded choices
for T in ['0.006','0.0060','0.00605','0.006058','0.00606']:
    T=mpf(T); print(T, "Phi<=r?",Phi(T)<=r, "eps0=",G*h(T)/(1-T))
