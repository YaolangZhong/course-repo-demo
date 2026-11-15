# Implement representative-agent time iteration

Read AGENTS.md, notes/models/representative_agent.md and
notes/algorithms/time_iteration.md. Reuse the existing package structure.

1. Create representative_agent.py for primitives, configuration, steady state and
   budget; create time_iteration.py for policy interpolation, bracketed roots and
   simultaneous updates. Keep the economic model separate from the algorithm.
2. Create run_growth.py runnable as `python -m econlab.run_growth`. Solve the baseline,
   simulate both requested initial conditions, and save policies, consumption,
   paths and a JSON diagnostics/configuration record under results/growth/.
3. Add tests against the separate full-depreciation analytical policy. Verify
   positivity, grid and midpoint Euler errors, baseline steady-state behavior,
   and clear failure on inadequate brackets or iteration caps.
4. Run the baseline, density refinement and wider-domain experiment. Compare on
   the common interior domain; report error magnitudes and runtimes. Do not confuse
   solver tolerance with approximation accuracy or use the closed form at delta=0.08.

Do not clip out-of-domain saving or suppress infeasibility. Run all existing tests,
update README.md with the implemented command and document numerical limitations.
