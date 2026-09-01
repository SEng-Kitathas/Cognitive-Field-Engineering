# CFE Cartography Hostile Constraint Map

Status: ACTIVE FIRST-CLASS COMPANION

The cartography itself is now treated as an engineered object with failure modes. Its job is not merely to organize experiments, but to survive adversarial attempts to make the map lie.

## Core invariants
- `SCIENTIFIC_OCCUPANCY_REQUIRES_ADMITTED_EVIDENCE`
- `UNKNOWN_CELL != NEGATIVE_CELL`
- `ADJACENCY != CONTINUITY`
- `MAP_AXIS != LEARNER_ONTOLOGY`
- `CELL_IDENTITY_REQUIRES_COMPILED_GEOMETRY_SIGNATURE`
- `PHENOTYPE_IS_VECTOR_NOT_SINGLE_SCORE`
- `MULTI_AXIS_MOVE != MAIN_EFFECT`
- `REGIME_SCOPE_IS_PART_OF_CELL_IDENTITY`
- `UNEXPLAINED_SIGN_FLIP_TRIGGERS_MISSING_AXIS_AUDIT`

## Threat model
### T1_AXIS_COLLAPSE
- Risk: Two causally distinct mechanisms are represented as one axis value.
- Failure: False smoothness / wrong adjacency.
- Hostile test: Split-axis sensitivity: re-encode candidate axis into finer values and test whether prior cell distinctions remain invariant.
### T2_AXIS_DUPLICATION
- Risk: Two axes encode the same latent intervention.
- Failure: Fake dimensionality / wasted experiments.
- Hostile test: Dependency audit and intervention equivalence test under matched compiled exposures.
### T3_CURATOR_ONTOLOGY_LEAK
- Risk: Map coordinates are treated as learner-native structure.
- Failure: Explanatory circularity.
- Hostile test: Require learner-payload leakage audit and label-free transfer condition.
### T4_SPARSE_CELL_OVERFIT
- Risk: Whole-shape claims inferred from too few occupied cells.
- Failure: Interpolated fiction.
- Hostile test: Evidence-density tags; prohibit manifold/interpolation claims where local neighbor support is absent.
### T5_EXECUTION_AS_BOUNDARY
- Risk: Runtime failures are mistaken for scientific negative cells.
- Failure: Phantom exclusions.
- Hostile test: Scientific occupancy requires admitted result identity only.
### T6_METRIC_PROJECTION_ERROR
- Risk: One summary metric hides opposing phenotype movement.
- Failure: Wrong cell sign.
- Hostile test: Store vector phenotype: balanced/false/true/transfer/composition/currentness; no scalar-only occupancy.
### T7_INTERACTION_ALIASING
- Risk: A multi-axis change is interpreted as a main effect.
- Failure: Wrong local derivative.
- Hostile test: Experiment-to-cell binding must enumerate all moved axes; >1 move classified interaction.
### T8_IMPLEMENTATION_NON_EQUIVALENCE
- Risk: Same high-level cell has multiple compiled realizations with different learner-visible geometry.
- Failure: Cell identity too coarse.
- Hostile test: Field verifier fingerprints required; cell occupancy stores compiled-geometry signature.
### T9_SCALE_DEPENDENCE
- Risk: Axis effect changes with learner/model/dose regime.
- Failure: Universalization from one scale.
- Hostile test: Every cell keyed by regime scope; cross-regime promotion requires replication.
### T10_PATH_DEPENDENCE
- Risk: Same nominal cell reached through different developmental histories yields different phenotype.
- Failure: Static lattice misses hysteresis.
- Hostile test: Add predecessor/history metadata and later test path-order reversals.
### T11_MISSING_AXIS
- Risk: Observed sign flips arise from an unmodeled variable.
- Failure: Map appears noisy when latent dimension exists.
- Hostile test: Residual sign-flip audit; recurrent unexplained heterogeneity triggers candidate-axis proposal.
### T12_FALSE_CONTINUITY
- Risk: Adjacent cells assumed smoothly related.
- Failure: Topological intuition overstates continuity.
- Hostile test: No interpolation without measured local derivatives; adjacency is experimental convenience, not continuity proof.
### T13_POSITIVE_RESULT_BIAS
- Risk: Ranking favors cells likely to win rather than cells likely to discriminate.
- Failure: Map gets pretty, not informative.
- Hostile test: Rank by expected ambiguity reduction and boundary value, not expected score gain.
### T14_NEGATIVE_SPACE_REIFICATION
- Risk: Unmeasured holes are spoken of as real absent mechanisms.
- Failure: Speculation becomes pseudo-evidence.
- Hostile test: Unmeasured cell status remains UNKNOWN, never NEGATIVE.
### T15_TIME_STALENESS
- Risk: Map lags current evidence.
- Failure: Next experiment chosen from obsolete shape.
- Hostile test: Scientific frontier change invalidates map freshness until reconciled.

## Consequence

The map is not assumed to be Euclidean, smooth, complete, or even correctly factorized. Axes are provisional engineering coordinates. Recurrent residuals, sign flips, path effects, or implementation-sensitive outcomes are evidence that the coordinate system itself needs revision.

The correct target is therefore not merely a lattice of experiments, but a **self-correcting map of constraints, boundaries, and latent dimensions**.
