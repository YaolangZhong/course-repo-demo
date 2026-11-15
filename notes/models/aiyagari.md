# Aiyagari: income risk and stationary equilibrium

A unit mass of households faces individual productivity risk and cannot trade
state-contingent insurance. Each household supplies productivity $z$ units of
effective labor and saves in an asset backed by productive capital. There is no
aggregate risk. Preferences are

$$\mathbb E_0\sum_{t=0}^\infty\beta^t u(c_t),\qquad u(c)=\log c.$$

## Household problem at given prices

Productivity takes values in $\mathcal Z\subset(0,\infty)$, with transition matrix
$P_z[j,j']=\Pr(z_{t+1}=z_{j'}\mid z_t=z_j)$. Rows sum to one.

| Object | Definition |
| --- | --- |
| State | individual assets and productivity $(k,z)$, $k\geq0$ |
| Action | next assets $0\leq k'<(1+r)k+wz$ |
| Budget | $c+k'=(1+r)k+wz$ |
| Saving policy | $\sigma(k,z)=k'$ |
| Consumption | $c_\sigma(k,z)=(1+r)k+wz-\sigma(k,z)$ |
| Transition | next assets equal $k'$; next productivity follows $P_z$ |

The household takes $r,w$ as given. Here $r$ is net interest and $1+r$ is the
gross return. Individual $k$ differs from aggregate capital $K$.

$$V(k,z)=\max_{0\leq k'<(1+r)k+wz}
\left\{\log((1+r)k+wz-k')+\beta\sum_{z'}P_z(z'\mid z)V(k',z')\right\}.$$

Define the Euler gap at the optimal policy:

$$D(k,z)=\frac1{c_\sigma(k,z)}-
\beta(1+r)\sum_{z'}P_z(z'\mid z)\frac1{c_\sigma(\sigma(k,z),z')}.$$

The borrowing constraint implies complementarity:

$$\sigma(k,z)\geq0,\qquad D(k,z)\geq0,\qquad \sigma(k,z)D(k,z)=0.$$

Interior saving has zero gap. At zero saving the gap may be positive: the household
would like to consume more now but cannot borrow. Equality must not be imposed
at every state. Feasibility and a transversality condition are also required for
infinite-horizon optimality.

## Firms and stationary equilibrium

Production is $Y=AK^\alpha L^{1-\alpha}$. Given trial $K>0$ and effective labor $L$,

$$r(K)=\alpha A(K/L)^{\alpha-1}-\delta,\qquad
w(K)=(1-\alpha)A(K/L)^\alpha.$$

Find the stationary productivity probabilities $\pi=\pi P_z$, $\sum_j\pi_j=1$,
and set $L=\sum_j\pi_jz_j$. This labor supply is fixed across trials for $K$.

The theoretical population distribution $\mu$ evolves under the policy-induced
transition kernel $P^\sigma$. Stationarity requires $\mu=\mu P^\sigma$.
Capital supply is $K^s=\int k\,d\mu(k,z)$. A stationary equilibrium satisfies
household optimality, firm optimality, stationarity and $K^s=K$.

## Baseline configuration

```python
A = 1.0
alpha = 0.36
beta = 0.96
delta = 0.08
z = (0.5, 1.5)
P_z = ((0.9, 0.1), (0.1, 0.9))
asset_lower = 0.0
asset_upper = 60.0
nodes = 500
capital_bracket = (6.0, 12.0)
```

Here $\pi=(0.5,0.5)$ and $L=1$. Use the quadratic grid
$k_i=60[i/(N-1)]^2$, $i=0,\ldots,N-1$. The denser lower end resolves the borrowing
region. The upper endpoint is artificial; diagnose its effect and expand it when
needed. Check the capital bracket numerically; it is an initial guess, not a theorem.
For these baseline price trials, require $\beta(1+r)<1$; this is a useful household
stationarity restriction, not by itself a proof of equilibrium existence or uniqueness.

See [time iteration](../algorithms/time_iteration.md) for household solution and
[stationary equilibrium](../algorithms/stationary_equilibrium.md) for distribution
and market clearing. These numbers are a teaching calibration, not an empirical
replication of Aiyagari (1994).
