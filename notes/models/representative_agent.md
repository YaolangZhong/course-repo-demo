# Representative-agent consumption and saving

A household owns capital $k_t$, supplies one unit of labor and maximizes

$$
\sum_{t=0}^\infty \beta^t u(c_t),\qquad u(c)=\log c,\qquad 0<\beta<1.
$$

Competitive firms produce $Y=AK^\alpha L^{1-\alpha}$ from aggregate capital $K$ and
labor $L=1$, with $A>0$ and $0<\alpha<1$; write $f(K)=AK^\alpha$. Capital depreciates
at rate $0<\delta\leq1$.

## Competitive equilibrium and the allocation problem

The price-taking household faces the budget $c_t+k_{t+1}=(1+r_t)k_t+w_t$, where $r_t$
is net interest and $w_t$ the wage. Firm optimality gives

$$
r_t=f'(K_t)-\delta,\qquad w_t=f(K_t)-K_tf'(K_t).
$$

A competitive equilibrium requires household optimality, firm optimality and market
clearing; the representative household holds all capital, $k_t=K_t$. Substituting
prices into the budget gives the resource constraint

$$
c_t+k_{t+1}=f(k_t)+(1-\delta)k_t.
$$

Compute the equilibrium allocation by maximizing the household objective subject to
this constraint, feasibility and the transversality condition
$\lim_{T\to\infty}\beta^T u'(c_T)k_{T+1}=0$; then recover prices from the allocation.

## States, actions, rewards and transitions

| Object | Definition |
| --- | --- |
| State | individual capital $k\in(0,\infty)$ |
| Action | next capital $k'$, with $0\lt k'\lt f(k)+(1-\delta)k$ |
| Reward | $u(c)$, with $c=f(k)+(1-\delta)k-k'$ |
| Transition | next capital equals the chosen $k'$ |
| Policy | saving $\sigma(k)=k'$ |
| Consumption | $c_\sigma(k)=f(k)+(1-\delta)k-\sigma(k)$ |

The state space is unbounded; a numerical grid is an approximation, not an economic
constraint. Zero capital is excluded because it yields no output and $\log 0$ is not
finite.

## Bellman and Euler equations

$$
V(k)=\max_{0<k'<f(k)+(1-\delta)k}\left\lbrace u(f(k)+(1-\delta)k-k')+\beta V(k')\right\rbrace .
$$

At an interior optimum the first-order condition is $u'(c)=\beta V'(k')$ and the
envelope condition is $V'(k)=[f'(k)+1-\delta]u'(c)$. With $u'(c)=1/c$ they give the
Euler equation

$$
\frac1{c_t}=\beta[f'(k_{t+1})+1-\delta]\frac1{c_{t+1}}.
$$

Current marginal utility equals the discounted gross return times future marginal
utility. The gross return $f'(k_{t+1})+1-\delta=1+r_{t+1}$ depends on next capital; it
is not a fixed interest rate.

## Baseline configuration

```python
A = 1.0
alpha = 0.36
beta = 0.96
delta = 0.08
nodes = 300
```

`nodes` is the number of capital grid points $N$. The positive steady state is

$$
k^{\ast}=\left(\frac{\alpha A}{1/\beta-1+\delta}\right)^{1/(1-\alpha)},\qquad c^{\ast}=f(k^{\ast})-\delta k^{\ast}.
$$

Use an evenly spaced capital grid on $[0.05k^{\ast},2k^{\ast}]$. Repeat with 600 nodes
and a wider interval to assess approximation error. Simulate 150 periods from
$0.5k^{\ast}$ and $1.5k^{\ast}$, report consumption, saving and prices, and check
whether the paths approach the steady state.

As a separate test case, full depreciation ($\delta=1$) has the closed-form policy

$$
\sigma(k)=\alpha\beta Ak^\alpha,\qquad c_\sigma(k)=(1-\alpha\beta)Ak^\alpha.
$$

It does not apply to the baseline, which has partial depreciation. See
[time iteration](../algorithms/time_iteration.md) for the numerical update.
