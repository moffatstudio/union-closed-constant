# Numeric sanity checks for the iid entropy method (lead's own derivation, 2026-09-08)
import numpy as np
def h(x):
    x=np.clip(x,1e-300,1-1e-16); return -(x*np.log2(x)+(1-x)*np.log2(1-x))
phi=(1+5**0.5)/2; psi=(3-5**0.5)/2
u=np.linspace(1e-4,1-1e-4,1500); U,V=np.meshgrid(u,u)
# Claimed lemma: h(uv) >= (phi/2)(u h(v) + v h(u))
lhs=h(U*V); rhs=(phi/2)*(U*h(V)+V*h(U))
d=lhs-rhs; i=np.unravel_index(d.argmin(),d.shape)
print("min(lhs-rhs) =",d.min(),"at u,v =",U[i],V[i],"  (equality expected at u=v=1/phi=%.4f)"%(1/phi))
# Two-point extremal: U in {u0,1}, P(U=u0)=q. Violation iff q h(u0^2) < (2q-1) h(u0).
# minimal frequency p=q(1-u0) admitting a violation, as function of u0:
u0=np.linspace(0.01,1/phi-1e-6,2000); r=h(u0**2)/h(u0); p=(1-u0)/(2-r)
print("inf over two-point families of violating frequency p =",p.min(),"  psi =",psi)
