# CFE Negative-Space Intervention Lattice

Status: ACTIVE RESEARCH MAP — NOT DOCTRINE

## Core move

Treat the CFE search space as a finite lattice over **high-level developmental-field interventions**, not over raw examples. We have already occupied enough cells to infer boundaries and prioritize adjacent holes.

## Axes
- **support_resolution**: NARROW_SLICE | IDENTIFYING_BASIS | COVERAGE_EXPLICIT
- **local_contrast_geometry**: HOMOGENEOUS_OR_DISPERSED | IDENTIFYING_COVISIBLE | TYPED_RELATION_COVISIBLE
- **temporal_topology**: SINGLE_PASS_FIXED_DOSE | EXTENDED_HORIZON | STRUCTURED_REVISIT_CURRENTNESS
- **connectivity**: LOCAL_ONLY | SPARSE_LONG_RANGE_BRIDGES
- **task_closure**: DIRECT_PRIMITIVE | COMPOSITION_TRANSFER | CROSS_LEVEL_EFFECT_TRANSFER
- **optimizer_window_topology**: MIXED | SEPARATED_OR_CONTROLLED

Full coarse lattice: **324 cells**. Occupied characterized cells: **6**. One-axis neighbors currently unoccupied: **43**.

## Occupied shape
### V10_NEIGHBORHOOD — OCCUPIED_MIXED
- Coordinates: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "IDENTIFYING_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "NARROW_SLICE", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "SINGLE_PASS_FIXED_DOSE"}`
- Earned: Learner-visible arrangement can cause large relation-family-specific phenotype changes; no general neighborhood advantage.
### V11_SUPPORT_BASIS — OCCUPIED_POSITIVE_CONDITIONAL
- Coordinates: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "HOMOGENEOUS_OR_DISPERSED", "optimizer_window_topology": "MIXED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "SINGLE_PASS_FIXED_DOSE"}`
- Earned: Broader identifying support materially changes and usually improves held-out predicate behavior, especially outside original support; not clean strict-inequality recovery.
### V12_COMPOSITION — OCCUPIED_NEGATIVE
- Coordinates: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "HOMOGENEOUS_OR_DISPERSED", "optimizer_window_topology": "MIXED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "COMPOSITION_TRANSFER", "temporal_topology": "SINGLE_PASS_FIXED_DOSE"}`
- Earned: Better primitive predicate acquisition did not transfer to zero-shot composition.
### V13_OPTIMIZER_WINDOW — OCCUPIED_NEGATIVE
- Coordinates: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "HOMOGENEOUS_OR_DISPERSED", "optimizer_window_topology": "SEPARATED_OR_CONTROLLED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "COMPOSITION_TRANSFER", "temporal_topology": "SINGLE_PASS_FIXED_DOSE"}`
- Earned: Homogeneous gradient-accumulation window separation did not improve predicate competence or composition; simple local optimizer-window interference weakened.
### V14R2_HORIZON — OCCUPIED_POSITIVE_BUT_INSUFFICIENT
- Coordinates: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "HOMOGENEOUS_OR_DISPERSED", "optimizer_window_topology": "MIXED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "EXTENDED_HORIZON"}`
- Earned: Longer exposure reproducibly moves predicate phenotype, but horizon alone fails stable two-sided competence criterion.
### DD1_FIELD_RESOLUTION — ACTIVE_UNRESOLVED
- Coordinates: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "IDENTIFYING_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "EXTENDED_HORIZON"}`
- Earned: No disposition yet; tests same atoms/support/tokens/dose with local identifying contrast co-visibility vs domain-matched homogeneous grouping.

## What the occupied cells already carve out

- **Support resolution matters**, but identifying support alone does not guarantee stable two-sided competence or composition.
- **Dose matters**, but dose alone is insufficient.
- **Optimizer-window separation is not the missing master variable.**
- **Primitive competence does not automatically compose.**
- **Local arrangement is causal**, but sign is conditional; therefore “coherence good” is outside the surviving shape.

The surviving region is therefore not a single-axis ridge. It is an **interaction surface**: support resolution × relation geometry × temporal topology × connectivity × closure demand.

## Highest-value negative-space holes
1. score 7 / occupied-neighbors 2: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "TYPED_RELATION_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "EXTENDED_HORIZON"}`
   - tests RELATIONAL_DISTANCE != RELATIONAL_TYPE
2. score 6 / occupied-neighbors 2: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "HOMOGENEOUS_OR_DISPERSED", "optimizer_window_topology": "MIXED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "STRUCTURED_REVISIT_CURRENTNESS"}`
   - tests developmental currentness/revisit rather than raw dose
3. score 6 / occupied-neighbors 1: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "TYPED_RELATION_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "SINGLE_PASS_FIXED_DOSE"}`
   - tests RELATIONAL_DISTANCE != RELATIONAL_TYPE
4. score 6 / occupied-neighbors 1: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "TYPED_RELATION_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "NARROW_SLICE", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "SINGLE_PASS_FIXED_DOSE"}`
   - tests RELATIONAL_DISTANCE != RELATIONAL_TYPE
5. score 5 / occupied-neighbors 1: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "HOMOGENEOUS_OR_DISPERSED", "optimizer_window_topology": "MIXED", "support_resolution": "COVERAGE_EXPLICIT", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "EXTENDED_HORIZON"}`
   - tests OBSERVED_RELATIONS != FIELD_COVERAGE
6. score 5 / occupied-neighbors 1: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "HOMOGENEOUS_OR_DISPERSED", "optimizer_window_topology": "MIXED", "support_resolution": "COVERAGE_EXPLICIT", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "SINGLE_PASS_FIXED_DOSE"}`
   - tests OBSERVED_RELATIONS != FIELD_COVERAGE
7. score 5 / occupied-neighbors 1: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "IDENTIFYING_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "COVERAGE_EXPLICIT", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "EXTENDED_HORIZON"}`
   - tests OBSERVED_RELATIONS != FIELD_COVERAGE
8. score 5 / occupied-neighbors 1: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "IDENTIFYING_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "COVERAGE_EXPLICIT", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "SINGLE_PASS_FIXED_DOSE"}`
   - tests OBSERVED_RELATIONS != FIELD_COVERAGE
9. score 5 / occupied-neighbors 1: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "IDENTIFYING_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "IDENTIFYING_BASIS", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "STRUCTURED_REVISIT_CURRENTNESS"}`
   - tests developmental currentness/revisit rather than raw dose
10. score 5 / occupied-neighbors 1: `{"connectivity": "LOCAL_ONLY", "local_contrast_geometry": "IDENTIFYING_COVISIBLE", "optimizer_window_topology": "MIXED", "support_resolution": "NARROW_SLICE", "task_closure": "DIRECT_PRIMITIVE", "temporal_topology": "STRUCTURED_REVISIT_CURRENTNESS"}`
   - tests developmental currentness/revisit rather than raw dose

## Shape-finding strategy

1. **Map local derivatives, not random cells.** From a characterized cell, move one axis only.
2. **Use negative results as boundary faces.** A failed cell removes a volume of simplistic explanations.
3. **Do not test interactions until their component axes have at least one characterized local derivative.**
4. **Prefer holes shared by multiple prior results.** They explain more of the existing shape per experiment.
5. **Stop searching raw arrangements.** Compile canonical geometry classes through DD-0 and verify the learner-visible realization.

## Current best whole-shape hypothesis

> CFE is not searching for one universally good arrangement. It is identifying a bounded response surface in which support resolution determines what distinctions are available, local relation geometry determines which distinctions are jointly reachable, temporal/revisit topology determines which basins stabilize or rotate, connectivity determines whether local structure can propagate across developmental distance, and task closure determines whether learned relations remain primitive or become reusable/compositional.

That whole shape is finite enough to map experimentally at the high level. The raw dataset combinatorics live underneath the compiler and do not need to be searched directly.
