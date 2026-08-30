# v1.1 Predicate/Policy Preregistration Amendment — Pre-Outcome

Status: **FROZEN BEFORE ANY NEW v1.1 MECHANISM MODEL OUTCOME**

## Amendment
The predicate task SHALL use an opaque learner-visible target key, `condition_z`, rather than the semantic word `overflow`.

Learner-visible predicate prompt form:

`capacity=..., queued=..., incoming=...; classify condition_z; return JSON only {"condition_z":true|false}`

The formula `queued + incoming > capacity`, the word `overflow`, and action-policy language SHALL NOT be supplied in predicate training or predicate primary evaluation prompts.

Curator-side truth remains:

`condition_z := queued + incoming > capacity`

## Reason
This amendment is made before any NF4, narrow-arm, identifying-arm, or policy model outcome under the new mechanism screen has been observed. It removes a pretrained-semantic shortcut: a capable base model may already understand the ordinary word `overflow`, which would make the screen partly a test of instruction following rather than learned boundary identification.

The scientific contrast remains unchanged:
- narrow support `{0,+1,0,+1}`
- identifying support `{-3,0,+1,+3}`
- identical paired capacity/incoming contexts
- identical target balance
- identical sequence/update-field topology

## Baseline admission gates
Before scientific training:
- NF4 predicate-primary strict accuracy MUST be `< 0.85`; if `>= 0.85`, the predicate benchmark is rejected for insufficient learning headroom.
- NF4 policy-primary strict accuracy MAY be high because the policy inputs use semantic action/mode language. If NF4 policy accuracy is `>= 0.90`, POLICY_FACTORIZED training SHALL be skipped as scientifically uninformative and the policy mapping shall be treated as already available in the base for this prompt contract.
- Baseline admission decisions are made before any new trained-arm outcome.

## Laws
- `OPAQUE_TARGET != OPAQUE_MECHANISM`
- `PRETRAINED_SEMANTIC_PRIOR != LEARNED_FIELD_RELATION`
- `PRE_OUTCOME_BENCHMARK_REPAIR != POST_OUTCOME_GOALPOST_MOVE`
