# V11 Input-Lock Portability Scar — 2026-08-30

## Status
Verified portability defect in reproduction surface; no scientific result defect and no rewrite of the sealed pre-runtime lock.

## Observed
- Original lock: `state/locks/V11_PREDICATE_POLICY_INPUT_LOCK_2026-08-30.json`
- Locked files: 27
- Git blob exact matches to sealed bytes: 19
- Git blob line-ending-only mismatches: 8
- `.gitattributes` explicitly declares LF for `*.md`, `*.json`, `*.jsonl`, and `*.py`.
- The eight mismatches are CRLF-to-LF only. No semantic/content drift was found in this comparison.

## Failure class
The pre-runtime lock correctly identifies the bytes used on the original Windows host, but a fresh Git checkout follows the repository's LF normalization policy. Therefore a clone can be scientifically content-equivalent while failing raw sealed-byte identity.

`LOCKED_BYTES != CHECKED_OUT_BYTES`
`NORMALIZED_EQUIVALENCE != SEALED_BYTE_IDENTITY`
`PORTABLE_GATE != WEAKER_GATE`
`SEALED_ENVIRONMENT != REPRODUCED_ENVIRONMENT`

## Append-only correction
The sealed v11 lock and its original byte-strict verifier are unchanged.

A portability sidecar records both the original sealed identity and the expected Git LF checkout identity. `tools/verify_v11_input_lock_portability.py` supports two explicit assurance modes:

- `--assurance exact`: requires the original sealed bytes; normalized checkout is a failure.
- `--assurance checkout-equivalent`: accepts only the exact LF checkout identities recorded by the sidecar and reports that this is **not sealed-byte identity**.

This prevents portability repair from silently weakening the scientific gate.
