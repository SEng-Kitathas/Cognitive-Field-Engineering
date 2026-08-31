# V14R Attempt-2 Live Publication Leak Correction

Date: 2026-08-31 14:19 Eastern Daylight Time
Status: CONTROL-PLANE PUBLICATION CORRECTION

During the donor-provenance continuity sync, mutable files under `state/analysis/V14R_PREDICATE_HORIZON_CAMPAIGN_ATTEMPT2_20260831T1730Z/` were accidentally copied into the stable Git publication checkout and committed in `4b6fbd932c957d1b2f0741166fcf5daec3f49492`.

This was a publication-boundary error, not a mutation of the live scientific campaign. The local active campaign directory was not altered by this correction.

Corrective action:
- remove the active attempt-2 subtree from the current Git publication tree;
- preserve the accidental publication in Git history rather than rewrite history;
- record this note append-only;
- continue excluding mutable active campaign roots from stable publication syncs until artifacts seal.

Law reinforced:
`ACTIVE MUTABLE CAMPAIGN != STABLE PUBLICATION SURFACE`
