# Lab 6 supplied baseline: verification

Run from the project root with the project environment activated:

```sh
python -m econlab.run_mccall
python -m unittest discover -s tests -v
```

On 15 November 2026, all six tests passed on Python 3.9.6 / NumPy 1.26.4.
The tests cover the analytical McCall solution, another finite MDP, infeasible-action
masking, exact ties, beta=0, iteration failure, malformed transition probabilities,
the installed package entry point and local documentation links.

| Method | Bellman residual | Iterations | Policy evaluation sweeps | Linear solves |
| --- | --- | --- | --- | --- |
| VFI | 9.246e-8 | 170 | 0 | 0 |
| PFI | 7.105e-15 | 3 | 0 | 3 |
| GPI/MPI | 7.489e-8 | 57 | 171 | 0 |

VFI performs Bellman optimality updates; its zero policy-evaluation-sweep count
must not be read as zero computational work. The methods' iteration counts are
not directly interchangeable units of work. Runtime is printed for each run.

All three accept wages 4 and 5, with the lowest accepted grid wage equal to 4.
The rejection value is 34.3243243. CSV state-level results and JSON diagnostics
are regenerated under ignored `results/`. The analytical check does not use one
numerical solver as the answer for another.

Lab 7 code is intentionally absent. These results do not validate future live
implementations of time iteration or Aiyagari equilibrium. GitHub-hosted CI has
not run because this repository has no configured remote.
