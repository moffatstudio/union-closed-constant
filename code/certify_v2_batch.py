import sys
from certify_v2 import part2, C1, C2

COMBOS = [(c, m) for c in (C1, C2) for m in (4, 5, 6)]  # 6 combos

def main(half):
    combos = COMBOS[0::2] if half == "A" else COMBOS[1::2]
    print("part2 driver %s: %d combos: %s" % (half, len(combos), combos), flush=True)
    for c, m in combos:
        part2(c, m, restarts=300)
    print("part2 driver %s: DONE" % half, flush=True)

if __name__ == "__main__":
    main(sys.argv[1])
