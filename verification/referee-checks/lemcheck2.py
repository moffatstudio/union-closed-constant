import numpy as np
np.seterr(all='ignore')
def h(p):
    p=np.asarray(p,float); o=np.zeros_like(p); m=(p>0)&(p<1)
    o[m]=-(p[m]*np.log2(p[m])+(1-p[m])*np.log2(1-p[m])); return o
w=0.810222; c=0.38284; C=1.00005; t0=0.006; r=(1-w)/w
Lt=lambda u: np.log2(1/u)+(1-u)/np.log(2)
rho=(1-t0)/h(np.array([t0]))[0]
# Lemma 2
a=np.linspace(0,1,4000001); print("L2 max h(a)-2sqrt(a(1-a)) =",np.nanmax(h(a)-2*np.sqrt(a*(1-a))))
# Lemma 3
u=np.concatenate([np.logspace(-16,-1,300000),np.linspace(1e-6,1,300000)])
print("L3 min h(u)-u*Lt(u)      =",np.nanmin(h(u)-u*Lt(u)))
# Lemma 4 identity + Lemma 5 + (*) on log grid in (0,t0]^2
g=np.logspace(-16,np.log10(t0),1400)
T,Tp=np.meshgrid(g,g)
tau=T+Tp-T*Tp; A=T*(1-Tp); B=Tp*(1-T); gam=T*Tp/tau; alp=A/(A+B)
Lam_id=tau*h(gam)+(A+B)*h(alp)
Lam=h(T)+h(Tp)-h((1-T)*(1-Tp))
print("L4 max |identity error|  =",np.nanmax(np.abs(Lam_id-Lam)))
m=np.minimum(T,Tp)
bnd=2*np.sqrt(T*Tp)+T*Tp*(Lt(m)+1+m/np.log(2))
print("L5 max Lambda-bound      =",np.nanmax(Lam-bnd))
ratio=w*Lam/((1-w)*np.sqrt(h(T)*h(Tp)))
print("(*) max wLam/((1-w)sqrt(hh)) =",np.nanmax(ratio),"  (<1 required)")
# monotonicity claims of Lemma 6
mm=np.logspace(-16,np.log10(t0),200000)
d=np.log2(1/mm)-2*mm/np.log(2); print("L6 min d/dm[m*Lt(m)]     =",d.min(),"(>0 required)")
f1=np.sqrt(mm*Lt(mm)); f2=np.sqrt(mm)*(1+mm/np.log(2))/np.sqrt(Lt(mm))
print("L6 m-factor monotone     =",bool(np.all(np.diff(f1+f2)>=-1e-18)))
MM=np.logspace(-16,np.log10(t0),200000); fM=np.sqrt(MM)/np.sqrt(Lt(MM))
print("L6 M-factor monotone     =",bool(np.all(np.diff(fM)>=-1e-18)))
# Lemma 8
y=np.linspace(1e-9,1-t0,3000000); print("L8 max y/h(y) on (0,1-t0] =",np.nanmax(y/h(y)),"rho =",rho)
