# Task 02: Representative-agent growth by time iteration

Builds on the existing `econlab` package from Task 01; add to it without changing the
McCall code. Follow [AGENTS.md](../AGENTS.md).

## Read

- Model: [representative agent](../notes/models/representative_agent.md)
- Algorithm: [time iteration](../notes/algorithms/time_iteration.md), Section 1 and
  the accuracy and contract sections

## Build

- `src/econlab/representative_agent.py`: primitives, baseline configuration, budget,
  prices and steady state.
- `src/econlab/time_iteration.py`: policy interpolation, bracketed root finding and
  the policy update, with no model-specific constants.
- `src/econlab/run_growth.py`, run as `python -m econlab.run_growth`: solve the
  baseline, simulate the two paths requested in the model note, then rerun with the
  note's denser grid and with a wider interval. Save policies, consumption, simulated
  paths and a JSON record of configuration and diagnostics under `results/growth/`.

## Verify

Add tests under `tests/` for:

- the full-depreciation closed-form policy, as a separate test case with its own
  configuration; never compare the baseline with it;
- positive consumption and Euler errors on grid nodes and interval midpoints;
- the baseline steady state: the policy reproduces it and both simulations approach it;
- a clear failure on an unbracketed root and on the iteration cap.

## Report

Maximum Euler errors on and off the grid, policy differences across the three runs on
their common interior domain, and runtimes. Report solver convergence and
approximation accuracy separately, and state the remaining numerical limitations.
