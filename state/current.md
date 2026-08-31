# CFE CURRENT STATE

As of: 2026-08-31 16:20 Eastern Daylight Time
Mode: BUILD-COMMIT
Role: R5 Reality Pressure Engine

## Active science
- V14R2 recovery `job-fc69b38e2e96`, PID 32848: RUNNING; 4/6 qualified trajectories in receipt.
- Current qualified seeds: [(2026083111, 'COMPLETE_SALVAGED'), (2026083112, 'COMPLETE_SALVAGED'), (2026083113, 'COMPLETE_TRAIN_SALVAGED_REEVALUATED'), (2026083114, 'COMPLETE_FRESH')].

## DD-0 qualification
First generative field compiler qualification is frozen `QUALIFIED_ENGINEERING_ONLY`.
- structural qualification SHA `5d9b32b4230c8bb367be89635b08781f7bef27f5df4a8cb9055b757c6599cd50`
- token qualification SHA `748ee0487b46b8d33fd90c6442ecaf256bfe5bb28ea9985dd3cb1a4937d70ff7`
- freeze SHA `b8bd8055b4aa29691ef1fd973d47ce056b71296d2c5f9bc15b58f904d720c26f`
- per-event token content: 134 vs 134
- compiled total tokens: 230 vs 230
- compiled streams differ by arrangement, as intended
- target relation co-visibility: 3 vs 0
- curator label leakage: 0
- deterministic replay: PASS

## Claim ceiling
The compiler can create and verify controlled learner-visible arrangement differences under matched event/payload/token accounting. This is not learner evidence.

## Resume point
If V14R2 closes, prioritize scientific closeout. Otherwise extend DD-0 with explicit revisit, coverage, and long-range bridge semantics before DD-1.
