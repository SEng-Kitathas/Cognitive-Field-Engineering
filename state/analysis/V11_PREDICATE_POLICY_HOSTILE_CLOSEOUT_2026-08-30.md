# v1.1 Predicate / Policy Mechanism Screen — Hostile Closeout

Status: **FROZEN SIX-SEED SCREEN COMPLETE / PREREGISTERED DISPOSITION APPLIED / MECHANISM STILL BOUNDED**

Aggregate SHA-256: `3e631f81a5c063fda3fdcf06f26fed8fe9e6de7217ce8e085f8ef161800ccf4d`
Input lock SHA-256: `f096dc597a1f1a9b74f8f46e05dbb6feb74129f76b7e2cd74b6be9d54a42af1a`

## Execution integrity

- 18/18 frozen train/eval jobs completed.
- Six fresh paired predicate seeds completed with the preregistered alternating arm order.
- Six POLICY_FACTORIZED seeds completed.
- Paired predicate arms used identical initialized LoRA hashes within every seed.
- Paired predicate arms used identical dataset-order hashes within every seed.
- No adaptive seeds, prompt changes, margin changes, threshold changes, optimizer changes, or parallel mechanism screens were introduced.
- JSON parse rate was 1.0 for all trained predicate and policy evaluations.

## Preregistered predicate result

Identifying-minus-narrow strict predicate accuracy by paired seed:

- 2026082801: `+0.410714`
- 2026082802: `+0.196429`
- 2026082803: `+0.250000`
- 2026082804: `+0.196429`
- 2026082805: `-0.053571`
- 2026082806: `+0.053571`

Summary:

- mean paired delta: **+0.175595** = +17.56 percentage points
- median paired delta: **+0.196429**
- positive seeds: **5/6**
- negative seeds: **1/6**
- mean out-of-original-support delta: **+0.241667** = +24.17 percentage points

The preregistered `H_WRONG_BASIS_SUPPORTED` disposition fires because:

1. mean paired delta > 0;
2. identifying basis wins at least 4/6 seeds (observed 5/6);
3. combined out-of-original-support performance improves;
4. trained outputs parse cleanly, so the effect is not solely output-contract compliance.

A descriptive two-sided exact sign test for 5 positive of 6 nonzero pairs is `p = 0.21875`. This was not the preregistered decision rule and does not reverse the preregistered disposition; it is included to keep the small-n evidence strength visible.

## Policy result

POLICY_FACTORIZED was **48/48 = 1.0** on every seed.

Across six seeds:

- mean policy accuracy: **1.0**
- seeds >= 0.90: **6/6**
- pooled `accept_all`: **1.0**
- pooled `backpressure_or_fail_explicitly`: **1.0**
- pooled `drop_oldest_keep_latest`: **1.0**

The preregistered `POLICY_SEPARABLY_LEARNABLE` disposition fires strongly.

This establishes that, under this prompt/data/runtime contract, the learner can acquire the mode-conditioned action mapping when overflow truth is supplied and arithmetic identification is removed.

It does not prove that the learner will compose this policy with an independently acquired predicate.

## Hostile support-slice analysis

The overall predicate improvement is real under the preregistered metric, but it is **not a clean strict-boundary solution**.

Mean identifying-minus-narrow accuracy difference by support region:

- equality: **+0.645833**
- negative slack: **+0.701389**
- near overflow `+1`: **-0.625000**
- farther overflow `+3/+7`: **-0.447917**

Descriptive pooled counts show the same shape:

- equality: NARROW `8/48 = 0.1667`; IDENTIFYING `39/48 = 0.8125`
- negative slack: NARROW `24/144 = 0.1667`; IDENTIFYING `125/144 = 0.8681`
- near overflow: NARROW `40/48 = 0.8333`; IDENTIFYING `10/48 = 0.2083`
- far overflow: NARROW `85/96 = 0.8854`; IDENTIFYING `42/96 = 0.4375`

Therefore the identifying basis did not simply install the intended rule `margin > 0`.

The narrow basis usually falls into a strong `condition_z=true` basin.

The identifying basis often shifts the learner toward a `condition_z=false/safe` basin. That recovers negative slack and equality very strongly, but frequently overcorrects and loses positive overflow states.

The earned result is:

> **Broader identifying support materially changes and usually improves held-out predicate accuracy relative to the under-resolved `{0,+1}` slice, especially outside the original support. The improvement is produced by a large change in the learned decision surface, not by clean recovery of the intended strict inequality.**

Do not compress this into:

> `identifying basis teaches the correct boundary`.

That stronger claim is not earned.

## Serial-order check

The arm order alternated by seed.

Mean paired identifying-minus-narrow delta:

- narrow-first seeds 2801/2803/2805: **+0.202381**
- identifying-first seeds 2802/2804/2806: **+0.148810**

Out-of-original-support:

- narrow-first: **+0.275000**
- identifying-first: **+0.208333**

Both execution-order groups remain positive. No simple first/second serial-position explanation is supported by this six-seed pattern.

## What this resolves

The original v1.0 bounded neighborhood was not merely unlucky in the abstract.

Its `{0,+1}` support was a real engineering weakness. Replacing that slice with a basis containing negative slack, equality, near overflow, and farther overflow changes learned transfer in the predicted favorable direction on 5/6 seeds and outside the original support.

So:

`COHERENT LOCAL TRUTH TABLE != IDENTIFYING EXPERIENCE BASIS`

is now supported prospectively under this learner/runtime regime.

## What remains unresolved

The screen does **not** show that the current four-point identifying basis is sufficient to learn the true strict boundary cleanly.

The remaining seam is not whether wider support matters. It does.

The remaining seam is:

> **What learner-visible field geometry produces a balanced predicate that preserves both sides of the boundary instead of moving the model from one one-sided attractor to another?**

Possible contributors still include:

- numerical/support geometry within the identifying field;
- optimizer-visible mixture of positive and negative regions;
- local spacing around the boundary;
- representation of equality as a special breakpoint;
- learner/LoRA capacity and optimizer horizon.

These are hypotheses, not conclusions.

## Next branch under the preregistration

The preregistered next branch fires:

`if predicate basis supported AND policy learnable -> build a separately preregistered JOINT_IDENTIFYING composition screen; do not jump directly to K1/K2/K4`.

The next screen should honor that branch while protecting against the residual predicate seam.

The scientifically clean form is:

1. train the predicate primitive and policy primitive without showing the exact composed task;
2. compare narrow vs identifying predicate support while keeping policy experience identical;
3. evaluate three readouts separately:
   - predicate-only transfer;
   - policy-only retention/separability;
   - composed action where overflow truth is hidden and must be inferred from capacity/queued/incoming before applying the mode policy;
4. keep the intermediate predicate readout visible so final action accuracy cannot hide predicate collapse;
5. use identical update-field/order geometry between composition arms except for the predicate basis manipulation.

This tests `PREDICATE o POLICY` rather than merely training the composed answer directly.

## Evidence ceiling

The result supports a local Identifying-CFE construction law under this fixed learner/compiler/runtime regime:

> **An under-resolved local support can materially distort learned transfer, and a basis that spans additional discriminating regions can improve transfer substantially.**

It does not establish a universal CFE law, Developmental CFE, a general cognitive archetype mechanism, or a finished field compiler.
