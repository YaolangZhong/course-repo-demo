# Source provenance

Prepared on 15 November 2026 from the local University of Tokyo computational
economics course materials.

| Project note | Course source |
| --- | --- |
| `notes/models/mccall.md` | `weeks/week_06/lab/starter/mccall_model.md` |
| `notes/algorithms/finite_mdp.md` | `weeks/week_06/lab/starter/algorithms.md`; local lecture links replaced by this provenance record |
| Representative-agent, Aiyagari and time-iteration notes | `weeks/week_07/lecture/slides/tex/Euler_Equations_and_Time_Iteration.tex` |
| Aiyagari numerical baseline | Preserved instructor script `scripts/week7_aiyagari_figures.py` |

The [course repository](https://github.com/YaolangZhong/U_Tokyo_Comp_Econ_Course)
is the source context. Some authoring files are private or unreleased; this project
is self-contained and does not import them at runtime. Numerical procedures and
diagnostics are lab additions, not additional lecture-slide content.

Method references named in Lecture 7: Coleman (1990), “Solving the Stochastic Growth
Model by Policy-Function Iteration”; Aiyagari (1994), “Uninsured Idiosyncratic Risk
and Aggregate Saving”; Krusell and Smith (1998), “Income and Wealth Heterogeneity
in the Macroeconomy” (future aggregate-risk extension).

No new license grant is inferred from access to teaching materials. The instructor
should choose redistribution terms before a public release.

The supplied `src/econlab/mccall.py` and `mdp.py` adapt the existing
`weeks/week_05/lab/starter/` code (that week's materials were used in Week 6).
Imports are package-relative and the MDP accepts beta=0, as the finite-MDP note
specifies. `finite_mdp.py` and `run_mccall.py` were prepared from the Lab 6
specification; no saved completed Lab 6 homework implementation was located.
