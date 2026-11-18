# Euler equations and time iteration

Time iteration updates the saving policy $\sigma$ using the old policy for future choices. Unlike
PFI in [finite MDP methods](finite_mdp.md), it never evaluates a value function. Write
the update as $\sigma^{(n+1)}=H\sigma^{(n)}$, where $n$ counts policy iterations. Here
Euler conditions define $H$; other models can require other optimality or equilibrium
conditions.

## Policy representation

Store representative-agent saving as an array of shape `(N,)` and Aiyagari saving as
`(N, J)`: $N$ grid nodes for $k$ on the first axis, $J$ current productivity states on
the second. Between nodes, interpolate saving piecewise linearly in $k$, separately for
each productivity, and compute consumption from the budget **after** interpolating
saving. Never mix current and next productivity indices.

Use one old policy array for the entire update, writing results into a new array.
Initialize representative-agent saving with $\sigma^{(0)}(k)=k$ and Aiyagari saving
with $\sigma^{(0)}(k,z)=0$, and check positive consumption at every node. If a changed
calibration makes the initial policy infeasible, construct another feasible policy
explicitly; do not floor negative consumption.

## 1. Representative-agent update

At each grid state $k$, hold $\sigma^{(n)}$ fixed. For candidate saving $x$ define
current consumption, next-period consumption and the Euler gap:

$$
c(x)=f(k)+(1-\delta)k-x,
$$

$$
c_+(x)=f(x)+(1-\delta)x-\sigma^{(n)}(x),
$$

$$
D(k,x;\sigma^{(n)})=\frac1{c(x)}-\beta[f'(x)+1-\delta]\frac1{c_+(x)}.
$$

1. **Bracket.** Let $k_{\min},k_{\max}$ be the grid endpoints and $\eta=10^{-10}$.
   Construct a bracket for $x$ inside
   $[k_{\min},\min\lbrace k_{\max},f(k)+(1-\delta)k-\eta\rbrace]$, so that $x$ stays
   inside the interpolation grid, with $c(x)$ and $c_+(x)$ strictly positive.
2. **Check the sign change.** Require $D\leq0$ at the lower endpoint and $D\geq0$ at
   the upper endpoint (a root at an endpoint is allowed). Otherwise fail, reporting
   the state and both endpoint gaps; expand the grid or improve the initial policy.
   Never report an artificial-boundary choice as optimal.
3. **Bisect.** A negative gap means raise $x$; a positive gap means lower $x$. Stop
   when the bracket width is below `root_tol=1e-10`; reaching `root_max_iter=100`
   steps is a failure.
4. **Update.** Set $\sigma^{(n+1)}(k)=x$. Finish all states before replacing the old
   array.
5. **Stop or repeat.** Measure $\lVert\sigma^{(n+1)}-\sigma^{(n)}\rVert_\infty$ over
   grid nodes. Stop when it is below `policy_tol=1e-8` and return $\sigma^{(n+1)}$;
   reaching `max_iter=3000` is a failure.
6. **Check.** Recompute Euler errors with the **returned policy on both sides** of the
   equation. Report feasibility, errors and iteration counts even when the policy
   change is small.

Neither a unique root nor convergence is guaranteed for an arbitrary interpolated
policy; rely on the checks above, not on these properties.

## 2. Aiyagari household update at fixed prices

For current $(k,z)$ and candidate saving $x$, set

$$
c(x)=(1+r)k+wz-x,
$$

$$
c_+(x,z')=(1+r)x+wz'-\sigma^{(n)}(x,z'),
$$

$$
D(k,z,x;\sigma^{(n)})=\frac1{c(x)}-\beta(1+r)\sum_{z'}P_z(z'\mid z)\frac1{c_+(x,z')}.
$$

At a fixed point $\sigma$, $D(k,z,\sigma(k,z);\sigma)$ is the Euler gap $D(k,z)$ of the
[Aiyagari model](../models/aiyagari.md).

1. Evaluate the gap at $x=0$. If it is nonnegative, set $\sigma^{(n+1)}(k,z)=0$.
2. Otherwise bisect as in Section 1 on
   $[0,\min\lbrace k_{\max},(1+r)k+wz-\eta\rbrace]$. Current and next-period
   consumption must be positive at every evaluation.
3. If the gap is still negative at the artificial upper boundary $k_{\max}$, fail with
   an instruction to enlarge the grid. Never clip saving to $k_{\max}$ or extrapolate
   beyond the grid.
4. Use the same simultaneous update, `root_tol`, `root_max_iter`, `policy_tol` and
   `max_iter`.
5. Recompute the complementarity error under the returned policy.

## Accuracy and reporting

Normalize the final Euler gap by current marginal utility: the Euler error is
$e=c_\sigma D$. For the representative agent report $|e|$. For Aiyagari report $|e|$ at
interior states and the complementarity error $\max\lbrace -e,0\rbrace$ where the
borrowing limit binds. The limit binds at an evaluated state, node or midpoint, when
the interpolated policy satisfies $\sigma(k,z)\leq$ `root_tol`. Report saving
feasibility separately.

Evaluate these errors on grid nodes **and interval midpoints**. Report maxima, minimum
consumption, boundary hits, policy change, runtime, root iterations and policy
iterations. An initial teaching target is a maximum Euler error below $10^{-2}$ off
grid; report the measured value rather than rounding it to zero. This target is an
accuracy diagnostic, not a value-function error bound: the residual bound in
[finite MDP methods](finite_mdp.md) does not carry over to time iteration.

Double grid density and expand the domain, comparing policies on a common interior
region. For the representative-agent model also compare the steady state and the
separate full-depreciation closed form.

For Aiyagari compare household saving with a grid-action VFI benchmark at the **same
prices**. Keep the benchmark small: use the model note's quadratic grid with 100 nodes
on $[0,k_{\max}]$, restrict saving to grid points, build the common finite-MDP input
(200 states, 100 actions) and solve it with the existing `VFI` class. Interpolate the
time-iteration saving onto this coarse grid; an initial teaching target is a maximum
difference below 0.5. Finite-action VFI and continuous-choice time iteration need not
agree to solver tolerance; refine the benchmark grid before interpreting a difference
as a coding error.

## Implementation contract

Keep economic primitives in model classes and numerical updates in a separate
`time_iteration.py`. Vectorize each update across all grid states with NumPy arrays
(bisect every state at once); a Python loop over states makes the equilibrium runs
impractically slow. Both solvers return the grid, saving, implied consumption,
convergence status, iterations, runtime and diagnostics. Invalid probabilities,
infeasible consumption, an unbracketed root or an iteration cap must raise a clear
failure; finishing execution is not success.
