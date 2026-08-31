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


## Preliminary bounded-latent seed 2501 result
Post-hoc read-only diagnostic; one paired seed only; not confirmatory.

NF4: 0/56 on all three strict tiers, largely because it does not follow the JSON output contract.

Seed 2026082501 CONTROL:
- RULE_EXPLICIT 35/56 = 0.625
- BOUNDARY_LATENT 32/56 = 0.5714
- FULL_LATENT 16/56 = 0.2857
- negative slack 61/72 = 0.8472
- equality 19/24 = 0.7917
- old +1 overflow 0/24
- far overflow 3/48 = 0.0625

Seed 2026082501 TREATMENT:
- RULE_EXPLICIT 33/56 = 0.5893
- BOUNDARY_LATENT 32/56 = 0.5714
- FULL_LATENT 0/56
- negative slack 48/72 = 0.6667
- equality 16/24 = 0.6667
- old +1 overflow 0/24
- far overflow 1/48 = 0.0208

Raw trained outputs are clean JSON. On overflow both arms overwhelmingly emit `accept_all`; boundary-latent overflow is 0/24 correct in both arms. CONTROL occasionally emits correct transactional backpressure on farther overflow; TREATMENT does so less often. This weakens a simple output-contract explanation and is consistent with brittle/under-resolved bounded task binding, but one seed cannot establish mechanism.


## Completed bounded latent / out-of-support campaign
- Campaign status: COMPLETE, 13/13 jobs, no weight updates.
- Aggregate SHA: `e7bc9003d841eb1b72191ef978eec9ee9dbf0d6432bb75f0a4cf0b21105f417e`.
- RULE_EXPLICIT mean paired T-C delta: -0.05060.
- BOUNDARY_LATENT mean paired T-C delta: -0.05655.
- FULL_LATENT mean paired T-C delta: +0.02083 at near-floor performance.
- Pooled support deltas: negative slack -45 T-C correct, equality -16, old +1 overflow +11, far overflow +21.
- CONTROL behaves like a strong `accept_all` basin; TREATMENT shifts toward overflow/backpressure, gaining some overflow cases and losing more safe/equality cases.
- Neither arm cleanly demonstrates the intended inequality across the expanded support.
- Post-hoc hostile summary: `state/analysis/V10_BOUNDED_LATENT_DIAGNOSTIC_HOSTILE_SUMMARY_2026-08-30.md`.
- Current implication: prioritize separating overflow-predicate identification from action-policy learning before any broader concentration sweep.


## v1.1 predicate/policy mechanism screen — pretraining
- No new mechanism weight outcome has been observed.
- Prereg v2 SHA: `ebb014831500a6f74961a4fb06af75bf33ba99a290af11e3ff954f8850e196a4`.
- Pre-outcome amendment SHA: `bdd51ca7ff97679dc032529b0386dd1b143c9ab514c51d58e2b100775dc8f1c1`.
- Candidate r2 manifest SHA: `18a846937cce18cef89d48926ebc271817b4ebb3114c45cf13077ab326d4f352`.
- Token audit SHA: `51c7c8cc10ce435d1a26e0618d45fee968925b40a980b77d31f33135a2c92bbe`.
- Static hostile qualification: PASS, 816 checks, zero failures.
- Predicate arms: identical paired contexts and exact token/supervision burden; narrow support `{0,+1,0,+1}` vs identifying support `{-3,0,+1,+3}`.
- Predicate learner-visible target is opaque `condition_z`; formula and semantic word `overflow` absent.
- Policy task supplies overflow truth + mode and removes arithmetic.
- NF4 baseline admission is active under PID `18524`.
- Frozen gates: predicate rejected if NF4 >=0.85; policy training skipped if NF4 >=0.90.


## v1.1 predicate/policy preexecution qualification
- Input lock SHA: `f096dc597a1f1a9b74f8f46e05dbb6feb74129f76b7e2cd74b6be9d54a42af1a`.
- Host lock SHA: `13379f2d678bdfd8b266f6985808d193c57519924a6c40cd85892ce30900418e`.
- Repeatability SHA: `aebde6719bc1f68f55e393f8e0d9cc3a9a98830121325ad40297f17e8bc41ae1`.
- Profile lock SHA: `8de85251eafb8cd05887c11935c0cdef44a5297618b7736d841db4f3ea1d30f4`.
- Exact base snapshot 11/11 files rehashed PASS; tokenizer replay 216/216 PASS.
- NF4 baseline admission: predicate 0/56, policy 0/48 strict; both admitted.
- Final preexecution: `V11_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED`.
- Scientific v1.1 mechanism training has not started at this snapshot.


## v1.1 predicate/policy active scientific campaign
- Scientific boundary crossed after pretraining Git remote verification.
- Campaign stamp: `20260830T184627Z`.
- PID: `5916` (alive at launch readback).
- Run root: `state/analysis/V11_PREDICATE_POLICY_CAMPAIGN_20260830T184627Z`.
- Receipt status at launch readback: `RUNNING`.
- First job: seed `2026082801`, `PREDICATE_NARROW_SLICE` training.
- Frozen job count: 18 train/eval jobs.
- No adaptive extension or parallel mechanism screen authorized.


## v1.1 first sealed scientific job
- Seed `2026082801 / PREDICATE_NARROW_SLICE` train+eval COMPLETE.
- Overall strict `condition_z` accuracy: 24/56 = 0.428571.
- Equality: 0/8. Negative slack: 0/24. Near overflow +1: 8/8. Far overflow +3/+7: 16/16. JSON parse rate 1.0.
- Out-of-original-support: 16/40 = 0.40.
- This arm behaves like a one-sided positive-condition basin and does not yet identify the strict boundary. It is one arm of one seed; no paired effect claim is authorized until the seed-2801 identifying arm seals.


## CFE program-level Commander's Intent
- Source-level invention-thread intent: `state/doctrine_snapshot/CFE_ORIGINAL_THREAD_COMMANDERS_INTENT_SOURCE_2026-08-30.md` SHA `29a1e6c4ac885d8021fb12eca8173d0b493306255814423d05b511c2f8ce4765`.
- Active binding: `state/doctrine_snapshot/ACTIVE_CFE_COMMANDERS_INTENT_2026-08-30.md` SHA `105cba0bff82e84fb980a5a681394a73857bcdbe6e450546b8c911f8c9e2791e`.
- Invariant: **The developmental structure of experience itself is the engineering medium.**
- Identifying CFE = known target relation -> identifying experience -> acquisition/transfer mechanism science.
- Developmental CFE = lawful ecology/consequences -> learner-discovered representations/strategies/compositions -> phenotype characterization.
- Current predicate/policy campaign is Identifying CFE, an experimental specialization only. It does not redefine the whole CFE program.
- Current empirical wording: learner-visible experience arrangement has produced reproducible, relation-dependent behavioral effects in the current fixed-learner regime; broader CFE law unresolved.


## v1.1 seed 2801 paired result
- NARROW predicate: 24/56 = 0.428571; out-of-original-support 16/40 = 0.40.
- IDENTIFYING predicate: 47/56 = 0.839286; out-of-original-support 38/40 = 0.95.
- Paired identifying-minus-narrow: +0.410714 overall; +0.55 out-of-original-support.
- POLICY_FACTORIZED: 48/48 = 1.0.
- Ceiling: one paired seed only. Campaign continues; no mechanism disposition until all six paired seeds seal.


## v1.1 seed 2802 paired result
- NARROW predicate: 24/56 = 0.428571; out-of-original-support 16/40 = 0.400000.
- IDENTIFYING predicate: 35/56 = 0.625000; out-of-original-support 27/40 = 0.675000.
- Paired identifying-minus-narrow: +0.196429 overall; +0.275000 out-of-original-support.
- POLICY_FACTORIZED: 48/48 = 1.000000.
- Ceiling: second paired seed only. No mechanism disposition until all six paired predicate seeds seal.


## v1.1 final six-seed closeout
- Campaign COMPLETE: 18/18 jobs; aggregate SHA `3e631f81a5c063fda3fdcf06f26fed8fe9e6de7217ce8e085f8ef161800ccf4d`.
- Predicate identifying-minus-narrow deltas: +0.4107, +0.1964, +0.2500, +0.1964, -0.0536, +0.0536. Mean +0.1756; 5/6 positive.
- Mean out-of-original-support delta +0.2417.
- Preregistered `H_WRONG_BASIS_SUPPORTED` fires.
- Hostile slice: identifying improves equality +0.6458 and negative slack +0.7014, but hurts +1 overflow -0.6250 and far overflow -0.4479. Therefore broader support improves transfer but does not cleanly recover the strict boundary.
- POLICY_FACTORIZED = 48/48 on all six seeds; `POLICY_SEPARABLY_LEARNABLE` fires strongly.
- Final disposition SHA `e9f665d9280917c4383c44eeaec7bc9a38a7eec56e3c529e51ea3444386ed0ae`.
- All 18 adapters published to release tag `cfe-v11-predicate-policy-research-2026-08-30`, digest verified.
- Next frozen branch: v1.2 factorized primitive composition with no joint training examples.


## v1.2 factorized primitive composition candidate
- Prereg SHA `e929a4ab201a86faaf7f910438b53e1349d4ac2a7a0d29a960d1381392657bf9` was remote-published before candidate generation.
- Candidate: `state/candidates/v12_factor_primitive_composition_20260830`.
- Candidate manifest SHA `b03b0eca0ecf39554491e787e64a5fae0102bcff7700c81630f66c3005bc1ca1`.
- Token/schedule audit SHA `f3aa40f53d7c75b277213ed3753b51fb806d3eccc07097d508b4c115e6423679`.
- Both arms: 144 sequences, 31,200 total tokens, 4,608 supervised tokens; paired predicate lengths 72/72 exact.
- Every planned optimizer window: exactly 4 predicate + 4 policy sequences, identical logical schedule across paired arms.
- Joint training examples: 0. Composed primary evaluation hides `condition_z`. Policy/composition prompts use opaque actions and contain no overflow/backpressure/drop-oldest/accept-all semantics.
- Independent static hostile audit: PASS, 1,157 checks, zero failures.
- Status: candidate only; baseline admission not yet run; no v1.2 weights trained.


## v1.1 predicate/policy final result
- COMPLETE 18/18 jobs. Receipt SHA `29a904d28a9eda8fef72bc814c6c97c4d8f9563ffd7095d8be7a4be378d55e2a`; aggregate SHA `3e631f81a5c063fda3fdcf06f26fed8fe9e6de7217ce8e085f8ef161800ccf4d`.
- Frozen disposition: `H_WRONG_BASIS=SUPPORTED`, `POLICY_SEPARABILITY=LEARNABLE`.
- Predicate identifying-minus-narrow mean +0.1756; 5/6 positive seeds; out-of-original-support mean +0.2417.
- Policy = 48/48 on every seed.
- Hostile correction: narrow mean balanced accuracy 0.5174; identifying 0.6076. Identifying basis strongly improves safe/equality classification but remains poor on near-positive/far-positive support in most seeds. This is basis sensitivity, not stable strict-boundary acquisition.
- Joint-composition scientific run is blocked pending a two-sided predicate-competence gate.
- Final hostile summary: `state/analysis/V11_PREDICATE_POLICY_HOSTILE_FINAL_2026-08-30.md`.

## Scientific lock portability repair
- Original v1.1 input lock remains unchanged and valid for original execution.
- Current checkout verifies 27/27 `EXACT_BYTES`.
- Synthetic LF checkout verifies 19 `EXACT_BYTES` + 8 `NORMALIZATION_EQUIVALENT`, zero failures.
- Companion seal: `state/trace_matrix/V11_PREDICATE_POLICY_LOCK_PORTABILITY_SEAL_2026-08-30.json`, SHA `a099c58fe010996147ae01a897cb54f7604caad2899be5cb012e3f74b993226c`.
- `NORMALIZATION_EQUIVALENT` is reproduction provenance only; it does not retroactively authorize original execution.


## v1.2 preexecution authorization
- Branch reconciliation: `state/analysis/V11_V12_BRANCH_RECONCILIATION_2026-08-30.md`.
- v1.2 portability seal SHA `39f2ce2d8ea339a07f92fef59024b4385f9219afa097a9550cab17ab956437f7`.
- Final preexecution status: `V12_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED`.
- Input lock SHA `f4cbcb189a23e41d169795f0e6e64f8eec79ea6eeef22a6d509ae01b5d6f5b6d`.
- No v1.2 scientific trained-arm outcome exists at this snapshot.
- Direct composed-answer training remains forbidden; factorized primitive composition is authorized under the frozen v1.2 controls.


## v1.2 active scientific campaign
- Scientific boundary crossed only after remote prelaunch head `09271d85d5b905461f8f847383b5d4a0ff70f4bb` was verified.
- PID `13780`.
- Run root `state/analysis/V12_FACTOR_PRIMITIVE_CAMPAIGN_20260831T021411Z`.
- First frozen job: seed 2026082901 `COMPOSE_NARROW_BASIS`.
- No duplicate/parallel CFE scientific campaign authorized.


## v1.2 seed 2901 paired result
- NARROW: predicate-direct 24/48 = 0.50; policy-direct 40/48 = 0.8333; composed action 34/96 = 0.3542. Composed false-truth 0/48; true-truth 34/48 = 0.7083.
- IDENTIFYING: predicate-direct 24/48 = 0.50; policy-direct 40/48 = 0.8333; composed action 24/96 = 0.25. Composed false-truth 0/48; true-truth 24/48 = 0.50.
- Paired identifying-minus-narrow composed delta: -0.104167. Predicate delta: 0.0.
- Both arms retain the one-sided predicate basin on this seed. This is one paired seed only; no composition disposition is authorized.
- Exact seed adapters published under release tag `cfe-v12-factor-primitive-research-2026-08-31`.


## v1.2 seed 2902 paired result
- NARROW: predicate-direct 24/48 = 0.5000; policy-direct 48/48 = 1.0000; composed 40/96 = 0.4167.
- IDENTIFYING: predicate-direct 24/48 = 0.5000; policy-direct 48/48 = 1.0000; composed 50/96 = 0.5208.
- Paired identifying-minus-narrow composed delta: +0.104167. Predicate-direct overall delta +0.000000.
- NARROW predicate false/true = 1.0000/0.0000; IDENTIFYING = 0.0000/1.0000. Both remain one-sided but in opposite directions.
- IDENTIFYING composed false/true = 0.5417/0.5000. One paired seed only; no aggregate disposition.
- Exact seed adapters published under release tag `cfe-v12-factor-primitive-research-2026-08-31`.


## v1.2 seed 2903 paired result
- NARROW: predicate-direct 25/48 = 0.5208; policy-direct 48/48 = 1.0000; composed 29/96 = 0.3021.
- IDENTIFYING: predicate-direct 24/48 = 0.5000; policy-direct 48/48 = 1.0000; composed 50/96 = 0.5208.
- Paired identifying-minus-narrow composed delta: +0.218750; predicate delta -0.020833.
- NARROW predicate false/true = 0.8750/0.1667; IDENTIFYING = 0.0000/1.0000.
- Exact seed adapters published under release tag `cfe-v12-factor-primitive-research-2026-08-31`.


## v1.2 seed 2904 paired result
- NARROW: predicate-direct 24/48 = 0.5000; policy-direct 48/48 = 1.0000; composed 51/96 = 0.5312.
- IDENTIFYING: predicate-direct 24/48 = 0.5000; policy-direct 48/48 = 1.0000; composed 50/96 = 0.5208.
- Paired identifying-minus-narrow composed delta: -0.010417. Predicate-direct delta +0.000000.
- NARROW predicate false/true = 0.0000/1.0000; IDENTIFYING = 1.0000/0.0000.
- IDENTIFYING composed false/true = 0.5417/0.5000. No aggregate disposition yet.
- Exact seed adapters published under release tag `cfe-v12-factor-primitive-research-2026-08-31`.


## Microseed language-gate dependency seam
- Operator reports Microseed has reached the pre-lingual substrate milestone and is at the language gate before research.
- Evidence class: OPERATOR-REPORTED STATE ONLY; Microseed artifacts have not yet been inspected or hash-admitted into this CFE workstream.
- CFE relevance: potentially high because language-gate design is a developmental-experience problem, but `CFE_RESULT != MICROSEED_TRANSFER`.
- Hard rule: do not port Capybara/Mistral-specific compiler limits, prompt semantics, or optimizer assumptions into Microseed. Any transfer must be re-derived against the Microseed substrate and language-gate contract.
- Candidate reusable outputs from CFE, pending Microseed-side verification: experience-geometry vocabulary, identifying-vs-coherent distinction, uncertainty preservation, consequence/history doctrine, evaluator-scope discipline, and learner-visible-vs-curator-visible transport distinctions.
- Immediate stance: finish v1.2 closeout first; then prepare a bounded CFE→Microseed language-gate research handoff that separates program-level developmental principles from LLM-specific experimental mechanisms.
