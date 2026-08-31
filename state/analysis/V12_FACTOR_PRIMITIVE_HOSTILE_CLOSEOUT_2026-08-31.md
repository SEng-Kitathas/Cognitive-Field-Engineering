# v1.2 Factorized Primitive Composition — Hostile Closeout

Status: **COMPLETE / PREREGISTERED COMPOSITION BASIS NOT SUPPORTED / NEXT MECHANISM SCREEN REQUIRED**

Campaign root: `state/analysis/V12_FACTOR_PRIMITIVE_CAMPAIGN_20260831T021411Z`

Campaign receipt SHA-256: `501dc31c844e17b8ad0c155a69584af0f38756ebc129f030f3de51fc5264586f`
Aggregate SHA-256: `af26fd4b626afddd2bb22445cf276cf3690b5e4352bb96f3b8acddcb0ec0ff20`
Preregistration SHA-256: `e929a4ab201a86faaf7f910438b53e1349d4ac2a7a0d29a960d1381392657bf9`
Input lock SHA-256: `f4cbcb189a23e41d169795f0e6e64f8eec79ea6eeef22a6d509ae01b5d6f5b6d`

## Execution integrity

- 12/12 frozen scientific jobs completed.
- Six fresh paired seeds completed.
- Both arms used the frozen factorized-primitive candidate and evaluator surfaces.
- No joint numeric-state + mode -> action training example was introduced.
- No adaptive seeds, prompt changes, support changes, action remapping, optimizer changes, or parallel scientific screen were introduced.
- Policy and predicate readouts remained separate from the composed-action readout.

## Preregistered composition result

Identifying-minus-narrow COMPOSED_ACTION deltas by paired seed:

- 2026082901: `-0.104167`
- 2026082902: `+0.104167`
- 2026082903: `+0.218750`
- 2026082904: `-0.010417`
- 2026082905: `-0.197917`
- 2026082906: `-0.052083`

Summary:

- mean paired composition delta: **-0.006944** = -0.69 percentage points
- identifying composition wins: **2/6**
- pooled false-truth delta: **-0.104167**
- pooled true-truth delta: **+0.090278**

Therefore the preregistered composition-basis support criteria do **not** fire.

`COMPOSITION_BASIS = NOT_SUPPORTED`

This is a negative result for this factorized composition construction under the current learner, transport, optimizer, and prompt contract.

It is not evidence that CFE as a program is false.

## Policy primitive

Direct policy learning was strong and symmetric:

- NARROW mean POLICY_DIRECT accuracy: **0.972222**
- IDENTIFYING mean POLICY_DIRECT accuracy: **0.972222**
- five of six seeds reached 48/48 in both arms;
- the first seed reached 40/48 in both arms.

Therefore policy acquisition is not the leading explanation for failed composition.

## Predicate primitive

Predicate behavior remained unstable.

Identifying-minus-narrow direct-predicate deltas:

`0.000000, 0.000000, -0.020833, 0.000000, +0.354167, 0.000000`

Mean direct-predicate delta: **+0.055556**.

But that mean is dominated by seed 2026082905.

Most arm/seed runs still fall into near one-sided basins:

- false approximately 0 / true approximately 1; or
- false approximately 1 / true approximately 0.

Seed 2026082905 is especially important:

- IDENTIFYING direct predicate: 41/48 = **0.854167**;
- false side = **1.0**;
- true side = **0.708333**;
- yet composed action = 28/96 = **0.291667**;
- NARROW composed action on the same seed = 47/96 = **0.489583**.

So:

> **BETTER DECLARED PRIMITIVE ACQUISITION != BETTER COMPOSITION**

at least at this seed and under this interface.

Across the six identifying runs, descriptive correlation between direct-predicate overall accuracy and composed-action accuracy is approximately **-0.53**. This was not preregistered and is not an inferential result; it is a hostile clue showing that the simple serial story `better predicate -> better composition` is not supported by this sample.

## What v1.2 weakens

The following simple story is weakened:

`broader identifying basis -> cleaner predicate -> automatic zero-shot recruitment with learned policy -> better composed action`

The experiment does not support that chain.

The v1.1 identifying-basis effect was real at its tested scope, but v1.2 shows that improving or changing a primitive's direct behavior is not enough to guarantee successful composition.

## What remains live

Three mechanism families remain materially live:

1. **optimizer-visible primitive interference**
   - predicate and policy sequences were mixed 4+4 inside every gradient-accumulation window;
   - same source multiset can create a different effective update field depending on local window composition.

2. **primitive-interface / learner-decomposition mismatch**
   - the curator declares `numeric state -> condition_z -> policy -> action`;
   - the learner may not recruit that same decomposition even when direct readouts look competent;
   - `CURATOR DECOMPOSITION != LEARNER DECOMPOSITION` is a candidate law, not yet earned doctrine.

3. **dose / optimizer horizon**
   - current primitive exposure may be insufficient for stable basin formation;
   - K-dose remains parked until local-interference is tested cleanly.

## Next discriminator

The strongest next screen is optimizer-visible primitive interference because it changes one causal feature while holding the experience multiset fixed.

Compare:

- `LOCAL_MIXED`: every accumulation window contains 4 predicate + 4 policy sequences;
- `WINDOW_SEPARATED`: accumulation windows are homogeneous, 8 predicate or 8 policy, with window types alternated under a frozen schedule.

Hold fixed:

- exact identifying predicate rows;
- exact policy rows;
- total row multiset;
- total tokens and supervised tokens;
- model/profile;
- optimizer hyperparameters;
- gradient accumulation = 8;
- epochs and total optimizer steps;
- evaluation surfaces.

This directly tests:

> **SAME EXPERIENCE MULTISET != SAME OPTIMIZER-VISIBLE DEVELOPMENTAL PRESSURE**

## Evidence ceiling

Earned statement:

> **Under the current fixed learner and mixed-window factorized training regime, a broader identifying predicate basis did not improve zero-shot composition with a separately learned opaque policy. Direct policy learning was strong, direct predicate behavior remained unstable, and the best direct-predicate seed did not yield better composition.**

Do not compress this into:

- `composition is impossible`;
- `CFE does not work`;
- `predicate learning is irrelevant`;
- `the learner definitely uses a different internal decomposition`;
- `optimizer interference is proven`.

Those claims are not earned.
