# CFE Reasoning Archaeology — Deep Research Wave 1

Status: **EXTERNAL RESEARCH SYNTHESIS / NON-AUTHORITATIVE / EXPERIMENT-GENERATING**
Date: 2026-09-02 22:50 Eastern Daylight Time
Primary ingress: `research/CFE_REASONING_ARCHAEOLOGY_DEEP_RESEARCH_HANDOFF_2026-09-02.md` SHA `afa4b9d8e4805679644b8c22f9ef71dc02f4ae3bd967ae077f4f7eb5a1147b44`

## Purpose
Attack the seams that decide whether the current reasoning synthesis can become an engineering object rather than remain an attractive interpretation:

1. faithful support/dependency extraction;
2. representation emergence/refinement across training;
3. value-guided reasoning effort / discriminator allocation;
4. learning from deliberation without copying raw trace text;
5. trace faithfulness / structural support vs narrated reasoning.

All findings below are **external donor evidence**, not CFE scientific promotion.

---

## 1. Representation development is now experimentally observable across training

### External evidence
Recent cross-checkpoint sparse-feature work reports that interpretable features can be aligned across pretraining snapshots and tracked through emergence, maintenance, rotation/degeneration, and later complex-feature formation. Two particularly relevant lines are:

- *Crosscoding Through Time: Tracking Emergence & Consolidation Of Linguistic Representations Throughout LLM Pretraining* (arXiv:2509.05291).
- *Evolution of Concepts in Language Model Pre-Training* (ICLR 2026 / arXiv:2509.17196).

The latter reports an early statistical-learning phase followed by feature emergence and later complex features, with feature-attribution analyses connecting representation evolution to downstream performance.

### What this supports
- Internal representation is not static during training.
- Training can be studied at the level of feature emergence/consolidation rather than only final benchmark score.
- CFE developmental-order experiments can potentially observe whether different experience geometries produce different feature-development trajectories.

### What this does NOT support
- It does not establish CFE.
- It does not show that a prerequisite-respecting curriculum is superior.
- It does not prove that complex features require specific simpler features first.
- Crosscoder features are analysis coordinates, not automatically learner-native ontology.

### CFE experiment unlocked
For a matched dependency-order experiment, checkpoint both arms throughout training and compare:
- feature-emergence timing;
- feature persistence/degeneration;
- representational similarity/divergence;
- transfer/composition competence;
- whether later prerequisite exposure repairs or preserves an earlier phenotype.

This gives the developmental-basin hypothesis a possible internal readout rather than only final behavior.

---

## 2. Faithful support extraction remains unsolved; single-method attribution is unsafe

### External evidence
Relevant modern lines include:

- *Mechanistic Interpretability of Chain-of-Thought Reasoning via Sequential Activation Patching* (arXiv:2608.22332): sequential patching finds temporally distributed CoT-related effects and overlapping head sets associated with trajectory maintenance and answer computation.
- *Causally Grounded Mechanistic Interpretability for LLMs with Faithful Natural-Language Explanations* (arXiv:2603.09988): circuit explanations can have high sufficiency but low comprehensiveness, exposing distributed backup mechanisms.
- *Mechanistic Data Attribution: Tracing the Training Origins of Interpretable LLM Units* (arXiv:2601.21996): influence-based attribution can connect training examples to the emergence of interpretable units and experimentally alter those units by targeted data intervention.
- *Is This the Subspace You Are Looking for? An Interpretability Illusion for Subspace Activation Patching* (ICLR 2024): causal patching can activate dormant pathways and produce a misleading localization story.
- Circuit-based reasoning verification (ICLR 2026 work using attribution graphs/transcoders) treats structural computation traces as diagnostics, but still operates through surrogate interpretability coordinates.

### Synthesis
`CAUSAL EFFECT != COMPLETE SUPPORT GRAPH`

A component can be sufficient under intervention without being the unique or complete support path. Backup pathways and intervention-induced behavior matter.

### CFE implication
Faithful support extraction should require triangulation:
1. causal intervention / ablation;
2. necessity + sufficiency checks;
3. stability across examples/checkpoints;
4. distributed/backup-path audit;
5. where possible, data-origin attribution;
6. comparison to known synthetic ground-truth dependency structure.

A useful benchmark for CFE is therefore not “can we draw a plausible circuit?” but “does extracted support recover the known dependency topology of a controlled developmental task, and does it predict local rollback under intervention?”

---

## 3. Reasoning effort should be allocated by expected value, not uniform depth

### External evidence
Current test-time-compute work increasingly formulates reasoning as a resource-allocation problem:

- *Scaling LLM Test-Time Compute Optimally Can Be More Effective Than Scaling Parameters for Reasoning* (ICLR 2025) shows the value of selecting test-time scaling strategies rather than blindly increasing compute.
- *Reasoning on a Budget* (2025 survey) distinguishes controllable fixed-budget reasoning from adaptive allocation based on difficulty/confidence.
- *Adaptive Test-Time Compute Allocation for Reasoning LLMs via Constrained Policy Optimization* (arXiv:2604.14853) explicitly optimizes expected accuracy under an average compute budget.
- *Adaptive Test-Time Compute Allocation via Learned Heuristics over Categorical Structure* (arXiv:2602.03975) allocates verification calls using state uncertainty and reports fewer verifier calls than uniform/best-of-N baselines on its benchmark.

### What this supports
The modern field is converging on the same high-level pressure as the archaeology:

`MORE REASONING != OBJECTIVE`

`EFFORT SHOULD DEPEND ON EXPECTED DECISION / VERIFICATION VALUE`

### What remains open
Most work optimizes inference-time compute after the model is trained. CFE/ISD asks a different developmental question: can experience teach a learner when additional reasoning/search is worth its cost?

The newly admitted ISD adaptive-effort STOP/CONTINUE anti-isomorph family is therefore aligned with, but not validated by, this external literature.

---

## 4. Learning from deliberation without verbatim trace imitation is plausible but not solved

### External evidence
Several recent approaches separate the information in reasoning from literal reproduction of the trace:

- *Compress-Distill* (arXiv:2606.05988) compresses teacher traces substantially; compressed traces preserve much of raw-trace accuracy while improving token efficiency, but raw traces remain best in the reported settings.
- KAVA / KV-cache distillation (ICLR 2026 submission) uses explicit CoT as a teacher signal for latent reasoning via hidden-state/KV matching.
- *Latent Guidance* (ICLR 2026) explicitly separates an implicit high-level plan from the student's textual execution and reports gains over several distillation baselines.
- RL-aware distillation (arXiv:2602.22495) selectively imitates teacher behavior only when it improves the student's current policy update, rather than enforcing fixed offline trace imitation.
- MIND (arXiv:2601.03717) argues that a single teacher rationale can be mismatched to a student's evolving capacity and uses multiple perspectives with capability-aware filtering.

### CFE relevance
This strongly motivates separating:
- **developmental consequence / strategy signal**, from
- **teacher's exact narrated inner monologue**.

It also aligns with the ISD training-body-purity and private-reasoning stripping rules already in force.

### Hard guard
None of these results proves that outcome-only training captures reason-maintenance state. Raw trace can still carry useful information, and compressed/latent methods trade fidelity, efficiency and student capacity differently.

The target experiment should ask which *minimal supervision surface* transfers:
- dependency-local repair;
- support persistence;
- discriminator selection;
- currentness propagation;
- representation refinement;
without requiring verbatim teacher-CoT imitation.

---

## 5. Trace text is not a faithful state ledger

### External evidence
- ICLR 2026 work on CoT trace dynamics reports strongly non-monotonic contribution of partial reasoning, sharp insight-like jumps, tangents, and cases where correct answers arrive with weak prior justification.
- Sparse-autoencoder + activation-patching work finds causally relevant CoT features can be distributed rather than concentrated in a few obvious textual steps.
- Sequential activation patching likewise finds temporally distributed causal effects.

### CFE implication
`TRACE TEXT != REASONING STATE` remains strongly justified as a guard.

Reason-maintenance research should treat text traces as observations of an underlying state process, not the state itself.

---

## 6. Developmental staging gains an instrumentation path, not proof

The new ISD dependency-stage doctrine and the CFE prerequisite-topology hypothesis become more experimentally tractable when paired with cross-checkpoint representation analysis.

Proposed matched study:

### Arm A — dependency-respecting
Primitive distinctions and identifying relations become available before dependent abstractions.

### Arm B — dependency-violating
Same information/dose but dependent abstractions arrive before their identifying prerequisites.

### Behavioral readouts
- primitive acquisition;
- composition;
- transfer;
- correction/relearning cost;
- local-vs-global rollback;
- novel discriminator selection.

### Internal-development readouts
- cross-checkpoint feature emergence;
- feature persistence/degeneration;
- representation similarity;
- causal role of features in transfer;
- whether later prerequisite exposure reorganizes or merely appends to the earlier representation.

### Interpretation guard
If internal features differ but behavior does not, that is representation-path evidence, not competence evidence. If behavior differs without interpretable feature differences, the developmental effect still stands behaviorally.

---

## Wave-1 priority update

### P0
1. **Dependency-order + representation-development experiment** — strongest bridge between current CFE developmental hypothesis and new instrumentation.
2. **Known-topology support extraction benchmark** — test whether causal/attribution tools can recover synthetic support dependencies and predict local rollback.
3. **Learning-from-deliberation ablation** — outcome-only vs concise structural supervision vs raw reasoning trace, measured on reason-maintenance transfer rather than only answer accuracy.

### P1
4. Cross-episode reusable conflict memory.
5. Currentness propagation under indirect dependency.
6. Orthogonal authority channels / truly independent verification.

### P2
7. Broader Anthropic/CFE-adjacent path-dependence comparison after the mechanistic tests above sharpen the target.

---

## Truth boundary

### Externally observed / published claims used as donor evidence
The cited works report representation evolution across checkpoints, adaptive compute allocation, mechanistic attribution/patching findings, trace-compression/latent-distillation approaches, and trace-dynamics analyses.

### CFE inferred
These lines jointly make it more plausible that developmental representation trajectories, support topology, and effort allocation are experimentally addressable.

### Still hypothetical
The unified CFE claim that dependency-respecting developmental geometry produces better representation basins and reason-maintenance competence remains unearned until matched causal training experiments are run.
