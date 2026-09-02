# CFE Standard Dataset Separation and Informed-Use Law

Activated: 2026-09-02
Status: **ACTIVE PROJECT LAW / DATA AUTHORITY BOUNDARY**

## Operator clarification
The immediate dataset program is **our informed standard post-training dataset**, not the CFE experimental matched-arm pack.

The standard dataset SHALL deliberately use what CFE, LHIT/Capybara, StarMap, hostile engineering, current post-training research, and local-model failures have already taught us **where those lessons survive ordinary engineering scrutiny**. It is therefore intentionally CFE/LHIT-informed, but it is not itself a CFE causal experiment.

## Core separation

`STANDARD UPLIFT DATASET != CFE EXPERIMENTAL PACK`
`CFE-INFORMED CURATION != CFE TREATMENT ARM`
`STEAL INVARIANTS NOT ABSTRACTIONS`
`GOOD DATA + GOOD ORDERING != PROOF OF CFE`
`CFE LESSONS MAY GUIDE STANDARD ENGINEERING WITHOUT CLAIMING CFE CAUSAL CREDIT`

### Standard dataset
Purpose:
- make selected local models substantially better in ordinary use;
- use the strongest freely available modern data we can lawfully and cleanly curate;
- preserve provenance, license, quality, verifier and contamination metadata;
- incorporate useful long-horizon, research, reasoning, coding, tool-use and interaction invariants;
- use conventional post-training practice as the primary engineering frame;
- deliberately embody CFE/LHIT-derived invariants that are already useful as engineering constraints.

The standard dataset SHALL use CFE-informed engineering heuristics where applicable:
- broad identifying support rather than narrow repetitive slices;
- useful contrast rather than homogeneous repetition;
- structured revisit of related capabilities instead of one-and-done exposure;
- coverage balancing across capability/domain/source;
- avoidance of long single-source/single-skill runs;
- explicit provenance, evidence and consequence signals;
- currentness/revision cases where an earlier answer becomes stale after new evidence;
- contradiction and recovery cases;
- isomorph / anti-isomorph contrast where available;
- preservation of meaningful negative space and UNKNOWN rather than forcing a confident answer;
- composition pressure, while respecting the earned scar that clean primitives do not guarantee composition;
- preservation of causally relevant multi-turn history rather than flattening everything into independent one-shot rows.

These are engineering heuristics here, not scientific CFE claims.

### CFE experimental pack
Purpose:
- later test whether developmental geometry adds causal value under matched atoms/dose/evaluator;
- derive matched control/treatment arrangements from a frozen standard atom pool where possible;
- preserve exact atom identity across arms.

The existing `FLEET_UPLIFT_PACK_V2_POLICY_2026-09-02.json` remains an experimental/downstream artifact and SHALL NOT govern construction of the standard dataset.

## Capybara / LHIT clarification
"Our Capybara" in the standard dataset means **strip LHIT/Capybara for useful invariants and apply those invariants more deliberately**, not require a fixed percentage of rows carrying the Capybara name.

Important stripped donor invariants include:
- multi-turn state carry with explicit currentness;
- follow-up consequence tracking;
- revisiting earlier assumptions after state/dependency change;
- delayed-consequence awareness across turns;
- contradiction recovery;
- unresolved-seam preservation and revision triggers;
- capability growth across a trajectory rather than isolated answer quality;
- sustained high-signal conversational continuity;
- question retention over long interaction;
- recovery after an unhelpful branch or mistaken intermediate conclusion;
- explicit distinction between remembered state, newly observed evidence and inferred consequence;
- warm/direct interaction style as a style donor only.

A long conversation is not enough by itself. A useful LHIT example should contain state that matters later, consequences that become visible later, a reason to revise or retain something, or a dependency/path that must stay coherent across turns.

Capybara corpora/models remain useful donors and candidate training material, but their label is not the target ontology.

## Better use of LHIT
The standard dataset SHOULD actively seek or construct qualified long-horizon episodes where:
1. an early turn establishes a state, rule, uncertainty or dependency;
2. later turns introduce new evidence, consequences or changed conditions;
3. the correct later response depends on retaining and updating the earlier state;
4. stale assumptions are explicitly revised when required;
5. unresolved information remains unresolved until evidence arrives;
6. success can be judged from the episode's actual consequence, not merely surface conversational similarity.

Where public data does not supply enough such episodes, candidate synthetic/teacher-generated episodes MAY be created, but only through a separate generation-and-verification pipeline with source prompts, teacher identity, verification evidence and rejection reasons preserved.

## CFE scientific contamination guard
The standard dataset SHALL NOT directly ingest CFE experiment/evaluation atoms that may later be used to test CFE or pre/post phenotype differences. CFE can inform curation rules without donating its scientific test cases to training.

## Build order
1. source registry and license/provenance snapshots;
2. canonical atom schema;
3. raw/source intake quarantine;
4. source-specific normalization;
5. quality/verifier filtering;
6. exact + semantic deduplication;
7. evaluation contamination filtering;
8. capability/behavior coverage audit;
9. CFE/LHIT-informed standard ordering and episode construction;
10. freeze a standard v1 corpus;
11. only after that, derive any CFE matched-arm experimental pack separately.

## Claim ceiling
A model improved on this standard dataset may be called better post-trained under the measured evaluation regime.

It may NOT be called evidence for CFE merely because CFE/LHIT lessons informed the engineering choices.
