# Liu's MATLAB scripts (not redistributed)

`liu_reproduce.py`, `concavity_ideal.py` and the transcript `literature/2306.08824_liu.md`
refer to three MATLAB files published by Jingbo Liu alongside arXiv:2306.08824. They are
his work and carry no licence, so they are not copied into this repository. Download them
from his page and verify the hashes:

| file | URL | SHA-256 |
|---|---|---|
| `frankl3.m` | https://jingbol.web.illinois.edu/frankl3.m | `5225e3d64590772e1c593d77efae9dd9405f2b385810a4983b8a536c9919e410` |
| `frankl5.m` | https://jingbol.web.illinois.edu/frankl5.m | `c9b2a929594f0f1ea9d05a4612a71b818c440035766c5a1a238fc150e5c67e7a` |
| `frankl7.m` | https://jingbol.web.illinois.edu/frankl7.m | `d48149ba4a864b602621715afd15f8f192b41b0f6f65b2ba5fcf4afda77f08d4` |

```
for f in frankl3 frankl5 frankl7; do curl -sO https://jingbol.web.illinois.edu/$f.m; done
sha256sum frankl*.m
```

Hashes recorded 2026-09-10. Nothing in this repository executes these files; the Python
reproductions (`code/liu_reproduce.py`, `code/concavity_ideal.py`) re-implement them.
