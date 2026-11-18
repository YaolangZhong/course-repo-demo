# Computational Economics Lab

One cumulative course project: clone it once and extend it all term.

- **Lab 6 (supplied, runnable):** McCall job search solved by VFI, PFI and GPI/MPI.
- **Lab 7 (live LLM coding):** notes and prompts are supplied; you write the solvers
  on top of the Lab 6 code.

## Setup

Python 3.9–3.12:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip==25.2
python -m pip install -r requirements.txt
python -m pip install --no-build-isolation --no-deps -e .
python -m econlab.run_mccall
python -m unittest discover -s tests -v
```

On Windows activate with `.venv\Scripts\Activate.ps1`.

`run_mccall` checks the three methods against each other and writes
`results/comparison.csv` and `results/diagnostics.json`. The baseline accepts
offers 4 and 5; its rejection value is about 34.3243.

## Labs

| Lab | Read | Prompt |
| --- | --- | --- |
| 6 | [McCall](notes/models/mccall.md), [finite MDP](notes/algorithms/finite_mdp.md) | [01](prompts/01_mccall.md) (reference) |
| 7 core | [Representative agent](notes/models/representative_agent.md), [time iteration](notes/algorithms/time_iteration.md) | [02](prompts/02_representative_agent.md) |
| 7 extension | [Aiyagari](notes/models/aiyagari.md), [stationary equilibrium](notes/algorithms/stationary_equilibrium.md) | [03](prompts/03_aiyagari.md) |

Read the notes first. Give the agent one prompt at a time, inspect its diff, run
its commands, and commit in small steps. Submit a commit SHA or tag.

## Layout

| Path | Purpose |
| --- | --- |
| `notes/models/` | Economic assumptions and equations |
| `notes/algorithms/` | Numerical procedures and accuracy criteria |
| `prompts/` | Implementation tasks for an LLM |
| `src/econlab/` | Lab 6 code; Lab 7 code goes here |
| `tests/` | Analytical and project checks |
| `results/` | Generated outputs, ignored by Git |
| `AGENTS.md` | Instructions for coding agents |
