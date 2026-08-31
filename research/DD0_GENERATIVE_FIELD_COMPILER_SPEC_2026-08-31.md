# DD-0 — Generative Developmental Field Compiler Qualification

Status: ENGINEERING QUALIFICATION SPEC — NOT LEARNER EVIDENCE

## Purpose
CFE cannot claim a field intervention merely because a curator-side sidecar or graph exists. DD-0 establishes a deterministic compiler/verifier boundary:

`CANONICAL DEVELOPMENTAL FIELD -> LEARNER FIELD PROJECTION -> EXPOSURE COMPILATION -> FIELD VERIFICATION`

The compiler is not a cognition model. It is an engineering instrument for making intended developmental geometry auditable at the learner-visible surface.

## Four layers
### 1. Canonical Developmental Field (CDF)
Contains curator-visible source objects:
- event IDs and learner-visible payloads;
- typed relations;
- relation direction when applicable;
- temporal/revisit constraints;
- local-neighborhood membership;
- long-range bridge membership;
- coverage requirements.

### 2. Learner Field Projection (LFP)
Selects which source events are exposed and which field dimensions determine arrangement. It SHALL NOT copy curator relation labels into learner-visible payload unless the experimental treatment explicitly requires that language.

### 3. Exposure Compiler (EC)
Produces deterministic learner-visible episodes/windows from the projection. A compiler mode may change ordering/window membership while preserving the exact event multiset.

### 4. Field Verifier (FV)
Checks what was actually compiled rather than trusting source intent.

## Qualification invariants
1. `CDF != LFP != EC OUTPUT != LEARNED GEOMETRY`.
2. Same-event-multiset arms must have identical event IDs and payload hashes with identical multiplicities.
3. Relation labels and sidecar-only metadata must not leak into learner text.
4. The intended geometric difference must be directly measured from compiled windows.
5. Deterministic compile: same source + same mode + same seed => byte-identical output.
6. Cross-platform deterministic serialization: UTF-8, LF, sorted JSON keys, no host-default newline dependence.
7. Coverage claims must be verified from compiled windows, not source-side membership alone.
8. Long-range links must be defined operationally as repeated exposure adjacency/co-window structure, not embedding distance.

## Initial compiler modes
### IDENTIFYING_LOCAL
Events connected by declared target relations are placed into co-visible windows while preserving all payloads and event multiplicities.

### RELATIONALLY_DISPERSED
The exact same event multiset is compiled so declared target-pair co-visibility is minimized subject to window-size and multiplicity constraints.

This is an engineering primitive, not yet the final DD-1 experiment.

## Qualification readouts
- event multiset identity;
- payload-byte multiset identity;
- learner-text leakage count;
- target-relation co-visibility count/rate;
- non-target co-visibility count/rate;
- window-size equality;
- deterministic replay SHA;
- coverage requirement satisfaction.

## Failure laws
- `SOURCE RELATION PRESENT != COMPILED RELATION VISIBLE`
- `SAME EVENT MULTISET != SAME FIELD GEOMETRY`
- `SIDEcar RELATION != LEARNER-VISIBLE RELATION`
- `COMPILER EXIT 0 != FIELD QUALIFIED`
- `BYTE-MATCHED EVENT MULTISET != TOKEN-MATCHED SEQUENCE` (token qualification remains a later gate)

## Promotion ceiling
DD-0 can only earn:
> The CFE toolchain can deterministically compile and verify controlled differences in learner-visible relational arrangement while preserving a matched source-event multiset.

It cannot earn any claim about learning or cognition.
