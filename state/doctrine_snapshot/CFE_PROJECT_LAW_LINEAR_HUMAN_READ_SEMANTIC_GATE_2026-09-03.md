# CFE Project Law — Linear Human Read / Semantic Gate (LHRSG)

Activated: 2026-09-03
Status: **ACTIVE PROJECT LAW**
Authority: explicit operator directive — “The Linear Human Read/Semantic Gate should be a project law — if it can be read, it gets Linear Human Read/Semantic Gate.”

## Core law

> **IF IT CAN BE MEANINGFULLY READ, IT SHALL RECEIVE A COMPLETE LINEAR HUMAN READ / SEMANTIC GATE BEFORE ITS SEMANTIC CONTENT MAY BE USED, ADMITTED, EXECUTED AS AUTHORITY, PROMOTED, SEALED, PUBLISHED, OR TREATED AS LOAD-BEARING.**

Compact form:

`READABLE -> LINEAR READ -> SEMANTIC GATE -> ONLY THEN SEMANTIC USE / LOAD-BEARING`

`AUTOMATED PASS != SEMANTIC PASS`

`SAMPLING != LINEAR READ`

`SEARCH HIT != SOURCE READ`

`STRUCTURAL VALIDITY != SEMANTIC VALIDITY`

`POST-MUTATION ARTIFACT != PRE-MUTATION READ`

## Scope

Every readable artifact that enters active CFE use SHALL receive LHRSG before its semantic content is relied upon.

Raw material MAY be stored, copied, hashed, indexed, registered, or preserved before LHRSG completion. Those operations do not authorize semantic reliance.

This law applies, as applicable, to:
- Markdown, plaintext, specifications, reports, research notes, doctrine, prompts, and documentation;
- source code, scripts, configuration, shell commands, patches, build files, and readable execution bundles;
- JSON, JSONL, CSV, YAML, TOML, XML, manifests, ledgers, registries, tables, datasets, eval packets, and training records;
- readable logs, traces, stdout/stderr, receipts, experiment reports, and diagnostic outputs when used as evidence;
- PDFs, rendered pages, slides, images, diagrams, or other visual artifacts when they can be semantically inspected;
- readable members extracted from archives or containers;
- generated artifacts before admission, execution authority, promotion, sealing, publication, or canonicalization.

Specific hard applications:
- **learner-visible training bodies:** every readable learner-visible row/record SHALL receive LHRSG before training authorization;
- **evaluation packets:** every readable eval item/scenario SHALL receive LHRSG before the eval is frozen as a scientific ruler;
- **source/code bundles:** every readable source/config/build file in the promoted or execution-authoritative bundle SHALL receive LHRSG;
- **reports/specifications/doctrine:** the complete readable artifact SHALL receive LHRSG before it becomes load-bearing.

There is no exemption because records appear repetitive, templated, machine-generated, structurally valid, previously similar, or numerous.

## Why this law exists

CFE repeatedly encounters failure modes that automated checks cannot reliably detect: semantically ambiguous items, logically wrong but schema-valid records, duplicated meaning under unique IDs, answer-channel shortcuts, stale references, misleading labels, contradictory prose, malformed experimental contracts, and artifacts whose bytes are internally consistent but whose meaning is wrong.

The 2026-09-03 ISD evaluation repair supplied a direct evidence scar: V2R3 passed generator gates and an independent hostile verifier, but a complete linear semantic read of all 96 scenarios still found three ambiguous General-Constraint items. The artifact was rejected and rebuilt as V2R4. Automated verification was necessary but not sufficient.

## What “linear read” means

A compliant linear read SHALL:
1. begin at the first readable content unit;
2. proceed in deterministic artifact order to the final readable content unit;
3. inspect every readable unit — no sampling, representative-only review, random subset, search-only review, summary substitution, or silent skipping;
4. preserve local context across boundaries so meaning is not judged as isolated fragments;
5. record any unreadable, truncated, corrupted, inaccessible, or intentionally skipped span explicitly;
6. fail closed for semantic use/promotion when full readable coverage was required but not achieved.

For line-oriented or record-oriented data, every line/record SHALL be included in the pass.
For page-oriented material, every page SHALL be inspected.
For ordered archive members, every readable member SHALL be inspected in deterministic member order.
For source trees or packages being promoted as a unit, every readable file in the promoted unit SHALL be inspected in deterministic path/package order.

`CHUNKING FOR PRACTICALITY != SAMPLING`

A large artifact MAY be read in consecutive bounded chunks, but coverage must still reach 100%, with deterministic ordering and restart position preserved.

If the artifact is too large to finish in the current interval, the correct state is not “good enough.” It is:

`LHRSG_INCOMPLETE__NOT_SEMANTICALLY_AUTHORIZED`

## What “semantic gate” means

The reviewer SHALL do more than confirm readability. The pass SHALL actively pressure meaning for, as applicable:
- ambiguity or multiple valid interpretations;
- contradiction within the artifact or against controlling doctrine/contract;
- wrong answer, wrong target, wrong label, wrong dependency, or wrong causal statement;
- duplicated semantic scenarios hidden behind unique IDs or superficial wording changes;
- shortcut surfaces, answer-position/token bias, leakage, cueing, or unintended isomorphs;
- stale paths, stale versions, stale hashes, stale authority references, or impossible read order;
- unsupported promotion language or inference presented as verification;
- control-plane material leaking into learner-visible training bodies;
- malformed examples, nonsensical tasks, incomplete instructions, unreachable conditions, or impossible constraints;
- code whose logic contradicts its stated contract despite passing syntax/static checks;
- data whose schema is valid but whose content is semantically defective;
- hidden category errors, unit mismatches, temporal mistakes, role/authority mistakes, or representation inadequacy;
- internal inconsistency between prose, code, manifest, verifier, and claimed result.

The gate is not satisfied by “looks reasonable.” Defects SHALL be recorded and dispositioned.

## Reviewer meaning

“Human Read” names the mode of inspection: a full semantic, context-aware read rather than a machine-only structural scan.

The pass MAY be performed by:
- the operator;
- the active reasoning model acting explicitly as semantic reviewer;
- both jointly;
- another explicitly identified reviewer.

Reviewer identity SHALL be recorded honestly. A model-performed pass SHALL NOT be mislabeled as operator-human attestation.

A stronger independent second review MAY be required by a more specific experiment, release, safety, or publication contract. LHRSG is the minimum CFE-wide readable-artifact gate, not a ceiling on review.

## Automation relationship

Automation SHALL be used aggressively to support LHRSG where useful:
- hashes and manifests;
- schema validation;
- duplicate/near-duplicate search;
- static analysis;
- tests and hostile mutations;
- contamination scanners;
- diffing;
- invariant checks;
- tokenization/render checks;
- indexing/navigation;
- chunk accounting.

But:

> **AUTOMATION MAY FIND WHERE TO LOOK HARDER; IT MAY NOT DECLARE SEMANTIC COMPLETION FOR A READABLE ARTIFACT.**

No automated PASS substitutes for the complete linear semantic pass.

## Mutation invalidation rule

LHRSG binds to exact bytes/content identity.

If a readable artifact changes after its gate:
- the prior gate receipt no longer covers the changed artifact;
- the new exact artifact SHALL be read again before semantic use/promotion;
- reading only changed lines is insufficient for final promotion because a local edit may alter global meaning or dependencies.

`ANY POST-GATE SEMANTIC MUTATION -> FULL LHRSG REPLAY BEFORE SEMANTIC AUTHORITY`

Mechanical container changes that provably do not change readable member bytes MAY reuse member-level LHRSG receipts if exact member hashes are unchanged and container/member mapping is independently verified.

## Opaque / binary boundary

An artifact that cannot be meaningfully read as semantic content does not receive a fake “human read.” It SHALL receive the strongest appropriate structural/runtime/integrity verification instead.

Examples include model-weight tensors, compiled binaries, opaque caches, and compressed container bytes.

However:
- readable metadata, manifests, headers, disassembly, extracted members, rendered representations, or source corresponding to the opaque object are independently subject to LHRSG when their meaning is used;
- `OPAQUE BINARY != EXEMPTION FOR READABLE CONTENT INSIDE A CONTAINER`.

## Promotion / admission / execution gate

A readable artifact SHALL NOT be treated as any of the following unless LHRSG has passed on the exact relevant bytes/content:
- semantically admitted evidence;
- execution-authoritative specification or code bundle;
- canonical;
- sealed;
- final;
- promoted;
- admitted training/eval material;
- training-authorized;
- publication-ready;
- load-bearing;
- authoritative evidence;
- verified semantic packet.

If complete reading is impractical, expensive, or unfinished, the correct state is:

`LHRSG_INCOMPLETE__NOT_PROMOTABLE`

Time pressure, artifact size, prior reputation, automated PASS, or apparent triviality/repetition SHALL NOT waive coverage at a semantic-authority boundary.

## Receipt requirement

Each consequential LHRSG SHOULD emit or update a receipt containing at minimum:
- artifact path/logical identity;
- exact SHA-256 or equivalent immutable content identity;
- bytes and, where meaningful, line/row/page/file counts;
- reviewer identity/type (`OPERATOR`, `MODEL_REVIEWER`, `JOINT`, or another explicit label);
- deterministic read order;
- coverage count and explicit confirmation of 100% readable coverage;
- unreadable/excluded spans, if any;
- defects found;
- defect dispositions;
- final PASS/FAIL/INCOMPLETE state;
- timestamp;
- whether mutation occurred after the pass.

A receipt without actual complete reading is false compliance and SHALL be treated as a defect.

## Relationship to PDVER and R4.1

LHRSG is a CFE-local specialization of the adopted Rahl Engineering R4.1 process authority, especially Evidence-before-Inference, Verify, hostile engineering, and post-embodiment readback.

For readable artifacts in CFE:

`PROBE -> DERIVE -> VERIFY -> EMBODY -> LHRSG ON FINAL READABLE EMBODIMENT -> RECURSE`

Preliminary reads MAY occur earlier. Final semantic authority requires LHRSG on the exact post-mutation artifact.

This project law is stricter than generic proportionality at the semantic-authority boundary: proportionality may change support machinery and review depth, but not complete readable coverage.

## Relationship to continuity

This law is load-bearing project doctrine and SHALL appear in:
- active doctrine snapshot;
- current state;
- next-step/promotion gates where relevant;
- trace matrix;
- revisit ledger when incomplete gates exist;
- Live Shadow;
- Design Thread Stream.

## Anti-ritual clause

LHRSG exists to catch semantic failure, not to generate paperwork theater.

A valid receipt bound to an unchanged exact artifact MAY be reused when the same unchanged artifact is relied upon again. Re-reading unchanged exact bytes merely for ceremony is not required unless a new review contract demands it.

Do not print the entire artifact into chat merely to prove it was read. Perform the read locally/server-side when possible and return only receipts, defects, and load-bearing conclusions.

`FULL READ != FULL CHAT DUMP`

## Evidence scar

The V2R3 ISD eval incident is the founding scar for this law:
1. structural generator gates passed;
2. independent verifier passed;
3. hostile suite passed;
4. complete linear semantic read still found three ambiguous items;
5. V2R3 was rejected;
6. V2R4 was rebuilt and reverified.

Therefore:

> **A machine-verifiable artifact can still be semantically wrong. If it can be read, read all of it before trusting it.**
