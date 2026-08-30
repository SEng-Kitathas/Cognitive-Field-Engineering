# CFE v1.1 Neighborhood-Concentration Dose Screen — Preregistration Draft

Status: **DRAFT CANDIDATE; NOT SCIENTIFICALLY STARTED**

## Why this replaces the naive 2×2 draft

The v1.0 hostile autopsy found that `neighborhood_id` is curator-only and is not serialized to the learner. Same-neighborhood membership is embodied through shared world/context realization: common review code, common capacity/incoming regime, common version/base-state realization, and related visible state.

Therefore a factorial design that independently varies “true neighborhood” and “surface homogeneity” risks removing the learner-visible carrier of neighborhood identity. That would make one factor scientifically empty or require a new explicit neighborhood marker that changes the task.

The cleaner next question is a dose question that uses only existing source experiences:

> How does the number of distinct source neighborhoods co-visible inside a four-cell block change learned phenotype when the global learner-visible experience multiset, family/domain/cell target burden, and model/training regime are held fixed?

## Arms

Every arm uses all 288 source experiences exactly once.

### `K1_TRUE_NEIGHBORHOOD`
Four matched cells come from one source neighborhood.
- distinct neighborhoods per block: 1
- closest to v1.0 `TREATMENT_NEIGHBORHOOD`

### `K2_PAIRED_NEIGHBORHOODS`
Four matched cells are split 2+2 across two source neighborhoods.
- distinct neighborhoods per block: 2
- missing middle dose in v1.0
- cell-pair assignment must rotate across the three possible 2+2 partitions so no fixed cell pairing defines the arm

### `K4_STRICT_SCRAMBLE`
Four matched cells come from four distinct source neighborhoods.
- distinct neighborhoods per block: 4
- closest to v1.0 `CONTROL_STRICT_CELL_SCRAMBLE`

## Load-bearing invariants

For every arm:
- exactly 72 learner-visible sequences;
- exactly four user/assistant cell pairs per sequence;
- exactly the same 288 source experiences globally;
- exactly the same family/domain/cell/assistant-target multiset;
- each source experience appears exactly once per arm;
- global learner-visible individual-experience multiset is exactly identical across K1/K2/K4;
- cell order and assistant-target sequence are matched within each paired block index;
- no curator metadata enters the learner stream;
- no outcome-based control or offset selection.

## K2 balancing law

Use an offset of 4 between the two neighborhoods and rotate the three 2+2 cell partitions across blocks:
- partition A: cells 0,1 from neighborhood i; cells 2,3 from i+4
- partition B: cells 0,2 from neighborhood i; cells 1,3 from i+4
- partition C: cells 0,3 from neighborhood i; cells 1,2 from i+4

The rotation must be deterministic and fixed before token/evaluation outcomes are inspected.

## Primary causal question

Treat neighborhood concentration as an ordered dose `K ∈ {1,2,4}` rather than assuming a monotonic direction.

Primary outcome: structural combined accuracy at the paired seed/run level.

Primary planned contrasts:
- K1 − K4: replication of the old endpoint contrast on a fresh screen;
- K2 − midpoint(K1,K4): test for nonlinearity / intermediate optimum;
- ordered dose trend only if preregistered before outcomes.

## Family-level mechanism question

The v1.0 post-hoc result motivates, but does not prove, family-specific response:
- `warrant_vs_taint` favored K1-like grouping;
- `bounded_transport` strongly favored K4-like grouping, especially on LHIT;
- `dependency_currentness` was largely saturated.

These family slices are secondary in v1.1 unless a separate primary family-specific screen is preregistered.

## Evaluation freshness

Do **not** treat the already-inspected v1.0 evaluation surface as blind confirmation.

Before v1.1 scientific training:
- generate a new independent evaluation field with a fresh seed and preferably fresh domain/entity vocabulary;
- generate a fresh LHIT surface from the same source laws but new nuisance values/domains;
- seal evaluation artifacts before training;
- do not tune K2 construction or training hyperparameters from new evaluation outcomes.

Old v1.0 evaluation may be retained as a secondary historical comparability surface only.

## Training

Default intent is to preserve the exact pinned base model, qualified LoRA profile, optimizer, epochs, microbatch, accumulation, packing rule, determinism, and no-eval-during-training contract unless a new runtime qualification explicitly changes them before the screen starts.

## Seed strategy

Use fresh seeds not previously used for v1.0 outcome-bearing runs.
Counterbalance K1/K2/K4 arm order across seeds mechanically.

Choose the independent seed count before training. Prefer enough seeds to distinguish a middle-dose effect from endpoint noise; do not use the old three-seed sign rule unchanged without justification.

## Promotion ceiling

A stable ordered or nonlinear concentration effect would support a narrow claim about local counterfactual concentration under this exact learner/compiler regime.

It would not by itself establish abstract relational representation, general reasoning improvement, external cognitive transfer, AI CORE, or Microseed applicability.

## Immediate build gates

1. Build deterministic K1/K2/K4 compiler from `field/v06/train_field.jsonl`.
2. Prove exact global experience-multiset equality and source-use equality across all three arms.
3. Prove K1/K2/K4 neighborhood-count topology for all 72 blocks.
4. Prove K2 partition rotation is balanced and not cell-confounded.
5. Run exact tokenizer burden audit using the qualified tokenizer.
6. Build fresh evaluation generator/surface before scientific training.
7. Freeze a new input lock and preregistration before any v1.1 outcome is observed.