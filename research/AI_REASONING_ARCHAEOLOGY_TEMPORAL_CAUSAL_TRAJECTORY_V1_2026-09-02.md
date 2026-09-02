# AI Reasoning Archaeology — Temporal/Causal Trajectory v1

Date: 2026-09-02
Status: **PROVISIONAL HISTORICAL CARTOGRAPHY / SOURCE-LEVEL + PRIMARY-SPECIMEN SUPPORT**

## Reading rule
This is not a progress ladder and not a SOTA history.

For every transition distinguish:
- `FIRST_OBSERVED_PUBLIC_EMBODIMENT`
- `DOCUMENTED_LINEAGE`
- `INDEPENDENT_FUNCTIONAL_RECURRENCE`
- `CANDIDATE_CAUSAL_ENABLER`
- `UNKNOWN`

`HISTORICALLY_PRECEDES != CAUSED`

## 1950s — reasoning as explicit state/control machinery
### Visible structures
- proof/search states;
- goals and subgoals;
- operators;
- premise selection;
- declarative vs imperative knowledge;
- explicit heuristics;
- partial-success need.

### Silent shift
The central problem is already not just deduction. It is **which knowledge becomes active and which operation should happen next**.

### Candidate trajectory pressure
Early systems expose control because designers must hand-author it.

## 1960s–1970s — hypotheses, evidence, uncertainty, and justification become explicit
### DENDRAL / scientific inference
Multiple explanatory structures compete against empirical evidence.

### Situation/common-sense logic
World state, action, observation, available knowledge, and representational adequacy become separable formal concerns.

### 1977 convergence cluster
Several independent papers attack different portions of the same larger problem:

- Version Spaces: preserve all evidence-consistent hypotheses compactly.
- Dependency-directed backtracking: track why facts hold so contradiction can revise causal support rather than history.
- HEARSAY-II focus: allocate scarce processing among competing potential internal actions on shared state.
- Multiple representations: use cheaper/coarser reasoning when sufficient and escalate representation when required.

### Historical implication
By 1977, **candidate maintenance, support lineage, attention allocation, and representation choice** are already separate engineering surfaces.

## 1979 — a bifurcation worth tracking
### Truth maintenance
Doyle turns belief reasons and contradiction-driven revision into a dedicated subsystem.

### Multiple Hypothesis Tracking
Reid independently turns temporal uncertainty into a branching/merging/pruning hypothesis-management problem.

These traditions share no need for common ontology, yet both discover:

`NEW EVIDENCE -> REQUALIFY OLD ALTERNATIVES`

and both need boundedness.

### Strong recurrence signal
The temporal tracker explicitly lets **future observations resolve past ambiguity**. That is a clean non-linguistic embodiment of history-sensitive hypothesis qualification.

## Early/mid 1980s — control and representation become objects of reasoning
### EURISKO
The search language itself becomes an engineering variable. Failure of AM highlights that useful semantic moves may be sparse under the wrong representation.

### Blackboard control
Control is separated from domain reasoning and treated as its own problem with explicit knowledge/state.

### Belief revision
Rational change under contradictory input becomes a formal object.

## 1986–1987 — reason-maintenance peak explicitness
### ATMS
The database no longer represents one current consistent world. A datum carries the minimal assumption environments under which it holds.

Conceptual contexts can be exponential while the actual representation stores minimal support/nogood structures.

### GDE / Reiter diagnosis
Discrepancy creates competing diagnoses; next measurements discriminate among them.

### Soar
Impasse-triggered deliberation can be compiled into persistent future control.

### Historical significance
This period contains explicit engineered versions of:
- live alternatives;
- branch-local support;
- conflict-region pruning;
- scoped revision;
- active discriminator choice;
- learning from deliberation.

Modern LLM research often treats these as newly emerging reasoning capabilities because their **embodiment changed**, not because the functional problems first appeared recently.

## Late 1980s–1990s — factorization, abduction, metareasoning, conflict learning
### Bayesian networks
Exploit conditional independence to factor global uncertainty.

### Abduction/theory formation
Reasoning is framed as forming assumption-qualified explanatory theories and examining their consequences.

### Rational metareasoning
Computational actions are chosen according to expected downstream decision value.

### Query by Committee
Active learning turns disagreement among live models into a query-selection signal.

### Dynamic/conflict-directed backtracking
Search repair becomes increasingly causal/nonchronological.

### Least commitment
Planning preserves optionality by refusing premature specification.

### GRASP / later CDCL
Conflicts become **learned reusable constraints** that permanently alter future search.

### Candidate meta-transition
The system does not merely survive failure anymore. It increasingly **compresses failure into future control knowledge**.

## 2000s–2010s — some reasoning structure moves into learned functions
Search/control systems increasingly mix:
- explicit branch structure;
- learned evaluation/prior functions;
- statistical uncertainty;
- external outcome authority.

AlphaGo is a clean later exemplar: explicit search topology remains while policy/value guidance moves into learned models.

### Non-monotonic historical interpretation
Reasoning structure did not disappear. Parts migrated from hand-authored symbolic control into learned compressed guidance.

## 2007 self-model/attention lineage
Chella/Gaglio provide an instructive non-LLM architecture:
- raw perceptual/subconceptual state;
- conceptual geometry;
- linguistic assertions;
- attention-gated admission;
- temporal prediction;
- higher-order historical self-state;
- compression of old history.

This independently reinforces the distinction:

`RICH CURRENT FIELD != MATERIALIZED SYMBOLIC VIEW`

and:

`TRUE DETAIL != WORTH ATTENDING/MATERIALIZING NOW`

## 2022 — generated language becomes a reasoning substrate
Chain-of-thought re-externalizes intermediate state as text.

This is a major substrate transition, not the invention of decomposition.

### What is gained
- flexible, domain-general intermediate representation;
- easy human inspection;
- generative decomposition without hand-designed symbolic state.

### What is lost or weakened
- explicit support lineage;
- crisp branch identity;
- guaranteed local rollback;
- structured uncertainty;
- independent authority;
- compact maintained hypothesis regions.

## 2022–2023 — old external machinery gets rebuilt around language models
### Self-Consistency
Multiple paths return, but as independent samples and answer marginalization.

### ReAct
Action/observation reality coupling returns.

### Reflexion
Persistent trial history returns.

### Tree of Thoughts
Branch evaluation/backtracking returns explicitly.

### Process supervision
Intermediate reasoning becomes locally judgeable/training-relevant.

### Candidate historical reading
Early LLM reasoning first gained a powerful **universal substrate**, then rapidly had to rebuild mechanisms older AI had made explicit.

## 2024–2026 — reasoning control starts re-internalizing into trained/latent policy
### Belief-R
Directly exposes selective revision failure.

### Rational Metareasoning for LLMs
Explicitly trains selective reasoning under value-of-computation pressure.

### Thought-Tracing
Reintroduces weighted live hypotheses over evolving state.

### AR-Bench
Shows active evidence acquisition remains much weaker than passive reasoning.

### KUP
Separates memorized update from propagated reasoning consequences.

### STALE
Shows retrieval of newer evidence does not guarantee invalidation of stale state or downstream policy adaptation.

### Reasoning as Trajectories
Finds functionally ordered latent subspaces and late correctness divergence.

### CTRLS
Explicitly models CoT as latent state transitions and optimizes transition dynamics.

### Candidate transition
Some explicit scaffolds are migrating back into learned/latent control:

`EXTERNAL REASONING ALGORITHM -> TRAINED REASONING POLICY`

But several maintenance functions remain weak:
- selective invalidation;
- support lineage;
- active discriminators;
- representation-level hypothesis competition;
- currentness propagation.

## The non-linear macro-pattern
A useful first approximation is:

1. **Explicit symbolic/control structure** — reasoning relations are visible because they are designed.
2. **Reason-maintenance specialization** — support, revision, alternatives, and control become dedicated mechanisms.
3. **Learned compression** — evaluation/control increasingly move into learned functions while some search remains explicit.
4. **Generative re-externalization** — LLMs recover flexible intermediate reasoning in language but weaken structured maintenance guarantees.
5. **Scaffold reconstruction** — tools, trees, verifiers, memory, reflection, and process supervision restore missing structure externally.
6. **Partial re-internalization** — reasoning models learn correction/search/effort policies, with some structure becoming latent again.

This cycle suggests:

> **AI history repeatedly moves reasoning structure between explicit external state, learned compressed state, and re-externalized deliberation.**

That is a hypothesis about embodiment migration, not a law of progress.

## Candidate causal enablers to test, not assume

### C1 — Expressive intermediate substrate
Did natural language dramatically reduce the engineering cost of generating intermediate representations across domains?

Alternative: scale/pretraining knowledge, not language-as-substrate, may explain most gains.

### C2 — Verifiable reward
Did domains with cheap objective verification enable reasoning policies to internalize search/correction more reliably?

Alternative: data quality or base-model scale may dominate.

### C3 — Representation geometry
Did reasoning improvements occur where training made useful state transitions locally reachable in latent space?

Alternative: observed latent geometry may be epiphenomenal.

### C4 — Conflict memory
Do systems improve disproportionately when failures become reusable constraints rather than discarded episodes?

Alternative: simple additional training volume may explain gains.

### C5 — Active discrimination
Does selecting evidence by hypothesis disagreement/expected partition reduction generalize beyond tightly formal diagnosis/learning settings?

Alternative: query-generation errors/costs may erase theoretical gains in open-world language tasks.

### C6 — Support/currentness structure
Are modern stale-memory and belief-revision failures primarily caused by missing explicit dependency/currentness structure?

Alternative: basic instruction-following/context-attention limitations may explain them.

## Reverse causal program
For every modern reasoning capability/failure:

1. identify the observable transition/function;
2. locate earlier independent embodiments;
3. identify what information those earlier methods required explicitly;
4. identify which of that information is absent/latent in modern systems;
5. enumerate candidate mechanisms that could supply it;
6. design matched modern tests;
7. only then infer what historical innovations mattered.

## Current strongest reverse inference
Modern reasoning did not need to invent many of the **functions** we now value.

The hard new problem is likely:

> **How do you recover the benefits of explicit reason-maintenance, multi-hypothesis, discrimination, and meta-control without surrendering the flexible distributed representations and generalization of modern foundation models?**

That is a much sharper research target than "make chain-of-thought better."
