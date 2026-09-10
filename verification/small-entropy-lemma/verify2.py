from mpmath import mp, mpf, log, sqrt
mp.dps=50
ln2=log(2)
def h(x):
    x=mpf(x)
    if x<=0 or x>=1: return mpf(0)
    return -(x*log(x)+(1-x)*log(1-x))/ln2
def Lt(u): return log(1/mpf(u))/ln2+(1-mpf(u))/ln2
w=mpf('0.810222')
# worst points from the grid: near diagonal corner, and tiny t
import itertools
t0=mpf('0.006')
bad=[]
for t in [t0, t0/2, mpf('1e-6'), mpf('1e-12'), mpf('1e-16')]:
    for tp in [t0, t0/2, mpf('1e-6'), mpf('1e-12'), mpf('1e-16')]:
        Lam=h(t)+h(tp)-h(t+tp-t*tp)
        bnd=2*sqrt(t*tp)+t*tp*(Lt(min(t,tp))+1+min(t,tp)/ln2)
        star=(1-w)*sqrt(h(t)*h(tp))-w*Lam
        bad.append((float(t),float(tp),float(bnd-Lam),float(star)))
for b in bad: print(b)
print("h(u)-u*Lt(u) at samples:", [float(h(u)-u*Lt(u)) for u in [mpf('1e-16'),mpf('1e-6'),mpf('0.006'),mpf('0.4')]])
