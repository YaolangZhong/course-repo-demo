# Repository architecture recommendation

Status: recommendation for review. A standalone local repository already exists;
no GitHub remote or publication decision has been made. The instructor has confirmed
that Lab 6 code should be included and Lab 7 should be implemented live with an LLM.

## Option A — separate cumulative lab repository (recommended)

- Stack: one ordinary Git repository, Python package, NumPy, one virtual environment
  per checkout and GitHub Actions. No database, backend server or deployment service.
- Fit: the course repository owns lectures, weekly instructions and publication;
  this repository owns evolving runnable lab work and its mathematical specifications.
  Course pages link to a verified lab release rather than copy its files.
- Development/maintenance: low; one additional repository, with independent commits,
  tests and release tags. This also avoids the course repository's student-file allowlist,
  which currently excludes project-level configuration such as pyproject and workflows.
- Access: computation is local after setup. GitHub and package downloads require
  network access; a release archive can support students unable to clone directly.
- Manage: repository access and ordinary dependency updates; no server or application
  credentials. Never store GitHub credentials in the project.
- Main risk: stale course links or mismatched releases. Link each assignment to the
  intended tag and record the tag in the course's assignment metadata at publication.

## Option B — one cumulative folder inside the course repository

- Stack: the same Python package and environment under a `labs/` folder in the course
  repository, with path-scoped CI and coordinated publication rules.
- Fit: one remote to manage, straightforward internal relative links.
- Development/maintenance: initially simple, but requires changing the current course
  allowlist/build conventions and separating lab changes from lecture publication.
- Access: local computation; the initial clone includes the course's other materials.
- Manage: the same repository permissions and dependencies; no server.
- Main risk: students inherit a larger, course-oriented checkout and mixed release
  history when their aim is to own and extend a research codebase.

## Recommended ownership

```text
Teaching/
  U_Tokyo_Comp_Econ_Course/       # existing course Git repository
    weeks/                      # lecture materials and assignment instructions
    docs/                       # private instructor preparation/reference solutions
  computational-economics-lab/  # independent lab Git repository
    README.md                   # purpose, setup, actual runnable commands
    AGENTS.md                   # short coding-agent rules
    notes/models/               # economic assumptions and baseline parameters
    notes/algorithms/           # numerical specifications and diagnostics
    src/econlab/                # reusable code; Lab 6 supplied, Lab 7 built live
    tests/                      # economic and numerical evidence
    prompts/                    # staged implementation tasks
    docs/                       # lab activities, maintenance and short reports
    .github/workflows/          # automated checks
    .venv/                      # local only
    results/                    # generated, local only
```

Within the lab project, organize by model and algorithm, not by weekly duplicate
folders. Treat weeks as activities, commits and release tags. Keep one canonical
model note and one implementation of a shared algorithm. Model classes supply
primitives; solvers compute decisions; experiment entry points produce reports.
Avoid a universal solver abstraction for both finite MDPs and Euler-based models.

The instructor maintains the starter and provides new notes/prompts over time.
Each student maintains one personal project for all remaining weeks. A template is
convenient for independent student histories; later instructor additions are then
integrated deliberately, not automatically synchronized. If automatic upstream
merging becomes a requirement, choose a shared-history workflow before release.
See [GitHub lifecycle](github.md) for setup and the template/fork tradeoff.

Recommendation: Option A. The decisive reason is that the student research project
has a different lifecycle from lecture publication. Remote owner, visibility and
student update/submission policy remain to be chosen; they do not block local work.
