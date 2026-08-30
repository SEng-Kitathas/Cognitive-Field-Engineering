# CFE Autonomous Helix Campaign 3 — local model/venv/cache readiness

Seed is Campaign 2 P20's generated next question. This campaign enforces the operator directive: search local drives before any model/weight download. Research only; no promotion authority. P20 hard-stops and emits the next actionable CFE discriminator.

## P01
**Question:** Which exact local model/weight artifacts, venvs, and caches can satisfy CFE’s pinned training-base and runtime requirements without network acquisition, and what identity gaps remain?
**Answer:** The required trainable base is `argilla/CapybaraHermes-2.5-Mistral-7B` at revision `d06c86726aadd8dadb92c5b9b9e3ce8ef246c471`; current local candidates are not yet proven exact matches.
**Evidence:** Sealed v0.9 `training_contract.json` plus local drive inventory.
**OARR:** A same-family Mistral checkpoint can still be a different fine-tune and invalidate the experiment.
**Loop+:** Classify each local asset by repo/revision/quantization/role before reuse.
**Helix:** Survivor = exact pinned base identity. Scar = local presence does not imply contract match. Demotion = family-name equivalence.
**Reservoir:** Model identity evidence.
**Disposition:** AUDIT; confidence 0.99.
**Next:** Does the local three-shard `mistral_capybara_3shard` checkpoint satisfy the exact pinned CFE base contract?

## P02
**Question:** Does the local three-shard `mistral_capybara_3shard` checkpoint satisfy the exact pinned CFE base contract?
**Answer:** No evidence supports that substitution: its manifest identifies `kaist-ai/mistral-orpo-capybara-7k`, not the pinned Argilla CapybaraHermes revision.
**Evidence:** Local `HF_VERIFICATION_MANIFEST.json`, README, config, and sealed v0.9 contract.
**OARR:** The tensors can share Mistral architecture while encoding different fine-tuning history.
**Loop+:** Compare config/tokenizer and repo lineage, but do not promote architecture similarity into identity.
**Helix:** Survivor = reject ORPO shard substitution. Scar = architecture sameness is not weight identity. Demotion = ORPO shards as CFE base.
**Reservoir:** Repo/revision lineage.
**Disposition:** AUDIT; confidence 0.99.
**Next:** Can the local Q3_K_S CapybaraHermes GGUF serve as the trainable NF4/QLoRA baseline?

## P03
**Question:** Can the local Q3_K_S CapybaraHermes GGUF serve as the trainable NF4/QLoRA baseline?
**Answer:** No. The sealed law explicitly says `Q3_BASELINE != NF4_QLORA_HOST_BASELINE`; Q3 is tokenizer/low-resource runtime reference only.
**Evidence:** `training_contract.json` model law plus local `MODEL_MANIFEST.json`.
**OARR:** Matching upstream family does not erase quantization and artifact-format differences.
**Loop+:** Use Q3 only for tokenizer/runtime reference where the contract permits.
**Helix:** Survivor = Q3 role bounded. Scar = quantized runtime probe is not trainable host baseline. Demotion = Q3 as NF4 base.
**Reservoir:** Quantization/role evidence.
**Disposition:** AUDIT; confidence 0.99.
**Next:** What local artifact would qualify as a lawful substitute for network snapshot download?

## P04
**Question:** What local artifact would qualify as a lawful substitute for network snapshot download?
**Answer:** A complete local HF-style snapshot byte-identifiable to the pinned repo/revision, with required config/tokenizer/index/shards and verifiable file hashes.
**Evidence:** `prepare_host_v09.py`; `RUNBOOK.md`.
**OARR:** A copied snapshot without commit/revision evidence may be stale or repacked.
**Loop+:** Accept only after identity, completeness, tokenizer, and manifest checks.
**Helix:** Survivor = local-first exact snapshot reuse. Scar = local cache needs provenance. Demotion = any-Mistral-folder substitution.
**Reservoir:** Snapshot-integrity evidence.
**Disposition:** BUILD-PLAN; confidence 0.98.
**Next:** How should the drives be searched for that exact pinned snapshot without relying on default Hugging Face cache paths?

## P05
**Question:** How should the drives be searched for that exact pinned snapshot without relying on default Hugging Face cache paths?
**Answer:** Search C:, D:, and E: for the exact revision string, repo slug, HF snapshot commit directory, shard/index patterns, tokenizer/config files, and content metadata before download.
**Evidence:** Operator directive plus visible-drive inventory.
**OARR:** A renamed folder may hide the exact snapshot even if names do not match.
**Loop+:** Search file contents/metadata as well as directory names.
**Helix:** Survivor = whole-drive asset search. Scar = default cache emptiness was insufficient. Demotion = default-cache-only search.
**Reservoir:** Filesystem inventory.
**Disposition:** EXECUTE; confidence 0.99.
**Next:** What checks prove that a discovered local snapshot is the pinned revision rather than merely compatible?

## P06
**Question:** What checks prove that a discovered local snapshot is the pinned revision rather than merely compatible?
**Answer:** Require repo/revision metadata or commit-path evidence, complete expected file set, hash manifest, config identity, and exact runtime tokenizer equality against all 144 sealed token references.
**Evidence:** `prepare_host_v09.py`; `RUNBOOK.md` stage 4.
**OARR:** Tokenizer equality alone cannot prove weight identity.
**Loop+:** Keep tokenizer proof and weight/revision proof as separate gates.
**Helix:** Survivor = dual weight/tokenizer identity. Scar = tokenizer match is not weight match. Demotion = tokenizer-only qualification.
**Reservoir:** Snapshot plus tokenizer evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** If an exact local pinned snapshot is found, should `snapshot_download` still be allowed to hit the network?

## P07
**Question:** If an exact local pinned snapshot is found, should `snapshot_download` still be allowed to hit the network?
**Answer:** No network acquisition is needed; bind host preparation to the verified local snapshot/cache path or offline resolution and record source identity.
**Evidence:** Operator directive; local-first doctrine.
**OARR:** Accidental online refresh could silently change files or provenance.
**Loop+:** Run offline/fail-closed and verify no network dependency for the qualified path.
**Helix:** Survivor = local-first reuse. Scar = network refresh can perturb identity. Demotion = redundant download.
**Reservoir:** Offline execution evidence.
**Disposition:** BUILD-PLAN; confidence 0.98.
**Next:** Which existing environment is the incumbent runtime for CFE model work?

## P08
**Question:** Which existing environment is the incumbent runtime for CFE model work?
**Answer:** `C:/Users/ancal/ProtoAGI/CFE/.venv_cuda/Scripts/python.exe` is the qualified incumbent; it reports Python 3.12.10 and has preserved host evidence.
**Evidence:** Live reconciliation plus `host_qualification`.
**OARR:** Another CUDA venv may have newer packages but is not automatically qualified for CFE.
**Loop+:** Compare other venvs only if the incumbent lacks a required package or host capability.
**Helix:** Survivor = qualified CFE venv. Scar = newer environment is not qualified environment. Demotion = venv novelty.
**Reservoir:** Runtime-environment evidence.
**Disposition:** AUDIT; confidence 0.99.
**Next:** What package/CUDA evidence must be checked in that venv before the pinned snapshot preflight?

## P09
**Question:** What package/CUDA evidence must be checked in that venv before the pinned snapshot preflight?
**Answer:** Verify torch/CUDA/GPU visibility plus exact transformers, peft, bitsandbytes, accelerate and supporting package versions; bind pip freeze/runtime manifest.
**Evidence:** `RUNBOOK.md` plus bootstrap hostile repair.
**OARR:** Imports can succeed while bitsandbytes CUDA kernels fail at runtime.
**Loop+:** Include an actual NF4 load/one-step execution probe, not imports alone.
**Helix:** Survivor = runtime stack qualification. Scar = import success is not CUDA execution. Demotion = import-only qualification.
**Reservoir:** Package plus CUDA execution evidence.
**Disposition:** VERIFY; confidence 0.98.
**Next:** What profile-selection rule governs the 6 GB RTX 4050 before any scientific arm trains?

## P10
**Question:** What profile-selection rule governs the 6 GB RTX 4050 before any scientific arm trains?
**Answer:** Test preregistered profiles in priority order: all-linear rank-8 first, q/v rank-8 fallback only if needed; lock the first profile that completes.
**Evidence:** `training_contract.json` adapter profiles and profile-selection law.
**OARR:** Choosing the profile after viewing scientific outcomes would adapt treatment to results.
**Loop+:** Keep evaluator inaccessible and profile lock pre-scientific.
**Helix:** Survivor = pre-outcome profile lock. Scar = host-fit selection is not outcome adaptation. Demotion = outcome-driven profile choice.
**Reservoir:** `PROFILE_LOCK` evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What exactly must the CUDA fit probe execute to count as a profile fit?

## P11
**Question:** What exactly must the CUDA fit probe execute to count as a profile fit?
**Answer:** On the longest sealed training sequence: real forward, backward, optimizer step, synchronized completion, trainable hash/count, and peak memory capture without OOM.
**Evidence:** `preflight_cuda_fit_v09.py`.
**OARR:** A forward-only fit can underestimate training memory.
**Loop+:** Record allocated/reserved memory plus failure details for rejected profiles.
**Helix:** Survivor = one-step real training fit. Scar = inference fit is not training fit. Demotion = forward-only preflight.
**Reservoir:** CUDA profile evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What tokenizer gate must pass after resolving the exact pinned snapshot?

## P12
**Question:** What tokenizer gate must pass after resolving the exact pinned snapshot?
**Answer:** Runtime tokenizer outputs must exactly equal sealed Q3 token references for all 144 CONTROL/TREATMENT arm sequences; any mismatch blocks training.
**Evidence:** `prepare_host_v09.py`; `RUNBOOK.md` stage 4.
**OARR:** Matching tokenizer files by name does not prove serialized behavior.
**Loop+:** Compare exact input-id arrays and mismatch hashes per row.
**Helix:** Survivor = 144-sequence tokenizer identity. Scar = file-name identity is not token behavior. Demotion = tokenizer-name check.
**Reservoir:** Token-reference evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What baseline evaluation must occur before adapter training begins?

## P13
**Question:** What baseline evaluation must occur before adapter training begins?
**Answer:** Evaluate the exact NF4 pinned base on frozen internal field/LHIT and retention surfaces before any scientific adapter modifies behavior.
**Evidence:** `RUNBOOK.md` stage 6.
**OARR:** Using Q3 results as baseline would mix quantization and weight-level effects.
**Loop+:** Bind base results to snapshot/environment manifests.
**Helix:** Survivor = exact NF4 base baseline. Scar = Q3 baseline is not host baseline. Demotion = Q3 baseline substitution.
**Reservoir:** Base-evaluation evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What scientific execution schedule is fixed once host/profile/base gates pass?

## P14
**Question:** What scientific execution schedule is fixed once host/profile/base gates pass?
**Answer:** Run three paired seeds 2026082501/2/3 with preregistered alternating arm order: CONTROL/TREATMENT, TREATMENT/CONTROL, CONTROL/TREATMENT.
**Evidence:** `training_contract.json` seeds plus execution order.
**OARR:** Changing order after thermal observations would reintroduce adaptation.
**Loop+:** Capture wall-clock/thermal telemetry without changing preregistered order.
**Helix:** Survivor = three paired seeds. Scar = host order effects remain inspectable. Demotion = dynamic arm order.
**Reservoir:** Execution-order evidence.
**Disposition:** BUILD-PLAN; confidence 0.99.
**Next:** What initialization proof is required inside each paired seed before optimization?

## P15
**Question:** What initialization proof is required inside each paired seed before optimization?
**Answer:** Hash all trainable LoRA parameters immediately after creation and require CONTROL/TREATMENT equality within that seed.
**Evidence:** `RUNBOOK.md` stage 9.
**OARR:** Same random seed can still yield different initialization if call order/environment diverges.
**Loop+:** Fail closed on hash mismatch before training.
**Helix:** Survivor = paired initialization identity. Scar = seed value alone is insufficient. Demotion = seed-only init proof.
**Reservoir:** Trainable-hash evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What training-completion invariant must every one of the six adapter runs satisfy?

## P16
**Question:** What training-completion invariant must every one of the six adapter runs satisfy?
**Answer:** Exactly 36 optimizer steps under the locked profile/hyperparameters, with per-step logs and no silent early completion.
**Evidence:** `training_contract.json`; `RUNBOOK.md` stage 8.
**OARR:** Exit 0 can coexist with fewer steps.
**Loop+:** Qualify `global_step == 36` before adapter acceptance.
**Helix:** Survivor = 36-step exposure. Scar = exit 0 is not matched training. Demotion = exit-code-only completion.
**Reservoir:** Training-step evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What artifact verification is required before loading any trained adapter into the evaluator?

## P17
**Question:** What artifact verification is required before loading any trained adapter into the evaluator?
**Answer:** Hash-verify adapter bytes and bind them to arm/seed/training manifest before evaluation; evaluator uses frozen inputs and no training-policy feedback.
**Evidence:** `RUNBOOK.md` stages 10-12.
**OARR:** Correct directory names can conceal stale or overwritten adapter files.
**Loop+:** Reject hash mismatch before model load.
**Helix:** Survivor = adapter byte identity. Scar = path identity is not byte identity. Demotion = path-only adapter load.
**Reservoir:** Adapter-manifest evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What conclusions may the scientific analyzer emit after a mechanically successful screen?

## P18
**Question:** What conclusions may the scientific analyzer emit after a mechanically successful screen?
**Answer:** Descriptive paired deltas under the bounded estimand only; it cannot promote “CFE works,” general reasoning, internal representation, external transfer, Microseed, or archetype claims.
**Evidence:** `training_contract.json` `claims_not_authorized`; `RUNBOOK.md`.
**OARR:** Mechanically clean execution can tempt narrative overreach.
**Loop+:** Require separate hostile scientific interpretation before promotion consideration.
**Helix:** Survivor = bounded scientific claims. Scar = execution integrity is not CFE effect. Demotion = automatic positive promotion.
**Reservoir:** Scientific-analysis evidence.
**Disposition:** AUDIT; confidence 0.99.
**Next:** What storage, cache, and offline-readiness conditions should be checked before host preparation uses any exact local pinned snapshot?

## P19
**Question:** What storage, cache, and offline-readiness conditions should be checked before host preparation uses any exact local pinned snapshot?
**Answer:** Confirm roughly 15 GB+ free for the pinned HF snapshot plus adapters/caches, a stable local cache/snapshot path, read access, and an offline path that does not trigger network refresh.
**Evidence:** `RUNBOOK.md` hardware expectation plus operator local-first directive.
**OARR:** A valid snapshot can still fail operationally if the chosen drive cannot hold cache/adapters or the loader silently tries to redownload missing files.
**Loop+:** Dry-run file completeness and offline resolution before CUDA model loading.
**Helix:** Survivor = local snapshot operational readiness. Scar = identity pass does not imply cache/disk readiness. Demotion = assume-default-cache sufficiency.
**Reservoir:** Disk, cache, and offline execution evidence.
**Disposition:** VERIFY; confidence 0.96.
**Next:** What is the correct response if any host, tokenizer, profile, run, adapter, or qualification gate fails mid-screen?

## P20 — HARD STOP
**Question:** What is the correct response if any host, tokenizer, profile, run, adapter, or qualification gate fails mid-screen?
**Answer:** Preserve the failed run; diagnose and revise if needed; hostile-pass the revision; restart a fresh complete screen rather than patch/resume matched claims.
**Evidence:** `RUNBOOK.md` failure rule.
**OARR:** Continuing only the failed arm breaks matched causal conditions.
**Loop+:** Require a new run identity and full paired restart after material changes.
**Helix:** Survivor = fail-closed full restart. Scar = half-screen continuation invalidates parity. Demotion = resume-in-place.
**Reservoir:** Failure provenance.
**Disposition:** HARD_STOP_P20; confidence 0.99. Promotion authority = NONE.
**Next:** Can the exact pinned `argilla/CapybaraHermes-2.5-Mistral-7B` revision `d06c86726aadd8dadb92c5b9b9e3ce8ef246c471` be located and fully qualified somewhere on C:, D:, or E: without any network acquisition?
