# Lab 6 implementation prompt (retained for reference)

The project now supplies this implementation. Review/run the existing code first;
this prompt records its specification and supports comparison with your own work.

Read AGENTS.md, notes/models/mccall.md and notes/algorithms/finite_mdp.md.
Port my existing Lab 6 solution if supplied; otherwise implement it from these notes.

Create src/econlab/mccall.py with McCallModel and src/econlab/finite_mdp.py with
VFI, PFI and GPI classes exposing solve(model). Preserve the common finite-MDP
interface, tie handling, residual thresholds and return conventions. Return values,
policy indices and labels, residual, iterations, evaluation sweeps, linear solves
and runtime. Keep the solver independent of the McCall class.

Create src/econlab/run_mccall.py runnable as `python -m econlab.run_mccall`.
Compare the three methods, report accepted wages and save results/comparison.csv.
Add numerical tests under tests/. With the supplied baseline, the acceptance set
is {4, 5}; independently derive and check this instead of copying one solver's output.
Check feasible policies, Bellman residuals and agreement between methods. Also test
one small different finite MDP so solver reuse is demonstrated.

Run the experiment and tests, fix errors, and update README.md with the actual
entry point and results. Explain discrepancies and report commands and evidence.
