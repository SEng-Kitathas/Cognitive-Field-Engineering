# CFE CURRENT STATE

As of: 2026-08-31 17:01 Eastern Daylight Time
Mode: BUILD-COMMIT
Role: R5 Reality Pressure Engine

## V14R2 — COMPLETE
- Job `job-fc69b38e2e96`: COMPLETED, return code 0.
- Six trajectories qualified. Independent closeout verification 46/46 PASS.
- Receipt SHA `bfea2ab7e2b37bd57ba47487bc0c35368912b7a9b906ec79bdf1d62dbc676489`.
- Aggregate SHA `9fa540f729fe09ce6f0e1fc7ee9d01ce46233327e0125a3e42e837b4aba9601d`.
- Final disposition SHA `e800ed80965ced521339ef85a038655a965d5984b0cd161675cc77a92ad61789`.
- Hostile closeout SHA `3b932cf12e57681ad4495dfcd28411225e0080e882684e8c1a9609cb9cb36b15`.

### Results
- H1 mean balanced accuracy: 0.579861
- H2: 0.708333
- H4: 0.763889
- H2-H1: +0.128472, positive 6/6
- H4-H1: +0.184028, positive 6/6
- H4-H2: +0.055556, positive 4/6
- H4 two-sided >=0.65: 3/6
- H4 overall >=0.75: 3/6

### Mechanical disposition
`DOSE_HORIZON_WEAKENED = true`
`HORIZON_IMPROVES_COMPETENCE = false`
`INTERMEDIATE_HORIZON_OPTIMUM = false`

Exposure matters strongly, but horizon alone does not reliably produce stable two-sided competence.

## DD-0
Tokenizer-aware compiler remains `QUALIFIED_ENGINEERING_ONLY`.

## Resume point
Finish heavy release publication, then open richer predicate-field resolution / learner-interface discrimination. Do not extend V14 beyond H4.
