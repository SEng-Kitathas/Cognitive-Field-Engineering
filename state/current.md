# CFE CURRENT STATE

Date: 2026-08-29
Mode: RECOVERY -> AUDIT -> BUILD-COMMIT
Primary role: R1 Conservative Auditor / R5 Reality Pressure as execution resumes

## Mission
Recover and execute the first qualified CFE v1.0 causal screen without rewriting the sealed v0.9 parent, weakening preregistration, or promoting scientific claims ahead of evidence.

## Active process doctrine
- Active SOP: `state/doctrine_snapshot/ACTIVE_RAHL_R3_1_CURRENT_STABLE_SOP_FOR_CFE_20260829.md`.
- Exact stable SOP source copy: `state/doctrine_snapshot/source/RAHL_ENGINEERING_R3_1_CURRENT_STABLE_SOP_20260829.md`.
- 1991-ish prose doctrine is active: plain language around the mechanism, proper language for the mechanism.
- Historical method stacks are not mandatory pipelines unless they serve a causal job or the operator explicitly requires them.

## Current live scientific branch
- Immutable parent: `C:\Users\ancal\ProtoAGI\CFE\sealed_parents\v09\CFE_RND_V0_9_2026-08-25`.
- Active descendant: `C:\Users\ancal\ProtoAGI\CFE\CFE_RND_V1_0_PREEXECUTION`.
- Live scientific run root: `C:\Users\ancal\ProtoAGI\CFE\CFE_RND_V1_0_PREEXECUTION\executed\CFE_V10_FIRST_SCREEN_20260830T013957Z`.
- Current scientific lock SHA-256: `a497c1cd013c834c9e9efc45b65fd09dbae0dca973f044afe706607cc8094695`.

## Verified pre-live state
- v1.0 child exists.
- Sealed v0.9 parent was reverified unchanged after the fork: 242 files; aggregate SHA-256 `41a33cf474e82d4b443b31c26ab2d653b2bca071f95ad6bd24173d88090e881d`.
- Premodel pytest: **56 passed**.
- Negative ingress tests: no-network default rejected; known-wrong local snapshot rejected.
- Exact model target: `argilla/CapybaraHermes-2.5-Mistral-7B` revision `d06c86726aadd8dadb92c5b9b9e3ce8ef246c471`.
- C:, D:, and E: were searched before download. No exact pinned snapshot was found.
- Existing Q3 GGUF and a different 3-shard Mistral/Capybara model were found and correctly rejected as the NF4/QLoRA training base.
- Exact pinned snapshot was then acquired by network under the recorded local-first gate.
- Runtime tokenizer matches every v1.0 token reference exactly.
- Host lock SHA-256: `047fc0e619b5ebe61f7dd9c6e5e1a1b356affba07a8b27795b394c3ad443aea6`.
- Profile lock SHA-256: `65b8bef8e07034d39a509ef6f5922151b01e1bb9929a7fb36d81640167de2f59`.
- Selected profile: `all_linear_r8`, eager attention, deterministic algorithms fail closed.
- Same-seed one-step repeatability: **PASS** with matching selected profile, initial trainable hash, post-step trainable hash, loss hex, and trainable parameter count.

## NF4 base phenotype
Evaluation completed before scientific training:
- field: 9/144 = **0.0625**
- LHIT: 24/96 = **0.25**
- retention: 10/24 = **0.4166666667**
- structural combined: 33/240 = **0.1375**

These are baseline measurements only. They do not establish a CFE effect.

## Current execution node
The v1.0 six-seed screen is complete. Stage 1 and Stage 2 execution integrity passed. No further v1.0 adaptive extension is authorized.

Post-screen hostile autopsy found:
- six-seed structural T-C deltas: `+0.05, -0.0541666667, +0.0375, -0.10, +0.05, -0.10`;
- endpoint effect is mixed/negative overall, not a stable positive TREATMENT advantage;
- strong phenotype split: TREATMENT favors `warrant_vs_taint` / field, CONTROL strongly favors `bounded_transport` / LHIT;
- adapter norm/distance/cosine do not explain the sign flips;
- neighborhood identity is curator-only and is embodied to the learner through shared base-state/context realization.

The naive Relation×Surface 2×2 redesign is challenged because removing surface/context sameness can remove the learner-visible carrier of neighborhood identity.

A cleaner v1.1 candidate has been built as a neighborhood-concentration dose screen:
- K1 = one neighborhood per four-cell block;
- K2 = two neighborhoods per block, balanced 2+2;
- K4 = four neighborhoods per block.

Candidate compiler passed exact global source/experience parity and target/cell parity. Exact pinned tokenizer audit passed: all arms 33,646 total tokens, 3,288 supervised tokens, max 499; each pairwise arm comparison has 70/72 exact sequence lengths and max delta 1.

A fresh evaluation source/compile was also generated with new vocabulary/domains and passed exact-overlap audit: 144/144 field and 96/96 LHIT prompts unique; zero exact overlap with training or old evaluation. This surface is fresh but not blind or independent replication.

A fresh six-seed order using all six permutations of K1/K2/K4 has been frozen as a draft candidate. No v1.1 model outcome has been observed and scientific training has not started.

## Recovery embodiment
Created `tools/resume_v10_first_screen.py`.
- SHA-256: `9b3b3f23970b4332e55b25f5452e81dea524066d17eaab793db44d631f09b62b`
- compile: PASS
- audit-only test against the live run: correctly returned BLOCKED because the current CONTROL directory is partial and lacks `RUN_MANIFEST.json`.
- behavior: refuse partial/corrupt output, verify completed train/eval artifacts by identity/hash, and execute exactly one first-missing frozen step per `--execute` invocation, then return with a receipt.

## Downstream analysis audit
Verified in code:
- independent unit = paired seed/run;
- evaluation rows remain nested measurements;
- row-level inference is not used for promotion;
- Stage-1 extension decision reads only the three preregistered structural seed deltas;
- STOP only if all three are nonzero and share one sign;
- otherwise extend exactly once to preregistered seeds 2026082504..06;
- family/domain slices cannot change the extension decision;
- no analyzer performs automatic scientific promotion.

## Scientific ceiling
The core empirical observation is now treated as **earned**: relational co-visibility geometry has a measurable, family-dependent effect on transfer to unseen domains under this exact learner/compiler regime. The observed family-level endpoint pattern is `+43 / 0 / -71` (TREATMENT minus CONTROL discordance by relation family), and the control is demonstrably capable of outperforming treatment.

What is **not earned** is a predictive mechanism or a usable cognitive-archetype engineering technique. We cannot yet predict which relation types benefit, saturate, or are harmed by tight neighborhood co-visibility. Therefore "CFE works and only needs dialing in" is not an authorized framing.

Current strongest formulation: **the core observation is right; the mechanism is unresolved.** Any next campaign must contain explicit predictions that can fail and must treat further null/negative results as evidence against the mechanism hypothesis, not automatically as tuning problems.

## Open seams
1. Run a bounded-transport neighborhood-composition audit: determine whether the current four-cell basis actually brackets the controlling distinction cleanly.
2. Build a fixed-density sibling-composition discriminator before the broader K1/K2/K4 dose sweep.
3. Build an optimizer-window permutation discriminator using the exact same sequences/content but different accumulation-window geometry.
4. Measure optimizer-visible horizon separately from neighborhood concentration where practical.
5. Keep K1/K2/K4 concentration dose as a later discriminator if starvation remains live after composition/horizon tests.
6. Preserve fresh evaluation and no-feedback boundaries; no scientific training starts until the revised preregistration and lock reflect this mechanism-first order.
7. Do not rewrite or extend the completed v1.0 screen.

## Strongest recovery receipt
`state/v10_fork/LIVE_V10_RECOVERY_2026-08-29T2206_ET.json`
SHA-256: `5a6c1e8af753de2e481a5a8187cde9742530dc01f1f4f6f89b1236a11c1d2a2c`


## GitHub publication continuity
- Target: `https://github.com/SEng-Kitathas/Cognitive-Field-Engineering.git`
- Publication model: thin normal clone; heavy R&D/reincarnation/model/checkpoint artifacts are opt-in release/archive assets.
- Per material turn: update continuity -> commit -> push when authenticated -> verify remote head.
- Local prepared checkout: `publication/github/Cognitive-Field-Engineering`.
- Publication is not called complete until remote commit readback succeeds.


## Active post-hoc diagnostic campaign
- Diagnostic source: `state/candidates/v10_bounded_latent_diagnostic_20260830`.
- 56 bounded states × 3 tiers = 168 prompts; margins -5,-2,-1,0,+1,+2,+5.
- Static audit: PASS; rival rules `==1`, `>=0`, `!=0`, `>1` are all discriminated.
- Campaign: NF4 base + all 12 sealed adapters, read-only, no optimizer updates.
- PID at launch: `6444`.
- Output: `state/analysis/V10_BOUNDED_LATENT_DIAGNOSTIC_CAMPAIGN_20260830`.
- Interpretation ceiling: post-hoc diagnostic only; FULL_LATENT failure can include prompt/task ambiguity and is not by itself proof of absent representation.
