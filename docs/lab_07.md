# Lab 7: from individual exercises to a research project

The core activity implements the representative-agent model using time iteration.
Aiyagari is the advanced extension. Complete each stage before moving to the next;
do not ask the LLM to build all three models in one response.

## 1. Establish the cumulative project

Open this folder, create its virtual environment and run the starter checks from
README.md. Inspect `.gitignore`, `AGENTS.md` and the source layout. Explain which
files describe economics, which describe numerical procedures, and which are
recreated locally. Port your Lab 6 solution using prompt 01 and record a baseline
commit once the three methods agree.

## 2. Implement the deterministic economy

Read the representative-agent note and derive the Euler residual yourself. Explain
why the future policy stays fixed while its argument changes. Use prompt 02 to
implement the solver. Inspect the root bracket and the old/new policy arrays.
Run the full-depreciation check before trusting baseline results. Compare simulated
paths with the analytical steady state and repeat on a finer grid.

## 3. Extend to heterogeneous households

Read the Aiyagari note. Explain why the return is now fixed within the household
solution and why zero saving requires an inequality. Use prompt 03 in its three
stages: household policy, stationary distribution, then equilibrium. Inspect how
saving between grid points sends mass to adjacent asset bins.

## 4. Record and review

For each stage save the configuration, commands, diagnostics and a short economic
interpretation. Commit the code, notes and concise report; regenerate large outputs
under `results/`. Review the diff before committing. A report should distinguish
solver convergence from discretization accuracy and economic conclusions.

## Deliverables

- One cumulative repository with a working environment and clear README.
- McCall VFI/PFI/GPI comparison carried forward from Lab 6.
- Representative-agent policy, consumption and transition paths; analytical and
  Euler-error checks; grid sensitivity.
- Advanced extension: Aiyagari saving policies, stationary wealth distribution,
  equilibrium prices/capital, market residual and sensitivity results.
- A concise account of what the LLM produced, what you changed, and which independent
  checks support the result. Retain useful prompts rather than entire chat histories.

No separate weekly virtual environment or duplicate solver folder is needed.
