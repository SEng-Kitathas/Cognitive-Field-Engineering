# CFE DESIGN THREAD STREAM

## Header
- Thread: CFE takeover / recovery / build
- Last Updated: 2026-08-29
- Purpose: chronological recovery spine

---

## Exchange — USER
Timestamp: 2026-08-29
Tags: DOCTRINE CHANGE, SOP ADOPTION

User instructed: "Adopt the newest stable SOP, the predecessor had some serious flaws" and uploaded `RAHL_ENGINEERING_IN_HOUSE_SOP_SPLIT_CANDIDATE_R3_1_2026-08-29(2).zip`.

---

## Exchange — ASSISTANT
Timestamp: 2026-08-29
Tags: AUDIT, PROMOTION, STATE CHANGE

Assistant verified the uploaded `(2)` ZIP is byte-identical to the already-known R3.1 candidate package (SHA-256 `4d205becc2413889bdb37c6b6ff7513d6f759a7dff1d9f9b8fddaddd8235a278`, 46 entries, clean ZIP test), so it was not treated as a newer release by filename alone.

A local-drive/project search found the later stable process artifact:
`E:\new pc\AI_Pushes_Sandbox\projects\tq2_reconstruction_20260827\state\doctrine_snapshot\RAHL_ENGINEERING_R3_1_CURRENT_STABLE_SOP_20260829.md`
SHA-256 `dd4254695ac0ae4ea2f78e10de9177dad10d40b171cf7bbb413896d539dd215b`.

The stable artifact supersedes the prior trusted-whole layer for process use, preserves source-package provenance, preserves inherited statement classes, rejects mandatory method-stack topology, and strengthens verifier live-section binding.

Assistant copied the exact stable source into CFE, created a CFE-specific adoption overlay excluding TQ2-local rules, updated the SOP line in `state/current.md`, and initialized `state/live_shadow.md`.

No CFE scientific claim or architecture was promoted by the SOP change.

---

## Exchange — USER
Timestamp: 2026-08-29
Tags: PROCEED, BUILD-COMMIT

User instructed: `Proceed`.

---

## Exchange — ASSISTANT
Timestamp: 2026-08-29 ET / 2026-08-30 UTC
Tags: RECOVERY, AUDIT, RUNTIME QUALIFICATION, NF4 BASELINE, STATE CHANGE

Assistant re-read CFE continuity/state surfaces and found the old current-state header stale. Live machine inspection verified that `CFE_RND_V1_0_PREEXECUTION` already exists and contains the v1.0 qualification surface.

Recovered verified v1.0 evidence includes: 4/4 narrow regeneration pass, earlier 55/55 full pytest pass, current 56/56 premodel pytest pass, 48-artifact v1.0 input lock, 347-check static hostile pass, all 1,680 legal strict-control scrambles audited, preregistered seed-extension rule, and unchanged v0.9 parent after fork.

Local-first asset receipt showed C:, D:, and E: had been searched for the exact Argilla revision before network use. A prior host-prep execution then downloaded exact revision `d06c86726aadd8dadb92c5b9b9e3ce8ef246c471` into `D:\CFE_HF_CACHE`. Runtime tokenizer replay reported zero mismatches across both 72-row v1.0 arms.

Assistant executed the remaining runtime gates:
- CUDA profile fit: first preregistered `all_linear_r8` profile fit successfully and was locked.
- Two-run same-seed repeatability: PASS; required witnesses matched exactly.

Assistant created fresh scientific run root:
`C:\Users\ancal\ProtoAGI\CFE\CFE_RND_V1_0_PREEXECUTION\executed\CFE_V10_FIRST_SCREEN_20260830T013957Z`
and bound exact copies of host/profile/repeatability/runtime identity artifacts.

NF4 native baseline evaluation then completed over 264 sealed cases:
- field 9/144 = 0.0625
- LHIT 24/96 = 0.25
- retention 10/24 = 0.4166666667
- structural combined 33/240 = 0.1375
- results SHA-256 `e7634de0eea4973064a1d291853ad393860546439ad4a81e866a8fd0d3101e8d`

No CONTROL/TREATMENT adapter training had begun at this point. Current and next-step state were rewritten to the verified live frontier; Live Shadow was updated. Next action: Stage-1 seed `2026082501`, CONTROL then TREATMENT, with immediate sealed evaluation after each arm.


---

## Exchange — USER
Timestamp: 2026-08-29
Tags: CONTINUE, RECOVERY

User instructed: "Pick up where you left off".

---

## Exchange — ASSISTANT
Timestamp: 2026-08-29
Tags: RECOVERY, AUDIT, BUILD-COMMIT, STATE REPAIR

Assistant rehydrated from the CFE Live Shadow and reconciled the live machine against stale state files.

Verified that CFE had advanced substantially beyond the old pre-v1.0 checkpoint:
- live `CFE_RND_V1_0_PREEXECUTION` child exists;
- premodel pytest is 56 passed;
- sealed v0.9 parent was reverified unchanged after fork;
- exact Argilla CapybaraHermes revision was acquired after a recorded C:/D:/E: local-first search found no exact pinned snapshot;
- runtime tokenizer equality passed;
- CUDA profile lock selected `all_linear_r8` with eager attention and fail-closed determinism;
- two same-seed one-step qualification runs matched required witnesses;
- NF4 base evaluation completed before scientific training.

A live Stage-1 training process was found for seed `2026082501`, arm `CONTROL_STRICT_CELL_SCRAMBLE`, under run root `CFE_V10_FIRST_SCREEN_20260830T013957Z`.

The original PowerShell launcher parent was no longer present, while its CONTROL Python child remained alive. Therefore the current arm could finish, but the original launcher could not advance the frozen paired sequence afterward.

Assistant audited the training/evaluation/analyzer/seed-extension code. Verified that paired seed/run is the inferential unit, evaluation rows are nested, family/domain slices cannot change the extension decision, and the extension rule is mechanical from the three Stage-1 structural deltas.

Assistant built `tools/resume_v10_first_screen.py` as a fail-closed recovery path. It compiles and, in audit-only mode, correctly refused to advance because the current CONTROL output directory existed without `RUN_MANIFEST.json`. It does not overwrite partial/corrupt output and only advances the first missing frozen step after verification.

Created `state/v10_fork/LIVE_V10_RECOVERY_2026-08-29T2206_ET.json`, then replaced stale `state/current.md`, `state/next_steps.md`, and `state/live_shadow.md` with the verified live frontier.

No scientific effect was promoted. No active training process was terminated or duplicated.

---

## Exchange — USER
Timestamp: 2026-08-29 22:13 ET
Tags: PROCEED, STATUS REQUEST

User instructed: `Proceed and give me a status update`.

---

## Exchange — ASSISTANT
Timestamp: 2026-08-29 22:13–22:20 ET
Tags: BUILD-COMMIT, CONTROL TRAIN COMPLETE, EVALUATION STARTED, WRAPPER SCAR

Assistant re-read the live Stage-1 execution state and verified seed `2026082501` CONTROL training was still active at 29/36 optimizer steps, then monitored it to completion without restarting or changing the frozen profile.

CONTROL training completed 36/36 and emitted `RUN_MANIFEST.json`. Verified witnesses include:
- final trainable SHA-256 `7c16a5dcc81330a24f8407a827d66ede4afa8464aa181fea34f4596fe33867d9`;
- adapter model SHA-256 `56e3178850b10c84fbebb3d8996b64fe207a8013e8fbac92e6844cf87c82f298`;
- adapter README/config/model files match the training manifest exactly;
- Trainer-reported train loss `0.027677866982988537`.

The first CONTROL evaluation invocation failed closed before model inference because the wrapper supplied the training parent directory to `--adapter` instead of the `adapter/` child directory. The failed eval directory contained no result files and was preserved as `CONTROL_STRICT_CELL_SCRAMBLE__FAILED_WRAPPER_BAD_ADAPTER_PATH`.

Assistant verified all actual adapter payload bytes against the producer run manifest, then relaunched the sealed 264-case CONTROL evaluation with the exact adapter directory and producer `RUN_MANIFEST.json`. At the last readback the corrected evaluator had started, passed the 48-artifact input lock, was loading the pinned checkpoint, and had not yet emitted `EVAL_MANIFEST.json`.

TREATMENT was not started early. No scientific effect claim was made.

---

## Exchange — USER
Timestamp: 2026-08-29 23:14 ET
Tags: PROCEED, BUILD-COMMIT

User instructed: `Proceed`.

---

## Exchange — ASSISTANT
Timestamp: 2026-08-29 23:14 ET
Tags: CONTROL EVAL COMPLETE, TREATMENT STARTED, STATE CHANGE

Assistant resumed from the corrected seed `2026082501` CONTROL evaluation. The sealed CONTROL `EVAL_MANIFEST.json` was present and verified:
- 264 cases;
- field 96/144 = 0.6666666667;
- LHIT 12/96 = 0.125;
- retention 16/24 = 0.6666666667;
- structural combined 108/240 = 0.45;
- results SHA-256 `d81771288aecb9e1e6a2961797d0593d5e73d91f2348ae3a2156545d6c749bc4`;
- producer run-manifest SHA-256 matches the CONTROL training manifest exactly;
- input-lock and host-lock identities match the frozen screen.

Assistant then started seed `2026082501` TREATMENT (`TREATMENT_NEIGHBORHOOD`) under the same host lock, profile lock, and static input lock. The treatment process passed the 48-artifact input lock, loaded all three pinned checkpoint shards, and entered the 36-step optimizer loop. At the latest bounded readback no treatment run manifest existed yet, so treatment is active, not completed.

No treatment-effect claim was made. CONTROL-vs-base movement remains descriptive only until paired TREATMENT and remaining preregistered seeds exist.

---

## Exchange — USER
Timestamp: 2026-08-29 23:14+ ET
Tags: RECOVERY QUESTION

User asked: `What happened?`

---

## Exchange — ASSISTANT
Timestamp: 2026-08-29 23:14+ ET
Tags: RECOVERY, FIRST PAIRED SEED COMPLETE

Assistant verified the apparent failure was in the chat/control-plane inference call, not the CFE scientific execution. Seed `2026082501` TREATMENT had continued on the machine, completed 36/36 training, and completed its sealed 264-case evaluation.

Verified first paired-seed result:
- CONTROL structural combined: 108/240 = 0.45;
- TREATMENT structural combined: 120/240 = 0.50;
- paired structural delta: +5.0 points for TREATMENT;
- field delta: 0.0;
- LHIT delta: +12.5 points (+12/96 correct);
- retention delta: -12.5 points (-3/24 correct).

TREATMENT result SHA-256: `8a1aa588cd2c9c773aba60fad1281cc11fbb422d259a7e26100cc03177377cc6`. Producer run-manifest and results bindings verified exactly.

This is directionally favorable but mixed one-seed evidence only. No CFE effect was promoted. Resume point advanced to seed `2026082502`, frozen order TREATMENT then CONTROL.

---

## Exchange — USER
Timestamp: 2026-08-29 23:14+ ET
Tags: CONTROL-PLANE FAILURE, RECOVERY

User observed that the assistant appeared to hang up after repeated inference failures.

---

## Exchange — ASSISTANT
Timestamp: 2026-08-29 23:14+ ET
Tags: RECOVERY, LIVE STATE RECONCILIATION

Assistant verified the server backend was healthy and that the failures were in the call/response path, not in CFE scientific execution.

Live CFE receipts showed additional progress during the chat failure:
- seed `2026082502` TREATMENT training and sealed evaluation completed;
- TREATMENT structural combined = 131/240 = 0.5458333333;
- field = 96/144 = 0.6666666667;
- LHIT = 35/96 = 0.3645833333;
- retention = 15/24 = 0.625;
- final trainable SHA-256 `aa81f3216a8e07e2082b920431f186acfb7a317d20fcf387803bcd4cdfa5e3df`.

Seed `2026082502` CONTROL was found actively running under the frozen host/profile/input-lock identity. Latest GPU telemetry showed about 5.86/6.14 GB VRAM and up to 100% utilization; no first optimizer-step line or `RUN_MANIFEST.json` existed yet, so it was classified as startup/model-load, not completed.

Continuity surfaces were updated to resume from seed `2026082502` CONTROL completion/evaluation.

---

## Exchange — USER
Timestamp: 2026-08-30 02:02 ET
Tags: BUILD-COMMIT, LONG CAMPAIGN, UNTIL BLOCKER

User instructed: `Resume, push long campaigns til substantive blocker`.

---

## Exchange — ASSISTANT
Timestamp: 2026-08-30 02:03 ET
Tags: SUPERVISOR LAUNCHED, STAGE2 CONTINUOUS EXECUTION

Assistant re-grounded on the Stage-2 frontier. Verified seed `2026082504` TREATMENT training and sealed evaluation were complete; seed `2026082504` CONTROL was the first missing frozen step and no CFE scientific child was active.

Assistant inspected `tools/resume_v10_first_screen.py` and confirmed it is a fail-closed one-step runner covering the remaining Stage-2 train/eval sequence plus Stage-2 qualification and analysis, with no further adaptive seed extension.

Assistant added `tools/run_v10_until_blocker.py` as a local supervisor that repeatedly audits the one-step recovery runner, executes exactly one lawful step, re-audits, and stops on BLOCKED, nonzero execution, unparseable/unknown state, max-step guard, or the preregistered Stage-2 terminal. Supervisor SHA-256: `26391aca016467b6c697ad078fd4bc868f855287cf59d55b06030c5c7386dff2`.

The project async job surface returned known `EXECUTION_SUBMIT_FAILED: job not found`, so assistant fell back to a durable local Popen supervisor with persisted stdout/stderr and PID metadata. The supervisor launched successfully and selected seed `2026082504` CONTROL training as step 1. Live process inspection confirmed the exact CONTROL training command under the Stage-2 extension-decision binding. No scientific parameters were changed.

---

## Exchange — USER
Timestamp: 2026-08-30
Tags: PROCEED, POST-SCREEN REDESIGN

User instructed: `oroceed` (interpreted as `proceed`).

---

## Exchange — ASSISTANT
Timestamp: 2026-08-30
Tags: HOSTILE AUTOPSY, V11 CANDIDATE, STATIC QUALIFICATION, STATE CHANGE

Assistant resumed from the completed six-seed v1.0 screen and ran a post-screen hostile causal autopsy rather than extending v1.0 beyond preregistration.

Verified post-hoc findings:
- six-seed structural TREATMENT-minus-CONTROL signs are `+/-/+/-/+/-`, secondary mean about -0.01944;
- discordant outcomes are strongly family-dependent: `warrant_vs_taint/catalog_review` favors TREATMENT while `bounded_transport/scheduler_buffer` strongly favors CONTROL, especially LHIT;
- adapter norm/distance/cosine do not explain the sign flips;
- learner-visible treatment blocks are more locally homogeneous than control blocks because neighborhood identity is embodied through shared base-state/context realization, not through serialized curator metadata.

Assistant persisted `state/analysis/HOSTILE_CAUSAL_AUTOPSY_V10_2026-08-30.md`.

A naive Relation×Surface 2×2 redesign was drafted, then challenged/demoted after verifying that `neighborhood_id` is curator-only and the shared visible context is the learner-visible carrier of neighborhood identity.

Assistant then built a cleaner v1.1 neighborhood-concentration dose candidate:
- `K1_TRUE_NEIGHBORHOOD` = 1 neighborhood per 4-cell block;
- `K2_PAIRED_NEIGHBORHOODS` = balanced 2+2 across 2 neighborhoods;
- `K4_STRICT_SCRAMBLE` = 4 neighborhoods per block.

The first K2 construction failed closed because rotating the 2+2 partition per block reused/omitted source objects. The compiler was corrected to rotate partitions by family/domain group; the corrected candidate uses each of the 288 source experiences exactly once per arm and balances the three 2+2 partitions 24/24/24.

Exact pinned-tokenizer audit passed for all three arms:
- 72 sequences per arm;
- 33,646 total tokens per arm;
- 3,288 supervised tokens per arm;
- max sequence 499;
- every pairwise arm comparison has 70/72 exact sequence lengths, max absolute delta 1, and paired supervised-token equality.

Assistant generated a fresh held-out evaluation source with new domains/vocabulary (`cargo_ledger`, `telemetry_ring`, `audit_dossier`), 144 field objects and 96 LHIT trajectories. It is explicitly labeled fresh but not blind or independent replication. Compiled fresh prompts are all exact-unique and have zero exact overlap with training individual experiences or the old v1.0 evaluation surface.

A fresh six-seed schedule (`2026082701..06`) was frozen as a draft candidate using all six permutations of K1/K2/K4 once, so every arm appears twice in each serial position.

Static hostile qualification `state/qualification/V11_STATIC_HOSTILE_CANDIDATE_2026-08-30.json` then passed 670 checks with zero failures. Status: `PASS_CANDIDATE__NOT_LOCKED__NOT_RUNTIME_QUALIFIED__NOT_TRAINED`.

No v1.1 scientific training has started. Resume point: build evaluator wiring for the fresh surface, freeze v1.1 training contract/input lock/preregistration, then run exact runtime replay and repeatability before any model outcome is observed.

---

## Exchange — USER
Timestamp: 2026-08-30
Tags: GITHUB PUBLICATION, CONTINUITY HARDENING, PROJECT POLICY

Operator reported the local server was back and ordered a full CFE GitHub publication to `SEng-Kitathas/Cognitive-Field-Engineering`, including continuity documents, reincarnation documentation, subtleties/nuance, commander intent, project history, engineering decisions, prohibitions against regression/reintroduction, the R3.1 SOP archive, and a `this conversation.md` continuity transcript. Operator required enough fidelity that the next thread can continue without re-explaining the project, required Git continuity to become a per-turn project policy, and explicitly required that installing/pulling the OS/runtime not force the entire R&D dump.

---

## Exchange — ASSISTANT
Timestamp: 2026-08-30
Tags: BUILD-COMMIT, PUBLICATION BOUNDARY, R3.1 ARCHIVE, SAFETY GATE

Assistant verified the CFE control plane healthy, found the local CFE root was not itself a Git repository, found the target GitHub repository reachable and empty over HTTPS, and found GitHub CLI/SSH unauthenticated. A separate publication checkout was cloned at `publication/github/Cognitive-Field-Engineering`. The publication was designed as a thin normal clone: active code/state/research/campaign continuity and small reproducibility artifacts in Git; heavyweight reincarnation archives, models, checkpoints and executed weight payloads as opt-in GitHub Release/archive assets referenced by hashes.

Publication documentation added: reincarnation read-first, commander intent, scientific claim ledger, project history/decisions, do-not-reintroduce ledger, publication/asset boundary, GitHub publication policy, per-turn Git continuity policy, transcript reconstruction, heavy-asset manifest, and explicit archive-fetch/turn-commit scripts. Full R3.1 SOP source ZIP was located, SHA-256 matched `4d205becc2413889bdb37c6b6ff7513d6f759a7dff1d9f9b8fddaddd8235a278`, CRC passed, and all 46 entries were extracted into the publication with an entry-level manifest. Publication safety scan passed: 228 files, ~2.31 MB, zero secret-token/private-key detections, zero forbidden binary/model/archive payloads, zero files >10 MB. Git commit/push/readback remained the next exact step.
