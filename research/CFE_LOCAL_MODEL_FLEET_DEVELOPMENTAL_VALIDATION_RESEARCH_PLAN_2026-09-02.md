# CFE Local Model Fleet Developmental Validation Research Plan

Date: 2026-09-02 08:14 Eastern Daylight Time
Status: **ACTIVE RESEARCH PLAN / NOT TRAINING AUTHORIZATION**

## Purpose
Use the local model fleet as a future controlled multi-learner test of CFE, while preserving today's ugly behavior as pre-intervention phenotype evidence.

The research target is not "make every model better." It is:

> **Determine which CFE developmental-geometry effects reproduce, disappear, reverse, or change shape across different learner regimes.**

## Phase 0 — preserve baseline phenotype
Before any CFE fleet intervention:
- preserve representative autonomous-loop traces and failure artifacts;
- hash/freeze selected probes;
- separate execution bugs from model behavior;
- define scoring rubrics before intervention;
- include success cases so the probe set does not become a collection of cherry-picked failures.

Candidate probe families:
1. governing-question retention over long trajectories;
2. semantic basin capture / topic drift;
3. relevance discrimination;
4. evidence sufficiency / refusal to launder weak support;
5. contradiction recovery;
6. current-constraint retention;
7. composition of learned relations;
8. transfer under isomorphs and anti-isomorphs;
9. calibration under UNKNOWN / insufficient evidence;
10. appropriate recruitment of cognitive effort rather than reflexive over-reasoning.

## Phase 1 — learner inventory
For each local learner record:
- exact model identity / revision / quantization or trainable base;
- architecture family;
- parameter scale;
- tokenizer;
- context regime;
- training interface available;
- optimizer/adapter constraints;
- hardware fit;
- pre-CFE phenotype baseline.

Do not treat quantized inference artifacts as equivalent to trainable source checkpoints.

## Phase 2 — matched three-arm design
Default experimental form for each eligible learner:

### Arm A — BASE
Untouched learner.

### Arm B — MATCHED ORDINARY CONTROL
Same atomic training material, total dose, supervision, and resource envelope as Arm C where feasible, but without the CFE learner-visible field manipulation.

### Arm C — CFE DEVELOPMENTAL FIELD
Same atomic material and matched resource envelope, compiled into the prospectively qualified CFE geometry.

Primary causal contrast:
`CFE - MATCHED ORDINARY CONTROL`

Secondary practical contrast:
`CFE - BASE`

The BASE comparison alone is insufficient because it confounds geometry with additional training.

## Phase 3 — phenotype vector
Do not collapse results to one benchmark score. Track a phenotype vector including:
- direct task competence;
- false/true side balance where applicable;
- transfer;
- composition;
- currentness/revision behavior;
- long-horizon question retention;
- semantic drift resistance;
- evidence discipline;
- contradiction recovery;
- calibration;
- compute/reasoning allocation;
- catastrophic regressions.

## Phase 4 — cross-learner cartography
Treat learner regime as an explicit conditioning coordinate, not nuisance variance.

For each intervention cell, record:
- sign by learner;
- effect size by learner;
- phenotype-vector movement;
- optimizer/training interface;
- capacity/context properties;
- path/history dependence.

Questions:
- Does the sign survive model-family changes?
- Does effect magnitude scale with capacity?
- Does a learner require a different integration/revisit horizon?
- Are apparent geometry laws actually optimizer-mediated?
- Do sign flips reveal a missing map axis?
- Does one coordinate system fail across learner classes?

## Phase 5 — hostile interpretation
Possible outcomes and required interpretations:

### Consistent positive across learners
Replication signal. Increase confidence in a regime-robust geometry effect, but do not call it universal.

### Positive only for one family
Learner-conditioned effect. Add/refine learner-regime coordinate.

### Sign flips
High-value cartography evidence. Trigger missing-axis / regime interaction audit. Do not average the disagreement away.

### Null across fleet
Demote the intervention as a broad developmental law; inspect whether the original effect was learner/optimizer specific.

### Broad practical improvement without matched-control separation
Useful engineering result, insufficient CFE causal evidence.

## Phase 6 — fleet training authorization threshold
Broad fleet intervention is authorized only after:
1. at least one CFE geometry axis has prospective causal support beyond a single fragile experiment;
2. the intervention compiler is engineering-qualified on the target learner interfaces;
3. matched controls are feasible;
4. baseline probes are frozen before training;
5. compute budget / rollback / artifact storage are explicit;
6. the first-class cartography identifies what cross-learner uncertainty the run reduces;
7. claims and failure branches are preregistered.

## Preservation rule
The embarrassing local-model outputs are part of the scientific history. Preserve representative examples with provenance.

`DO NOT TRAIN AWAY THE BASELINE BEFORE YOU HAVE MEASURED IT.`

## Long-range research value
If the fleet eventually shows structured differences under matched CFE fields, it gives CFE something much stronger than a leaderboard improvement: a way to estimate how developmental geometry interacts with learner architecture and to reconstruct a more general constraint topology.
