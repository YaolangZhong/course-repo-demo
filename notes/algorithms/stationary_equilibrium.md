# Distribution iteration and stationary equilibrium

The household solver takes prices as given. Equilibrium adds distribution iteration
and an outer market-clearing calculation. Use the [Aiyagari model](../models/aiyagari.md)
and [time-iteration specification](time_iteration.md).

## 1. From a policy to a finite transition matrix

Let $d_{ij}$ be the probability mass at grid state $(k_i,z_j)$; its entries are
nonnegative and sum to one. This finite probability array approximates the theoretical
distribution $\mu$. Flatten states using index $iJ+j$ when forming a matrix.

For saving $x=\sigma(k_i,z_j)$ between adjacent grid points $k_\ell,k_{\ell+1}$, set

$$\lambda=\frac{x-k_\ell}{k_{\ell+1}-k_\ell}.$$

For each next productivity $z_{j'}$, assign transition probabilities

$$P^\sigma_{(i,j),(\ell,j')}=(1-\lambda)P_z[j,j'],\qquad
P^\sigma_{(i,j),(\ell+1,j')}=\lambda P_z[j,j'].$$

At an exact endpoint assign its entire asset weight to that endpoint. The weights
preserve expected next assets: $(1-\lambda)k_\ell+\lambda k_{\ell+1}=x$.
This lottery is a numerical approximation to deterministic saving, not additional
economic asset risk. Reject out-of-grid saving before calculating weights.

The transition matrix must have nonnegative entries and unit row sums. It need not
be stored densely: pushing mass into neighboring bins implements the same operation.

## 2. Stationary distribution

1. Start from a uniform distribution over all asset-productivity states.
2. Apply $d_{m+1}=d_mP^\sigma$ with row-vector convention, using a separate new array.
3. Stop when $\|d_{m+1}-d_m\|_\infty<10^{-12}$, capped at 50,000 iterations.
4. Return the new distribution and verify its own residual
   $\|dP^\sigma-d\|_\infty$, total mass and minimum entry. Do not silently
   renormalize a transition bug away.
5. Compute

   $$K^s=\sum_{i,j}k_i d_{ij},\qquad
   \bar k'=\sum_{i,j}\sigma(k_i,z_j)d_{ij}.$$

Stationarity implies $K^s=\bar k'$. Also check $\sum_i d_{ij}\approx\pi_j$.
Power iteration requires appropriate mixing and can fail for periodic chains;
multiple recurrent classes can make the stationary distribution nonunique. Check
sensitivity to another initial distribution. Do not interpret hitting the iteration
cap as a stationary solution.

## 3. Outer market clearing

Define $G(K)=K^s(K)-K$.

1. Compute $\pi,L$ once. Choose two positive trial capital stocks.
2. At each endpoint compute firm prices, solve the household problem, and compute
   its stationary distribution. Verify inner convergence before using $G(K)$.
3. Require opposite signs of $G$ at the endpoints; expand or revise the bracket
   explicitly if needed. Do not presume the baseline bracket always works.
4. Bisect the capital bracket. Each new $K$ requires a new household solution
   and distribution at its new prices. Retain the half with opposite endpoint signs.
5. Stop when $|K^s(K)-K|<2\times10^{-5}$, capped at 60 outer iterations.
   A small bracket alone is not enough if the market residual remains large.
6. Return $K,r,w,\sigma,d$ and all inner and outer diagnostics from the same trial.

Warm starts are optional after a cold-start implementation works. Check their
feasibility at the new prices and confirm the final result agrees with a cold start.
The numerical supply map need not be globally monotone; always retain and check
actual bracket signs.

## 4. Equilibrium checks and experiments

Report capital clearing, household Euler/complementarity errors, distribution
residual, mass, positive consumption and mass in the top five asset nodes.
With $C=\sum_{i,j}c_\sigma(k_i,z_j)d_{ij}$, check the goods-market implication

$$C+\delta K\approx AK^\alpha L^{1-\alpha}.$$

Repeat the equilibrium with 1,000 nodes on $[0,60]$, then 700 nodes on $[0,90]$.
Compare $K,r,w$ and saving on their common domain; use relative change in $K$ below
0.5% as an initial teaching target, not an existence or uniqueness certificate.
Report any failed target and investigate. Negligible tail mass does not alone
justify an upper bound if policies still hit it.

Save parameters, grids, tolerances, iteration history and summary diagnostics with
the outputs. Separate solver convergence, discretization sensitivity and economic
interpretation in the report.
