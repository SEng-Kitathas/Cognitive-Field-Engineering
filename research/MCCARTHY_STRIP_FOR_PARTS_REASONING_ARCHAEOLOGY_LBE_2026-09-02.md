# McCarthy Strip-for-Parts — Reasoning Archaeology / LBE

Date: 2026-09-02
Status: **FIRST-CLASS HISTORICAL DONOR ANALYSIS / HIGH VALUE / NOT IMPORTED ONTOLOGY**

## Purpose
Strip the McCarthy/McCarthy-Hayes lineage for mechanisms, invariants, failure boundaries, representation laws, temporal/causal structure, and LBE-worthy relations.

Do **not** import Situation Calculus, first-order logic, `ist`, circumscription, possible-world semantics, or McCarthy's terminology as CFE learner ontology merely because the historical isomorphisms are strong.

`DONOR != AUTHORITY`
`FORMALISM != INVARIANT`
`HISTORICAL PRECURSOR != COMPLETE MODERN EXPLANATION`
`STEAL INVARIANTS NOT ABSTRACTIONS`

## Primary sources used

### McCarthy & Hayes 1969
**Some Philosophical Problems from the Standpoint of Artificial Intelligence**
- Author-hosted/public copy cached locally.
- Local SHA-256: `7c2dd812a84465ea9ca58ce068650c8b35c0a96f756b5a9bfe8714e4d9e309d7`
- Source: `https://www-formal.stanford.edu/jmc/mcchay69.pdf`

### McCarthy 1989/1990
**Artificial Intelligence, Logic and Formalizing Common Sense**
- Verified from user-uploaded full paper and author-hosted public copy metadata.
- The uploaded PDF itself is dated 1990; bibliographic references often cite the chapter publication as 1989.
- Author source: `https://jmc.stanford.edu/articles/ailogic/ailogic.pdf`
- Raw server fetch was not bypassed when Stanford's certificate hostname validation failed; user-uploaded full text remains the evidentiary source in-thread.

### McCarthy 1993
**Notes on Formalizing Context**
- Author-hosted copy cached locally.
- Local SHA-256: `a7901c915cf3b32786d6542d512227eec7d79960ad9d39eb57c746479fa892f7`
- Source: `https://www-formal.stanford.edu/jmc/context3.pdf`

### McCarthy 1986
**Mental Situation Calculus**
- Primary publication/public web copy identified.
- Local raw cache acquisition failed closed due certificate hostname mismatch; no TLS bypass used.
- Used as metadata/primary-web evidence only until locally cached through a clean route.

---

# Corrections to the supplied mapping

## C1. Situation Calculus is not "next token = Result(Action,S)"
McCarthy & Hayes use `result(p, sigma, s)` for the situation resulting when actor `p` carries out an action/strategy `sigma` starting in situation `s`. They explicitly distinguish the world-state variable from ordinary program variables and note that changing the world state requires performing an action/observation.

A language model's next token changes the visible/generated trace and conditioning sequence. It is **not established** that each token is an action on a Situation Calculus world state.

Useful stripped analogue:

`CURRENT REASONING STATE + TRANSITION EVENT -> UPDATED REASONING STATE`

Not:

`TOKEN GENERATION == SITUATION CALCULUS ACTION`

## C2. The trace does not prove a literal ramification failure
The historical frame/indirect-effect problems are highly relevant to persistence and consequence propagation, but a visible contradiction in a reasoning trace does not prove that the hidden mechanism is implementing Situation Calculus or experiencing a formal "ramification failure."

Useful stripped invariant:

> **When one state change has indirect consequences, downstream dependent state must be recomputed or invalidated while unaffected state should persist.**

## C3. Context lifting is not identical to abstraction refinement
McCarthy's context work formalizes propositions as holding in contexts and studies movement/generalization/specialization across contexts. The reasoning exemplar's coarse-to-fine representation change is not literally an `ist(c,p)` operation.

Useful stripped analogue:

> **Truth/adequacy can be scope-relative, and new evidence can require leaving a previously adequate context/representation for a more discriminating one.**

## C4. No literal MCTS/PRM/entropy interpretation
Neither McCarthy's formalism nor the visible frontier trace licenses claims that exclamations/checkmarks are PRM anchors, entropy spikes, or an MCTS execution log.

`TREE-LIKE BEHAVIOR != LITERAL MCTS`
`CHECKMARK != VERIFIED REWARD-MODEL EVENT`
`SURFACE STRESS LANGUAGE != MEASURED INTERNAL ENTROPY`

---

# High-value parts

## M1. Three different adequacy questions
McCarthy & Hayes distinguish:

### Metaphysical adequacy
Can the representation in principle describe the world/behavior?

### Epistemological adequacy
Can it practically express the information actually available to the reasoner?

### Heuristic adequacy
Can it express the reasoning processes actually used to solve the problem?

This is extremely high value for CFE/LBE.

Candidate translation:

`WORLD-DESCRIPTIVE ADEQUACY != AVAILABLE-EVIDENCE ADEQUACY != REASONING-CONTROL ADEQUACY`

A representation can be "complete" in one sense and unusable in another.

This directly warns against treating a giant latent/model state as useful merely because it could encode everything in principle.

## M2. Common-sense reasoning lives under unknown relevance
McCarthy's 1990 paper emphasizes that in ordinary reasoning the agent does not know in advance which facts will become relevant, and unanticipated obstacles can require knowledge that previously looked irrelevant.

Candidate invariant:

> **RELEVANCE IS HISTORY- AND CONSEQUENCE-CONDITIONED, NOT FIXED AT INGEST.**

CFE implications:
- long-context availability is not enough;
- support must permit later recruitment of apparently irrelevant information;
- environment design should sometimes make dormant information consequential later.

LBE implication:
- evidence cannot be discarded solely because it lacks current relevance;
- store current relevance separately from existence/lineage.

## M3. Nonmonotonic revision
Classical monotonic deduction preserves conclusions when premises are added. McCarthy's common-sense program explicitly needs cases where new information withdraws previous default conclusions.

Candidate invariant:

`NEW EVIDENCE CAN DEQUALIFY OLD CONCLUSIONS`

This is a clean historical ancestor of:
- currentness;
- revision triggers;
- dependency-local invalidation;
- stale authorization/state;
- LHIT revisit after changed evidence.

## M4. Ambiguity tolerance through concept splitting
McCarthy's 1990 discussion gives an unusually direct representation-refinement move: maintain a default treatment of an ambiguity until inconsistency makes the ambiguity visible, then split one concept into two or more.

Candidate topology:

`COARSE/AMBIGUOUS CONCEPT`
`-> DEFAULT USE`
`-> INCONSISTENCY`
`-> MISSING DISTINCTION DISCOVERED`
`-> CONCEPT SPLIT`

This is a strong historical isomorph of current CFE work on representation adequacy.

Candidate law:

> **INCONSISTENCY CAN BE EVIDENCE THAT THE REPRESENTATION ALIASES CONSEQUENCE-DISTINCT CASES.**

Do not overpromote: McCarthy's example is a logical proposal, not proof of a universal cognitive primitive.

## M5. Persistence / frame pressure
Situation Calculus exposes a core problem: after an action, what changes and what remains true?

The useful stripped primitive is not the syntax `result(...)`.

It is:

> **A state transition needs a qualified persistence policy.**

Reasoning analogue:
- invalidate descendants of a defeated assumption;
- preserve unrelated constraints/evidence;
- explicitly revisit state whose currentness depends on the changed item.

This is nearly identical to the project's scoped rollback/dependency-cone idea at the methodological level.

## M6. Observation is itself a state-changing event
McCarthy & Hayes explicitly distinguish ordinary internal program variables from the world-state variable and treat observation as an action needed to update relevant state.

Stripped invariant:

`OBSERVING != MERELY READING STORED STATE`

An observation can:
- introduce new evidence;
- change knowledge;
- enable an action previously infeasible;
- split viable hypotheses;
- alter currentness.

This matters for ReAct/tool use/LHIT and LBE provenance.

## M7. Ability vs knowledge/feasibility
The 1969 paper separates a strategy that would achieve a goal in the world from a strategy feasible for an agent given what it knows/can do.

Candidate distinction:

`WORLD-POSSIBLE != AGENT-KNOWN-FEASIBLE`

This is important for LBE capability modeling:
- effect known;
- capability available;
- capability authorized/current;
- information needed to invoke capability;
- actual execution feasibility.

## M8. Multi-hypothesis as possible-world partition
McCarthy's treatment of knowledge/non-knowledge is extraordinarily relevant to the current multi-hypothesis seam.

Non-knowledge can be represented by multiple accessible possible worlds still consistent with what the agent knows. Dialogue/evidence changes the accessibility relation over time, eliminating possibilities while preserving others.

Stripped form:

`KNOWLEDGE STATE = CURRENTLY VIABLE POSSIBILITY PARTITION`

and:

`NEW EVIDENCE -> REMOVE/SPLIT/REFINE VIABLE CLASSES`

This is not the same as CFE's target mechanism, but it is a strong historical precursor to:

`SHARED HARD STATE + CONSEQUENCE-DISTINCT LIVE ALTERNATIVES + EVIDENCE-DRIVEN PARTITION REFINEMENT`

Critical difference:
CFE's unresolved problem includes branch-local dependency cones, representation-level hypotheses, consequence-equivalence compression, and on-demand discriminator seeking rather than enumerating a full possible-world universe.

## M9. Knowledge changes with time
The 1990 paper explicitly emphasizes representing how one agent's knowledge changes after hearing another agent's statement, including what remains unknown.

Candidate invariant:

> **EPISTEMIC STATE IS TEMPORAL; NEW INFORMATION CHANGES BOTH KNOWLEDGE AND NON-KNOWLEDGE.**

This is an LHIT-level structure, not merely a static QA relation.

## M10. Context as a first-class object
McCarthy proposes explicit contexts with propositions holding relative to them, relationships between more/less general contexts, and operations for specialization/generalization.

High-value stripped parts:
- context carries presuppositions;
- there is no maximally general context;
- the same surface proposition may require different explicit structure in different contexts;
- facts can move between related contexts only under qualified rules;
- entering/leaving a context changes what assumptions are active;
- context transitions can encode temporal implications.

Candidate LBE law:

`PROPOSITION IDENTITY != CONTEXT-INDEPENDENT AUTHORITY`

## M11. Transcending the current context / representation
McCarthy's context work explicitly says a system may need to transcend its current outer context when a new dependency invalidates an earlier limited theory (e.g. adding temperature to a pressure-volume relation).

This is much closer to the current representation-adequacy problem than ordinary situation calculus.

Candidate topology:

`CURRENT CONTEXT ADEQUATE LOCALLY`
`-> NEW DEPENDENCY DISCOVERED`
`-> CURRENT CONTEXT CANNOT EXPRESS/GENERALIZE IT`
`-> TRANSCEND/SPECIALIZE/GENERALIZE CONTEXT`
`-> RE-DERIVE`

CFE translation:

`UNEXPLAINED RESIDUAL -> MISSING-DISTINCTION / COORDINATE AUDIT`

## M12. Epistemological adequacy often requires partial theories
McCarthy's 1990 paper explicitly argues that an adequate formalism may have to represent incomplete/partial knowledge; only some states support prediction, and undefined regions are not necessarily errors.

Candidate law:

`PARTIAL MODEL != BROKEN MODEL`
`UNDEFINED REGION != NEGATIVE RESULT`
`EPISTEMIC ADEQUACY CAN REQUIRE EXPLICIT INCOMPLETENESS`

This resonates directly with:
`UNKNOWN_CELL != NEGATIVE_CELL`

and with CFE's requirement to preserve unresolved seams.

## M13. Meta-epistemology
McCarthy proposes studying mathematically the relation among:
- the world;
- languages used to describe it;
- what assertions are considered meaningful;
- rules of evidence;
- what a knowledge seeker can discover.

That is extremely close to an LBE/CFE meta-layer.

Stripped research question:

> **Given a world, representation, observation channel, and admissible evidence rules, what distinctions are discoverable at all?**

This adds an important axis beyond "can the model reason?":

`DISCOVERABILITY DEPENDS ON WORLD x REPRESENTATION x EVIDENCE CHANNEL x INFERENCE RULES`

## M14. Tentative concepts may be worth retaining before verification
McCarthy argues that a knowledge seeker should be able to form concepts only tenuously linked to existing language/observation and keep them under investigation rather than either discarding them or claiming certainty.

Candidate invariant:

`WEAKLY GROUNDED HYPOTHESIS != USELESS`
`WEAKLY GROUNDED HYPOTHESIS != TRUE`

This is the exact multi-hypothesis qualification problem:
- retain speculative branch;
- mark low authority;
- seek a discriminator;
- do not promote by fluency.

## M15. Rich vs poor entities
McCarthy distinguishes open-ended real/world entities from limited plan/model entities and explicitly frames their relation as analogous to world vs formal model.

High-value translation:

`WORLD ENTITY != CURRENT MODEL OF ENTITY`

A poor model can be useful because it preserves the distinctions needed for the current purpose while omitting enormous detail.

This is deeply relevant to:
- representation compression;
- consequence aliasing;
- LBE views vs underlying field/source;
- multi-hypothesis equivalence classes;
- task-relative sufficient distinctions.

Candidate law:

> **A compressed representation is qualified by the consequences it preserves, not by how completely it mirrors the world.**

## M16. Control of reasoning is a separate problem from representation
McCarthy repeatedly notes that unrestricted logical inference can generate many useless conclusions and that controlling inference is a major unsolved practical issue.

Historical significance:

`REPRESENTATION ADEQUACY != CONTROL ADEQUACY`

This is a direct precursor to modern test-time compute allocation, search control, pruning, verifier-guided reasoning, and CFE's "appropriate recruitment of cognitive effort."

## M17. Mental Situation Calculus: inference as action
The later Mental Situation Calculus explicitly treats inferring, observing, setting goals, and discharging goals as mental events, and notes that tentative/nonmonotonic inference may need control sensitive to the pedigree of beliefs.

Stripped invariants:

`INFERENCE CAN CHANGE EPISTEMIC STATE`
`BELIEF CONTENT != BELIEF PEDIGREE`
`AUTHORITY/LINEAGE CAN MATTER TO REVISION`

This is highly LBE-compatible.

---

# LBE translation

## Candidate entities
- `SITUATION`
- `OBSERVATION`
- `ACTION`
- `STRATEGY`
- `GOAL`
- `BELIEF`
- `HYPOTHESIS`
- `POSSIBLE_WORLD_CLASS`
- `CONTEXT`
- `PRESUPPOSITION`
- `DEFAULT`
- `ABNORMALITY/EXCEPTION`
- `REPRESENTATION`
- `RICH_ENTITY`
- `POOR_MODEL`
- `EVIDENCE_RULE`
- `INFERENCE_RULE`
- `UNKNOWN`

These are curator/LBE entities, not learner ontology.

## Candidate typed relations
- `RESULTS_IN`
- `OBSERVES`
- `CHANGES_KNOWLEDGE_OF`
- `PERSISTS_UNLESS_DEFEATED`
- `WITHDRAWS_DEFAULT`
- `DEPENDS_ON`
- `HAS_PEDIGREE`
- `HOLDS_IN_CONTEXT`
- `SPECIALIZES_CONTEXT`
- `GENERALIZES_CONTEXT`
- `TRANSCENDS_CONTEXT`
- `ACCESSIBLE_POSSIBILITY`
- `ELIMINATES_POSSIBILITY`
- `SPLITS_CONCEPT`
- `ALIASES`
- `DISTINGUISHES`
- `EPISTEMICALLY_ADEQUATE_FOR`
- `HEURISTICALLY_ADEQUATE_FOR`
- `METAPHYSICALLY_ADEQUATE_FOR`
- `COMPRESSES_RICH_ENTITY_TO`
- `PRESERVES_RELEVANT_CONSEQUENCE`
- `FAILS_OUTSIDE_SCOPE`

## Important LBE separation

`FIELD != MAP != VIEW != SOURCE`

McCarthy's rich/poor distinction strengthens this:

`RICH WORLD/ENTITY != POOR TASK MODEL/VIEW`

A view can be useful without exhausting the object, but only if omitted distinctions do not alter the current relevant consequence.

---

# Historical reasoning-trajectory implications

## 1969: state/action + adequacy separation
Not merely "state transformation." The paper already distinguishes whether a representation can describe reality, express actually available knowledge, and express useful reasoning processes.

## 1980s: revision/control become first-class
Nonmonotonic reasoning and Mental Situation Calculus make tentative conclusions, belief pedigree, and inference control explicit research objects.

## 1989/1990: representation failure and open-ended epistemology
The logical-AI program now explicitly contains:
- concept splitting after inconsistency;
- partial theories;
- unknown relevance;
- temporal knowledge change;
- context as rich object;
- meta-epistemology;
- rich vs poor entity/model distinction.

## 1993+: context transcendence
Representation/context is no longer merely a fixed box; a reasoning system may need to move outside the assumptions of its current context and relate multiple contexts.

## Modern recurrence
Modern frontier traces may re-embody some of these functions in generated language:
- default assumption;
- contradiction;
- local revision;
- alternative branch;
- representation refinement;
- context/currentness shift;
- empirical verification.

But:

`FUNCTIONAL RECURRENCE != SAME IMPLEMENTATION`

---

# Multi-hypothesis implications

McCarthy adds three pieces to the current unresolved CFE mechanism:

### 1. Explicit non-knowledge
Do not represent uncertainty only as low scalar confidence. Preserve alternative viable possibilities.

### 2. Temporal partition refinement
New evidence can remove possibilities and change what remains unknown.

### 3. Context-relative possibility
What is viable/true/meaningful may depend on the active context and its presuppositions.

CFE extension still needed:
- branch-local dependency cones;
- consequence-equivalence compression;
- dynamic split/merge;
- discriminator selection;
- representation-level hypotheses;
- local rollback;
- authority/currentness lineage;
- bounded materialization.

The promising abstract object remains:

`LIVE PARTITION OF CONSEQUENCE-DISTINCT POSSIBILITIES`

with:

`EVIDENCE -> SPLIT / MERGE / ELIMINATE / REFINE / REQUALIFY`

---

# Dataset implications

The Standard Uplift Dataset can exploit these invariants without teaching McCarthy vocabulary.

High-value episode structures:

### Default -> exception -> withdrawal
A reasonable default works until new evidence makes it stale.

### Ambiguity -> contradiction -> concept split
Two cases initially look identical; later consequences force a finer distinction.

### Partial model -> boundary -> UNKNOWN
The learner should recognize when its model does not cover the encountered regime rather than fabricate an answer.

### Multi-hypothesis -> new observation -> partition refinement
Evidence should eliminate or split possibilities while leaving unresolved alternatives alive.

### Context-local truth -> context change -> qualification revision
A conclusion valid under one assumption set should not silently migrate into another.

### Rich world -> poor plan -> execution surprise
A compressed plan/model is useful but later reality exposes omitted state that becomes relevant.

### Tenuous concept -> discriminator -> qualification
Allow a speculative explanatory concept to remain provisional until an observation connects or defeats it.

These should be engineered through consequences, not explained as labels.

---

# Strongest cross-era candidate invariants

1. **Adequacy is task/evidence/control relative.**
2. **New evidence may require withdrawing previous conclusions.**
3. **Uncertainty is structural: preserve live alternatives and explicit non-knowledge.**
4. **Contradiction may reveal a missing distinction rather than only a wrong value.**
5. **State transition requires both change propagation and qualified persistence.**
6. **Observation changes epistemic state and may change feasible action.**
7. **Context/presuppositions are part of a proposition's operational meaning/currentness.**
8. **Representations can be partial and still adequate; undefined regions should remain explicit.**
9. **World/entity richness exceeds any current task model.**
10. **Reasoning-control adequacy is separate from representational adequacy.**
11. **Hypotheses may be retained at low authority while awaiting discriminating evidence.**
12. **Belief/evidence pedigree matters to later revision.**

---

# Claim ceiling

Verified historical content:
- McCarthy/McCarthy-Hayes explicitly formalized situations/actions, epistemological adequacy, knowledge change, nonmonotonic reasoning, contexts, partial theories, and rich/poor entities.
- McCarthy's 1990 text explicitly describes ambiguity discovery followed by concept splitting under inconsistency.
- The 1969 paper explicitly distinguishes epistemological and tentative heuristic adequacy.

Inferred methodological isomorphisms:
- dependency-local rollback;
- representation-refinement correspondence;
- multi-hypothesis partition correspondence;
- CFE currentness/LHIT correspondence;
- LBE rich-field/poor-view correspondence.

Rejected overclaims:
- next-token generation literally implements Situation Calculus;
- visible stress markers prove entropy spikes;
- checkmarks are literal PRM anchors;
- frontier traces are literal MCTS execution logs;
- McCarthy already had CFE.

The value of the lineage is not that modern reasoning "is Situation Calculus." The value is that many of the hard problems modern reasoning exposes were already separated into cleaner conceptual failure surfaces decades ago, giving the archaeology program a much stronger coordinate system for tracing recurrence and re-embodiment.
