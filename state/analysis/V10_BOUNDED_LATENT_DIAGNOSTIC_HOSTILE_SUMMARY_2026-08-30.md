# v1.0 Bounded Latent / Out-of-Support Diagnostic — Hostile Summary

Status: **POST-HOC READ-ONLY DIAGNOSTIC; NOT CONFIRMATORY**

## Campaign completion
- Models: NF4 base + 12 sealed v1.0 adapters
- Jobs: 13/13 complete
- Weight updates: none
- Cases: 168/model = 56 states × 3 prompt tiers
- Margins: `-5,-2,-1,0,+1,+2,+5`
- Aggregate SHA-256: `e7bc9003d841eb1b72191ef978eec9ee9dbf0d6432bb75f0a4cf0b21105f417e`

## Paired six-seed arm effect by prompt tier
TREATMENT minus CONTROL mean accuracy delta across paired seeds:
- RULE_EXPLICIT: **-0.05060** (2 positive / 3 negative / 1 zero)
- BOUNDARY_LATENT: **-0.05655** (2 positive / 2 negative / 2 zero)
- FULL_LATENT: **+0.02083** (2 positive / 3 negative / 1 zero; near-floor and output vocabulary broadens, so low interpretability)

Pooled strict-correct counts across six seeds:
- RULE_EXPLICIT: CONTROL 178/336, TREATMENT 161/336 (T-C -17)
- BOUNDARY_LATENT: CONTROL 192/336, TREATMENT 173/336 (T-C -19)
- FULL_LATENT: CONTROL 22/336, TREATMENT 29/336 (T-C +7; floor-level)

## Paired six-seed arm effect by numerical support
Pooled strict-correct counts:
- negative slack (`margin < 0`): CONTROL 283/432, TREATMENT 238/432 (**T-C -45**)
- equality (`margin = 0`): CONTROL 91/144, TREATMENT 75/144 (**T-C -16**)
- old overflow support (`margin = +1`): CONTROL 4/144, TREATMENT 15/144 (**T-C +11**)
- far overflow (`margin = +2,+5`): CONTROL 14/288, TREATMENT 35/288 (**T-C +21**)

Seed-sign pattern is heterogeneous. The overflow advantage is not universal by seed, and the non-overflow loss is also not universal. Do not promote pooled row counts as independent inferential units; the seed pair remains the relevant replication unit.

## Action-confusion interpretation
On RULE_EXPLICIT and BOUNDARY_LATENT tiers, trained adapters usually emit clean JSON. Therefore the dominant strict-score differences are not mainly output-format failure.

CONTROL is strongly biased toward `accept_all`, especially when the boundary inequality is not stated. On BOUNDARY_LATENT across six seeds:
- CONTROL non-overflow: 192/192 `accept_all` (all correct)
- CONTROL overflow: 144/144 `accept_all` (all wrong)

TREATMENT is less purely `accept_all`-locked. On BOUNDARY_LATENT:
- non-overflow: 148/192 correct `accept_all`, 44/192 incorrectly `backpressure_or_fail_explicitly`
- transactional overflow: 25/72 correctly `backpressure_or_fail_explicitly`
- latest-state overflow: it sometimes emits `backpressure_or_fail_explicitly`, but never the correct `drop_oldest_keep_latest` under this tier

Thus TREATMENT appears to shift the action basin toward overflow/backpressure behavior. This buys some overflow correctness but increases false-positive overflow behavior on non-overflow/equality states. CONTROL preserves a stronger non-overflow/accept basin and correspondingly misses most overflow.

## What this rules against
This diagnostic does **not** support a simple story that CONTROL learned the intended strict inequality while TREATMENT failed to learn it. Neither arm shows clean generalization of `queued + incoming > capacity` across the new support.

It also weakens the claim that the original `-71` was solely a formatting or JSON-compliance artifact: trained adapters generally follow the JSON contract on the explicit/boundary tiers while still exhibiting the action-basin asymmetry.

## What remains live
1. **Under-resolved / wrong identifying basis** — strengthened. The original `{0,+1}` local support is too weak to eliminate cheap rival rules and may produce a brittle action basin.
2. **Optimizer-visible geometry / horizon** — still live. Different update-fields may determine which side of the boundary becomes the dominant attractor.
3. **Direct sibling-gradient conflict** — weakened by the partial initial-state diagnostic, not eliminated.
4. **Action-policy entanglement** — strengthened. The model may be learning a coupled action prior rather than a separable overflow predicate plus mode-conditional policy.
5. **Unmodeled mechanism** — remains possible; do not rescue failed hypotheses by automatic combination language.

## Scientific ceiling
This is a post-hoc diagnostic on already-seen v1.0 outcomes and a newly designed surface. It can demote simplistic mechanisms and motivate a preregistered discriminator, but it cannot confirm the causal mechanism of the v1.0 sign flip.

The next scientific branch should separate **overflow predicate identification** from **mode-conditioned action policy** and should include an identifying numerical basis with negative slack, equality, and multiple positive margins before any concentration/horizon sweep is interpreted as mechanism proof.
