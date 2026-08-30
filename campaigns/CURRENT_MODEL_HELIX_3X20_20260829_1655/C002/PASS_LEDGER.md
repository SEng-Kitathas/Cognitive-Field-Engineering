# CFE Autonomous Helix Campaign 2 — causal-identification hardening

Seed is Campaign 1 P20's generated next question. Research only; no promotion authority. Each pass includes OARR, Loop+, Helix, Reservoir, and a generated next discriminator. P20 hard-stops and emits Campaign 3's seed.

## P01
**Question:** What is the strongest remaining threat to causal identification in CFE v1.0 after portability and regression gates are repaired?
**Answer:** The strongest threats are non-independent evaluation units and learner-visible shortcut/confound leakage; both can fake treatment effects.
**Evidence:** Campaign 1 plus preregistered repair list.
**OARR:** Perfect causal-unit accounting cannot rescue a treatment/control content leak.
**Loop+:** Pressure statistical independence and information parity as separate axes.
**Helix:** Survivor = causal-identification focus. Scar = multiple threats can coexist. Demotion = software-only readiness.
**Reservoir:** Causal-threat classes.
**Disposition:** DISCUSSION; confidence 0.93.
**Next:** What estimand should the first causal screen actually claim if it succeeds?

## P02
**Question:** What estimand should the first causal screen actually claim if it succeeds?
**Answer:** At most the matched local-neighborhood co-visibility training effect under this exact learner/compiler/training regime.
**Evidence:** v0.9 `RUNBOOK.md`.
**OARR:** Calling the estimand “general reasoning improvement” exceeds the sealed contract.
**Loop+:** Keep external transfer and internal representation as separate future hypotheses.
**Helix:** Survivor = bounded first-screen estimand. Scar = general CFE claims unauthorized. Demotion = general-reasoning estimand.
**Reservoir:** Claim-scope evidence.
**Disposition:** DISCUSSION; confidence 0.99.
**Next:** What is the independent experimental unit for inference under that estimand?

## P03
**Question:** What is the independent experimental unit for inference under that estimand?
**Answer:** The independently trained paired seed/run is the defensible unit; prompt/eval rows are nested measurements within it.
**Evidence:** `training_contract.json` seeds plus pseudoreplication repair.
**OARR:** Three paired seeds provide limited independent N, so uncertainty must remain wide.
**Loop+:** Retain row-level diagnostics without converting them into independent replicates.
**Helix:** Survivor = seed/run unit. Scar = N=rows is invalid. Demotion = prompt-row N.
**Reservoir:** Unit-of-analysis evidence.
**Disposition:** BUILD-PLAN; confidence 0.94.
**Next:** Which CONTROL/TREATMENT factors must be held identical so the estimand remains causal?

## P04
**Question:** Which CONTROL/TREATMENT factors must be held identical so the estimand remains causal?
**Answer:** Base revision/tokenizer, learner-visible burden, targets, optimizer schedule, adapter profile, seed handling, evaluator, and runtime qualification must match except intended neighborhood structure.
**Evidence:** `training_contract.json`; `RUNBOOK.md`.
**OARR:** Wall-clock/thermal order can still confound otherwise matched arms.
**Loop+:** Use preregistered alternating arm order across seeds.
**Helix:** Survivor = paired-arm parity. Scar = order confounding remains. Demotion = loose arm parity.
**Reservoir:** Training-manifest evidence.
**Disposition:** BUILD-PLAN; confidence 0.98.
**Next:** How should the control geometry be checked so it is a true causal comparator rather than a weaker task?

## P05
**Question:** How should the control geometry be checked so it is a true causal comparator rather than a weaker task?
**Answer:** Verify matched family/domain/cell/target support, learner-visible content burden, and sequence/token accounting while scrambling neighborhood co-visibility only.
**Evidence:** `RUNBOOK.md`.
**OARR:** A control that accidentally destroys task difficulty can exaggerate treatment benefit.
**Loop+:** Compare difficulty proxies and exact token/target support by pair.
**Helix:** Survivor = strict causal-cell-matched control. Scar = control weakening can mimic effect. Demotion = nominal scramble sufficiency.
**Reservoir:** Control-geometry evidence.
**Disposition:** VERIFY; confidence 0.96.
**Next:** What leakage audit should run on learner-visible streams before any training?

## P06
**Question:** What leakage audit should run on learner-visible streams before any training?
**Answer:** Search for arm-predictive provenance, warrant, IDs, ordering, metadata, duplicate nuisance features, and unique tokens outside intended geometry.
**Evidence:** Preregistered nuisance-uniqueness repair.
**OARR:** A tokenizer-level shortcut may exist even when human-visible text looks matched.
**Loop+:** Audit both rendered text and token-ID features.
**Helix:** Survivor = learner-visible parity. Scar = human inspection alone can miss token shortcuts. Demotion = text-only leakage audit.
**Reservoir:** Stream plus token evidence.
**Disposition:** VERIFY; confidence 0.94.
**Next:** How should pseudoreplication be removed from the evaluator while preserving useful row-level diagnostics?

## P07
**Question:** How should pseudoreplication be removed from the evaluator while preserving useful row-level diagnostics?
**Answer:** Compute inferential deltas per independent paired seed/run; keep row-level scores descriptive or nested in a hierarchical model.
**Evidence:** P03 plus preregistered repair.
**OARR:** A hierarchical model with only three clusters can still look overconfident.
**Loop+:** Report cluster count and sensitivity to each seed explicitly.
**Helix:** Survivor = unit-level inference. Scar = small independent N limits precision. Demotion = hierarchical-model overconfidence.
**Reservoir:** Seed-level analysis.
**Disposition:** BUILD-PLAN; confidence 0.92.
**Next:** What uncertainty reporting is honest with only three paired seeds?

## P08
**Question:** What uncertainty reporting is honest with only three paired seeds?
**Answer:** Report paired seed deltas, robust descriptive intervals/sensitivity, and avoid narrow asymptotic certainty claims treating rows as independent.
**Evidence:** Three preregistered seeds.
**OARR:** A single outlier seed can dominate the sign of the effect.
**Loop+:** Include leave-one-seed-out sign/stability analysis as descriptive pressure.
**Helix:** Survivor = uncertainty proportional to N. Scar = precision is limited. Demotion = row-bootstrap certainty.
**Reservoir:** Uncertainty evidence.
**Disposition:** DISCUSSION; confidence 0.90.
**Next:** When is seed extension lawful if the three-seed screen is inconclusive?

## P09
**Question:** When is seed extension lawful if the three-seed screen is inconclusive?
**Answer:** Only under a precommitted extension trigger, seed list/generation rule, stopping rule, and analysis plan fixed before extension outcomes.
**Evidence:** Seed-extension preregistration requirement.
**OARR:** Outcome-triggered extension can still bias if thresholds are vague.
**Loop+:** Make the inconclusive region and maximum extension explicit.
**Helix:** Survivor = outcome-independent extension. Scar = optional stopping risk. Demotion = ad-hoc extra seeds.
**Reservoir:** Preregistration.
**Disposition:** BUILD-PLAN; confidence 0.95.
**Next:** How does the preregistered alternating wall-clock arm order reduce a host-side confound?

## P10
**Question:** How does the preregistered alternating wall-clock arm order reduce a host-side confound?
**Answer:** It prevents thermal/time order from being perfectly aligned with treatment by alternating CONTROL/TREATMENT order across seeds.
**Evidence:** `training_contract.json` execution order.
**OARR:** Alternation cannot remove drift that changes within each paired run.
**Loop+:** Capture temperature/memory/runtime telemetry to inspect residual order effects.
**Helix:** Survivor = alternating paired order. Scar = residual host drift remains. Demotion = fixed treatment order.
**Reservoir:** Host telemetry.
**Disposition:** VERIFY; confidence 0.98.
**Next:** What initialization equality must be proven within each paired seed?

## P11
**Question:** What initialization equality must be proven within each paired seed?
**Answer:** CONTROL and TREATMENT initial trainable LoRA parameter hashes must be identical within each seed before training diverges.
**Evidence:** `RUNBOOK.md` fail-closed stage 9.
**OARR:** Same seed value does not prove identical initialized trainable tensors.
**Loop+:** Hash trainable parameters immediately after LoRA creation.
**Helix:** Survivor = verified paired initialization. Scar = seed config is not initialization identity. Demotion = seed-only equality.
**Reservoir:** Initial-parameter hashes.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What training-completion equality must be enforced across all six scientific runs?

## P12
**Question:** What training-completion equality must be enforced across all six scientific runs?
**Answer:** Each run must execute exactly 36 optimizer steps under the locked profile and hyperparameters.
**Evidence:** `training_contract.json` expected optimizer steps; `RUNBOOK.md` stage 8.
**OARR:** Exit code 0 with fewer steps is not matched training exposure.
**Loop+:** Qualify `global_step` plus per-step logs before evaluation.
**Helix:** Survivor = matched optimizer exposure. Scar = process exit is not scientific pass. Demotion = exit-code completion.
**Reservoir:** Training logs.
**Disposition:** VERIFY; confidence 0.99.
**Next:** How must the evaluator remain separated from training-policy adaptation?

## P13
**Question:** How must the evaluator remain separated from training-policy adaptation?
**Answer:** Freeze evaluator inputs/rubric and deny evaluator access during profile selection or training; no checkpoint/outcome adaptation.
**Evidence:** `training_contract.json`: evaluator_access false; evaluation during training false.
**OARR:** Manual inspection of held-out outcomes before finalization can still leak policy.
**Loop+:** Record evaluator access boundaries and timestamps.
**Helix:** Survivor = held-out evaluator separation. Scar = human leakage remains possible. Demotion = informal evaluator isolation.
**Reservoir:** Evaluator provenance.
**Disposition:** BUILD-PLAN; confidence 0.97.
**Next:** Why must exact NF4 base evaluation occur before any scientific arm training?

## P14
**Question:** Why must exact NF4 base evaluation occur before any scientific arm training?
**Answer:** It establishes the frozen weight-level baseline before adapters can alter behavior, preserving before/after causal interpretation.
**Evidence:** `RUNBOOK.md` stage 6.
**OARR:** Using the Q3 runtime probe as baseline would confound quantization and weight identity.
**Loop+:** Compare NF4 base only from the exact pinned HF snapshot.
**Helix:** Survivor = exact host-base baseline. Scar = Q3 is not NF4 host baseline. Demotion = Q3 as baseline.
**Reservoir:** Base-evaluation evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What adapter identity checks are required before post-training evaluation?

## P15
**Question:** What adapter identity checks are required before post-training evaluation?
**Answer:** Hash each completed adapter and verify the hash before loading it for evaluation, binding it to seed/arm/training manifest.
**Evidence:** `RUNBOOK.md` stage 10 plus primary evidence list.
**OARR:** A directory name can point to partially overwritten adapter bytes.
**Loop+:** Include adapter file list and hashes in the evaluation manifest.
**Helix:** Survivor = adapter artifact identity. Scar = path identity is not byte identity. Demotion = path-only adapter identity.
**Reservoir:** Adapter hash evidence.
**Disposition:** VERIFY; confidence 0.98.
**Next:** What does an execution-integrity qualifier authorize, and what does it explicitly not authorize?

## P16
**Question:** What does an execution-integrity qualifier authorize, and what does it explicitly not authorize?
**Answer:** It can certify matched execution mechanics; it cannot establish a CFE effect or promote scientific interpretation.
**Evidence:** `RUNBOOK.md` scars; qualifier non-promotion.
**OARR:** A perfectly executed null result is still scientifically meaningful but not a positive CFE claim.
**Loop+:** Separate execution verdict from scientific analyzer and hostile interpretation.
**Helix:** Survivor = execution/science boundary. Scar = integrity pass is not effect. Demotion = execution as scientific promotion.
**Reservoir:** Qualification evidence.
**Disposition:** DISCUSSION; confidence 0.99.
**Next:** What is the fail-closed response to a mid-screen failure or profile change?

## P17
**Question:** What is the fail-closed response to a mid-screen failure or profile change?
**Answer:** Preserve the failed run, diagnose/revise/hostile-pass if needed, then restart the complete screen; do not patch and resume matched claims.
**Evidence:** `RUNBOOK.md` failure rule.
**OARR:** Restarting only the failed arm would break paired comparability.
**Loop+:** Require a new run identity and complete paired execution after material change.
**Helix:** Survivor = fresh-screen restart rule. Scar = half-run repair breaks comparability. Demotion = resume-in-place.
**Reservoir:** Failure/restart evidence.
**Disposition:** BUILD-PLAN; confidence 0.99.
**Next:** Which robustness checks can pressure a positive effect without silently changing the preregistered primary analysis?

## P18
**Question:** Which robustness checks can pressure a positive effect without silently changing the preregistered primary analysis?
**Answer:** Use preregistered or clearly secondary sensitivity checks: per-seed sign, evaluator subsets, control-feature diagnostics, and retention tradeoffs; label them secondary.
**Evidence:** Claim-scope plus preregistration discipline.
**OARR:** Fishing across many metrics can manufacture apparent robustness.
**Loop+:** Track multiplicity and preserve primary/secondary labels.
**Helix:** Survivor = secondary robustness pressure. Scar = robustness search can become p-hacking. Demotion = unbounded metric search.
**Reservoir:** Secondary-analysis ledger.
**Disposition:** DISCUSSION; confidence 0.90.
**Next:** What retention or side-effect evidence must accompany any positive transport effect?

## P19
**Question:** What retention or side-effect evidence must accompany any positive transport effect?
**Answer:** The frozen retention surfaces must remain intact enough to rule out a “gain” produced by broad degradation, forgetting, or evaluation collapse; report tradeoffs beside the primary effect.
**Evidence:** `RUNBOOK.md` frozen internal field/LHIT plus retention surfaces; primary evidence list.
**OARR:** A treatment can improve the target metric by sacrificing unrelated retained behavior, creating a misleading local win.
**Loop+:** Compare paired retention deltas and inspect whether any benefit is merely redistribution of capacity.
**Helix:** Survivor = effect-plus-retention interpretation. Scar = target gain can hide collateral degradation. Demotion = target-only promotion.
**Reservoir:** Retention and side-effect evidence.
**Disposition:** VERIFY; confidence 0.94.
**Next:** What evidence threshold should be required before any positive CFE claim is considered for promotion?

## P20 — HARD STOP
**Question:** What evidence threshold should be required before any positive CFE claim is considered for promotion?
**Answer:** Require a bounded estimand, matched execution, no leakage/control failure, consistent paired-seed direction/magnitude with honest uncertainty, retention evidence, and separate hostile scientific review.
**Evidence:** Combined campaign evidence and sealed claim bounds.
**OARR:** A low p-value from pseudoreplicated rows cannot substitute for causal integrity.
**Loop+:** Promotion review must include demotion triggers and explicitly unauthorized broader claims.
**Helix:** Survivor = promotion requires a causal chain. Scar = statistical significance alone is insufficient. Demotion = p-value promotion.
**Reservoir:** Promotion trace and retention evidence.
**Disposition:** HARD_STOP_P20; confidence 0.95. Promotion authority = NONE.
**Next / Campaign 3 seed:** Which exact local model/weight artifacts, venvs, and caches can satisfy CFE’s pinned training-base and runtime requirements without network acquisition, and what identity gaps remain?
