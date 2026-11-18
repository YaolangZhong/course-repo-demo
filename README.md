# Computational Economics Lab

A cumulative project for solving dynamic economic models numerically with the
help of a coding agent. Each model is specified in mathematical notes, turned into
code through a written prompt, and verified against independent checks. Later
models reuse the code written for earlier ones.

- **McCall job search (implemented):** a finite Markov decision process solved by
  value function iteration (VFI), policy function iteration (PFI) and generalized
  policy iteration (GPI/MPI), with the three methods checked against each other.
  Notes: [model](notes/models/mccall.md), [algorithm](notes/algorithms/finite_mdp.md).
- **Representative-agent growth (notes only):** a deterministic consumption–saving
  economy solved by time iteration on the Euler equation.
  Notes: [model](notes/models/representative_agent.md),
  [algorithm](notes/algorithms/time_iteration.md).
- **Aiyagari (notes only):** incomplete markets with idiosyncratic income risk and a
  borrowing constraint; household policies, the stationary distribution and
  market-clearing prices are solved as a stationary equilibrium.
  Notes: [model](notes/models/aiyagari.md),
  [algorithm](notes/algorithms/stationary_equilibrium.md).

The last two have no solver code yet: you implement them from their notes, using
the tasks in `prompts/`, on top of the existing package.

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

## Working with it

Read the notes first. Give the agent one prompt at a time, inspect its diff, run
its commands, and commit in small steps. Submit a commit SHA or tag.

## Layout

| Path | Purpose |
| --- | --- |
| `notes/models/` | Economic assumptions and equations |
| `notes/algorithms/` | Numerical procedures and accuracy criteria |
| `prompts/` | Implementation tasks for an LLM |
| `src/econlab/` | McCall and finite-MDP code; new models and algorithms go here |
| `tests/` | Analytical and project checks |
| `results/` | Generated outputs, ignored by Git |
| `AGENTS.md` | Instructions for coding agents |
