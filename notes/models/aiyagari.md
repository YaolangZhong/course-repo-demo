# Aiyagari: income risk and stationary equilibrium

A unit mass of households faces uninsurable individual productivity risk; there is no
aggregate risk. A household with productivity $z$ supplies $z$ units of effective labor
and saves in a single asset, capital. Preferences are

$$
\mathbb E_0\sum_{t=0}^\infty\beta^t u(c_t),\qquad u(c)=\log c,\qquad 0<\beta<1.
$$

## States, actions, rewards and transitions

The household takes the net interest rate $r$ and the wage $w$ as given; $1+r$ is the
gross return. Productivity takes values $z_j$, $j=0,\ldots,J-1$, in a finite set
$\mathcal Z\subset(0,\infty)$ and follows a Markov chain with transition probabilities
$P_z(z'\mid z)=\Pr(z_{t+1}=z'\mid z_t=z)$, stored as the matrix entry `P_z[j, j']`.
Rows sum to one.

| Object | Definition |
| --- | --- |
| State | individual capital (assets) and productivity $(k,z)$, with $k\geq0$ |
| Action | next capital $k'$, with $0\leq k'\lt(1+r)k+wz$ |
| Reward | $u(c)$, with $c=(1+r)k+wz-k'$ |
| Transition | next capital equals the chosen $k'$; next productivity follows $P_z$ |
| Policy | saving $\sigma(k,z)=k'$ |
| Consumption | $c_\sigma(k,z)=(1+r)k+wz-\sigma(k,z)$ |

Individual capital $k$ differs from aggregate capital $K$. The borrowing limit is zero:
$k'\geq0$.

## Bellman and Euler equations

$$
V(k,z)=\max_{0\leq k'<(1+r)k+wz}\left\lbrace u((1+r)k+wz-k')+\beta\sum_{z'\in\mathcal Z}P_z(z'\mid z)V(k',z')\right\rbrace .
$$

Under the optimal policy $\sigma$, define the Euler gap

$$
D(k,z)=\frac1{c_\sigma(k,z)}-\beta(1+r)\sum_{z'\in\mathcal Z}P_z(z'\mid z)\frac1{c_\sigma(\sigma(k,z),z')}.
$$

The borrowing limit implies the complementarity conditions

$$
\sigma(k,z)\geq0,\qquad D(k,z)\geq0,\qquad \sigma(k,z)D(k,z)=0.
$$

Interior saving has zero gap. At $\sigma(k,z)=0$ the gap may be positive: the household
would like to borrow but cannot, so the Euler equation must not be imposed with
equality at every state. Feasibility and the transversality condition
$\lim_{T\to\infty}\beta^T\mathbb E_0[u'(c_T)k_{T+1}]=0$ are also required.

## Firms and stationary equilibrium

Firms produce $Y=AK^\alpha L^{1-\alpha}$ with $A>0$ and $0<\alpha<1$; capital
depreciates at rate $0<\delta\leq1$. Effective labor is $L=\sum_j\pi_jz_j$, where $\pi$
is the stationary productivity distribution: $\pi=\pi P_z$ and $\sum_j\pi_j=1$. It does
not depend on $K$. Given aggregate capital $K>0$, firm optimality gives

$$
r(K)=\alpha A(K/L)^{\alpha-1}-\delta,\qquad w(K)=(1-\alpha)A(K/L)^\alpha.
$$

The population distribution $\mu$ over $(k,z)$ evolves under the policy-induced
transition kernel $P^\sigma$ and is stationary when $\mu=\mu P^\sigma$. Capital supply
is $K^s=\int k\ d\mu(k,z)$. A stationary equilibrium satisfies household optimality,
firm optimality, stationarity and capital market clearing, $K^s=K$.

## Baseline configuration

```python
A = 1.0
alpha = 0.36
beta = 0.96
delta = 0.08
z = (0.5, 1.5)
P_z = ((0.9, 0.1), (0.1, 0.9))
asset_upper = 60.0
nodes = 500
capital_bracket = (6.0, 12.0)
```

`nodes` is the number of capital grid points $N$ and `asset_upper` is the upper grid
endpoint $k_{\max}$; the grid starts at the borrowing limit $0$. Here $\pi=(0.5,0.5)$ and $L=1$. The grid is
quadratic,

$$
k_i=k_{\max}\left[\frac{i}{N-1}\right]^2,\qquad i=0,\ldots,N-1,
$$

so it is denser near the borrowing limit. The upper endpoint $k_{\max}$ is artificial:
diagnose its effect and enlarge it when needed. `capital_bracket` is an initial guess
for the equilibrium $K$, not a theorem; check it numerically. At every trial $K$
require $\beta(1+r)<1$; this is a household stationarity restriction, not a proof of
equilibrium existence or uniqueness.

See [time iteration](../algorithms/time_iteration.md) for the household solution and
[stationary equilibrium](../algorithms/stationary_equilibrium.md) for the distribution
and market clearing. The numbers are a teaching calibration, not a replication of
Aiyagari (1994).
