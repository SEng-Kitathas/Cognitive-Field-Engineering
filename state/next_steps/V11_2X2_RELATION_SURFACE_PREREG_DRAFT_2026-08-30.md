# CFE v1.1 2×2 Relation × Surface Redesign — Preregistration Draft

Status: **DRAFT FOR BUILD; NOT YET SCIENTIFICALLY STARTED**
Parent evidence: completed v1.0 six-seed screen + hostile causal autopsy.

## Question

Does true cognitive-neighborhood co-visibility change learned phenotype after local nuisance surface/context homogeneity is independently controlled?

## Factors

### Factor A — RELATION
- `TRUE_NEIGHBORHOOD`: all four matched cells derive from the same latent neighborhood.
- `STRICT_CROSS_NEIGHBORHOOD`: the four matched cells preserve family/domain/cell/assistant-target roles but derive from distinct neighborhoods.

### Factor B — SURFACE
- `LOCAL_HOMOGENIZED`: nuisance surface anchor/context identity is held common across the four cells where that can be done without changing latent cell truth or target semantics.
- `LOCAL_DIVERSIFIED`: nuisance surface anchors/context realizations are distinct across the four cells, matched in distribution and burden.

## Four arms

1. `TRUE_NEIGHBORHOOD__SURFACE_HOMOGENIZED`
2. `TRUE_NEIGHBORHOOD__SURFACE_DIVERSIFIED`
3. `STRICT_CROSS_NEIGHBORHOOD__SURFACE_HOMOGENIZED`
4. `STRICT_CROSS_NEIGHBORHOOD__SURFACE_DIVERSIFIED`

The v1.0 treatment is closest to arm 1. The v1.0 control is closest to arm 4. Arms 2 and 3 are the missing counterfactuals needed to separate relation from surface diversity.

## Non-negotiable construction rules

- Start from a new descendant branch. Do not rewrite v1.0 sealed inputs/results.
- Preserve the same semantic cell roles and assistant targets across all four arms.
- Preserve family/domain composition exactly.
- Preserve the global source/content multiset wherever logically possible; where nuisance realization must be synthesized/remapped, record exact transformation lineage.
- Nuisance anchor changes must be semantically inert with respect to the task answer.
- Prove no label leakage is introduced by surface remapping.
- Packing disabled.
- Same base model and exact pinned revision unless a new project explicitly changes the scientific question.
- Same LoRA profile unless preregistered qualification requires a new screen.
- Same evaluator and evaluation cases for direct comparability, with any new diagnostic slices declared secondary.

## Required pretraining gates

1. **Semantic invariance gate**
   - For every surface-remapped example, parsed latent cell key and assistant target must remain identical to the source example.

2. **Factor-separation gate**
   - RELATION identity and SURFACE identity must be independently enumerable.
   - No arm may infer one factor deterministically from nuisance metadata not intended by the design.

3. **Surface-diversity gate**
   - Within-block lexical/context diversity must match the intended SURFACE factor.
   - The two RELATION levels under the same SURFACE level should be as closely matched as possible on measured lexical Jaccard, token counts, and anchor-count distribution.

4. **Burden gate**
   - paired/quadrupled sequence count, supervised-token burden, sequence length, and target burden must be equal or explicitly bounded and preregistered.

5. **Strict-control exhaustive audit**
   - enumerate legal cross-neighborhood assignments and verify distinct-neighborhood constraints with no target/cell violations.

6. **Leakage scan**
   - nuisance anchors, IDs, ordering, filenames, and serialization must not reveal arm identity to the learner.

7. **Runtime replay**
   - exact tokenizer replay and deterministic one-step repeatability before scientific training.

## Primary contrasts

Primary inferential unit remains paired seed/run.

For structural combined outcome:

- **RELATION main effect**: average(TRUE_NEIGHBORHOOD) − average(STRICT_CROSS_NEIGHBORHOOD), marginalizing over SURFACE.
- **SURFACE main effect**: average(HOMOGENIZED) − average(DIVERSIFIED), marginalizing over RELATION.
- **RELATION×SURFACE interaction**: whether the relation effect changes sign/magnitude across surface levels.

The interaction is load-bearing because v1.0 may have bundled relation with local surface homogeneity.

## Secondary outcomes

Report separately:
- independent field
- LHIT
- retention
- family/domain slices
- treatment-only/control-only case flips
- repeated case asymmetry across seeds

Do not use secondary slices to redefine the primary contrast after seeing outcomes.

## Seed strategy

Do not reuse the v1.0 six seeds as if they were unseen confirmation.

Before execution, choose and freeze a new balanced seed schedule with arm-order counterbalancing across the four arms. The schedule must be generated mechanically before any v1.1 outcome is observed.

## Stop / extension rule

No adaptive extension based on favorable outcomes.

Choose the Stage-1 seed count and any one-time extension rule before scientific training. If compute permits, prefer enough independent seeds to estimate the 2×2 interaction rather than relying on a three-seed sign rule.

## Promotion ceiling

A positive RELATION main effect under matched SURFACE levels would support a narrower claim that true-neighborhood grouping contributes beyond local surface homogeneity under this exact regime.

A SURFACE main effect without RELATION would demote the abstract neighborhood claim and identify local context diversity/homogeneity as the stronger mechanism.

A strong interaction would mean neither factor has a context-free effect and future CFE design must treat their coupling as part of the mechanism.

No result from this screen alone promotes general reasoning, external cognitive transfer, AI CORE, or Microseed claims.

## Immediate build actions

1. Build a surface-remapping compiler that operates only on nuisance realization while preserving latent cell/target truth.
2. Generate four candidate arm datasets from the same source pool.
3. Run semantic-invariance, factor-separation, burden, leakage, and exhaustive control gates.
4. Produce a locked v1.1 input manifest and preregistration artifact.
5. Only then qualify runtime and start scientific training.