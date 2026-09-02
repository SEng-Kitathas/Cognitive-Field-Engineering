# AI Reasoning Trace Temporal Cartography — Forest Synthesis v1

Date: 2026-09-02
Status: **FIRST TRACE-LEVEL TEMPORAL CARTOGRAPHY / HIGH-VALUE RESEARCH / HOSTILE REVIEW PENDING**

Primary trace deck:
`state/analysis/AI_REASONING_TRACE_SPECIMENS_V1_20260902.json`
SHA-256: `e1f05fd59d69c3f8dd02f8b069247b550ef9a4a05311975ffa229f9296bd7726`

Temporal categorical matrix:
`state/analysis/AI_REASONING_TRACE_TEMPORAL_MATRIX_V1_20260902.json`
SHA-256: `180669e30f5b5dd405d3887af6fd21537053fb7d5323b679fd3eeb61cea7473f`

## Objective
Chart actual reasoning/search/revision traces across AI history and ask what they silently imply about:
- active state;
- viable alternatives;
- support/dependency structure;
- representation adequacy;
- control and metacontrol;
- authority/evidence;
- time/currentness;
- failure and repair;
- compression;
- learning from deliberation;
- allocation of reasoning effort.

Then treat the whole longitudinal field as the object, not isolated historical tricks.

`TRACE != PAPER`
`TRACE SPECIMEN != WHOLE SYSTEM`
`FOREST != FEATURE COUNT`
`CHRONOLOGY != CAUSATION`

---

# Trace spine

## 1959 — GPS: reasoning as explicit state-difference reduction
The means-ends trace is structurally explicit:

`current state -> desired state -> salient difference -> relevant operator -> prerequisite subgoal -> transformation -> remaining difference`

Silent implications:
- reasoning is consequence-directed rather than free continuation;
- operators are indexed by what differences they can change;
- subgoals arise when a useful operator is not yet applicable;
- transformations can change some features while intentionally preserving others;
- control/search state is distinct from object state.

What is missing from the specimen:
- maintained rich alternative sets;
- explicit support environments;
- learned representation change.

## 1977 — Version Spaces: evidence moves the boundary of possibility
The candidate-elimination trace changes the unit of reasoning.

Instead of one chosen hypothesis:

`all evidence-consistent rules -> new evidence -> remove inconsistent region -> minimally shift general/specific boundaries -> all surviving rules remain live`

The deep signal is not the specific rule language. It is:

> **uncertainty can be represented as a structured region with a boundary that changes under evidence.**

Past evidence constrains every future update; history is not merely context—it defines which transformations are legal.

## 1979 — Multiple Hypothesis Tracking: later evidence reaches backward
The tracking trace adds a temporal dimension absent from ordinary static hypothesis sets:

`ambiguous measurement -> several associations -> recursively weighted joint hypotheses -> later measurement -> earlier association requalified -> prune / merge / factor`

Silent implications:
- later evidence can alter the qualification of an earlier interpretation;
- ambiguity is allowed to persist rather than being forced closed;
- currently similar hypotheses can be merged for economy;
- independent subproblems can be factored;
- false and missing observations must exist inside the possibility model.

This is one of the clearest non-language historical embodiments of **consequential history**.

## 1986 — ATMS: belief content separates from the conditions under which it holds
ATMS makes support topology first-class:

`datum -> minimal assumption environments -> multiple inconsistent contexts coexist -> contradiction -> nogood support combination -> exclude region -> reinstate unaffected derivations elsewhere`

The million silent things here include:
- content and support are distinct state;
- a contradiction does not globally erase knowledge;
- UNKNOWN is not negation;
- support conditions can compactly represent many full contexts;
- failure can generalize to a forbidden region;
- reason maintenance can be separated from domain inference.

This is not a neural architecture prescription. It is a very clean engineered embodiment of support-aware possibility maintenance.

## 1987 — GDE: model/world residual becomes an experiment-selection problem
The worked diagnosis trace:

`model prediction != measured artifact -> minimal competing diagnoses -> choose X because it separates high-probability candidates -> observe X -> update candidate set -> repeat`

The deep transition is from passive uncertainty to **active discrimination**.

Not all additional evidence has equal value. The best observation is the one whose possible outcomes partition the surviving explanations.

This independently recovers CFE's identifying-support intuition from a completely different engineering tradition.

## 1987 — Soar: strip the successful trace for its dependency spine
Soar's learning trace is especially important for the user's LHIT warning.

It does **not** preserve an entire subgoal episode as the learned object. It traces backward from the result through the production dependencies relevant to that result, then compiles the useful relation into a chunk.

Silent implication:

> **experience is valuable because of the dependency structure it contains, not because every surface event deserves preservation.**

This is almost an explicit historical example of `STEAL INVARIANTS NOT ABSTRACTIONS` applied to a reasoning trace.

## 1993 — Dynamic Backtracking: rollback to cause, not clock
The worked map-coloring trace makes the repair topology visible:

`assign values -> dead end -> inspect elimination explanations -> identify causal assignments -> undo only relevant support -> store new elimination reason -> reorder search -> retain unrelated hard-won deductions`

This gives a very strong invariant candidate:

> **Temporal recency is not a valid proxy for causal responsibility.**

The system preserves Czechoslovakia's valid assignment even while revising an earlier/later ordering around Bulgaria/Denmark.

That is exactly what naive autoregressive "start over" reasoning fails to guarantee.

## 1996 — GRASP: failure becomes future structure
The SAT trace pushes beyond repair:

`decisions -> propagated implications -> implication graph -> conflict -> causal analysis -> learned clause -> nonchronological backtrack`

The conflict is compressed into a constraint that changes all future search.

Silent implication:

> **The most valuable product of a failed reasoning episode may be the reusable boundary it reveals, not the corrected answer.**

This has direct implications for debugging, research falsification, developmental learning, and dataset design.

## 2022 — Chain-of-Thought: flexible intermediate representation, weakened reason maintenance
The CoT specimen re-externalizes intermediate state in natural language:

`problem -> generated intermediate arithmetic state -> later step consumes prior generated result -> final answer`

This is a major representational liberation: a domain-general model can generate its own intermediate vocabulary without the symbolic-state engineering required by GPS/ATMS/SAT.

But the same trace lacks several things older systems made explicit:
- support environments;
- branch-local assumptions;
- conflict regions;
- guaranteed local rollback;
- separate verification authority.

The history is therefore not "old systems could not reason, then LLMs learned reasoning."

A better reading is:

> **LLMs gained a radically flexible reasoning substrate while sacrificing or hiding some explicit maintenance structure.**

## 2022 — ReAct: reality re-enters the loop
The HotpotQA trajectory restores a crucial structure:

`search -> observation -> relational lookup -> ambiguity observed -> refined search -> external answer evidence -> finish`

The new ingredient is not merely tools. It is authority:

> the environment can provide information that changes the next reasoning state.

A thought changes internal context; an action can change evidence state.

This distinction is foundational for research agents, code/tool agents, and consequential LHIT.

## 2023 — Tree of Thoughts: explicit branching is rebuilt outside the model
ToT restores:
- multiple semantic states;
- bounded frontier management;
- evaluation;
- pruning;
- lookahead/backtracking.

But its branches are generally materialized as independent thought states and evaluated by model-based heuristics.

Compared with ATMS/GDE, it still lacks a clean representation of:
- minimal support environments;
- branch-local dependency cones;
- reusable conflicts;
- consequence-equivalence compression;
- evidence-seeking discriminators.

Thus:

`TREE OF TEXT != SUPPORT-AWARE MULTI-HYPOTHESIS FIELD`

## 2024 — Belief-R: modern models rediscover selective revision as a failure
The specimen is deceptively simple:

`initial inference -> new premise -> either retract old conclusion or preserve it`

The benchmark finds a tradeoff between models that revise too little and models that revise too much.

That is the exact reason-maintenance problem:

> **revision sensitivity is not revision selectivity.**

The desired operation is dependency-local:
change what lost support; preserve what did not.

## 2025 — DeepSeek-R1: some control moves inside the generated trace
The visible example:

`algebraic path -> local distrust / reevaluation -> return to earlier equation -> recompute -> revised path`

The surface phrase is irrelevant. The structural change is that a trained model can generate a control-state transition inside the same semantic stream.

Compared with ToT, some correction policy is re-internalized.

Compared with ATMS/GRASP, the support and rollback structure is much less explicit and may be unfaithful or inefficient.

This suggests a historical migration, not simple progress.

## 2026 — STALE: memory becomes reason maintenance again
The memory trace:

`old state -> later non-negating observation -> latent attribute update -> downstream old memory becomes inapplicable -> later query must resist semantically relevant stale retrieval`

The strongest point is Type-II propagated conflict:
new information updates one variable, but a different old belief loses validity because of the consequence chain.

This is the frame/currentness/support problem in conversational form.

`RETRIEVAL != CURRENTNESS RESOLUTION`

## 2026 — CTRLS: transition quality becomes an explicit model target
The paired case studies hold setup relatively fixed and show divergence at an intermediate symbolic transition:

`same setup -> one bad transition / one sound transition -> downstream trajectories diverge -> different terminal answer`

The important signal is not that CTRLS is the correct formalism. It is that current research is explicitly treating **ordered transitions between intermediate states** as an object worth modeling rather than treating CoT as an unordered string of helpful tokens.

---

# The forest: what changed across time?

## F1 — Reasoning structure migrates between planes
The clearest non-linear historical pattern is a repeated migration:

1. **Explicit external structure** — goals, branches, assumptions, conflicts and control are hand-designed and inspectable.
2. **Specialized maintenance** — TMS/ATMS/diagnosis/SAT separate support and conflict state from domain inference.
3. **Learned compression** — evaluation/search guidance increasingly moves into learned functions.
4. **Generative re-externalization** — language models make intermediate semantic state flexible and visible again.
5. **Scaffold reconstruction** — tools, ToT, verifiers, memory and process supervision rebuild missing structure outside the model.
6. **Partial re-internalization** — reasoning-trained models begin to internalize search/correction/effort-allocation policies.
7. **Current frontier seam** — flexible neural representation and explicit reason maintenance are still not cleanly unified.

This is a **migration hypothesis**, not a causal law.

## F2 — Generality and explicit maintainability appear to trade places
Old systems often have:
- crisp dependencies;
- explicit alternatives;
- local rollback;
- strong external authority;
- poor/open-world representation flexibility.

Modern language models often have:
- broad semantic representation;
- dynamic abstraction;
- cross-domain generalization;
- weak/hidden support lineage;
- brittle selective revision;
- costly redundant search.

The likely research target is not to return to symbolic AI.

It is:

> **preserve modern representational flexibility while recovering the useful invariants of explicit reason maintenance.**

## F3 — Multi-hypothesis is a maintenance problem more than a generation problem
Across Version Spaces, MHT, ATMS, diagnosis, ToT and modern hypothesis tracking, merely generating alternatives is the easy/common piece.

The hard recurring questions are:
- which alternatives are truly consequence-distinct?
- under what assumptions does each hold?
- which evidence supports which branch?
- what can be merged without losing future separability?
- what new evidence would split the survivors?
- what becomes invalid when support changes?
- what is still UNKNOWN?
- when should a representation itself split?

This is why independent chain sampling + voting feels insufficient.

## F4 — Time is causal structure, not sequence length
Several traces show different kinds of consequential history:
- Version Spaces: all prior examples constrain legal boundary movement.
- MHT: later observations requalify earlier associations.
- ATMS: old derivations become active/inactive as support environments change.
- Dynamic Backtracking: chronological order is explicitly rejected as a repair criterion.
- ReAct: observations alter future reasoning/action state.
- STALE: later evidence invalidates old applicability through indirect consequence.

Thus:

`LONGER HISTORY != MORE CONSEQUENTIAL HISTORY`

and:

`TEMPORAL ORDER != CAUSAL DEPENDENCY`

This is the same stripped LHIT lesson at reasoning-trace scale.

## F5 — Failure evolves from terminal label to reusable structure
Historical progression in the specimens:

`failure -> try another operator`
`-> failure eliminates hypothesis region`
`-> failure localizes assumptions`
`-> failure becomes nogood/conflict explanation`
`-> failure becomes learned clause/chunk`
`-> modern trace often returns to prose correction without durable explicit conflict memory`

This suggests a large missed opportunity in modern reasoning/data:

> **train on the portable boundary exposed by failure, not merely the repaired response.**

## F6 — Representation adequacy sits above ordinary hypothesis revision
The history repeatedly warns that search can fail because the coordinate system is wrong:
- GPS depends on a difference/operator vocabulary.
- Version Spaces depends on the rule-language ordering.
- GDE's diagnostic grain is set by the available model-artifact differences.
- Soar compiles dependencies expressed in its production representation.
- CoT gains flexibility by moving to language.
- frontier traces sometimes explicitly discover that a coarse abstraction is insufficient.
- CTRLS/2026 geometry research targets transition/representation structure directly.

Therefore:

`HYPOTHESIS SEARCH INSIDE BAD REPRESENTATION -> PATCHING / RUMINATION`

A multi-hypothesis system must eventually allow **representation-level alternatives**, not only answer-level alternatives.

## F7 — Authority separation repeatedly repairs internal reasoning
Across eras, high reliability often comes from a separate adjudication channel:
- theorem/proof constraints;
- empirical data;
- measurements;
- SAT contradiction;
- environment observation;
- tool result;
- formal verifier.

Modern self-evaluation sometimes collapses generator and judge into one correlated source.

Candidate invariant:

> **Orthogonal evidence channels are especially valuable where the generator and evaluator would otherwise share the same blind spot.**

## F8 — Useful reasoning effort is conditional
GPS prioritizes hard differences; HEARSAY/meta-control schedules useful internal actions; GDE spends measurements where they split candidates; Russell/Wefald values computation by decision effect; ReAct uses sparse thoughts in action-heavy tasks; modern models expose thinking budgets.

The recurring target is:

`EFFORT ~ EXPECTED DISCRIMINATORY / DECISION VALUE`

not:

`EFFORT ~ DIFFICULT-LOOKING PROMPT` or `ALWAYS THINK LONGER`.

## F9 — Compression is safe only when future discriminators survive
Several histories are fundamentally compression stories:
- Version Space boundaries compress many hypotheses.
- MHT merges similar estimates and factors clusters.
- ATMS minimal supports/nogoods compress contexts.
- GRASP clauses compress failure regions.
- Soar chunks compress useful deliberation dependencies.
- language models compress huge learned histories into weights.

The shared qualification is:

> **compression is safe only if distinctions needed by future consequence remain recoverable.**

That links reasoning archaeology directly to StarMap/LBE/Rosetta questions.

---

# Reverse reasoning: what may matter causally?

The temporal map does not prove causes, but it sharpens candidate explanations.

## R1 — Why does plain CoT regress on maintenance functions older AI made explicit?
Candidate cause:
Natural language intermediate state is flexible but does not inherently carry machine-usable support/context/conflict structure.

Discriminator:
Compare matched CoT against support-annotated branch state under equal compute and identical base model.

## R2 — Why does ToT help yet remain expensive/brittle?
Candidate cause:
It materializes full semantic branches instead of compact support/equivalence/conflict structure.

Discriminator:
Compare full branch materialization with shared hard state + branch-local deltas/support.

## R3 — Why do memory systems retrieve stale information?
Candidate cause:
Memory stores text/embeddings more readily than dependency/currentness structure.

Discriminator:
Compare semantic retrieval alone against explicit support/currentness propagation under matched memory content.

## R4 — Why do reasoning models still ruminate?
Candidate cause:
Correction policy is learned, but generalized conflict memory and value-of-computation control are weak/implicit.

Discriminator:
Give repeated isomorphic failures and measure whether explicit structural conflict carry reduces repeated search beyond extra-context controls.

## R5 — Why do strong models patch inside bad abstractions?
Candidate cause:
Hypothesis search is easier/cheaper than representation-level change, so local patches dominate until contradiction pressure becomes extreme.

Discriminator:
Construct matched tasks where the only efficient solution requires splitting an aliased representation; vary pressure/revisit geometry.

---

# Strongest current forest synthesis

The earlier hypotheses can now be combined more precisely:

> **Reasoning is constraint-preserving state transformation under changing evidence.**

plus:

> **When the current representation aliases consequence-distinct states, capable reasoning must refine the representation itself.**

plus the temporal archaeology result:

> **The reasoner must maintain a compact support topology over still-possible states so that evidence can selectively preserve, split, merge, invalidate and refine them, while failure becomes reusable constraint information and control spends computation/observations where they can alter consequence.**

The central unresolved engineering problem is therefore not "make longer chains of thought."

It is:

> **How do we combine flexible learned representation with bounded, support-aware, temporally current, multi-hypothesis reason maintenance without forcing the learner into a brittle curator ontology?**

That is the forest.

---

# Claim ceiling
This v1 synthesis is grounded in 15 source-located trace specimens plus the wider 67-source archaeology field.

It supports:
- recurring functional structures;
- a non-linear temporal migration hypothesis;
- cross-domain design hypotheses;
- direct matched experiments.

It does not establish:
- universal cognitive primitives;
- hidden causal mechanisms inside modern LLMs;
- that old symbolic architectures should be transplanted;
- that visible CoT faithfully describes internal computation;
- that chronological appearance identifies causal innovation.
