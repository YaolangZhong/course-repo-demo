# Agent instructions

Standing rules for every task. Task-specific deliverables are in `prompts/`.

- Read in this order before editing: `README.md`, the model note
  (`notes/models/`), the algorithm note (`notes/algorithms/`), the requested prompt.
- The mathematics in `notes/` is the specification. If it is ambiguous or
  inconsistent, stop and report the precise equation; never change an economic
  assumption to make code run.
- Implement one prompt at a time, only when it is requested. Existing code and tests
  must keep passing; the representative-agent and Aiyagari models stay
  notes-only until their prompt is requested, so do not pre-fill their solvers.
- Keep model primitives separate from algorithms, and reuse existing code before
  writing new code. NumPy and the standard library only.
- Notation follows the notes: full McCall states `(U,w)`, `(E,w)`; `sigma` policy;
  `k` individual and `K` aggregate capital; `r` net interest; `R` reward; `D` Euler gap.
- Update policies simultaneously: compute every new entry from the old array.
- Raise an error on nonpositive consumption, invalid probability rows, out-of-grid
  saving or an iteration cap. Never clip, floor, extrapolate or renormalize to hide
  one.
- Test each result against a check that does not reuse the solver: a closed form, a
  residual, or an accounting identity named in the notes.
- Keep results, environments and credentials out of Git. Store parameters and
  diagnostics with generated outputs. Update `README.md` when capabilities or entry
  points change.
- Before finishing, run from the root in the project environment
  `python -m unittest discover -s tests -v`, the changed experiment and
  `git diff --check`. Report what passed and what remains unverified.
