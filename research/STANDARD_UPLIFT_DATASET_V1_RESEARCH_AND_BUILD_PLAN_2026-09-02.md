# Standard Uplift Dataset v1 — Research and Build Plan

Date: 2026-09-02
Status: **ACTIVE STANDARD DATA PROGRAM / NOT CFE EXPERIMENTAL PACK**

## Objective
Build a compact, modern, high-information post-training corpus for selected local models, optimized for practical reasoning, research, mathematics, software/code, tool use, long-horizon interaction, instruction following, and evidence discipline.

The immediate target is ordinary model uplift. CFE contributes engineering lessons but does not define a treatment arm here.

## Design posture
Prefer quality, diversity, verifier support, provenance and functional coverage over raw row count.

`DATA VOLUME != DATA VALUE`
`DATASET REPUTATION != ROW QUALITY`
`VERIFIED SUCCESS > PRETTY TRACE`
`COMPLETE LEARNER-VISIBLE CONTEXT > PRESTIGIOUS BUT MISSING PROMPT`
`TOKEN-BUDGET COVERAGE > ROW-COUNT BALANCING`

## Canonical atom schema
Every admitted training atom should carry enough metadata to be re-rendered for different learners without losing lineage:

- `atom_id`
- source repository / exact source revision
- source row ID / split / subset
- license / source-license details
- language
- capability tags
- domain tags
- interaction shape: single-turn / multi-turn / tool trajectory
- messages / tool schema / observations
- reasoning content stored separately from final answer where source permits
- verifier or success evidence
- source quality metadata
- long-horizon/LHIT invariant tags
- token-length estimates per target tokenizer
- exact/fuzzy contamination fingerprints
- dedup lineage
- admission state and reason

Reasoning traces should not be blindly fused into every target model's visible answer format. The atom keeps reasoning and final answer separable so target-specific renderers can preserve thinking-capable models without forcing hidden-chain style onto ordinary assistants.

## Initial capability lanes
These are coverage targets, not rigid quotas. Final allocation is token-weighted and quality-limited.

### 1. Mathematical reasoning
Desired properties:
- verified final answers;
- difficult rather than repetitive-easy problems;
- proof/derivation variety;
- arithmetic/algebra/geometry/combinatorics/number theory mix;
- optional tool-integrated reasoning kept distinguishable from pure reasoning.

Primary candidates:
- `open-r1/OpenR1-Math-220k`, default subset — Apache-2.0, verified traces;
- `nvidia/Nemotron-SFT-Math-v4` — current high-quality 2026 math source, but mixed CC-BY/CC-BY-SA terms require row/source license segregation before admission.

### 2. General reasoning / STEM
Primary candidates:
- `open-thoughts/OpenThoughts-114k` — Apache-2.0;
- carefully selected reasoning/STEM material from NVIDIA post-training releases when prompt/answer context is complete and license/provenance is clear.

### 3. Software / coding
Desired properties:
- executable or externally checkable solutions where possible;
- code critique and repair, not only code generation;
- repository-scale reasoning in a bounded share;
- SQL/data tasks as a separate capability tag.

Primary candidates:
- `nvidia/Nemotron-SFT-Competitive-Programming-v2` — mixed CC-BY/ODC-By/MIT; segregate license by source;
- `nvidia/Open-SWE-Traces` — CC-BY-4.0; prefer `resolved=1`, remove hacking/benchmark leakage patterns, preserve repository license metadata;
- `nvidia/Nemotron-SFT-SWE-v3.5` remains candidate-only until its model-card wording and license scope are reconciled.

### 4. Tool use / agent execution
Primary candidates:
- `nvidia/Nemotron-SFT-Agentic-v2` — current 2026 tool-use trajectories;
- successful-only trajectories from `open-thoughts/OpenThoughts-Agent-SFT-100K` where task completion is explicit.

Rules:
- failed trajectories are not positive SFT targets by default;
- tool failures may be retained only for explicitly labeled recovery/correction examples;
- tool schemas and observations must remain learner-visible when they are necessary to understand the action.

### 5. Deep research / evidence synthesis
Primary candidates:
- `osunlp/QUEST-SFT-Data-Open-ended` — MIT;
- `osunlp/QUEST-SFT-Data-Objective` — MIT;
- `simplex-ai-inc/LiteResearcher-SFT-Data` — Apache-2.0;
- `NextTokenAI/NextSearch-1-Trajectories`, Apache-2.0 config only unless a different license is explicitly accepted.

Desired behavior:
- multi-source search;
- source comparison;
- evidence-grounded synthesis;
- query decomposition;
- recovery from unhelpful search results;
- explicit uncertainty when evidence is insufficient;
- distinction between retrieved evidence and generated interpretation.

Do not treat intermediate teacher reasoning as factual ground truth merely because the final answer passed.

### 6. Instruction following / conversational quality
Primary candidate:
- `nvidia/Nemotron-SFT-Instruction-Following-Chat-v2` — ODC-By.

Selection should favor precise constraint following, structured outputs, multi-turn correction, and concise competent answers rather than verbosity for its own sake.

### 7. LHIT / long-horizon interaction / Capybara lineage
Donor sources:
- `LDJnr/Capybara` — Apache-2.0;
- `argilla/Capybara-Preferences-Filtered` — Apache-2.0;
- `argilla/distilabel-capybara-dpo-7k-binarized` — Apache-2.0;
- later, selected locally generated continuations only after independent quality verification.

Admission is based on useful invariants, not the Capybara label. No fixed Capybara percentage is authoritative.

### 8. Structured/data reasoning
Pull selectively from high-quality text-to-SQL, structured-output and schema-constrained sources. Treat structured-output correctness as a separately checkable capability.

## Initial corpus scale
Do not begin with a million-row mixture.

### Stage A — Standard Core Pilot
Target roughly `8–15 million assistant-target tokens` after filtering.

Purpose:
- prove the schema and filters;
- measure whether the mix improves the first learner without obvious regression;
- estimate per-lane marginal value;
- avoid spending weeks training on a bad mixture.

The actual row count is intentionally unspecified because a 300-token instruction and a 6,000-token research trajectory are not equivalent units of developmental dose.

### Stage B — Expanded Standard Corpus
Only after Stage A survives phenotype and regression evaluation. Expand lanes whose marginal value is positive and underrepresented; do not mechanically scale every source.

## Informed standard ordering
The standard dataset has one practical training ordering, not a CFE treatment/control pair.

Ordering may use conservative CFE/LHIT-informed heuristics:
- interleave capability families;
- avoid long homogeneous source runs;
- revisit related skills after spacing;
- maintain broad support;
- place contrasting failure/correction patterns near enough to be useful;
- preserve causally relevant multi-turn history intact.

This ordering is an engineering choice and carries no CFE scientific claim.

## Quality gates
Before final admission:
1. complete prompt/context exists;
2. output is not an error/refusal artifact unless intentionally teaching recovery;
3. success/verifier evidence is preserved when available;
4. no unresolved license state;
5. no exact duplicate;
6. no near-duplicate dominating a capability lane;
7. no known evaluation contamination;
8. no malformed tool/message transitions;
9. target length fits at least one planned training view without destructive truncation;
10. source provenance remains recoverable.

## Preference stage
Preference data is kept separate from SFT. Capybara filtered preferences can contribute here, alongside later modern preference sources after quality/licensing review.

`REJECTED RESPONSE != SFT TARGET`

## Outstanding priors that do NOT block source intake
- final trainable Capybara-successor base model;
- Qwen3.6/Gemma challenger benchmarking;
- 8K/16K MTP runtime tuning;
- CFE DD2 scientific completion;
- final CFE matched-arm experiment design.

These matter before later model selection/scientific claims, not before standard dataset construction.

## Hard gate before final freeze
The evaluation-only contamination registry and local pre-training phenotype probes must be frozen and applied before a candidate atom set becomes a trainable release.
