# CFE NEXT STEPS

Date: 2026-08-29
Current frontier: live v1.0 first causal screen, Stage 1.

## Immediate
1. Complete/read back `state/analysis/V10_BOUNDED_LATENT_DIAGNOSTIC_CAMPAIGN_20260830` (PID 6444 at launch).
2. Require all 13 read-only model evaluations or an explicit failed job receipt; no partial aggregate promotion.
3. Analyze paired seed deltas separately for RULE_EXPLICIT, BOUNDARY_LATENT, FULL_LATENT and support buckets negative/equality/+1/far-overflow.
4. Use the diagnostic to rank basis-under-resolution vs optimizer-field/horizon vs interference; do not call post-hoc results confirmation.
5. Only then decide whether to build a new bounded source basis, an update-field permutation screen, or eventually run the parked K1/K2/K4 candidate.
6. No v1.1 weight mutation before that decision is frozen/preregistered.

## Stage-1 close
Completed:
- execution qualification: PASS, zero failures;
- paired-seed analysis: complete;
- seed-extension decision: `EXTEND_STAGE2_PREREGISTERED`.

Artifact bindings:
- qualification SHA-256 `b36c39dcf64211eff472891e7dc43a7a49fc001bd0acb0e2a6ce6f289ba92772`;
- scientific analysis SHA-256 `67ccb77c5896887f95eef763fa6cc9f432d5373edc4cf6b60f28c50340732a20`;
- decision SHA-256 `799fcb53452f359cdaa5ed04c943f1912b3e92085a581b596fd04e27b949b3ae`;
- preregistration SHA-256 `86290633f34bc24d03532d541c740684e03fb5a6b33c31df821fa47a92696d82`.

## If Stage 2 is triggered
9. Run exactly the frozen Stage-2 order in `SEED_EXTENSION_PREREGISTRATION_V10.json`.
10. Qualify Stage 2 separately and analyze it separately; six-seed summary is secondary.
11. No further adaptive seed extension is allowed.

## Interpretation gate
12. Keep all machine analysis descriptive until a separate hostile causal interpretation attacks:
   - seed consistency;
   - treatment-only vs control-only cases;
   - family/domain concentration;
   - retention damage;
   - residual token/surface cues;
   - training-loss path asymmetry;
   - adapter norm/weight-change asymmetry;
   - any claim beyond the exact local-neighborhood co-visibility screen.

## Recovery tool
Use `tools/resume_v10_first_screen.py` only after the live partial arm closes.
- Without `--execute`: audit only.
- With `--execute`: verify completed steps and run missing frozen steps.
- It refuses partial or corrupt outputs rather than overwriting them.

## Model acquisition rule
Before any future model/weight download, search local drives first and qualify exact identity. The current Argilla base satisfied this rule: C:, D:, E: were searched and no exact pinned revision was found before network acquisition.

## Non-goals
Do not promote from this screen to:
- “CFE works” in general;
- general reasoning improvement;
- internal relational representation;
- external cognitive transfer;
- AI CORE/cognitive archetypes;
- Microseed applicability.


## Git continuity / publication
1. Commit the prepared CFE publication tree.
2. Push to `SEng-Kitathas/Cognitive-Field-Engineering`.
3. Verify remote head equals local commit.
4. Publish heavy reincarnation/R&D ZIPs as opt-in release assets when authenticated GitHub API/CLI access exists; never move them into the normal clone.
5. Thereafter, every material turn must update/push continuity under `policy/PER_TURN_GIT_CONTINUITY_POLICY.md`.
