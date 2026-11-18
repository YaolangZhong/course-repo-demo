# Working in this project

Read README.md, the model note, the algorithm note and the requested prompt before
editing. Mathematics is the specification: if it is ambiguous or inconsistent,
report the precise equation before changing economic assumptions.

- Lab 6 code must stay runnable. Lab 7 is notes/prompts only until its live coding
  task is explicitly started; do not pre-fill its solvers.
- Implement one prompt at a time. Keep model primitives separate from algorithms and
  reuse existing code. NumPy and the standard library only, unless justified.
- Notation: full McCall state labels; sigma for saving, k for individual capital,
  K for aggregate capital, r for net interest.
- Update policies simultaneously. Check positive consumption and probability rows.
  Never hide out-of-grid saving by clipping or extrapolation.
- Add independent checks as applicable: McCall's reservation wage, the
  full-depreciation analytical saving policy, Euler/complementarity residuals,
  distribution mass/stationarity, market clearing.
- Keep results, environments, credentials and raw transcripts out of Git. Store
  parameters and diagnostics with generated outputs.
- Update README.md when capabilities or entry points change.
- Before finishing, run `python -m unittest discover -s tests -v`, the changed
  experiment and `git diff --check` from the root with the project environment.
  Report what passed and what remains unverified.
