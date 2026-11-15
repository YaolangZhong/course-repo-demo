# Construction and maintenance plan

## Construction decisions

Use one standalone Python project and one Git history, separate from the course
website's publication tooling. Organize economics by model and methods by algorithm.
Weeks are milestones in CHANGELOG.md and lab activities, not copies of the codebase.
A small `src/econlab` package makes imports consistent in scripts and tests.
NumPy plus the standard library is sufficient for the initial exercises.

The repository is a student starter. Keep instructor reference solutions outside
its directory and Git history; ignoring a solution after committing it does not
remove it from history. The original Lab 6 assignment remains an archival source,
while this project's adapted notes are maintained here.

## Implementation sequence

| Stage | Inputs | New code | Completion evidence |
| --- | --- | --- | --- |
| Foundation | Notes and course conventions | Package, environment, CI | Fresh install and starter checks |
| Lab 6 | McCall and finite MDP notes | `mccall.py`, `finite_mdp.py`, `run_mccall.py` | Bellman residual and reservation-wage check |
| Lab 7 core | Representative-agent and time-iteration notes | `representative_agent.py`, `time_iteration.py`, `run_growth.py` | Closed-form policy, Euler errors, steady state |
| Lab 7 extension | Aiyagari and equilibrium notes | `aiyagari.py`, `distribution.py`, `equilibrium.py`, `run_aiyagari.py` | KKT, invariant distribution, market clearing |
| Later weeks | New model or method specification | Extend shared modules or add one focused module | Existing checks plus new model evidence |

The Python filenames above are intended implementation targets, not claims that
these solvers are already included in the starter.

## Weekly cycle

1. Pull the current main branch, inspect the working tree and create a task branch.
2. Add or revise the mathematical note and the experiment's parameters first.
3. Ask the agent for one bounded implementation step. Review the diff and run checks.
4. Keep shared algorithms model-independent where their interfaces genuinely match;
   do not force discrete MDPs and continuous Euler problems into one artificial interface.
5. Save small numerical summaries and interpretation in a report under `docs/`.
   Put reproducible bulk arrays/figures under ignored `results/`, with a JSON
   manifest containing parameters, tolerances, runtime, dependency versions and Git revision.
6. Update README entry points and CHANGELOG. Run all fast tests and affected experiments.
7. Review and merge the branch, then tag a verified milestone. Do not tag unfinished
   implementations as completed labs.

Run fast correctness tests on every push/PR. Keep full grid-refinement experiments
as explicit commands because they cost more; run them before a numerical release.
Only add dependencies when an exercise needs them, pin versions and verify a clean
installation. If Python support changes, update requirements, README and CI together.

## Ownership

Students own the generated code, review and numerical interpretation. The instructor
owns the starter specifications and release notes. An agent is an implementation
assistant, not evidence that the mathematics or computation is correct. Keep shared
rules in AGENTS.md; keep task-specific instructions in prompts.
