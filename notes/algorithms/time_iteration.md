# Euler equations and time iteration

Time iteration updates a saving policy using the old policy for future choices.
Unlike Howard PFI, it does not evaluate a value function before improving the policy.
The common notation is $\sigma^{(n+1)}=H\sigma^{(n)}$. Euler conditions define
$H$ for these models; other models can require other optimality or equilibrium conditions.

## Policy representation

Store representative-agent saving as an array of shape `(N,)` and Aiyagari saving
as `(N, J)`, with assets first and current productivity second. Use piecewise linear
interpolation of saving along the capital grid, separately for each productivity.
Compute consumption from the budget **after** interpolating saving. Never mix
current and next productivity indices.

Use one old policy array for the entire update, writing results into a new array.
Initialize representative saving with $\sigma^{(0)}(k)=k$ on the specified baseline
grid, checking positive consumption. For Aiyagari initialize saving to zero.
If a changed calibration makes the initial policy infeasible, construct another
feasible policy explicitly rather than replacing negative consumption with a floor.

## 1. Representative-agent update

At each grid state $k$, hold $\sigma^{(n)}$ fixed and define

$$c(x)=f(k)+(1-\delta)k-x,$$
$$c'(x)=f(x)+(1-\delta)x-\sigma^{(n)}(x),$$
$$\mathcal C(k,x;\sigma^{(n)})=
\frac1{c(x)}-\beta[f'(x)+1-\delta]\frac1{c'(x)}.$$

1. Construct a feasible bracket for $x$ inside the interpolation grid with both
   consumptions strictly positive. A numerical upper limit is
   $\min\{k_{\max},f(k)+(1-\delta)k-\eta\}$, with $\eta=10^{-10}$.
2. Check that the gap changes sign (allow a root at a bracket endpoint).
   If no admissible bracket exists, report the state and endpoint gaps. Expand the
   grid or improve initialization; do not label an artificial-boundary choice optimal.
3. Solve the scalar root by bisection. Under the admissible monotone update, negative
   gap means raise saving and positive gap means lower saving. Check this orientation
   explicitly. Stop when bracket width is below `root_tol=1e-10`; cap at 100 steps.
4. Set $\sigma^{(n+1)}(k)=x$. Finish all states before replacing the old array.
5. Measure $\|\sigma^{(n+1)}-\sigma^{(n)}\|_\infty$. Stop below `policy_tol=1e-8`,
   with `max_iter=3000`; reaching the cap is failure.
6. Recompute Euler errors using the **returned policy on both sides** of the equation.
   Report feasibility, error and iteration counts even if the policy change is small.

A unique root and convergence rely on economic and numerical regularity; do not
assume arbitrary interpolated policies satisfy these properties.

## 2. Aiyagari household update at fixed prices

For current $(k,z)$ and candidate saving $x$, set

$$c(x)=(1+r)k+wz-x,$$
$$c'(x,z')=(1+r)x+wz'-\sigma^{(n)}(x,z'),$$
$$\mathcal C(k,z,x;\sigma^{(n)})=
\frac1{c(x)}-\beta(1+r)\sum_{z'}P_z(z'\mid z)\frac1{c'(x,z')}.$$

1. Evaluate the gap at $x=0$. If it is nonnegative, set new saving to zero.
2. Otherwise bracket an interior root in
   $[0,\min\{k_{\max},(1+r)k+wz-\eta\}]$ and use bisection as above.
   Positive current and future consumption is required at every evaluation.
3. If the gap is still negative at the artificial upper boundary, fail with an
   instruction to enlarge the grid. Do not silently clip saving to $k_{\max}$ or
   extrapolate beyond the grid.
4. Apply the same simultaneous updates, policy tolerance and iteration cap.
5. Recompute the complementarity error under the returned policy.

## Accuracy and reporting

Normalize the final Euler gap by current marginal utility: $e=c_\sigma\mathcal C$.
For representative-agent saving report $|e|$. For Aiyagari report $|e|$ at interior
states and $\max\{-e,0\}$ at the borrowing boundary. Classify a boundary using a
small tolerance tied to `root_tol`; also report saving feasibility separately.

Evaluate these errors on grid nodes **and interval midpoints**. Report maxima,
minimum consumption, boundary hits, policy change, runtime, root iterations and
policy iterations. An initial teaching target is maximum relative Euler error below
$10^{-2}$ off grid; report the measured value rather than rounding it to zero.
This target is an accuracy diagnostic, not a rigorous value-function error bound.
The contraction residual bound in [finite MDP methods](finite_mdp.md) cannot simply
be transferred to this policy iteration.

Double grid density and expand the domain, comparing policies on a common interior
region. For the representative model also compare the steady state and the separate
full-depreciation closed form. For Aiyagari compare household saving with a grid-action
VFI benchmark at the **same prices**; finite-action VFI and continuous-choice time
iteration need not agree to solver tolerance. Refine the grid before interpreting
policy differences as a coding error.

## Implementation contract

Keep economic primitives in model classes and numerical updates in a separate
`time_iteration.py`. Both solvers return the grid, saving, implied consumption,
convergence status, iterations, runtime and diagnostics. Invalid probabilities,
infeasible consumption, an unbracketed root or an iteration cap must produce a clear
failure. Do not return a success flag merely because execution ended.
