# CFE v1.0 Hostile Causal Autopsy — 2026-08-30

Status: **POST-SCREEN ANALYSIS; NO SCIENTIFIC PROMOTION**
Mode: AUDIT / BUILD-PLAN

## Executive finding

The frozen six-seed v1.0 screen does **not** show a stable positive advantage for `TREATMENT_NEIGHBORHOOD` over `CONTROL_STRICT_CELL_SCRAMBLE`.

Structural TREATMENT-minus-CONTROL deltas by seed:
- 2026082501: +0.0500000000
- 2026082502: -0.0541666667
- 2026082503: +0.0375000000
- 2026082504: -0.1000000000
- 2026082505: +0.0500000000
- 2026082506: -0.1000000000

Secondary six-seed mean: about -0.01944. Signs: 3 positive / 3 negative.

Stage 2 independently qualified with zero execution-integrity failures. The negative/mixed scientific result is therefore not explained by a known execution-integrity failure.

## Case-level asymmetry

Across all six paired evaluations, discordant outcomes are not distributed uniformly across evaluation families.

### `bounded_transport` / `scheduler_buffer`
- TREATMENT-only correct: 11
- CONTROL-only correct: 82
- net discordance: **-71 for TREATMENT**

### `warrant_vs_taint` / `catalog_review`
- TREATMENT-only correct: 43
- CONTROL-only correct: 0
- net discordance: **+43 for TREATMENT**

### `dependency_currentness` / `shipping_manifest`
- TREATMENT-only correct: 0
- CONTROL-only correct: 0
- both correct: 288
- neither: 144

### By evaluation kind
- field: T-only 21, C-only 1, net **+20 TREATMENT**
- LHIT: T-only 33, C-only 81, net **-48 TREATMENT**
- retention: T-only 3, C-only 6, net **-3 TREATMENT**

The aggregate sign instability therefore hides a strong phenotype trade: TREATMENT helps one relational family while CONTROL strongly helps another, especially on LHIT.

## Repeated case asymmetry

Several LHIT cases are CONTROL-only correct in four of six seeds and never TREATMENT-only correct. This is not merely one noisy seed changing aggregate totals. A stable subset of the LHIT surface preferentially resolves under CONTROL.

Conversely, a smaller set of LHIT cases is repeatedly TREATMENT-only correct, and many catalog-review field cases become TREATMENT-only correct in seed 2026082505.

## Optimization-path checks

Training loss and gradient traces vary by seed and arm, including several isolated `NaN` gradient-norm log values in earlier runs. All affected runs completed and passed execution qualification.

Adapter geometry was inspected through the qualified CFE runtime:
- arm adapter norms are very close within each seed;
- T-vs-C adapter cosine similarity is about 0.984–0.991;
- correlation of structural delta with total-norm difference is weak (~0.18 at N=6);
- correlation with arm adapter distance is weak (~0.15);
- correlation with cosine is weak (~-0.15).

This does not support a simple explanation that the winning arm merely moved farther in adapter-weight space.

## Learner-visible block geometry

The treatment/control sidecars and compiled learner-visible JSONL expose a major identification seam.

The global learner-visible experience multiset is matched, but local block composition differs as intended by the intervention:

- TREATMENT: the four matched cells in a block come from the **same neighborhood**.
- CONTROL: the same four cell roles are filled from **different neighborhoods**.

This grouping also changes within-block surface/context diversity.

Measured on the 72 four-cell blocks:

### CONTROL_STRICT_CELL_SCRAMBLE
- mean pairwise lexical Jaccard among four user messages: **0.8961351**
- every block has four distinct user messages
- in the directly detected `Review X` anchor family, 24/24 blocks expose four distinct anchors

### TREATMENT_NEIGHBORHOOD
- mean pairwise lexical Jaccard among four user messages: **0.9687006**
- every block has four distinct user messages
- in the directly detected `Review X` anchor family, 24/24 blocks expose one repeated anchor

Example:
- TREATMENT block: `Review B` appears across all four matched cells.
- CONTROL counterpart: matched cells use `Review B`, `Review D`, `Review F`, `Review H`.

Across paired blocks, user-message position 0 is identical in all 72 pairs, while positions 1–3 differ in all 72 pairs.

## Interpretation

This is **not automatically a defect in the v1.0 treatment**. If the causal estimand is the full effect of grouping true neighborhood siblings into one learner-visible block, local contextual homogeneity is part of that intervention.

It **is** a blocker to a stronger claim that the result isolates abstract relational/neighborhood geometry independently of nuisance surface homogeneity or local contextual diversity.

The current screen cannot distinguish these mechanisms:
1. benefit/harm from true relational neighborhood co-visibility;
2. benefit/harm from repeated local surface anchors/context;
3. benefit/harm from increased within-block surface diversity in CONTROL;
4. interactions among those factors.

## Strongest current scientific statement

Under this exact CapybaraHermes/NF4/LoRA/compiler regime, changing four-cell local grouping while holding the global learner-visible experience multiset and supervised burden fixed produces large, family-specific phenotype changes. True-neighborhood grouping does **not** show a stable overall advantage across six paired seeds. It favors `warrant_vs_taint`/field behavior while strict cell-scramble strongly favors `bounded_transport`/LHIT behavior.

No broader claim about general CFE, abstract relational representation, or cognitive transfer is authorized.

## Redesign gate

The next clean experiment should decompose **latent neighborhood relation** from **local nuisance surface homogeneity** rather than adding more seeds to the completed v1.0 screen.

Recommended design: a preregistered 2×2 screen with factors:
- RELATION: true-neighborhood vs strict cross-neighborhood scramble
- SURFACE: locally homogenized vs locally diversified nuisance-anchor/context realization

The design must preserve the same cell/target burden, global content accounting, sequence/token burden as tightly as possible, and must prove that the SURFACE manipulation does not change the latent relational cells or targets.

This redesign is a new scientific branch. It must not rewrite the completed v1.0 artifacts.