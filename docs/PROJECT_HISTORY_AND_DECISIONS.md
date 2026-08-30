# Project History and Engineering Decisions

## Ancestral design
Earlier CFE generations established several standards that remain load-bearing:
- `SOURCE_GEOMETRY != COMPILED_EXPOSURE_GEOMETRY != OPTIMIZER_VISIBLE_GEOMETRY != LEARNED_GEOMETRY`.
- `RICH_CONTRAST_SET != IDENTIFYING_CONTRAST_SET`.
- explicit binding and latent relation transfer are distinct evaluation tiers.
- harm is evidence; attack overload, interference, ordering, optimizer dynamics, or flawed neighborhood design rather than rescuing the metric.

## v1.0 first screen
Base: `argilla/CapybaraHermes-2.5-Mistral-7B`, pinned revision `d06c86726aadd8dadb92c5b9b9e3ce8ef246c471`.

Arms:
- `CONTROL_STRICT_CELL_SCRAMBLE`
- `TREATMENT_NEIGHBORHOOD`

72 sequences/arm, 4 cells/sequence, microbatch 1, gradient accumulation 8, 4 epochs, 36 optimizer steps, packing disabled, selected `all_linear_r8` profile.

Stage 1 seeds 2501–2503 produced mixed signs and mechanically triggered the preregistered Stage 2 extension.
Stage 2 seeds 2504–2506 completed and passed integrity qualification.

Structural T-C deltas across six seeds:
`+0.0500, -0.05417, +0.0375, -0.1000, +0.0500, -0.1000`.
Secondary six-seed mean about `-0.01944`; signs 3 positive / 3 negative.

Family-level discordance revealed the important result:
- warrant-vs-taint: +43
- dependency-currentness: 0
- bounded-transport: -71

## Post-screen causal autopsy
The project rejected the framing “CFE is right and only needs dialing in.”

Four live mechanisms were separated:
1. diversity starvation;
2. sibling interference;
3. wrong-neighborhood / wrong identifying basis;
4. optimizer-horizon mismatch.

A machine-readable disposition was frozen: if the mechanism tournament fails to discriminate, disposition is `EVIDENCE_AGAINST_CURRENT_MECHANISTIC_PICTURE`; automatic combination-rescue is forbidden.

## v1.1 candidate history
A K1/K2/K4 neighborhood-concentration candidate was built and passed 670 static hostile checks, exact source/global experience parity, and exact token burden parity.

It remains valuable but was **demoted from immediate next experiment** after cheaper discriminators were identified. No v1.1 scientific training has started.

## Bounded-transport design seam
The exact source audit found treatment neighborhoods fix capacity/incoming and present only margins 0 and +1. Control unintentionally increases local numerical diversity. This makes the original treatment a policy truth-table basis but potentially under-resolved for the arithmetic invariant.

The historical CFE lineage already defined identifying neighborhoods in terms of eliminating rival rules, so this is a theory-to-embodiment gap rather than a new post-hoc philosophy.
