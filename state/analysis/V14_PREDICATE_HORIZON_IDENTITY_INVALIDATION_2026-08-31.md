# V1.4 Predicate Horizon — Execution Identity Invalidation

Status: **ORIGINAL V14 IDENTITY INVALIDATED; NO SCIENTIFIC EVALUATION ADMITTED**

The original V14 campaign launched under a valid input lock at 10:02:51 ET. At 10:08:38 ET, while seed3111 training was still running, the locked upstream v1.3 final-disposition file was replaced during later closeout enrichment. The original lock required 2,347 bytes / SHA `526ae885...`; the replacement is 1488 bytes / SHA `48f29fa9c5176c9e7e08c5ecf4ec55758f75902adc26059d592ff7cc93817773`.

Training reached H1/H2/H4 and wrote checkpoints, but before any H1 evaluation the evaluator reverified the lock, detected the drift, and exited fail-closed at 10:26:01 ET.

Therefore:
- no original-V14 H1/H2/H4 result exists;
- seed3111 training artifacts are quarantined and cannot enter aggregate science;
- the verifier behaved correctly;
- the original identity cannot be restored because the exact locked predecessor bytes are not recoverable from project Git or unreachable objects;
- recovery requires a new identity and fresh runtime qualification.

Recovery identity: **V14R1**. Scientific question, frozen prereg, candidate bytes, six preselected seeds, H1/H2/H4 horizons and optimizer settings remain unchanged. Only the extinct parent-artifact identity is bridged by an explicit pre-outcome recovery amendment.
