# v1.1 Predicate / Policy Mechanism Screen — Hostile Final Interpretation

Status: **COMPLETE PROSPECTIVE SCREEN; LOCAL IDENTIFYING-CFE RESULT; NOT A GENERAL CFE LAW**

Campaign root: `state/analysis/V11_PREDICATE_POLICY_CAMPAIGN_20260830T184627Z`
Campaign receipt SHA-256: `29a904d28a9eda8fef72bc814c6c97c4d8f9563ffd7095d8be7a4be378d55e2a`
Aggregate SHA-256: `3e631f81a5c063fda3fdcf06f26fed8fe9e6de7217ce8e085f8ef161800ccf4d`

## Frozen questions

1. Does replacing the narrow `{0,+1}` boundary slice with an identifying numerical basis improve transfer of the opaque `condition_z` predicate under matched sequence/update-field structure?
2. Is the mode-conditioned action policy separately learnable when arithmetic is removed and overflow truth is supplied?

No seed extension, prompt mutation, optimizer mutation, or post-outcome threshold change occurred.

## Mechanical preregistered disposition

The frozen aggregate emitted:

- `H_WRONG_BASIS = SUPPORTED`
- `POLICY_SEPARABILITY = LEARNABLE`
- preregistered next branch = `JOINT_IDENTIFYING_PREREG_REQUIRED`

This disposition is historical truth and SHALL NOT be rewritten.

Predicate identifying-minus-narrow paired deltas across six seeds:

`+0.4107, +0.1964, +0.2500, +0.1964, -0.0536, +0.0536`

- positive paired seeds: **5/6**
- mean paired delta: **+0.1756** = +17.56 points
- mean out-of-original-support delta: **+0.2417** = +24.17 points

The pre-frozen wrong-basis criterion therefore passed.

Policy:

- all six seeds: **48/48 = 1.0**
- all action classes pooled: **1.0**

The pre-frozen separability criterion therefore passed decisively.

## Hostile correction: the identifying basis did not cleanly install the strict predicate

The aggregate headline is not the whole mechanism.

Held-out predicate evaluation has 56 cases per seed:

- 32 `condition_z = false` cases
- 24 `condition_z = true` cases

Therefore:

- constant `false` earns 32/56 = **57.14%**
- constant `true` earns 24/56 = **42.86%**

### Narrow arm behavior

Five of six narrow seeds are approximately a `condition_z=true` basin.

Pooled support accuracy:

- negative slack: 24/144 = **16.67%**
- equality: 8/48 = **16.67%**
- near overflow (+1): 40/48 = **83.33%**
- far overflow (+3/+7): 85/96 = **88.54%**

Seeds 2801, 2802, 2804, and 2806 are exactly constant-true on the 56 held-out cases. Seed 2803 is one case away. Seed 2805 flips toward the opposite basin.

Mean post-hoc balanced accuracy = **0.5174**.

### Identifying arm behavior

The identifying arm strongly improves recognition of the non-overflow side but does not reliably learn the positive side of the strict inequality.

Pooled support accuracy:

- negative slack: 125/144 = **86.81%**
- equality: 39/48 = **81.25%**
- near overflow (+1): 10/48 = **20.83%**
- far overflow (+3/+7): 42/96 = **43.75%**

Seeds 2802-2805 classify all 32 false cases correctly but recover only 3-5 of 24 true cases. Seed 2801 is substantially better on both sides. Seed 2806 shifts toward the opposite error pattern.

Mean post-hoc balanced accuracy = **0.6076**.

Thus the identifying basis produced a real prospective phenotype change and improved balanced performance, but it did **not** yield stable acquisition of `queued + incoming > capacity` across the six seeds.

## What the prospective screen earned

It supports this local construction statement:

> Under this fixed learner, optimizer, and transport regime, the numerical support inside the learner-visible experience field materially changes the learned boundary phenotype. Replacing the narrow `{0,+1}` slice with `{-3,0,+1,+3}` improved held-out performance in 5/6 paired seeds and improved mean balanced accuracy, while the factorized policy mapping was separately learnable.

This is stronger than the v1.0 post-hoc claim because the basis contrast, seeds, thresholds, and dispositions were frozen before new trained-arm outcomes.

## What it did not earn

It does **not** establish:

- that the identifying arm cleanly learned the intended strict inequality;
- that `{-3,0,+1,+3}` is a sufficient identifying basis for this learner;
- that the v1.0 `-71` is fully explained by support under-resolution;
- that joint predicate+policy composition is ready for a clean causal test;
- a general CFE law across learners, mechanisms, domains, or optimizers.

## Preregistration weakness exposed by the result

The preregistered wrong-basis success criterion required:

- positive mean paired delta;
- at least 4/6 positive paired seeds;
- improvement outside old support;
- no output-format-only explanation.

Those conditions correctly detect a useful arm difference, but they do not require **two-sided predicate competence**.

Because the held-out evaluation contains 32 false and 24 true cases, a shift from a constant-true basin toward a mostly-false basin can satisfy the aggregate criterion without learning the intended boundary.

Therefore:

`PREREGISTERED DISPOSITION PASS != FULL MECHANISM ACQUISITION`

This is an evaluator/success-criterion scope defect, not a reason to rewrite the completed result.

## Next branch disposition

The frozen aggregate says `JOINT_IDENTIFYING_PREREG_REQUIRED`. Preserve that as the preregistered branch decision.

However, **joint scientific weight mutation should remain blocked** until the next preregistration contains a predicate-competence admission gate that cannot be satisfied by class-basin shift.

A clean gate should include, pre-outcome:

- balanced or class-symmetric primary evaluation;
- per-side minimum competence, not aggregate accuracy alone;
- explicit negative-slack, equality, near-positive, and far-positive criteria;
- rejection of constant-class or near-constant-class solutions;
- identical evaluator class burden where possible;
- no change to optimizer horizon in the same discriminator.

The next experiment should first answer whether a richer identifying basis can produce a stable **two-sided boundary**, rather than immediately composing an incompletely acquired predicate with policy.

## Policy result

The factorized policy result is clean at tested scope:

- six of six seeds at 48/48;
- all three action classes at 100% pooled accuracy.

Earned statement:

> Under this prompt/data/learner regime, the mode-conditioned action mapping is separately learnable when overflow truth is supplied and arithmetic identification is removed.

Do not generalize beyond that tested contract.

## Portability lesson discovered concurrently

The original scientific lock remains byte-valid on the execution/publication host: 27/27 exact.

A fresh LF-normalized checkout can differ on eight locked text files because repository `.gitattributes` declares LF checkout while the original lock sealed CRLF bytes for those files.

This is a portability defect, not a scientific mutation.

The original lock remains unchanged. A companion portability seal now records raw identity plus CRLF-to-LF canonical identity, with verifier outcomes `EXACT_BYTES`, `NORMALIZATION_EQUIVALENT`, `FAIL`, and `MISSING`.

`NORMALIZATION_EQUIVALENT` is admitted only for reproduction provenance; it does not retroactively authorize the original scientific execution.

## Final status

**Prospective evidence supports basis sensitivity and policy separability. It does not yet show stable strict-boundary acquisition. The immediate scientific problem is no longer merely “narrow versus identifying”; it is how to construct a learner-visible basis that produces two-sided relational competence rather than moving the model between decision basins.**
