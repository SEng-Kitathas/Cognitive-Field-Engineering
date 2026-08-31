# Sealed Artifact Portability Policy

Status: **ACTIVE PROJECT POLICY**

## Problem

A scientific lock may seal exact source bytes on one host while version-control checkout rules reproduce semantically identical text with different line endings.

Therefore:

- `LOCKED_BYTES != CHECKED_OUT_BYTES` can be true without scientific mutation.
- `SEALED_ARTIFACT != REPRODUCED_ENVIRONMENT`.
- `BYTE_MISMATCH != AUTOMATIC_SCIENCE_DEFECT`.

But normalization must never be used to hide a real mutation.

## Two identities

Every portable text artifact covered by a scientific lock SHOULD have two separately reported identities:

1. **raw identity** — exact bytes and byte count sealed by the original lock;
2. **canonical text identity** — SHA-256 after the declared transport normalization only.

For the current CFE repository, the declared canonical text normalization is:

`CRLF -> LF`

with no other content transformation.

No whitespace trimming, Unicode normalization, JSON reserialization, key sorting, encoding conversion, or semantic parsing is permitted by this portability layer.

## Verification outcomes

A portability verifier SHALL return one of:

- `EXACT_BYTES` — checked-out bytes match the original lock exactly;
- `NORMALIZATION_EQUIVALENT` — raw bytes differ, but canonical text bytes match the companion portability seal;
- `FAIL` — neither identity matches;
- `MISSING` — artifact absent.

## Authority ceiling

`NORMALIZATION_EQUIVALENT` is sufficient only to establish that a fresh checkout is transport-equivalent to the sealed text artifact under the declared newline rule.

It is **not** sufficient to claim that the original scientific execution consumed those normalized checkout bytes.

The original execution remains bound to the original raw lock and runtime receipts.

Therefore:

`REPRODUCTION_PROVENANCE_EQUIVALENCE != ORIGINAL_EXECUTION_AUTHORIZATION`

## Lock preservation

Existing scientific input locks SHALL NOT be rewritten after outcome merely to make a fresh clone verify green.

Instead, create a companion portability seal that binds:

- original lock SHA-256;
- original raw SHA-256 and byte count per file;
- canonical LF SHA-256 and canonical byte count per text file;
- normalization rule;
- verifier implementation identity.

This preserves historical truth while repairing reproducibility.

## Future locks

Future scientific lock schemas SHOULD declare transport form before scientific execution begins.

Preferred pattern:

- raw execution identity;
- canonical repository identity;
- checkout/normalization policy;
- explicit verifier semantics.

A future lock may choose LF as both execution and repository form, but that choice must be made pre-outcome and mechanically verified.

## Governing laws

- `LOCKED_BYTES != CHECKED_OUT_BYTES`
- `SEALED_ARTIFACT != REPRODUCED_ENVIRONMENT`
- `NORMALIZATION_EQUIVALENT != EXACT_BYTES`
- `REPRODUCTION_PROVENANCE_EQUIVALENCE != ORIGINAL_EXECUTION_AUTHORIZATION`
- `CORRECTED_PORTABILITY != REWRITTEN_SCIENTIFIC_HISTORY`
