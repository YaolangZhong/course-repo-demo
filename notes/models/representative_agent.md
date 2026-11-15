# Representative-agent consumption and saving

A household owns capital, supplies one unit of labor, and maximizes

$$\sum_{t=0}^\infty \beta^t u(c_t),\qquad u(c)=\log c,\quad 0<\beta<1.$$

Competitive firms produce $f(k)=Ak^\alpha$, where $A>0$ and $0<\alpha<1$.
Capital depreciates at rate $\delta$. Output allocation and accumulation are

$$c_t+i_t=f(k_t),\qquad k_{t+1}=(1-\delta)k_t+i_t.$$

Eliminating investment gives the economy-wide resource constraint:

$$c_t+k_{t+1}=f(k_t)+(1-\delta)k_t.$$

## Competitive equilibrium and the allocation problem

The price-taking household faces $c_t+k_{t+1}=(1+r_t)k_t+w_t$.
Firm optimality gives

$$r_t=f'(k_t)-\delta,\qquad w_t=f(k_t)-k_tf'(k_t).$$

Competitive equilibrium requires household optimality, firm optimality and
capital, labor and goods market clearing. Substituting factor prices into
the household budget recovers the resource constraint. Compute the equilibrium
allocation by maximizing the same household objective subject to that constraint;
then recover prices. Require feasibility and the transversality condition
$\lim_{T\to\infty}\beta^T u'(c_T)k_{T+1}=0$.

## States, actions, rewards and transitions

| Object | Definition |
| --- | --- |
| State | $k\in(0,\infty)$ |
| Action | next capital $k'$, with $0<k'<f(k)+(1-\delta)k$ |
| Reward | $R(k,k')=\log(f(k)+(1-\delta)k-k')$ |
| Transition | next capital equals the chosen $k'$ |
| Saving policy | $\sigma(k)=k'$ |
| Consumption | $c_\sigma(k)=f(k)+(1-\delta)k-\sigma(k)$ |

The theoretical state space is unbounded. A finite numerical grid below is an
approximation, not a new economic constraint. Zero capital is excluded: with no
capital there is no output and log consumption is not finite.

## Bellman, envelope and Euler equations

The deterministic transition reduces the conditional expectation to $V(k')$:

$$V(k)=\max_{0<k'<f(k)+(1-\delta)k}
\{u(f(k)+(1-\delta)k-k')+\beta V(k')\}.$$

At an interior optimum, differentiating with respect to $k'$ gives
$u'(c_t)=\beta V_k(k_{t+1})$. The envelope condition is

$$V_k(k_t)=[f'(k_t)+1-\delta]u'(c_t).$$

Together they imply

$$\frac1{c_t}=\beta\,[\alpha A k_{t+1}^{\alpha-1}+1-\delta]\frac1{c_{t+1}}.$$

Current marginal utility equals the discounted marginal return times future
marginal utility. The return depends on next capital; it is not a fixed interest
rate in this allocation problem.

## Baseline configuration

```python
A = 1.0
alpha = 0.36
beta = 0.96
delta = 0.08
nodes = 300
```

The positive steady state satisfies

$$k^*=\left(\frac{\alpha A}{1/\beta-1+\delta}\right)^{1/(1-\alpha)},
\qquad c^*=A(k^*)^\alpha-\delta k^*.$$

Use an evenly spaced capital grid on $[0.05k^*,2k^*]$ initially. Repeat with
600 nodes and a wider interval to assess approximation error. Simulate 150
periods from $0.5k^*$ and $1.5k^*$, reporting consumption, saving and prices.
Check whether the paths approach the analytical steady state.

An independent analytical check uses **full depreciation**, $\delta=1$,
as a separate test case:

$$\sigma^*(k)=\alpha\beta A k^\alpha,\qquad
c^*(k)=(1-\alpha\beta)A k^\alpha.$$

The baseline has partial depreciation; this closed-form policy does not apply to it.
See [time iteration](../algorithms/time_iteration.md) for the numerical update.
