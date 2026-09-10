import numpy as np
from mpmath import mp, mpf, log, sqrt
mp.dps=40
w=mpf('0.810222'); c=mpf('0.38284'); C=mpf('1.00005')
ln2=log(2)
def h(x):
    x=mpf(x)
    if x<=0 or x>=1: return mpf(0)
    return -(x*log(x)+(1-x)*log(1-x))/ln2
twow=2*w
print("2w =",twow)
print("2w(1-c) =", twow*(1-c))
q0=C/twow
print("q0 = C/(2w) =",q0)
G=(1-c)-q0
print("G =",G)
# condition (*): w*Lam(t,t') <= (1-w)*sqrt(h(t)h(t')), Lam = h(t)+h(t')-h(1-(1-t)(1-t'))
r=(1-w)/w
print("(1-w)/w =",r)
def Lam(t,tp):
    tau=t+tp-t*tp
    return h(t)+h(tp)-h(tau)
def ratio(t,tp):
    return Lam(t,tp)/sqrt(h(t)*h(tp))
# diagonal: solve ratio(t,t)=r
import mpmath
f=lambda t: ratio(t,t)-r
t0=mpmath.findroot(f, mpf('0.007'))
print("diagonal critical t0 =",t0, " h(t0)=",h(t0))
print("eps0 candidate =", G*h(t0)/(1-t0))
