# CFE Autonomous Helix Campaign 1 — v1.0 descendant and pre-live repair chain

Cognition: GPT-5.6 Sol, role-separated under R3.1/PCMMAD. Research only; no promotion authority. P(N+1) question is generated from P(N). P20 is a hard stop and emits Campaign 2's seed.

## P01
**Question:** What is the next step in the v1.0 descendant creation process after protecting and fingerprinting the sealed v0.9 parent?
**Answer:** Create `CFE_RND_V1_0_PREEXECUTION` as a descendant only; sealed v0.9 stays immutable.
**Evidence:** `state/current.md`; `state/next_steps.md`.
**OARR:** If creation writes into the sealed parent, ancestry is invalid even if tests pass.
**Loop+:** Also compare the parent hash-tree before and after the fork.
**Helix:** Survivor = immutable v0.9 ancestry. Scar = prior Windows portability failure. Demotion = none.
**Reservoir:** Parent-integrity evidence.
**Disposition:** BUILD-PLAN; confidence 0.98.
**Next:** Which invariants must the v1.0 descendant preserve to prove it is a child rather than a mutation of sealed v0.9?

## P02
**Question:** Which invariants must the v1.0 descendant preserve to prove it is a child rather than a mutation of sealed v0.9?
**Answer:** Preserve parent bytes/hashes, input-lock identity, ancestry pointer, and zero parent writes; changes occur only in the child.
**Evidence:** Sealed parent plus current state.
**OARR:** A byte-identical child without an ancestry receipt can still lose lineage.
**Loop+:** Check metadata/provenance identity separately from payload identity.
**Helix:** Survivor = child-only mutation boundary. Scar = lineage can be lost without payload corruption. Demotion = none.
**Reservoir:** Provenance metadata.
**Disposition:** BUILD-PLAN; confidence 0.96.
**Next:** What evidence should prove that creating the v1.0 child did not mutate the sealed v0.9 parent?

## P03
**Question:** What evidence should prove that creating the v1.0 child did not mutate the sealed v0.9 parent?
**Answer:** Capture parent manifest/hash-tree before and after copy, require equality, and emit a child ancestry receipt naming the parent.
**Evidence:** Append-only doctrine; sealed-parent path.
**OARR:** Filesystem copy tooling could alter timestamps while payload hashes stay fixed; payload identity must be the authority.
**Loop+:** Record both payload hashes and non-authoritative filesystem metadata deltas.
**Helix:** Survivor = hash-based parent immutability. Scar = filesystem metadata is not payload authority. Demotion = timestamp equality as required invariant.
**Reservoir:** Integrity plus filesystem metadata.
**Disposition:** VERIFY; confidence 0.95.
**Next:** Which v0.9 files are the first lawful targets for the Windows portability repair inside the child?

## P04
**Question:** Which v0.9 files are the first lawful targets for the Windows portability repair inside the child?
**Answer:** The four historical generators: depth, provenance-depth, provenance-latent, and anti-isomorph v0.5 generators.
**Evidence:** Discriminator A execution record.
**OARR:** Patching tests only could hide a generator portability defect instead of repairing it.
**Loop+:** Inspect all write sites in those generators for host-default newline behavior.
**Helix:** Survivor = four-generator repair surface. Scar = test-only fixes can mask root cause. Demotion = parent mutation.
**Reservoir:** Source-code write sites.
**Disposition:** BUILD-PLAN; confidence 0.99.
**Next:** What exact serialization contract should those four generators implement on Windows?

## P05
**Question:** What exact serialization contract should those four generators implement on Windows?
**Answer:** Emit UTF-8 with explicit LF canonical newlines while preserving logical JSON/JSONL content and ordering.
**Evidence:** Discriminator A LF-normalized equality plus parsed equality.
**OARR:** Changing JSON formatting/order together with newline repair would confound the fix.
**Loop+:** Compare parsed objects and non-hash manifest metadata before/after.
**Helix:** Survivor = UTF-8/LF canonical serialization. Scar = manifest hashes lawfully change when payload bytes change. Demotion = host-default newline behavior.
**Reservoir:** Semantic-vs-byte identity.
**Disposition:** BUILD-PLAN; confidence 0.99.
**Next:** How do we prevent the portability patch from silently changing scientific content while fixing bytes?

## P06
**Question:** How do we prevent the portability patch from silently changing scientific content while fixing bytes?
**Answer:** Constrain the patch to encoding/newline boundaries; preserve records, seeds, order, schemas, and non-hash metadata.
**Evidence:** Discriminator A comparisons.
**OARR:** Canonicalization that also sorts keys or rewrites whitespace may create unnecessary new bytes.
**Loop+:** Use parsed equality plus field-level metadata comparison as a guard.
**Helix:** Survivor = minimal portability delta. Scar = over-repair creates provenance burden. Demotion = broad serialization rewrite.
**Reservoir:** Field-level semantic diff.
**Disposition:** VERIFY; confidence 0.98.
**Next:** What interpreter-binding repair is required for deterministic regeneration on Windows?

## P07
**Question:** What interpreter-binding repair is required for deterministic regeneration on Windows?
**Answer:** Invoke regeneration through `sys.executable` or the already-qualified CFE interpreter, not ambient `python`.
**Evidence:** `state/next_steps.md`.
**OARR:** A correct generator can still fail determinism if subprocesses resolve a different interpreter/environment.
**Loop+:** Bind cwd and environment receipt alongside interpreter path.
**Helix:** Survivor = qualified-interpreter binding. Scar = ambient PATH is not execution identity. Demotion = unqualified subprocess invocation.
**Reservoir:** Execution-environment evidence.
**Disposition:** BUILD-PLAN; confidence 0.98.
**Next:** What narrow regression gate should run immediately after the newline and interpreter-binding patches?

## P08
**Question:** What narrow regression gate should run immediately after the newline and interpreter-binding patches?
**Answer:** Run the four historical deterministic-regeneration tests and require all four to pass in the qualified Windows environment.
**Evidence:** Historical pytest plus Discriminator A.
**OARR:** A semantic-only comparison could miss renewed byte drift.
**Loop+:** Require raw-byte equality under canonical LF plus parsed equality and manifest self-consistency.
**Helix:** Survivor = four-test portability gate. Scar = parsed equality alone is insufficient. Demotion = semantic-only acceptance.
**Reservoir:** Test plus byte evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** What constitutes a sufficient pass for those four deterministic-regeneration tests?

## P09
**Question:** What constitutes a sufficient pass for those four deterministic-regeneration tests?
**Answer:** 4/4 tests pass; regenerated canonical bytes match repaired expectations; parsed data match; generated manifests self-hash consistently.
**Evidence:** Discriminator A design.
**OARR:** Forcing old manifest bytes to match would be wrong because hash fields track payload bytes.
**Loop+:** Check non-hash manifest metadata separately from hash-bearing fields.
**Helix:** Survivor = causal newline diagnosis. Scar = manifest byte equality is not the right invariant. Demotion = old-manifest-byte equality.
**Reservoir:** Manifest semantics.
**Disposition:** VERIFY; confidence 0.99.
**Next:** After the narrow four tests pass, what broader regression gate is required before any reseal?

## P10
**Question:** After the narrow four tests pass, what broader regression gate is required before any reseal?
**Answer:** Run the full Windows pytest suite and require the v1.0 descendant target of 55/55.
**Evidence:** `state/next_steps.md`.
**OARR:** Four repaired tests can pass while unrelated regressions were introduced.
**Loop+:** Compare the failure surface against the v0.9 51/4 baseline.
**Helix:** Survivor = full-suite regression gate. Scar = narrow success does not imply package health. Demotion = narrow-only acceptance.
**Reservoir:** Full regression evidence.
**Disposition:** VERIFY; confidence 0.99.
**Next:** If full pytest reaches 55/55, is the v1.0 descendant ready to reseal and move to model work?

## P11
**Question:** If full pytest reaches 55/55, is the v1.0 descendant ready to reseal and move to model work?
**Answer:** No. Portability/regression success is necessary but remaining preregistered pre-live defects still block model work.
**Evidence:** `state/next_steps.md`.
**OARR:** Treating 55/55 as scientific readiness would collapse software verification into experiment validity.
**Loop+:** Replay the preregistered P2-P7 repair list before reseal.
**Helix:** Survivor = software/science gate separation. Scar = test pass is not scientific readiness. Demotion = 55/55 as promotion.
**Reservoir:** Experiment-validity evidence.
**Disposition:** BUILD-PLAN; confidence 0.99.
**Next:** Which remaining pre-live defect should receive the highest causal-validity pressure first?

## P12
**Question:** Which remaining pre-live defect should receive the highest causal-validity pressure first?
**Answer:** Evaluator pseudoreplication is a high-risk seam because row-level replication can overstate independent evidence.
**Evidence:** Current preregistered repair list.
**OARR:** Learner-visible shortcut leakage could be equally damaging even with perfect aggregation.
**Loop+:** Treat pseudoreplication and shortcut uniqueness as coupled but separately tested seams.
**Helix:** Survivor = independent-unit analysis. Scar = multiple causal threats remain. Demotion = row-count as sample size.
**Reservoir:** Analysis-unit evidence.
**Disposition:** DISCUSSION; confidence 0.88.
**Next:** How should evaluator aggregation be repaired to avoid pseudoreplication?

## P13
**Question:** How should evaluator aggregation be repaired to avoid pseudoreplication?
**Answer:** Aggregate inferential evidence at an independent unit such as paired seed/run, with prompt rows nested rather than treated as independent replicates.
**Evidence:** Preregistered evaluator pseudoreplication repair.
**OARR:** Too few independent units can make precise interval claims unjustified even with clustering.
**Loop+:** Report descriptive row distributions separately from unit-level inference.
**Helix:** Survivor = independent experimental units. Scar = large row counts do not create independent N. Demotion = prompt-row independence.
**Reservoir:** Statistical-unit evidence.
**Disposition:** BUILD-PLAN; confidence 0.90.
**Next:** What learner-visible warrant/provenance uniqueness check is required next?

## P14
**Question:** What learner-visible warrant/provenance uniqueness check is required next?
**Answer:** Audit learner-visible fields so treatment identity, provenance labels, warrant text, or nuisance duplicates cannot serve as shortcuts.
**Evidence:** Preregistered nuisance-uniqueness repair.
**OARR:** A hidden shortcut may survive exact token-budget matching.
**Loop+:** Search feature uniqueness and arm-predictive metadata, not only token counts.
**Helix:** Survivor = content-parity pressure. Scar = token parity does not imply information parity. Demotion = token-count sufficiency.
**Reservoir:** Learner-visible feature audit.
**Disposition:** VERIFY; confidence 0.90.
**Next:** What determinism repair is required before trusting repeated CONTROL/TREATMENT execution?

## P15
**Question:** What determinism repair is required before trusting repeated CONTROL/TREATMENT execution?
**Answer:** Fail closed on determinism requirements and pin the attention/backend path used by the scientific screen.
**Evidence:** Preregistered fail-closed determinism plus pinned attention.
**OARR:** Nominal seed equality cannot rescue nondeterministic backend drift.
**Loop+:** Record backend, CUDA, kernel/attention selection, and repeated-step behavior.
**Helix:** Survivor = fail-closed determinism. Scar = seed config is not verified deterministic execution. Demotion = seed-only determinism.
**Reservoir:** Runtime-backend evidence.
**Disposition:** BUILD-PLAN; confidence 0.92.
**Next:** What host-qualification evidence should be repeated before scientific training?

## P16
**Question:** What host-qualification evidence should be repeated before scientific training?
**Answer:** Repeat the one-step CUDA host/profile qualification and preserve completion, memory, loss, and environment receipts before any arm run.
**Evidence:** Preregistered repeated one-step host qualification; v0.9 preflight.
**OARR:** A single successful fit can be a transient memory-state accident.
**Loop+:** Compare repeated peak-memory and completion behavior before locking the profile.
**Helix:** Survivor = pre-training fit gate. Scar = one fit is not stable host qualification. Demotion = single-shot host fit.
**Reservoir:** Host-repeat evidence.
**Disposition:** VERIFY; confidence 0.92.
**Next:** How should bootstrap dependencies be treated so environment setup cannot masquerade as reproducibility?

## P17
**Question:** How should bootstrap dependencies be treated so environment setup cannot masquerade as reproducibility?
**Answer:** Treat bootstrap requirements as installation guidance; reproducibility authority comes from captured runtime environment/package/CUDA/GPU identity.
**Evidence:** v0.8 hostile repair; host qualification.
**OARR:** Pinned requirements alone can still resolve differently across platforms or indexes.
**Loop+:** Bind runtime freeze and environment hash into training/evaluation manifests.
**Helix:** Survivor = runtime environment lock. Scar = bootstrap list is not runtime lock. Demotion = requirements-file authority.
**Reservoir:** Environment-manifest evidence.
**Disposition:** BUILD-PLAN; confidence 0.96.
**Next:** What must the executable 1,680-control audit establish before reseal?

## P18
**Question:** What must the executable 1,680-control audit establish before reseal?
**Answer:** It must run as an executable fail-closed audit over all 1,680 controls and surface any shortcut, mismatch, or violated invariant.
**Evidence:** `state/next_steps.md`.
**OARR:** A static checklist can pass while executable controls fail.
**Loop+:** Retain per-control outcome plus aggregate failure digest and exact code revision.
**Helix:** Survivor = executable control audit. Scar = documentation is not execution. Demotion = checklist-only control audit.
**Reservoir:** Control-execution evidence.
**Disposition:** VERIFY; confidence 0.90.
**Next:** How must seed-extension behavior be preregistered before outcomes are observed?

## P19
**Question:** How must seed-extension behavior be preregistered before outcomes are observed?
**Answer:** Define extension trigger, added seeds, stopping rule, analysis handling, and failure criteria before viewing extension outcomes.
**Evidence:** `state/next_steps.md`.
**OARR:** Post-hoc seed addition can convert noisy results into selective evidence.
**Loop+:** Bind the preregistration artifact hash into the resealed package before execution.
**Helix:** Survivor = outcome-independent extension rule. Scar = adaptive sampling can inflate confidence. Demotion = post-outcome seed selection.
**Reservoir:** Preregistration evidence.
**Disposition:** BUILD-PLAN; confidence 0.94.
**Next:** What complete gate sequence must a fresh v1.0 reseal survive before the model stage is even eligible?

## P20 — HARD STOP
**Question:** What complete gate sequence must a fresh v1.0 reseal survive before the model stage is even eligible?
**Answer:** Require parent-immutability proof, portability 4/4, full 55/55, nuisance audit, unit-level analysis repair, determinism/backend lock, repeated host fit, runtime lock, executable 1,680-control audit, seed-extension preregistration, regeneration/hostile review, then fresh hashes/reseal.
**Evidence:** Combined CFE frontier.
**OARR:** Passing software gates while any scientific gate remains open would create false readiness.
**Loop+:** Re-run hostile review against the integrated child rather than composing local passes by assumption.
**Helix:** Survivor = integrated pre-live gate stack. Scar = local passes do not automatically compose. Demotion = partial-gate readiness.
**Reservoir:** Integrated hostile review.
**Disposition:** HARD_STOP_P20; confidence 0.96. Promotion authority = NONE.
**Next / Campaign 2 seed:** What is the strongest remaining threat to causal identification in CFE v1.0 after portability and regression gates are repaired?
