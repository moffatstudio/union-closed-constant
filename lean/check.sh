#!/usr/bin/env bash
# Full verification: build, no `sorry`, no axioms beyond propext / Classical.choice / Quot.sound.
# Exits 0 only if everything passes.
set -uo pipefail
cd "$(dirname "$0")"

fail() { echo "FAIL: $1"; exit 1; }

echo "== 1. lake build =="
build_out=$(lake build 2>&1)
build_rc=$?
echo "$build_out" | grep -v '^trace:'
[ $build_rc -eq 0 ] || fail "lake build exited with $build_rc"

echo "== 2. no 'sorry' =="
if echo "$build_out" | grep -qi "declaration uses 'sorry'"; then
  fail "'sorry' reported by the build"
fi
if grep -rn "sorry" UnionClosedCeiling UnionClosedCeiling.lean AxiomCheck.lean; then
  fail "'sorry' occurs in the sources"
fi
echo "ok: no sorry in the build output or the sources"

echo "== 3. #print axioms =="
ax_out=$(lake env lean AxiomCheck.lean 2>&1)
ax_rc=$?
echo "$ax_out"
[ $ax_rc -eq 0 ] || fail "lake env lean AxiomCheck.lean exited with $ax_rc"

# every checked declaration must appear
n_decls=$(grep -c '^#print axioms' AxiomCheck.lean)
n_lines=$(echo "$ax_out" | grep -c "depends on axioms\|does not depend on any axioms")
[ "$n_decls" -eq "$n_lines" ] || fail "expected $n_decls axiom reports, got $n_lines"

bad=$(echo "$ax_out" | grep "depends on axioms" \
  | sed 's/.*\[\(.*\)\].*/\1/' | tr ',' '\n' | tr -d ' ' \
  | grep -v -x -e propext -e 'Classical.choice' -e 'Quot.sound' -e '')
if [ -n "$bad" ]; then
  echo "$bad"
  fail "disallowed axioms"
fi
echo "ok: only propext, Classical.choice, Quot.sound"

echo
echo "ALL CHECKS PASSED"
