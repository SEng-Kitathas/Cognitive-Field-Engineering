# CFE Research Lineage Publication Policy

Status: **ACTIVE PROJECT POLICY**

## Purpose

CFE research must be reconstructable backward as an unbroken chain.

The publication rule is stronger than continuity-only backup:

> **Every research artifact that materially records what was proposed, attempted, executed, observed, rejected, repaired, qualified, or concluded SHALL be published or explicitly manifested to a published heavy-asset surface.**

This includes failed work and superseded work. Scientific history is not cleaned up for presentation.

## Normal Git surface

The normal Git repository SHALL contain, when reasonably small:

- preregistrations and amendments;
- source/candidate data and sidecars;
- token references and audits;
- code used to generate, train, evaluate, qualify, aggregate, or inspect;
- qualification receipts and locks;
- run/evaluation manifests;
- result JSON/JSONL;
- analyses and hostile summaries;
- stdout/stderr logs, including failures and warnings;
- PID/job metadata needed to reconstruct execution chronology;
- abandoned/superseded candidates and failed design attempts;
- decision/disposition ledgers;
- continuity and Design Thread Stream records;
- manifests for every heavy artifact excluded from Git.

A file is not omitted merely because it is ugly, failed, obsolete, or inconvenient.

## Heavy research surface

Files too large or unsuitable for normal Git—model weights, adapters, checkpoints, large archives, model caches—SHALL remain outside the thin clone and be published as immutable/versioned GitHub Release assets or an equivalent explicit archive surface.

Every such artifact SHALL have a Git-tracked manifest containing:

- original project-relative path;
- published asset name or archive member path;
- bytes;
- SHA-256;
- producing run/job identity where available;
- whether it is required for forensic reconstruction, rerun, or only exact weight reproduction;
- publication status and release identity.

`NOT_IN_NORMAL_GIT != NOT_PUBLISHED`

## Active-run rule

For a long-running campaign:

- sealed completed job artifacts SHALL be synchronized to Git on each material turn;
- active logs/receipts may be published as snapshots and updated in later commits;
- completed heavy adapters/checkpoints SHALL be added to a release bundle as soon as practical;
- the active partial job itself is never mutated merely to make publication cleaner;
- later commits/releases extend lineage; they do not rewrite earlier history.

## Failure preservation

Failed runs, failed qualification attempts, broken candidates, serialization failures, wrapper failures, and aborted diagnostics SHALL remain recoverable when they materially influenced later decisions.

`FAILED_ATTEMPT != DISPOSABLE_HISTORY`

## Thin-clone constraint

This policy does **not** repeal the thin-clone rule.

Normal clone/install must not download model weights, adapters, giant reincarnation archives, or other heavy R&D payloads.

The correct split is:

`COMPLETE RESEARCH LINEAGE = GIT EVIDENCE + HASHED HEAVY RELEASE SURFACE`

not:

`COMPLETE RESEARCH LINEAGE = PUT EVERYTHING IN GIT`

## Verification

A research-publication turn is not complete until:

1. project tree and publication tree are compared;
2. every missing non-heavy research artifact is synchronized or explicitly justified;
3. every heavy artifact is represented in a Git manifest;
4. intended heavy assets are uploaded/read back when the source bytes are available;
5. Git commit is pushed;
6. remote HEAD is read back and equals local HEAD;
7. release assets, when uploaded, are read back with matching size/digest.

## Governing rule

> **A future researcher must be able to walk backward from a claim to its analysis, results, run/eval manifests, executable code, locked inputs, preregistration, failed predecessors, and source intent without relying on chat memory.**
