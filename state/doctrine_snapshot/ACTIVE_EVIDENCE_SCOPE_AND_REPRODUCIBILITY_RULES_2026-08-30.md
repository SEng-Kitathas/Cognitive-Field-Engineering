# ACTIVE EVIDENCE-SCOPE AND REPRODUCIBILITY RULES — 2026-08-30

Status: **ACTIVE ENGINEERING / SCIENTIFIC PROCESS DOCTRINE**

These rules are the project-relevant lessons carried forward from cross-project engineering evidence. They are abstracted away from the source project's local details.

## 1. Verifier scope must match earned evidence

> **A verifier may enforce only distinctions the evidence has actually earned.**

A passing implementation should not be rejected merely because it differs from one historical representation when multiple representations are behaviorally valid at the tested scope.

Therefore:

- `TESTED SCOPE != GENERAL LAW`
- `EXACT HISTORICAL REPRESENTATION != NECESSARILY REQUIRED MECHANISM`
- `EVALUATOR CONTRACT != UNDERLYING CAPABILITY`

When evidence broadens the accepted tested set, update the living verifier explicitly and preserve the old verifier/result as historical truth.

## 2. Corrected interpretation does not rewrite history

> **CORRECTED INTERPRETATION != REWRITTEN HISTORY**

If an old evaluator produced FAIL under its old contract, that historical result remains true.

Later evidence may show that the old contract was overbound, incomplete, or aimed at the wrong distinction.

The correct lineage is:

`old contract -> historical result`

followed by:

`new evidence -> revised interpretation / revised living verifier`

Do not delete or recolor old red results merely because the current understanding changed.

## 3. External reports have an evidence ceiling

> **EXTERNAL REPORT != HASH-VERIFIED EXTERNAL EVIDENCE**

A credible external reproduction report may raise confidence and may justify further inspection.

It does not become artifact-level evidence until the relevant foreign inputs/results are admitted by identity/hash and bound to the reported run.

Likewise:

- `ONE EXTERNAL RUN != MECHANISM DISCRIMINATION`
- `REPORTED REPRODUCTION != INDEPENDENT HASH-VERIFIED REPRODUCTION`

For CFE, foreign reproduction should ideally bind:

- exact source/input package;
- model/runtime identity;
- run manifest;
- raw result/evaluation artifacts;
- relevant logs/traces;
- hashes and comparison receipt.

## 4. Execution path and artifact identity are different objects

> **EXECUTION PATH != ARTIFACT IDENTITY**

The path used as `argv[0]`, launcher path, wrapper path, symlink, or relocated executable path is not necessarily the canonical identity path used for provenance.

Resolve identity for hashing/manifest purposes without silently replacing the execution path semantics.

This distinction applies to tools, model snapshots, launchers, interpreters, and transplanted runtimes.

## 5. A portable artifact is not automatically a portable experiment

> **ARTIFACT PACKAGE != EXECUTION ENVIRONMENT**

Moving or restoring code/model bytes does not automatically restore the environment in which they functioned.

A reproducible CFE package must account for relevant environment dependencies such as:

- tokenizer assets and special-token IDs;
- model/cache/snapshot paths;
- runtime package versions;
- CUDA/driver assumptions;
- attention backend;
- environment variables;
- module/search/data paths;
- helper executable identities;
- filesystem/layout assumptions;
- deterministic-runtime settings.

Therefore:

`SAME SOURCE + SAME WEIGHTS != SAME EXECUTABLE EXPERIMENT`

unless the runtime/environment contract is also recovered or requalified.

## 6. Research-lineage implication

These rules reinforce the active publication policy:

A future researcher must be able to walk from a current claim backward through:

`claim -> interpretation -> evaluator contract -> raw results -> run manifest -> code/runtime identity -> locked inputs -> preregistration -> historical failures/superseded attempts`

without relying on chat memory or rewritten history.
