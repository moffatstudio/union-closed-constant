import io
p = 'note.tex'
s = io.open(p, encoding='utf-8').read()
i = s.index('\\begin{table}')
j = s.index('\\end{table}') + len('\\end{table}')
rows = [
 r"adversary family & atom budget per component & $c=0.38284$ & $c=0.38288$\\\midrule",
 r"non-degenerate ($\E_\mu\ent(X)\ge10^{-3}$), 300--500 restarts & 4 & 1.0000733 & 1.0000085\\",
 r" & 5 & 1.0000733 & 1.0000085\\",
 r" & 6 & 1.0000733 & 1.0000085\\",
 r"hiding family $\mu_\delta$, $\delta\in\{10^{-2},\dots,10^{-6}\}$, $y\in\{0.05,0.2,0.5,0.7\}$ & exact & $\ge1.000073$ & ---\\",
 r"mixed laws (two-point $+$ tiny atom), seeded & 4 & 1.0000733 & ---\\\bottomrule",
]
caption = (r"\caption{Minimum of the ratio in Hypothesis~\ref{hyp:global} at $w=0.810222$ ($\beta=0.189778$). "
           r"Every minimiser found is the two-point law $0.893\,\delta_{0.6909}+0.107\,\delta_0$ with $q\in\{0,1\}$; "
           r"the hiding family converges to its limit $2w(1-c)=1.000073$ from above.}")
table = ("\\begin{table}[h]\\centering\n\\begin{tabular}{llrr}\\toprule\n" + "\n".join(rows)
         + "\n\\end{tabular}\n" + caption + "\n\\end{table}")
s = s[:i] + table + s[j:]
io.open(p, 'w', encoding='utf-8').write(s)
print("table rewritten")
