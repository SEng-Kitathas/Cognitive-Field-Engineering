# CFE NEXT STEPS

> **Authority rule:** This file is chronological work-queue history. Later dated sections supersede earlier conflicting next actions. For bounded active execution priority, use `state/next_steps/ACTIVE_NEXT_STEPS.json` together with `state/live_shadow.md`. Historical queues remain lineage, not current authorization.

As of: 2026-09-02 01:05 Eastern Daylight Time

## Overnight active
1. Complete bounded local archaeology scan.
2. Execute three research lanes: MACHINERY, CARTOGRAPHY, EXTERNAL; each lane is 3x20 autonomous passes with OARR, Loop+, Semantic Helix, Attention Reservoir and CSC audit-only hard stop.
3. Research output remains non-authoritative until morning synthesis/hostile adjudication; no auto-promotion.
4. At research completion, dedicated inference service is terminated and `RESEARCH_LANE_COMPLETE.sentinel` is emitted.
5. DD2R1 then verifies/downloads only the train-manifest-bound seed3121/CYCLIC_SPACED adapter and attempts clean-state evaluation.
6. If salvage evaluation fails after bounded retries: stop DD2R1 with no further training.
7. If salvage evaluation passes: continue seed3121 pair and remaining fresh DD2 pairs under unchanged scientific contract; aggregate only 6/6.
8. Morning readback must reconcile research artifacts against first-class cartography before any promotion or new experiment selection.

## Fleet validation — gated future work
- Preserve and freeze representative pre-CFE phenotype probes before any CFE fleet intervention.
- Inventory eligible local learners/trainable checkpoints.
- Do not launch broad fleet training until the authorization threshold in the fleet research plan is met.

## Rosetta/LBE historical branch — parked but preserved
- Do not mix into active CFE science without explicit branch selection.
- If reopened, first experiment should test whether a function-preserving block representation + small router can outperform ordinary retrieval at equal active-memory/compute budget.
- Use Rosetta structural atlas for candidate motif selection, not as the functional substrate itself.

## Fleet Uplift Pack v2
- Build new v2 pack; do not reuse empty v1 output directory as authoritative artifact.
- Freeze Capybara core first: LDJnr/Capybara + filtered Capybara chosen responses; keep preference pairs for separate preference phase.
- Benchmark candidate modern Capybara bases before download/train selection.
- Repair/upgrade llama.cpp CUDA backend separately; CPU-only 35B-A3B is already usable at ~14 tok/s.

## Resource-gated continuation — 2026-09-02
1. Do not launch Qwen3.5-35B-A3B, MTP, QLoRA, or any other heavy CFE model job while a foreign model runtime is live.
2. Before any later heavy run, execute `tools/cfe_resource_authority_guard.py`; require PASS immediately before launch and again after CFE-owned server startup.
3. When a safe window exists, run `tools/run_qwen35_a3b_mtp_benchmark_safe.py` sequentially: target-only baseline -> Q8 MTP, never concurrently.
4. If MTP fails compatibility or loses throughput, preserve the failure and only then consider a target-distilled MTP/EAGLE/DFlash route.
5. Continue low-impact dataset/LHIT/Capybara design and model-quality research while blocked.

## Speculative runtime next steps — 2026-09-02
1. Treat `Q4_K_M MTP + n_max=2` as the current best-tested local speculative profile for the Claude-distilled Qwen3.5-35B-A3B at 4K/single-slot.
2. Do not use the Q8 MTP sidecar as default on this 6GB GPU; it reduces target residency and lost throughput in paired testing.
3. Before wider deployment, test the chosen Q4/n=2 profile at 8K and 16K context under the same resource guard; stop if another project claims resources.
4. Keep Qwen3.6-35B-A3B and Gemma 4 26B-A4B as model-fit challengers, but do not download/load them until a later safe window and explicit comparison packet is ready.
5. Keep the stale-runtime reclamation rule active: healthy socket alone does not prove current ownership; require multi-signal liveness before preserving a warm load indefinitely.

## Reasoning-trace quarry next steps — 2026-09-02
1. Do not acquire/decode/store exploit-recovered proprietary hidden reasoning blocks; use `arXiv:2608.09867` only as research/security evidence.
2. Add structural reasoning annotations to the Standard Uplift quarantine/A0 pipeline, keeping literal style fingerprints separate from invariant labels.
3. Use open visible reasoning families (DeepSeek-R1/R1-distill, OpenThoughts, qualified open Qwen traces) for same-task/isomorphic trace comparison.
4. Score correction, verification, alternative-path search, currentness, evidence-state separation, question retention, failed-branch recovery, composition, redundancy and token efficiency independently of raw trace length.
5. Treat memorization-shortcut detection as a suspicion label unless contamination/memorization evidence independently confirms it.
6. Feed the resulting invariant/efficiency findings back into A0 selection/rendering; do not expand A0 token budget merely to preserve long source traces.

## High-value reasoning state-transition quarry — 2026-09-02
1. Treat `research/REASONING_STATE_TRANSITION_TOPOLOGY_AND_SILENT_INVARIANTS_2026-09-02.md` as a first-class research input to Standard Uplift Dataset design and future CFE cartography.
2. Build a 50–200 trace lawful/open comparison set across math, code, research, tool-use, and long-horizon currentness tasks.
3. Annotate traces by ordered state transitions/dependency changes, not literal self-talk phrases; keep style fingerprints separate.
4. Test recurrence of: dependency-local invalidation, scoped rollback, unresolved-seam retention, minimal revision, verification escalation, authority transfer, qualified compression, and conditional reasoning effort.
5. Test whether state-transition order predicts success beyond event multiset and token length.
6. Use recurring structures to inform standard-data episode construction, but do not teach the labels as learner ontology by default.
7. Promote no primitive/invariant beyond provisional status without recurrence, hostile comparison, operationalization, and recorded counterexamples/failure boundaries.

## Representation-adequacy / granularity-shift research — 2026-09-02
1. Add representation-level events to the 50–200 trace Silent Invariants quarry: `DETECT_MISSING_DISTINCTION`, `REFINE_REPRESENTATION_GRANULARITY`, `REPLACE_COORDINATE_SYSTEM`, and `REFINEMENT_WITH_CONSERVATION`.
2. Test whether repeated local patch failure predicts later representation refinement and whether that transition improves correctness/token efficiency.
3. Build consequence-aliasing probes: pairs where a coarse representation maps two states together but their relevant consequences differ.
4. In Standard Uplift A0/A1 construction, include some episodes where a coarse abstraction initially works, later boundary evidence defeats it, local patches fail, and a finer distinction becomes necessary; do not explicitly teach the meta-labels.
5. Reconcile this surface with CFE cartography missing-axis audits before promoting any new cartographic axis.
6. Compare representation refinement across math, code, research, tool-use and LHIT episodes; require recurrence before calling it an invariant.
7. Keep literal MCTS/PRM/entropy-spike interpretations excluded unless independent evidence identifies the hidden mechanism.

## Anthropic comparative donor follow-up — 2026-09-02
1. Treat Anthropic's public alignment-training findings as an external methodological donor, not evidence that Anthropic has CFE proper.
2. Add `CONTEXTUAL_AFFORDANCE_FIELD` as a candidate CFE test surface: hold the nominal task fixed while varying learner-visible tools/system/environment context, then measure downstream phenotype under matched controls.
3. Add `DEVELOPMENTAL_HYSTERESIS` as a candidate research question: after an overt behavior is trained away, test whether prior developmental history leaves altered future reachability compared with a learner that never experienced that path.
4. Distinguish `SURFACE_SIMILARITY`, `CONSEQUENCE_SIMILARITY`, and `PRINCIPLE/CONSTRAINT_SIMILARITY` in Standard Uplift source/episode selection.
5. Decompose "diversity" into support coverage, discriminators, affordances, consequence structures, histories/revisits, and representation pressure; do not use diversity as a scalar explanation.
6. Before promoting any new cartographic axis, reconcile these donor hypotheses against existing CFE axes/threats and design matched controls.

## AI Reasoning Archaeology / reason-maintenance next pressure — 2026-09-02
1. **Hostile-review the highest-leverage historical specimens at event level**, starting with Version Spaces (1977), Stallman/Sussman dependency-directed backtracking (1977), Doyle TMS (1979), Reid MHT (1979), de Kleer ATMS (1986), GDE (1987), Russell/Wefald metareasoning (1991), Dynamic Backtracking (1993), GRASP (1996), and representative modern revision/currentness/trajectory papers. Done when source-exact events, failure boundaries, and counter-interpretations are recorded in LBE rather than source-level coding only.
2. **Build explicit historical trace specimens**, not only paper-level nodes: proof/search steps, assumption environments, conflict/nogood propagation, measurement selection, branch pruning/merging, and reasoning-control decisions. Preserve bounded excerpts and exact locators; raw copyrighted source remains local.
3. **Run matched modern discriminator E1–E7** from the reason-maintenance synthesis: self-consistency vs maintained-support field; global regenerate vs dependency-local repair; no conflict memory vs generalized conflict; supporting/random query vs identifying discriminator; fixed vs representation-level branch; fixed budget vs value-of-computation gating; static update vs propagation-aware currentness.
4. **Keep the multi-hypothesis target composition-first.** Test whether shared hard state + support lineage + conflict memory + discriminator selection can be composed with existing LBE/state instruments before inventing a new primitive or architecture.
5. **Measure branch compression by consequence**, not prose similarity: maintain lineage for currently consequence-equivalent alternatives so later evidence can split them. Treat `CURRENTLY CONSEQUENCE-EQUIVALENT != ONTOLOGICALLY IDENTICAL` as an active research guard.
6. **Extend the historical map backward/sideways** into scientific-discovery systems, theorem proving, abductive reasoning, model checking, probabilistic programming, causal inference, active experimental design, and other independently developed reason-maintenance traditions when they add discriminating structure rather than bibliography volume.
7. **Extend the modern quarry** with lawful/open reasoning traces and trace-faithfulness evidence. Annotate ordered state/representation/control/authority transitions rather than stylistic self-talk.
8. **Standard Uplift integration:** convert only recurring/operationally useful invariants into hidden curator-side episode structures; do not teach ATMS/TMS/MHT/CDCL vocabulary to the learner by default. Keep standard-data engineering separate from CFE experimental claims.
9. **CFE experiment promotion gate:** no new CFE cartographic axis or law from historical recurrence alone. Require matched intervention, operationalization, recurrence, hostile counterexamples, and failure boundaries.
10. **Historical causality guard:** continue separating first public observation, documented lineage, independent functional recurrence, and candidate causal enabler. No chronology-to-causation shortcut.

## Trace temporal cartography / forest application next steps — 2026-09-02
1. Expand the 15-trace deck to **30–50 source-located traces** with balanced historical coverage and domain diversity; prioritize worked executions over descriptive papers.
2. Hostile-review every trace at event level: exact source locator, observed event order, inferred silent structure, alternative interpretations, and failure boundary. Do not promote trace-surface inference into hidden mechanism.
3. Add trace specimens from under-covered lineages: scientific discovery/Meta-DENDRAL, MYCIN consultation/explanation, blackboard control, MHT worked association trees, belief revision/AGM examples, least-commitment planning, theorem proving/proof assistants, probabilistic programming/causal inference, model checking, and modern code/tool traces.
4. Build a **cross-era recurrence query layer in LBE** so questions like “show every independent embodiment of dependency-local rollback before LLMs” or “where does later evidence requalify earlier state?” are answerable without chronology/lineage confusion.
5. Run forest-level matched modern tests: support-aware multi-hypothesis vs sample-and-vote; dependency-local repair vs global regenerate; discriminator seeking vs relevant/supporting query; conflict-memory transfer vs no-conflict-memory; representation-level branch vs fixed representation; currentness propagation vs semantic retrieval; value-of-computation gating vs fixed reasoning budget.
6. Apply recurring invariants across **code/debugging, research, planning/agents, tool use, memory/currentness, science/diagnosis, math/verification** using the cross-domain ledger. Require consequence-structure match before transfer.
7. Wire the Standard Uplift selector/renderer to report coverage of hidden curator dimensions from `STANDARD_UPLIFT_REASON_MAINTENANCE_CROSS_DOMAIN_INTEGRATION_V1_2026-09-02.json`; no donor-label quota and no learner-facing historical jargon by default.
8. Build cross-domain isomorph/anti-isomorph episode sets: same stripped invariant under different domains, plus superficially similar cases where the correct state transition differs.
9. Preserve LHIT as a **consequential-history invariant family**, not a conversation format: include code, research, planning, debugging, memory and tool episodes where old state causally matters later.
10. Test `STATE-CHANGE DENSITY` and `USEFUL-TRANSITION DENSITY` against raw CoT length as data-quality predictors; do not assume longer trace == richer reasoning.
11. Maintain the forest guard: no scalar “AI reasoning progress score.” Track representational flexibility, support visibility, branching, repair locality, authority separation, currentness, learning-from-deliberation and effort allocation separately.
12. Before dataset training, use the trace/cartography findings to hostile-audit A0 candidate episode composition and ensure the modern/CFE-informed standard pack captures cross-domain invariants rather than overfitting math/reasoning prose.

## Standard Uplift LHIT cross-domain completion pressure — 2026-09-02
1. Treat `STANDARD_UPLIFT_LHIT_CROSS_DOMAIN_COVERAGE_GATE_V1_2026-09-02.json` as blocking for final Standard corpus promotion.
2. Source or lawfully generate **MEMORY_CURRENTNESS** episodes with indirect/non-negating stale-state invalidation, selective preservation of unrelated memory, and currentness propagation.
3. Source or lawfully generate **SCIENCE_DIAGNOSIS** episodes with live competing explanations, model/world residuals, discriminating measurements, revision under evidence, and representation/model refinement where local hypotheses fail.
4. Do not satisfy the gate by adding source labels alone. Coverage is counted only after license, contamination, dedup, quality, and invariant review.
5. Wire v2 `lhit_cross_domain` candidate dimensions into the later selector/admission stage as **coverage evidence**, not automatic admission or weighting.
6. Build cross-domain isomorph/anti-isomorph sets spanning code, research, planning/tool, math, memory/currentness, science/diagnosis, and long horizon so LHIT cannot be solved by conversation-format recognition.
7. Require explicit single-record LHIT-style examples in final coverage to prove `LHIT != MULTI_TURN FORMAT` operationally.
8. Audit heuristic precision before using counts for balancing; current v2 candidate counts are intentionally broad screening signals and may contain false positives.
9. Keep Capybara as donor/training surface only; no Capybara quota may stand in for measured LHIT invariant coverage.

## Standard Uplift pre-admission next pressure — 2026-09-02
1. **Contamination is now the sole training-admission blocker for the 1,802-atom pre-admission SFT candidate.** Apply `state/locks/STANDARD_UPLIFT_DATASET_V1_EVALUATION_EXCLUSION_LOCK_2026-09-02.json` exactly; do not weaken protected families to preserve corpus size.
2. Acquire/freeze compact local registries for the protected public eval families: AIME 2024/25/26 official, GPQA/GPQA-Diamond, MMLU-Pro, IFEval/IFBench, LiveCodeBench, SWE-bench/Verified, Terminal-Bench, BFCL, HLE, and BrowseComp/deep-research final comparison questions. Store registries locally/non-Git when redistribution is inappropriate; publish hashes/manifests only.
3. Run normalized exact hash + fuzzy/near-duplicate matching against the 1,802 candidate, preserving source-native contamination/decontamination metadata and manually reviewing ambiguous high-similarity cases.
4. Prioritize high-risk source lineages from `STANDARD_UPLIFT_SOURCE_CONTAMINATION_METADATA_AUDIT_20260902.json`: OpenR1 olympiad, Nemotron Math AoPS, OpenThoughts reasoning mix, Nemotron Code Codeforces, LiteResearcher BenchSeedQA, QUEST/NextSearch deep-research tasks. Do not infer whole-source clearance from partial native decontamination claims.
5. Current internal/private CFE eval screen already PASS: 49 files / 1,720 eval text items / 0 exact / 0 near >=0.90. **Rerun after final fleet phenotype/eval packet freeze.**
6. Keep the 80 Open-SWE traces physically segregated until SWE benchmark-form contamination is explicitly cleared; do not re-add them merely to increase code-agent volume.
7. Keep 40 repeated-prompt alternate trajectories physically separate. They are distinct trajectories, not exact duplicates; no objective ranking exists yet. Reintroduce only if a later diversity/trajectory-selection experiment justifies their weighting.
8. After contamination filter freezes the row set, run hostile invariant-quality sampling by domain/invariant, especially precision of LHIT cross-domain tags and project-generated memory/science surfaces. `HEURISTIC TAG != VERIFIED INVARIANT` remains binding.
9. Run tokenizer/target-context profiling only on the final post-contamination row set; reject/descope destructive truncation rather than silently cropping consequential history.
10. Preference data remains separate from SFT through all gates. Do not merge `Capybara-Preferences-Filtered` into SFT merely because the SFT candidate is ready.
11. No training run until contamination + final quality + tokenization gates all PASS and an explicit training authorization artifact is created.

## New-thread execution frontier — 2026-09-02 20:01 EDT
1. Rehydrate from `state/NEW_THREAD_REHYDRATION_2026-09-02.md` before widening work.
2. Verify manual contamination adjudication artifact SHA `7426a49b980e156819b0a0e6524bd35197492e8a95362354e86fa89e7af93a3a`.
3. Build a **successor** Standard pre-admission candidate; do not overwrite the historical 1,802-atom candidate.
4. Quarantine exactly the 11 genuine V3 protected-eval/template-leak atom IDs; verify successor count 1,791 before refill and preserve partition lineage.
5. Refill with >=9 independently clean, quality-qualified, non-duplicate atoms selected by capability/invariant deficit, not arbitrary quota pressure. Do not restore RAW, Open-SWE, contaminated rows, or segregated alternates merely to hit 1,800.
6. Rerun full V3 public protected-eval exact+fuzzy scan; manually adjudicate any new hits.
7. Rerun current internal/private eval overlap; rerun again after final fleet phenotype/eval packet freeze.
8. Run hostile invariant-quality review on final row set, then tokenizer/render/truncation profile; preserve consequential episodes whole.
9. Freeze exact A0 row IDs, ordering/rendering, hashes, and pre-training phenotype probes.
10. Create explicit training-authorization artifact only after all gates pass; then baseline/train/post-train.
11. In parallel, continue first-class reasoning archaeology/multi-hypothesis program. Do not allow Standard dataset completion pressure to demote or forget CFE science, historical temporal/causal trace cartography, representation adequacy, or Commander’s Intent.


## Standard three-lineage / purity frontier — 2026-09-02 21:25 Eastern Daylight Time
1. Treat row/token counts as descriptive/resource variables only; never add weak rows or delete high-value episodes to hit a number.
2. Hostile-review current Standard episodes against `STANDARD_UPLIFT_THREE_LINEAGE_MECHANISM_CROSSWALK_V1_20260902.json`; verify actual learner-visible state transitions, not curator-tag counts.
3. Build anti-isomorph cases for live alternatives, dependency-local repair, discriminator selection, currentness, representation refinement, UNKNOWN preservation, and failure-boundary reuse.
4. Address the adaptive-effort/value-of-computation hole only with clean consequence-based tasks where more reasoning/action has a cost and stopping quality matters; long CoT is not coverage.
5. Re-run training-body purity after every selector/generator mutation. All project/dataset governance stays in sidecars.
6. Re-evaluate long-context rows under value/coverage rather than a fixed A0 quota; preserve complete causal history where retained.
7. Final freeze still requires contamination/license/dedup/quality/render integrity + final frozen private-eval rerun + explicit training authorization.


## ISD developmental staging frontier — 2026-09-02 22:21 Eastern Daylight Time
1. Episode-review source rows into dependency depth using learner-visible consequence, not domain prestige, difficulty or heuristic tags.
2. Resolve high-value source families first and maintain `UNRESOLVED_TIER` for ambiguous rows.
3. Build prerequisite edges among verified mechanism families; each edge requires task-consequence/identifiability justification.
4. Compile spiral revisit plan so T0/T1 primitives reappear inside T2/T3/T4 contexts without duplicate padding.
5. Use Isomorphic Predator to supply positive/anti-isomorph embodiments at each stage, with donor provenance sidecar-only.
6. Fill T4 only when genuine frontier-synthesis episodes are verified; do not label long research traces T4 merely because they are long.
7. After stage map is adequate, compile an exact developmental ordering sidecar; do not mutate learner-visible content to encode stage.
8. Before training freeze: whole-corpus purity/contamination/dedup/license/render + frozen private-eval rerun + explicit authorization.
9. In parallel, preregister a CFE dependency-order experiment to test staged vs dependency-violating fields under matched information/dose.

## Reasoning archaeology deep-research continuation — 2026-09-02 22:35 ET
1. Use `research/CFE_REASONING_ARCHAEOLOGY_DEEP_RESEARCH_HANDOFF_2026-09-02.md` as the research ingress surface; reread the active Commander’s Intent file before any doctrine-changing proposal.
2. Extend the archaeology by functional seam, not by chronology alone. Highest-value hunts: representation-level branching/refinement; support-lineage extraction in neural reasoners; consequence-equivalence compression; conflict memory; currentness propagation; active discriminator selection; adaptive/value-of-computation control; learning from deliberation without trace imitation; orthogonal authority channels.
3. For every new system/paper/trace annotate state, hypothesis/possibility, support/dependency, representation, control, authority, time/currentness, compression, failure class, and learning-from-deliberation. Use `EXPLICIT / IMPLICIT / NOT_VISIBLE_IN_SPECIMEN / UNKNOWN` rather than inferred absence.
4. Keep chronology, documented lineage, functional recurrence, and candidate causal-enabling relations as separate edge classes. `FUNCTIONAL RECURRENCE != SHARED IMPLEMENTATION`; `CHRONOLOGY != CAUSATION`.
5. Convert recurring high-value structures into matched discriminators: support-aware field vs sample/vote; dependency-local repair vs regeneration; conflict memory vs no carry; discriminating vs merely supporting evidence; fixed vs refinable representation; fixed vs value-guided reasoning budget; static vs propagation-aware currentness; identical experience multiset under altered developmental geometry.
6. Preserve security/provenance boundary: do not acquire/decode/train on proprietary hidden-CoT recovered via exploits. Open visible reasoning traces only under ordinary rights/provenance gates.
7. Feed verified/hostile-surviving invariants into LBE and cross-domain Standard/CFE research only through re-derived consequence structure; never copy donor ontology or learner-facing jargon by default.


## Reasoning archaeology deep-research Wave 1 frontier — 2026-09-02 22:50 Eastern Daylight Time
1. Draft/preregister dependency-order x representation-development experiment with matched information/dose and checkpoint instrumentation.
2. Build synthetic known-support-topology benchmark to test whether attribution/circuit methods recover true dependency cones and predict local rollback.
3. Design learning-from-deliberation supervision ablation: answer/outcome only vs concise structural state-transition supervision vs raw trace; evaluate reason maintenance, currentness, rollback and discriminator transfer.
4. Next research wave: reusable conflict memory, indirect currentness propagation, orthogonal authority channels.
5. Keep external donor results in research plane until an explicit write/promotion gate is earned.


## ISD next compiler frontier — 2026-09-02 23:06 Eastern Daylight Time
1. Resolve the remaining 1158 rows by high-value family: instruction-following/chat, Capybara dialogue, competitive programming, math/OpenThoughts/OpenR1. Do not equate subject difficulty with dependency depth.
2. For single-turn math/code, stage only when prerequisite/composition/representation structure is explicit enough to justify an edge; otherwise leave unresolved or treat as stage-neutral competence support.
3. Hostile-review source-derived T2/T3 samples for actual state dependency vs repeated independent actions; demote false developmental depth when necessary.
4. Map resolved rows to prerequisite-DAG mechanism nodes where learner-visible consequence supports it; stage alone is insufficient.
5. Replace minimal transition-only bridge revisits with verified spiral isomorphs/anti-isomorphs as those mappings become available; avoid duplicate padding.
6. Fill T4 only from genuine novel decomposition/self-directed discrimination/representation-creation episodes.
7. Final order freeze only after stage coverage is adequate, whole-corpus purity/contamination/render gates pass, frozen private-eval rerun passes, and explicit training authorization is issued.


## ISD canonical-blueprint execution frontier — 2026-09-02 23:49 Eastern Daylight Time
1. Rebuild/finalize the trainable ISD order from the canonical blueprint, not from older isolated staging/support notes.
2. Finish stage/spiral bridge quality review; replace generic repeats with consequence-bearing isomorph/anti-isomorph requalifications where possible.
3. Freeze arm-symmetric trainable payload under the highest runtime-qualified context ceiling; retain excluded complete episodes in a shared long-context reserve, never destructively crop.
4. Seal baseline phenotype/eval packet before training.
5. Freeze matched-arm preregistration: DEVELOPMENTAL_SPIRAL vs ORDER_DESTROYED_CONTROL, same exact trainable atoms, supervised token multiset, base model, trainable initialization, LoRA/optimizer, dose and evaluation.
6. Run preflight/resource probes under frozen profile; any context/profile change before launch updates both arms and prereg identity.
7. Launch paired training only after explicit authorization artifacts pass; report submitted/started/completed/registered separately.
8. Evaluate ordinary competence plus composition, transfer, currentness, local repair, rollback selectivity, hypothesis maintenance, discriminator selection, adaptive effort, representation/framing recovery and correction cost.
9. Preserve intermediate checkpoints if feasible for representation-development analysis; interpretability remains triangulation, not learner ontology.


## 2026-09-03 12:16 ET — Active revisit-timing replication queue
1. Let `job-d1276bf4bfb6` complete the frozen six-seed LATE-vs-FRONTLOAD campaign without interactive interference.
2. If visibility/control plane fails, do not infer process failure. Reconnect and inspect `REPLICATION_PROGRESS.json`, per-arm `RUN_MANIFEST.json`, and `recovery_current`. Resume only through the qualified resilient trainer; no dose replay.
3. At completion, verify 12/12 arm runs and all paired initial + first19 trainable/adapter hash equalities before interpreting outcomes.
4. Q1 disposition: count seeds where LATE exposure136 already has ADAPTIVE_EFFORT accuracy=1.0 and pair-complete=1.0 before revisit dose.
5. Q2 disposition: compare DISCRIMINATOR_SELECTION pair-complete at exposure140 LATE vs FRONTLOAD within seed; report wins/ties/losses and exact two-sided sign test on non-ties.
6. Secondary: within LATE, compare Discriminator Selection 136->140 and Adaptive Effort persistence 136->140; preserve sign flips and family-local effects.
7. Only after replication result is sealed decide whether to promote a fixed-regime prerequisite/revisit mechanism claim, design a minimal-foundation ablation, or move the Magnum campaign onward into T2/T3.


## 2026-09-03 14:34 ET — Post-replication execution frontier
1. **Do not launch another training campaign implicitly from this checkpoint.** The completed revisit-timing result first needs to become the new continuity baseline.
2. Mine the completed 12-arm LATE/FRONTLOAD artifacts before spending more GPU: per-item margins, row-loss trajectory, checkpoint state, and seed-local divergence associated with Adaptive-Effort success or late rescue. Preserve `OBSERVED PREDICTOR != CAUSAL MECHANISM`.
3. Treat `FOUNDATIONS19 general sufficiency` as demoted: preregistered result = 1/6 successes (`NOT_REPLICATED`). Do not use the exploratory single-seed 136 result as a planning invariant.
4. Treat `late revisits cause Discriminator-Selection jump` as demoted: 0/6 fresh LATE trajectories showed a positive 136->140 pair-complete change; LATE vs FRONTLOAD discriminator timing was six ties.
5. Preserve the independently replicated broader prerequisite-first vs scramble order effect (5 wins / 1 tie / 0 losses) while narrowing its mechanism interpretation. `FINER MECHANISM FAILURE != BROADER ORDER EFFECT FAILURE`.
6. If existing artifacts cannot resolve schedule geometry, freeze and preregister an **original-SPACED add-on** on seeds `2026090501..2026090506`. Use the exact original spaced revisit positions, frozen 140-exposure multiset, same model/LoRA/optimizer/eval, and exact paired initialization requirements. Reuse completed LATE/FRONTLOAD arms rather than rerunning them.
7. Primary discriminator for that add-on: within-seed SPACED vs LATE vs FRONTLOAD Adaptive-Effort pair-complete phenotype and margins. Secondary: whether distributed revisits reduce seed sensitivity. Do not use between-campaign seed frequencies as a substitute for paired comparison.
8. In parallel, define a **learner-state/topology probe** research seam: ask whether early checkpoint margins, gradient/adapter geometry, or other low-cost observables predict which adaptation trajectory will cross the later phenotype boundary. Guard: `ADAPTATION MICROSTATE != PRETRAINED-MODEL TOPOLOGY`.
9. Only after schedule geometry is pressure-tested decide whether the Magnum program should: (a) ablate minimal foundations, (b) test distributed revisit/requalification geometry, or (c) advance into T2/T3.
10. Keep DD2 Structured Revisit separate and unresolved; do not import the ISD Block-A disposition into DD2.
11. Publication is a separate step. Current local result is not published; publication checkout is clean at `3b41dd54dc9f229f17acaa8c890a03d4ddd5dde3`.


## 2026-09-03 — LHRSG-constrained frontier
1. **P0 — Complete 1,840/1,840 LHRSG on exact canonical Magnum training bytes** (`ISD_CANONICAL.private.jsonl`, SHA `b85229cd...`). Consecutive chunking is permitted; sampling is forbidden. Until complete: `NOT_TRAINING_AUTHORIZED`.
2. Any learner-visible training defect found during that pass SHALL create an append-only successor with explicit quarantine/demotion; do not silently rewrite the canonical file.
3. Preserve V2R7 eval exact bytes SHA `cf2568d...`. Its 96/96 LHRSG receipt is PASS. Any semantic edit invalidates the receipt and requires full 96/96 replay.
4. Optional low-cost archaeology after the training-body gate: rescore saved historical adapters on exact V2R7 using permutation-neutral semantic choice scoring. Label all such use POST_OUTCOME / DIAGNOSTIC.
5. Before new causal training, preregister/freeze exact training body, exact eval, permutation-neutral scorer, paired seeds, learner/base revision, exposure multiset, schedule arms, optimizer, stopping rule, and claim ceiling.
6. Fresh prerequisite-first vs phase-scramble paired replication is required before restoring an Adaptive-Effort developmental-order scientific claim.
7. Do not prioritize SPACED/LATE/FRONTLOAD schedule geometry until the broader order signal survives the repaired prospective ruler.
8. Keep DD2 Structured Revisit separate and unresolved.
9. Extend LHRSG to any other readable artifact when it enters active semantic use. Reuse exact-hash receipts for unchanged bytes; do not reread ceremonially.


## 2026-09-03 17:14 ET — Thread-reincarnation publication queue
1. Build the full **public-safe** GitHub delta needed for a clean fresh-thread restart: active current/next/doctrine/revisit/trace/shadow/stream, R4.1 authority/adoption bindings, LHRSG law/receipts, current Commander’s Intent binding and key immutable intent addenda, latest measurement-repair science, current engineering scars, and new-thread handoff/index/bootstrap surfaces.
2. Reuse existing LHRSG receipts only where exact bytes are unchanged. Any new or mutated readable artifact in the publication set must receive full final-byte LHRSG before promotion.
3. Preserve the normal-clone boundary: do not stage the 1,840-row private training body, V2R7 private eval JSONL, private result JSONL, gated/protected benchmark text, credentials, model weights, adapters, or heavy runtime artifacts.
4. Main publication commit -> push -> remote HEAD/content readback. Only then may publication be called successful.
5. Write a publication readback receipt with exact commit, remote-head equality, staged-file manifest, hashes, exclusions, and warnings; propagate any load-bearing result into continuity and push a final continuity-only commit if needed.
6. Fresh thread resumes at **1,840/1,840 training-body LHRSG**. Reviewer-method seam remains unresolved; do not weaken the semantic gate to fit a fast but underqualified reviewer.
7. No new training until training-body LHRSG passes (or append-only successor passes) and exact experiment/eval/scorer/seeds/base/schedule/optimizer/stopping rule are prospectively frozen.


## 2026-09-03 17:08 ET — Thread-exit publication frontier
1. **P0 — finish the public-safe GitHub reincarnation checkpoint before leaving this thread.** Sync active continuity/state, R4.1 authority, LHRSG law/receipts, public-safe measurement-repair dispositions, transcript, and the new 2026-09-03 human+machine rehydration packets into `publication/github/Cognitive-Field-Engineering`.
2. Apply LHRSG to the exact readable publication bundle after all mutation. Automated secret/size/hash/Git checks support but do not replace the full linear semantic read.
3. Keep private/non-Git: exact 1,840-row learner-visible training payload; private V2R7 prompt text; model weights; checkpoints/adapters; protected/gated benchmark text; credentials; transient execution logs.
4. Commit only intended public-safe files; push authenticated `main`; read back remote `main` before claiming publication.
5. Create a publication receipt recording the verified content commit and remote readback. A later receipt commit may carry that readback; do not confuse its existence with the content commit it documents.
6. **Fresh-thread P0 after publication:** complete exact 1,840/1,840 learner-visible training-body LHRSG on SHA `b85229cd04d68e9990deda091131fdf4f81981497a1f322127e8253ac0d89fef`. No new training before full semantic authorization.
7. If any training row fails LHRSG, preserve the old body and build an append-only corrected successor; replay full LHRSG on exact successor bytes.
8. Preserve V2R7 exact eval bytes SHA `cf2568d771bc2d2484bd1f300308572cee8c4beefc53dea2cf10021c7324e2d8` and 96/96 LHRSG receipt. Any mutation invalidates that gate.
9. Only after training-body closure: optional historical V2R7 permutation-neutral rescore as POST_OUTCOME archaeology, then fresh preregistered paired prerequisite-first vs phase-scramble confirmation.
10. Do not reopen SPACED/LATE/FRONTLOAD schedule geometry until broad order effects survive a prospectively frozen repaired measurement regime.


## 2026-09-03 19:57 ET — Post-publication resume queue
1. Fresh thread: rehydrate from published 2026-09-03 continuity under RECOVERY/AUDIT and verify current remote/local Git head.
2. Resume the full learner-visible Magnum LHRSG: 1,840/1,840 records, deterministic order, no sampling.
3. If any row fails, preserve historical bytes and build an append-only corrected successor; restart complete LHRSG on the successor.
4. No new training until the training-body gate closes and the next experiment/eval/scorer/seeds/base/schedule/optimizer/stopping rule are prospectively frozen.
5. Historical V2R7 rescoring is optional post-outcome archaeology only; do not restore the old full-AE phenotype claim.

## R4.2 adoption finalization gate — 2026-09-03T23:35:16-04:00
1. Freeze repaired adoption candidate and complete final-byte LHRSG on all new/semantically mutated readable load-bearing artifacts.
2. Freeze explicit public allowlist; exclude private/heavy/scanner/receiver-log/nested-ancestry-archive payloads.
3. Build/push/independently verify Commit A from verified parent `6b2dc681ded9151451107b9ec7396099757765dd`.
4. Create/gate/publish Commit B post-publication receipt + only continuity surfaces requiring the completed-publication fact; verify B parent=A and local==remote.
5. Only after `R4.2_ADOPTION_COMPLETE__REMOTE_VERIFIED` resume the 1,840/1,840 training-body LHRSG frontier. No new training.
