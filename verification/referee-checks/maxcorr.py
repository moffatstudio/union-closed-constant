import numpy as np
# atoms order: [1, 0, y];  marginals p1=q, p0=(1-q)(1-d), py=(1-q)d
def rho(q,d,b_mode='prod'):
    p1=q; p0=(1-q)*(1-d); py=(1-q)*d
    e=py
    b=q*p0  # M(1,0)=M(0,1)
    a=p1-b
    dd=p0-py-b
    M=np.array([[a,b,0.],[b,dd,e],[0.,e,0.]])
    assert abs(M.sum()-1)<1e-12, M.sum()
    m=M.sum(1)
    assert np.allclose(m,[p1,p0,py]), (m,[p1,p0,py])
    assert (M>=-1e-15).all(), M
    Q=M/np.sqrt(np.outer(m,m))
    s=np.linalg.svd(Q,compute_uv=False)
    return s
for d in [1e-1,1e-2,1e-3,1e-4,1e-6]:
    s=rho(0.617,d)
    print("delta=%.0e  singular values:"%d, np.round(s,6))
