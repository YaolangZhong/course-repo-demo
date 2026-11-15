# Working in this project

Read README.md, then the model note, algorithm note and requested prompt before
editing. Mathematics is the specification. If it is ambiguous or inconsistent,
report the precise equation before changing economic assumptions.

- Keep model primitives separate from algorithms; reuse existing code before adding
  another helper. Use NumPy and the standard library unless a new dependency is justified.
- Preserve the full McCall state labels. Use sigma for saving, k for individual
  capital/assets, K for aggregate Aiyagari capital, and r for net interest.
- Update policies simultaneously. Check positive consumption and probability rows.
  Never hide out-of-grid saving by clipping or extrapolation.
- Implement one prompt at a time. State changed files and run commands from the root
  with the project environment. Do not claim success from unexecuted code.
- For numerical work, add independent checks: McCall's known reservation wage,
  the full-depreciation analytical saving policy, Euler/complementarity residuals,
  distribution mass/stationarity and equilibrium market clearing, as applicable.
- Keep results, environments and credentials out of Git. Store reproducible parameters
  and diagnostics with generated outputs; do not check in raw conversation transcripts.
- Update README.md when implemented capabilities or entry points change. Keep future
  work clearly marked and record substantive weekly changes in CHANGELOG.md.
- Before finishing run `python -m unittest discover -s tests -v`, the changed experiment,
  and `git diff --check`. Report what passed and what remains unverified.
