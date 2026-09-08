"""
Splits the 3x3 (c, m) certification grid across two processes (machine rule: at most 2
concurrent). Usage: python certify_batch.py A   /   python certify_batch.py B
"""
import sys
from certify_ideal import run_cell, C_VALUES, M_VALUES

ALL_COMBOS = [(c, m) for c in C_VALUES for m in M_VALUES]  # 9 combos

def main(half):
    combos = ALL_COMBOS[0::2] if half == "A" else ALL_COMBOS[1::2]
    print("certify driver %s: %d combos: %s" % (half, len(combos), combos), flush=True)
    for c, m in combos:
        run_cell(c, m)
    print("certify driver %s: DONE" % half, flush=True)

if __name__ == "__main__":
    main(sys.argv[1])
