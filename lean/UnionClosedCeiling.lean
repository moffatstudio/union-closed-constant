import UnionClosedCeiling.Entropy
import UnionClosedCeiling.Framework
import UnionClosedCeiling.Ceiling
import UnionClosedCeiling.Refined
import UnionClosedCeiling.Classes

/-!
# A ceiling for single-letter protocol arguments (Sections 2.2 and 3 of the paper)

Main results:

* `UnionClosedCeiling.product_ceiling`   -- Theorem 3.1 (product ceiling)
* `UnionClosedCeiling.hiding_bound`      -- Theorem 3.4, inequality (H)
* `UnionClosedCeiling.diagonal_bound`    -- Theorem 3.4, inequality (D)
* `UnionClosedCeiling.fixed_point_form`  -- Theorem 3.4, the fixed-point form
* `UnionClosedCeiling.refined_ceiling_numeric` -- Theorem 3.4, `c ≤ 0.3829`
* `UnionClosedCeiling.containsProduct_*`, `UnionClosedCeiling.admitsHiding_*` -- Lemma 3.3
-/

#print axioms UnionClosedCeiling.product_ceiling
#print axioms UnionClosedCeiling.hiding_bound
#print axioms UnionClosedCeiling.diagonal_bound
#print axioms UnionClosedCeiling.fixed_point_form
#print axioms UnionClosedCeiling.refined_ceiling_numeric
#print axioms UnionClosedCeiling.containsProduct_iidClass
#print axioms UnionClosedCeiling.containsProduct_allCouplings
#print axioms UnionClosedCeiling.containsProduct_mixtureOfProducts
#print axioms UnionClosedCeiling.admitsHiding_allCouplings
#print axioms UnionClosedCeiling.admitsHiding_mixtureOfProducts
