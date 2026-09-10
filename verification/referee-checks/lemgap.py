from mpmath import mp, mpf, log
mp.dps=40
def H(p):
    p=mpf(p)
    if p<=0 or p>=1: return mpf(0)
    return -(p*log(p)+(1-p)*log(1-p))/log(2)
t0=mpf('0.006'); rho=(1-t0)/H(t0)
cstar=mpf('0.382885259967')
print("rho =",mp.nstr(rho,10))
print("\n eps0 = [2w(1-c)-C]/(2w rho);  best case C->1 gives eps0_max = [2w(1-c)-1]/(2w rho)")
print(" and 2w(1-c) <= (1-c)/(1-c**) since w < w0(c**)\n")
for c in ['0.38284','0.38288','0.3828840','0.3828850','0.38288526']:
    c=mpf(c)
    w_max=1/(2*(1-cstar))
    top=2*w_max*(1-c)          # sup of 2w(1-c) over admissible w
    eps_max=(top-1)/(2*w_max*rho)
    print("c=%s  sup 2w(1-c)=%s  eps0_max(C->1)=%s  >=1e-7: %s"%(
        mp.nstr(c,9), mp.nstr(top,12), mp.nstr(eps_max,6), eps_max>=mpf('1e-7')))
# threshold c where eps0_max drops below 1e-7
w=1/(2*(1-cstar))
# (1-c)/(1-cstar) - 1 = 2 w rho * 1e-7  ->  1-c = (1-cstar)(1+2 w rho 1e-7)
c_thr=1-(1-cstar)*(1+2*w*rho*mpf('1e-7'))
print("\nwindow closes only for c <= %s  (c** - %s)"%(mp.nstr(c_thr,12), mp.nstr(cstar-c_thr,4)))
# the paper's own C at 0.38284
w2=mpf('0.810222'); C=mpf('1.00005')
print("\nat c=0.38284, C=1.00005: eps0 =",mp.nstr(((1-mpf('0.38284'))-C/(2*w2))/rho,8))
