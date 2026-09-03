# Standard Uplift — Modern Adaptive-Effort Donor Quarry

Status: RESEARCH-ONLY / NON-AUTHORITATIVE DONOR SURFACE

Purpose: pressure the Standard adaptive-effort / value-of-computation hole with modern external research without importing paper vocabulary into learner-visible training data.

## Modern signals surfaced in bounded research

- arXiv:2602.01070v5, *What If We Allocate Test-Time Compute Adaptively?* — proposes verifier-guided adaptive reasoning/tool/compute allocation and reports gains over uniform test-time scaling; relevant donor pattern: allocate compute to high-utility reasoning paths rather than uniformly.
- arXiv:2504.13171v1, *Sleep-time Compute: Beyond Inference Scaling at Test-time* — reports that useful precomputation can reduce later test-time compute and that value depends on query predictability; relevant donor pattern: reasoning effort should depend on expected downstream reuse/value.
- arXiv:2110.09624v1, *Ideal Partition of Resources for Metareasoning* — explicit resource-partition framing between metareasoning/planning and execution; relevant historical-modern bridge.

## CFE translation

The useful transfer is not “teach the model to say value of computation.” It is to construct matched task-world episodes where:

1. another check/search/reasoning step has a real cost;
2. current evidence sometimes already identifies a safe action;
3. in matched near-neighbor cases, ambiguity remains and an additional check can materially change the decision;
4. STOP and CONTINUE are both correct in different states;
5. the learner sees only task-world evidence, cost, action choices, and consequences.

## Guard laws

- EXTERNAL RESEARCH != CFE LAW.
- MODERN PAPER VOCABULARY != TRAINING TARGET.
- LONGER REASONING != BETTER METAREASONING.
- ADAPTIVE EFFORT COVERAGE REQUIRES STOP/CONTINUE ANTI-ISOMORPHS.
- PROJECT GOVERNANCE AND CURATOR PAIR LABELS REMAIN SIDECAR-ONLY.
