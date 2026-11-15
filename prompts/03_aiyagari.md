# Extend the project to Aiyagari

Read AGENTS.md, notes/models/aiyagari.md, notes/algorithms/time_iteration.md and
notes/algorithms/stationary_equilibrium.md. Complete and verify one stage before
starting the next; preserve the existing McCall and representative-agent checks.

1. Add aiyagari.py for household primitives and firm prices. Extend time_iteration.py
   with the fixed-price household update and borrowing-boundary complementarity.
   Test policy feasibility, boundary inequality and interior Euler errors. Implement
   a grid-action VFI benchmark and compare saving at identical prices.
2. Add distribution.py for the two-neighbor mass transition and invariant distribution.
   Test mass preservation and expected next assets on a hand-computable grid, then
   check stationarity, the productivity marginal and independence from initialization.
3. Add equilibrium.py for bracketed market clearing. Create run_aiyagari.py runnable
   as `python -m econlab.run_aiyagari`. Save parameters, policy, distribution, prices,
   equilibrium capital, residuals and outer history under results/aiyagari/.

Run the baseline and both refinement experiments from the notes. Report household,
distribution, capital-market and goods-market errors separately. Fail visibly on
out-of-grid choices, nonpositive consumption or unconverged inner solves. Never
reuse a policy at new prices without solving the new household problem.

Run all tests, update README.md and write a concise numerical interpretation.
