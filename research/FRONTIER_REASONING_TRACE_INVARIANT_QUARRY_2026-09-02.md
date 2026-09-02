# Frontier Reasoning Trace Invariant Quarry

Date: 2026-09-02
Status: **ACTIVE RESEARCH-ONLY QUARRY / STANDARD-DATASET INFORMANT**
Authority: **NO DIRECT TRAINING ADMISSION FROM PROPRIETARY RECOVERED TRACES**

## Purpose
Use observable/open reasoning traces and published security/reasoning research to identify structural reasoning invariants that may improve the Standard Uplift Dataset v1.

This branch does **not** seek to copy proprietary hidden chain-of-thought. Its job is to compare trace structures, strip away model-specific prose/style, and recover useful behavioral/temporal invariants that can be re-derived into lawful training examples.

## Core law

`STEAL INVARIANTS NOT ABSTRACTIONS`

Applied here:

`REASONING PHRASE != REASONING MECHANISM`
`STYLE CONVERGENCE != MECHANISM CONVERGENCE`
`RECOVERABLE TRACE != TRUSTWORTHY TRACE`
`PUBLICLY POSTED ENCRYPTED BLOCK != CLEAN TRAINING DATA`
`HIDDEN COT EXTRACTION RESEARCH != TRAINING AUTHORIZATION`

## Primary external evidence

### 1. Panfilov et al. 2026 — Stealing Reasoning Traces from Proprietary LLM APIs
Primary source: arXiv:2608.09867.

Verified high-level findings from the paper:
- encrypted reasoning blocks were portable across some models/sessions inside provider ecosystems;
- weaker compatible models could be abused as decoders;
- the authors reconstructed 315,320 blocks from 6,708 public trajectories;
- recovered traces included substantial PII/credential leakage;
- the authors explicitly recommend stripping reasoning/opaque blocks from public logs where secrets/private information may have been exposed;
- short reasoning prefills can shift another model's reasoning/answer style, but the authors characterize these observations as suggestive/inconclusive for memorization or distillation.

### Dataset consequence
The reconstructed proprietary traces are **RESEARCH EVIDENCE ONLY**. They SHALL NOT be imported into Standard Uplift Dataset v1.

Reasons:
1. privacy/credential contamination is demonstrated, not hypothetical;
2. the traces are derived through exploitation of provider security properties;
3. recovered text is a reconstruction surface and not automatically epistemically privileged;
4. using them would collapse the project's provenance/authority discipline;
5. wording/style artifacts could masquerade as reasoning invariants.

The paper itself may inform our trace-analysis taxonomy and privacy filtering.

## Open reasoning quarry

### DeepSeek R1 family
DeepSeek-R1 is an appropriate open reasoning donor because the model/technical report are open and the visible/API reasoning surface is intentionally exposed. DeepSeek documentation separates reasoning content from final answer, and the release states that API outputs may be used for fine-tuning/distillation.

Permitted uses:
- public/open DeepSeek-R1 trace datasets with clear provenance/license;
- locally generated traces from open weights where resource authority permits;
- API outputs only under the provider's current terms and with provenance retained;
- comparison of R1/R1-distill trace structures with other open reasoning models.

### Other open-weight reasoning families
Candidate donors include open Qwen reasoning/thinking models and other open-weight models whose visible trace interface and licenses permit research/training use. Each source must pass the normal source registry and license gates before training admission.

## Trace invariant taxonomy
The analysis SHALL annotate structural events rather than literal phrases.

### R1 — Correction / branch rejection
Evidence that the model recognizes a branch is inconsistent, unproductive, or contradicted and changes course.

Do not key solely on words such as "wait" or "actually". Require a measurable state/approach change.

### R2 — Verification loop
The model independently checks a derived result against constraints, recomputes a sub-result, runs a tool/test, or validates the answer through a distinct route.

`REPETITION != VERIFICATION`

### R3 — Alternative-path search
The model considers more than one plausible route and selects/rejects based on consequence/evidence rather than prose preference.

### R4 — Currentness / revision
New information changes the validity of an earlier premise, plan, authorization, or answer, and the trace updates accordingly.

### R5 — Evidence-state separation
The trace distinguishes direct observation, remembered/input state, inference, uncertainty, and unresolved unknowns.

### R6 — Question retention
The trace preserves the governing objective across locally attractive branches and returns subsidiary work to the original problem.

### R7 — Consequence propagation
An early assumption/action produces later constraints or observations which influence subsequent reasoning.

### R8 — Failed-branch recovery
The trace retains valid accumulated state while backing out only the failed subpath.

### R9 — Composition
The trace combines previously established primitives/relations into a new solution rather than merely restating them.

### R10 — Memorization/shortcut suspicion
Signals include abrupt solution reproduction, unusually low search/revision burden, large contiguous answer/code/proof emission, or benchmark-identical wording.

This label is **SUSPICION ONLY** unless independent contamination/memorization evidence exists.

### R11 — Degenerate reasoning
Repetition loops, performative self-talk, irrelevant branch expansion, style mimicry, excessive trace length without new state, and symbolic churn.

### R12 — Efficient sufficient reasoning
The shortest trace that still preserves the necessary discriminators, evidence transitions, verification, and recovery structure.

## Comparison design
Where legal/open data permits, compare multiple reasoning families on the same or isomorphic tasks.

Preferred task families:
- difficult but decontaminated mathematics;
- algorithmic/code problems with executable verification;
- symbolic/logic tasks with checkable consequences;
- tool-use tasks with visible observations;
- long-horizon state/currentness episodes;
- research tasks where evidence citations can be checked.

### Measurements
Do not treat raw token count as the main metric.
Record:
- solution correctness / verifier outcome;
- trace target-token count;
- number of state-changing reasoning events;
- correction count;
- independent verification count;
- alternative-path count;
- unresolved-unknown handling;
- branch-recovery events;
- tool/evidence-grounding events;
- question-retention failures;
- redundancy / non-state-changing token fraction;
- style fingerprints separately from structural labels.

## Standard dataset translation
The output of this quarry is primarily **selection and construction rules**, not copied trace text.

Examples:
- prefer tasks/episodes that require an actual correction rather than examples containing the phrase "wait";
- prefer verification-bearing math/code traces when verification changes confidence or catches an error;
- preserve tool observations that cause a plan revision;
- generate synthetic LHIT episodes whose later answer genuinely depends on earlier state;
- retain UNKNOWN when evidence is insufficient;
- reject long traces where most tokens do not alter the reasoning state;
- produce bounded reasoning views for Qwen3 rather than automatically supervising every source thought token.

## Privacy / security exclusion
Do not acquire, decode, normalize, store, or train on recovered proprietary hidden-reasoning blocks obtained through security exploits.

If public logs contain opaque/encrypted reasoning fields, treat them as sensitive and strip/quarantine them rather than attempting recovery.

Do not admit secrets, credentials, PII, private tool state, or unreleased provider internals into training or research artifacts.

## Claim ceiling
Open reasoning traces can reveal useful observable reasoning structures.
They do not prove those text structures are faithful descriptions of internal computation, nor that copying their wording teaches the same mechanism.

The project seeks transferable invariants and learner-visible training consequences, not mythology about an LLM's inner monologue.
