# Bounded Transport Neighborhood Basis Audit — 2026-08-30

Status: **POST-HOC MECHANISM AUDIT; NOT CONFIRMATORY**

## Verified source geometry

The v1.0 `bounded_transport` source neighborhood contains four cells generated as the Cartesian product:

- mode ∈ {`transactional`, `latest_state`}
- overflow ∈ {false, true}

Within one neighborhood, `capacity` and `incoming` are fixed.

The queue is chosen so that:
- no-overflow cell: `queued + incoming - capacity = 0`
- overflow cell: `queued + incoming - capacity = +1`

Therefore each local four-cell treatment neighborhood spans only margins `{0,+1}`. It has no negative-slack example.

Example source neighborhood:
- latest_state, no overflow: capacity 12, incoming 3, queued 9, margin 0 → `accept_all`
- latest_state, overflow: capacity 12, incoming 3, queued 10, margin +1 → `drop_oldest_keep_latest`
- transactional, no overflow: capacity 12, incoming 3, queued 9, margin 0 → `accept_all`
- transactional, overflow: capacity 12, incoming 3, queued 10, margin +1 → `backpressure_or_fail_explicitly`

## Verified local exposure difference

Across the 24 bounded-transport sequences:

### TREATMENT_NEIGHBORHOOD
Per sequence:
- distinct capacities: 1
- distinct incoming values: 1
- distinct queued values: 2
- distinct source neighborhoods: 1
- distinct margins: 2
- mean capacity span: 0
- mean queue span: 1

### CONTROL_STRICT_CELL_SCRAMBLE
Per sequence:
- distinct capacities: 4
- distinct incoming values: 1 in the current offset construction
- distinct queued values: 4
- distinct source neighborhoods: 4
- distinct margins: 2
- mean capacity span: 18
- mean queue span: 18

Thus CONTROL does not merely destroy true-neighborhood co-visibility. For bounded transport it also forces the learner to see the same cell/target roles across substantially different numerical realizations inside one sequence.

## Verified update-field difference

With microbatch 1 and gradient accumulation 8, an optimizer step integrates eight consecutive sequences.

For seed 2026082501, bounded-transport exposures inside an eight-sequence update-field show systematically greater neighborhood/capacity diversity under CONTROL than TREATMENT. Examples:

- window with one bounded sequence: TREATMENT = 1 neighborhood / 1 capacity / span 0; CONTROL = 4 neighborhoods / 4 capacities / span 18.
- window with three bounded sequences: TREATMENT = 3 neighborhoods / 3 capacities / span 9–13; CONTROL = 8–12 neighborhoods / 8–12 capacities / span 23–28.

The global source multiset remains matched, but optimizer-visible local numerical diversity is not.

## Mechanistic interpretation

The original bounded neighborhood is a strong local **policy truth-table** basis but a weak **arithmetic-invariant** basis.

It holds `capacity` and `incoming` fixed even though they are operands in the causal relation:

`overflow := queued + incoming > capacity`

This differs importantly from `warrant_vs_taint`, where a held-constant field such as `review_code` is nuisance/context while the causal axes (`taint`, `independent corroboration`) vary.

Therefore the v1.0 family sign flip may reflect a variable-role error in neighborhood construction:

- holding nuisance context fixed can sharpen causal contrast;
- holding causal operands fixed can starve identification of the invariant across values.

This is stronger and more specific than the generic claim that bounded transport merely needed “more diversity.”

## Hypotheses separated by the next discriminator

### Same-cell rearrangement arm
Use the exact same four original cells but change their serial order / adjacency pattern.

Purpose:
- tests order-sensitive sibling interference while keeping basis constitution fixed.

If rearrangement materially repairs gradient conflict or transfer, `H_INTERFERENCE` gains support and `H_WRONG_NEIGHBORHOOD` is weakened.

### Reconstituted boundary-basis arm
Construct a genuinely different four-cell local basis in which the causal operands vary across cells while preserving the overflow/policy distinction.

Minimum requirement:
- include safe slack below the boundary, not only equality (`margin 0`);
- include overflow above the boundary;
- vary capacity and/or incoming across the four cells;
- preserve both policy modes and target semantics;
- match sequence/token/target burden against the original basis.

Purpose:
- tests whether the original cells themselves were the wrong basis for learning the arithmetic invariant.

If all rearrangements of the original four cells remain harmful but a reconstituted basis repairs transfer, `H_WRONG_NEIGHBORHOOD` gains support over pure sibling interference.

## Important constraint

The current v1.0 source pool cannot instantiate the reconstituted boundary basis cleanly because its non-overflow examples are all exactly at margin 0 and each neighborhood fixes capacity/incoming. A genuine basis test therefore requires a **new source generator / new scientific branch**, not a clever reshuffle of existing four-cell neighborhoods.

Do not present a K4-style cross-neighborhood scramble as the reconstituted-basis arm; that would reintroduce the concentration/diversity confound.

## Scientific ceiling

This audit identifies a concrete design seam. It does not establish that wrong-neighborhood construction caused the -71. The claim remains post-hoc until a preregistered discriminator is run.
