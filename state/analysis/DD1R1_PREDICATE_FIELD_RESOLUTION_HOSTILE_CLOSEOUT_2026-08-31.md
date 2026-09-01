# DD1R1 Predicate Field Resolution — Hostile Closeout

Date: 2026-08-31 23:57 Eastern Daylight Time
Scientific identity: `DD1_PREDICATE_FIELD_RESOLUTION_20260831`
Execution recovery identity: `DD1R1_PREDICATE_FIELD_RESOLUTION_20260831`
Disposition: **FIELD_RESOLUTION_SUPPORTED**

## Verified result
- 6/6 paired seeds complete.
- Identifying-co-visible mean balanced accuracy: **0.6736111111111112**.
- Domain-matched margin-homogeneous dispersed mean balanced accuracy: **0.6423611111111110**.
- Mean paired delta: **+0.03125**.
- Identifying wins: **4/6**; dispersed wins: **2/6**; ties: 0.
- Mean false accuracy: identifying **0.680556**, dispersed **0.625000**.
- Mean true accuracy: identifying **0.666667**, dispersed **0.659722**.
- Identifying stable two-sided >=0.65: **1/6**.

## Mechanical disposition
Frozen preregistration returns `FIELD_RESOLUTION_SUPPORTED` because:
- mean paired BA delta > 0: PASS;
- identifying wins >=4/6: PASS;
- false-side noninferiority within 0.05: PASS;
- true-side noninferiority within 0.05: PASS.

Strong support is NOT earned because:
- identifying mean BA >=0.75: FAIL;
- identifying two-sided >=0.65 on >=4/6: FAIL (1/6).

## Earned claim
> **Under matched atomic experiences, support, token budget, dose, learner, optimizer, evaluator, and paired row schedules, making the four identifying predicate margins jointly visible within learner sequences produced a modest positive mean acquisition effect and won four of six paired seeds. Local field resolution therefore matters causally in this fixed regime, but local co-visibility alone is not sufficient for stable two-sided competence.**

## Hostile reading
- Effect size is modest on average (+3.125 points BA), not a dramatic universal lift.
- Sign remains seed-dependent: 2/6 seeds favor dispersion, including one large -18.75 point reversal.
- Stable two-sided competence remains poor in the identifying arm (1/6).
- Therefore `LOCAL IDENTIFYING COVISIBILITY = GENERALLY SUFFICIENT` is rejected.
- This does not prove a universal geometry law or learner-internal relational ontology.
- The result does establish that local joint reachability has a positive main effect under unusually strong same-experience controls.

## Cartographic consequence
The DD1 cell changes from ACTIVE_UNRESOLVED to OCCUPIED_POSITIVE_CONDITIONAL.

New boundary:
`GLOBAL IDENTIFYING SUPPORT + DOSE != LOCAL IDENTIFYING REACHABILITY`

But also:
`LOCAL IDENTIFYING REACHABILITY != STABLE COMPETENCE SUFFICIENCY`

Highest-value next holes are those that can explain the remaining instability without collapsing back into raw dose: typed relation, explicit coverage/boundary geometry, structured revisit/currentness, and long-range connectivity.

## Provenance
Aggregate SHA `b7443ebc82e03d746b2a895b1e8615d9a001a15a6a04fffd6e0a6fe6cd3c69a9`.
Disposition SHA `da7352670a765e3dc57614b2703ed9814ea98025d179cf6c8b9ed84431400f0f`.
Updated map SHA will be computed after write.
