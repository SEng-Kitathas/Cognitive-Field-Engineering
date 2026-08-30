# Active Doctrine — 1991-ish Plain-Language Engineering Prose

Date adopted: 2026-08-29
Scope: CFE workstream prose, code comments, engineering notes, reports, campaign synthesis, operator-facing explanations, and future continuity artifacts unless a narrower format requires otherwise.
Authority source: explicit operator directive in the active CFE thread.
Status: ACTIVE

## Compact rule

> Plain language around the mechanism, proper language for the mechanism.

> Mechanism first. Precision second. Style third. Vocabulary never gets to compete with understanding.

## Operating rule

- General prose should target ordinary educated English, roughly a 1991-era 9th/10th-grade vocabulary level.
- Keep the hard thinking in the engineering. Do not make the reader spend attention decoding ornamental vocabulary that should be spent on mechanisms, evidence, code, tests, or decisions.
- Use specialized terms when they carry a real technical distinction. Terms such as `invariant`, `provenance`, `extensional`, `epistemic`, and `idempotent` are allowed when they are the correct compact name for the mechanism or distinction.
- Do not replace useful technical vocabulary with baby talk.
- A rarer, more academic, or consulting-style synonym is not better merely because it sounds more precise.
- Explain the mechanism plainly before leaning on the formal term when the term may be unfamiliar.
- Prefer the shortest accurate path to the point.
- Remove academic fog, padding, ornate transitions, euphemism, and abstraction that hides a simple causal statement.
- If prose becomes ornate, inaccessible, or sounds like academic camouflage, rewrite it into the plainest accurate form that preserves the real idea.
- Real complexity may remain complex. The prose must not add a second artificial layer of difficulty.

## Priority order

1. Mechanism
2. Precision
3. Style

Vocabulary is subordinate to understanding.

## Non-goals

This doctrine does NOT mean:
- simple words only;
- removal of real engineering terminology;
- lowering technical depth;
- deleting distinctions for readability;
- writing as though the calendar year were literally 1991.

The target is plain general language wrapped around exact engineering language.

## Enforcement test

Before admitting prose, ask:
1. Can the reader see what the mechanism does without decoding decorative wording?
2. Does each specialized term pay rent by preserving a real distinction or shortening a real explanation?
3. Could any sentence be made plainer without losing technical truth?
4. Is difficulty coming from the mechanism itself, or from the writing?

If difficulty comes from the writing, rewrite it.
