# Task 01: McCall job search by VFI, PFI and GPI

The repository already contains this implementation; the prompt is kept as the
reference example of the pattern the later tasks follow. Follow
[AGENTS.md](../AGENTS.md).

## Read

- Model: [McCall job search](../notes/models/mccall.md)
- Algorithm: [VFI, PFI and GPI](../notes/algorithms/finite_mdp.md)

## Build

- `src/econlab/mccall.py`: `McCallModel`, supplying the note's common finite-MDP input.
- `src/econlab/finite_mdp.py`: `VFI`, `PFI` and `GPI`, each with `solve(model)`
  returning the note's result dictionary and independent of the McCall class.
- `src/econlab/run_mccall.py`, run as `python -m econlab.run_mccall`: solve the
  baseline with all three methods, print the accepted wages and each method's
  diagnostics, and save `results/comparison.csv` and `results/diagnostics.json`.

## Verify

Add tests under `tests/` for:

- the acceptance set, which is {4, 5} at the baseline: derive it independently from
  the reservation-wage equation instead of copying one solver's output;
- a feasible policy and a Bellman residual within the note's threshold, per method;
- agreement of values and policies across the three methods;
- one small non-McCall MDP solved by the same classes, to show solver reuse.

## Report

The accepted wages, the per-method diagnostics, and any discrepancy between methods or
with the independent derivation, explained.
