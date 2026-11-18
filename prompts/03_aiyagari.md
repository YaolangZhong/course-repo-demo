# Task 03: Aiyagari stationary equilibrium

Builds on Task 02: extend its `time_iteration.py` and start only once
`python -m econlab.run_growth` and its tests pass. Follow [AGENTS.md](../AGENTS.md).

## Read

- Model: [Aiyagari](../notes/models/aiyagari.md)
- Algorithms: [time iteration](../notes/algorithms/time_iteration.md), Section 2 and
  the accuracy section, and
  [stationary equilibrium](../notes/algorithms/stationary_equilibrium.md)

## Build

Work in three stages; finish the Verify items of one stage before starting the next.

1. Household: `src/econlab/aiyagari.py` for household primitives and firm prices;
   the fixed-price household update in `src/econlab/time_iteration.py`; the note's
   coarse-grid VFI benchmark for saving at the same prices, reusing `MDP` and `VFI`.
2. Distribution: `src/econlab/distribution.py` for the two-neighbor transition and
   the stationary distribution.
3. Equilibrium: `src/econlab/equilibrium.py` for bracketed market clearing, and
   `src/econlab/run_aiyagari.py`, run as `python -m econlab.run_aiyagari`. Run the
   baseline and the two refinement runs of the equilibrium note. Save parameters,
   policy, distribution, prices, equilibrium capital, residuals and the outer
   iteration history under `results/aiyagari/`.

## Verify

Add tests under `tests/` for:

1. feasible saving, interior Euler errors and complementarity errors at the borrowing
   limit, on nodes and midpoints; saving against the VFI benchmark;
2. mass preservation and expected next capital on a hand-computable grid, then
   stationarity, the productivity marginal and independence from the initial
   distribution;
3. capital-market clearing with a checked bracket, and the goods-market identity.

## Report

Household, distribution, capital-market and goods-market errors separately; the change
in equilibrium capital, prices and saving across the three runs; any missed target;
and a concise economic interpretation of the numbers.
