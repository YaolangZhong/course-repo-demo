# Computational Economics Lab

One project for economic models, numerical algorithms and reproducible experiments.
Start with Lab 6's McCall model, extend it with Lab 7's representative-agent and
Aiyagari models, and keep adding future material here.

This is a **student starter**: the mathematical specifications, environment,
project checks and implementation prompts are supplied. Numerical solver modules
are an exercise to implement with an LLM and verify. A passing starter check does
not mean that the economic models have been solved.

## Start here

Use Python 3.9–3.12 for the pinned teaching environment. Open this folder in VS Code,
then run in its terminal:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip==25.2
python -m pip install -r requirements.txt
python -m pip install --no-build-isolation --no-deps -e .
python -m econlab
python -m unittest discover -s tests -v
```

On Windows use `python` to create the environment and
`.venv\Scripts\Activate.ps1` in PowerShell to activate it. Select this environment
as the VS Code Python interpreter. Recreate `.venv` on each machine; do not copy it
or commit it to Git. Dependencies are pinned in `requirements.txt`.

## Work through the labs

1. **Lab 6:** read [McCall](notes/models/mccall.md) and
   [finite-MDP algorithms](notes/algorithms/finite_mdp.md), then use
   [the Lab 6 implementation prompt](prompts/01_mccall.md). Bring in your existing
   solution if available and verify it against the specification.
2. **Lab 7, core:** read [the representative-agent model](notes/models/representative_agent.md)
   and [time iteration](notes/algorithms/time_iteration.md), then use
   [the representative-agent prompt](prompts/02_representative_agent.md).
3. **Lab 7, extension:** read [Aiyagari](notes/models/aiyagari.md) and
   [stationary equilibrium](notes/algorithms/stationary_equilibrium.md), then use
   [the Aiyagari prompt](prompts/03_aiyagari.md).

See [the Lab 7 activity](docs/lab_07.md) for sequencing and deliverables.
Read each note before asking the agent to code. Inspect its diff, run its commands,
and explain the numerical evidence yourself.

## Where work belongs

| Folder/file | Purpose |
| --- | --- |
| `notes/models/` | Economic assumptions, equations and baseline configurations |
| `notes/algorithms/` | Numerical procedures, interfaces and accuracy criteria |
| `src/econlab/` | Reusable Python code generated and reviewed during the labs |
| `prompts/` | Small, reviewable implementation tasks for an LLM |
| `tests/` | Runnable verification; starter checks are supplied |
| `results/` | Generated outputs, ignored by Git; created by experiments |
| `docs/` | Lab activity, maintenance, provenance and GitHub workflow |
| `AGENTS.md` | Short project instructions for coding agents |
| `requirements.txt`, `pyproject.toml` | Reproducible environment and package definition |

[Maintenance](docs/maintenance.md) explains the weekly workflow.
[GitHub setup](docs/github.md) explains the repository lifecycle.
[Provenance](docs/provenance.md) records the course sources.
