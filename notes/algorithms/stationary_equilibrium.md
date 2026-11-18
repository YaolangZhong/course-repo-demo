# Distribution iteration and stationary equilibrium

The household solver takes prices as given. Equilibrium adds distribution iteration
and an outer market-clearing calculation. Use the [Aiyagari model](../models/aiyagari.md)
and [time iteration](time_iteration.md).

## 1. From a policy to a finite transition matrix

Let $d_{ij}$ be the probability mass at grid state $(k_i,z_j)$, $i=0,\ldots,N-1$,
$j=0,\ldots,J-1$; entries are nonnegative and sum to one. The array $d$, shaped
`(N, J)` like the saving policy, approximates the population distribution $\mu$, and
the matrix $P^\sigma$ below approximates the model's transition kernel. When forming a
matrix, state $(i,j)$ has flat index $iJ+j$.

For saving $x=\sigma(k_i,z_j)$ with $k_\ell\leq x\leq k_{\ell+1}$, set

$$
\lambda=\frac{x-k_\ell}{k_{\ell+1}-k_\ell}.
$$

For each next productivity $z_{j'}$, assign transition probabilities

$$
P^\sigma_{(i,j),(\ell,j')}=(1-\lambda)P_z(z_{j'}\mid z_j),\qquad
P^\sigma_{(i,j),(\ell+1,j')}=\lambda P_z(z_{j'}\mid z_j).
$$

If $x$ is itself a grid point, all weight goes to that point. The weights preserve
expected next capital: $(1-\lambda)k_\ell+\lambda k_{\ell+1}=x$. This lottery is a
numerical approximation to deterministic saving, not additional economic risk. Reject
out-of-grid saving before calculating weights.

The transition matrix must have nonnegative entries and unit row sums. It need not be
stored densely: pushing mass into neighboring bins implements the same operation.

## 2. Stationary distribution

1. Start from a uniform distribution over all grid states.
2. Apply $d^{(m+1)}=d^{(m)}P^\sigma$ (row-vector convention), using a separate new array.
3. Stop when $\lVert d^{(m+1)}-d^{(m)}\rVert_\infty$ is below `dist_tol=1e-12`;
   reaching `dist_max_iter=50000` is a failure.
4. Return $d=d^{(m+1)}$ and report its own residual $\lVert dP^\sigma-d\rVert_\infty$,
   total mass and minimum entry. Do not renormalize: a mass error signals a
   transition bug.
5. Compute

   $$K^s=\sum_{i,j}k_i d_{ij},\qquad \bar k'=\sum_{i,j}\sigma(k_i,z_j)d_{ij}.$$

Stationarity implies $K^s=\bar k'$. Also check $\sum_i d_{ij}\approx\pi_j$. Power
iteration can fail for periodic chains, and multiple recurrent classes make the
stationary distribution nonunique; check sensitivity to another initial distribution.

## 3. Outer market clearing

Define excess capital supply $G(K)=K^s(K)-K$, where $K^s(K)$ is capital supply at
prices $r(K),w(K)$.

1. Compute $\pi$ and $L$ once. Start from the baseline `capital_bracket`, two positive
   trial values of $K$.
2. At each endpoint compute firm prices, solve the household problem and compute its
   stationary distribution. Verify inner convergence before using $G(K)$.
3. Require opposite signs of $G$ at the endpoints; expand or revise the bracket
   explicitly if needed. Do not presume the baseline bracket always works.
4. Bisect the bracket. Each new $K$ requires a new household solution and distribution
   at its new prices. Retain the half with opposite endpoint signs.
5. Stop when $|G(K)|$ is below `market_tol=2e-5`; reaching `market_max_iter=60`
   outer iterations is a failure. A small bracket alone is not enough if the market residual remains large.
6. Return $K,r,w,\sigma,d$ and all inner and outer diagnostics from the same trial.

Warm starts are optional once a cold start works: check their feasibility at the new
prices and confirm the result matches a cold start. The numerical supply map need not
be monotone; always check actual bracket signs.

## 4. Equilibrium checks and experiments

Report capital clearing, household Euler and complementarity errors, distribution
residual, mass, positive consumption and mass in the top five $k$ nodes. With
$C=\sum_{i,j}c_\sigma(k_i,z_j)d_{ij}$, check the goods-market implication

$$
C+\delta K\approx AK^\alpha L^{1-\alpha}.
$$

Repeat the equilibrium with 1,000 nodes on $[0,60]$, then 700 nodes on $[0,90]$, each
on the model note's quadratic grid with the new $N$ and $k_{\max}$. Compare $K,r,w$
and saving on their common domain; use a change in $K$ below 0.5% of its baseline
value as an initial teaching target, not an existence or uniqueness certificate. Report
any failed target and investigate. Negligible tail mass does not alone justify an upper
bound if policies still hit it.

Save parameters, grids, tolerances, iteration history and summary diagnostics with the
outputs. Report solver convergence, discretization sensitivity and economic
interpretation separately.
