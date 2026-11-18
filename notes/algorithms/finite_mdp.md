# VFI, PFI and GPI

This note specifies three solvers for finite discounted Markov decision processes
(MDPs): value function iteration (VFI), policy function iteration (PFI) and generalized
policy iteration (GPI), implemented as modified policy iteration with a fixed number of
evaluation sweeps. They share the input format, conventions and numerical defaults
below and are implemented in [`finite_mdp.py`](../../src/econlab/finite_mdp.py).

## Common finite-MDP input

Let $S$ be a finite state set, $\mathcal A(s)$ a nonempty feasible action set, $R(s,a)$
a deterministic one-period reward, $P(s'\mid s,a)$ the transition kernel and
$\beta\in[0,1)$ the discount factor.

$$
Q_V(s,a)=R(s,a)+\beta\sum_{s'\in S}P(s'\mid s,a)V(s'),\qquad
(TV)(s)=\max_{a\in\mathcal A(s)}Q_V(s,a).
$$

For a deterministic policy $\sigma$, define $R^\sigma(s)=R(s,\sigma(s))$ and
$P^\sigma(s,s')=P(s'\mid s,\sigma(s))$. Then

$$
T_\sigma V=R^\sigma+\beta P^\sigma V,\qquad
(I-\beta P^\sigma)V^\sigma=R^\sigma.
$$

Arrays have one row per state and one column per action. A model object (for example
[`MDP`](../../src/econlab/mdp.py)) supplies the attributes below; the solvers must not
depend on a particular model class.

| Attribute | Shape | Meaning |
| --- | --- | --- |
| `states` | length `N` | State labels |
| `actions` | `(N, M)` | Action label of each column in each state |
| `feasible` | `(N, M)` | Boolean mask of allowed actions |
| `rewards` | `(N, M)` | One-period rewards |
| `P` | `(N, M, N)` | Current state, action column, next state |
| `beta` | scalar | Discount factor |

Each feasible transition row must be nonnegative and sum to one, and every state needs
a feasible action. Mask infeasible action values with $-\infty$ before maximizing.
Policies are stored as action **column indices**; results also report the corresponding
action labels.

Every evaluation sweep is simultaneous: compute all new values from the same old array.
Initialize values to zero and the policy to the first feasible action in each state. In
greedy selection, keep the current action when it attains the maximum exactly;
otherwise choose the first maximizing column. Do not treat nearly equal action values
as ties.

The Bellman residual is $\rho(V)=\lVert TV-V\rVert_\infty$. Defaults are target value
error `epsilon=1e-6` ($\epsilon$) and `max_iter=10000`. Every solver returns a value
array whose own residual has been checked, $\rho(V)\leq(1-\beta)\epsilon$, which
guarantees $\lVert V-V^{\ast}\rVert_\infty\leq\epsilon$. Reaching `max_iter` is a
failure, not a result.

Each solver class (`VFI`, `PFI`, `GPI`) has a `solve(model)` method returning a
dictionary with `values`, `policy_indices`, `policy` (action labels), `residual`,
`error_bound` $=\rho(V)/(1-\beta)$, `converged`, `iterations`, `evaluation_sweeps`,
`linear_solves` and `seconds`. `iterations` counts passes through the main loop;
`evaluation_sweeps` and `linear_solves` are totals over the whole run.

## 1. Value function iteration (VFI)

0. **Input:** the MDP, $\epsilon$ and `max_iter`.
1. **Initialize:** $V_0=0$, the initial policy $\sigma_0$ (used only for ties) and $n=0$.
2. **Compute action values:** $Q_n=Q_{V_n}$.
3. **Update:** $V_{n+1}(s)=\max_{a\in\mathcal A(s)}Q_n(s,a)$ in a new array, and
   $\sigma_{n+1}$ greedy with respect to $Q_n$ (tie rule relative to $\sigma_n$).
4. **Measure:** $\rho(V_n)=\lVert V_{n+1}-V_n\rVert_\infty$.
5. **Stop or repeat:** if $\rho(V_n)\leq(1-\beta)\epsilon$, go to Step 6. Otherwise
   increment $n$ and return to Step 2.
6. **Return:** $V_n$ and $\sigma_{n+1}$.

The returned array is $V_n$, whose residual was just measured, not the unchecked update
$V_{n+1}$. Checking and returning $V_{n+1}$ would be equally valid; what matters is
that the checked and returned arrays coincide.

## 2. Policy function iteration (PFI)

0. **Input:** the MDP, $\epsilon$ and `max_iter`.
1. **Initialize:** the initial policy $\sigma_0$ and $n=0$.
2. **Evaluate fully:** solve $(I-\beta P^{\sigma_n})V_n=R^{\sigma_n}$, so
   $V_n=V^{\sigma_n}$. Use a linear-system solver, not a matrix inverse.
3. **Improve:** choose $\sigma_{n+1}$ greedy with respect to $Q_{V_n}$, using the tie rule.
4. **Stop or repeat:** if $\sigma_{n+1}=\sigma_n$, go to Step 5. Otherwise increment
   $n$ and return to Step 2.
5. **Check and return:** require $\rho(V_n)\leq(1-\beta)\epsilon$ and return $V_n$ and
   $\sigma_n$. If the policy is stable but this check fails, report a numerical failure.

One linear solve is a full policy evaluation, not one evaluation sweep.

## 3. Generalized policy iteration (GPI): finite-sweep MPI

GPI is the general interaction of policy evaluation and policy improvement. The solver
here is **modified policy iteration (MPI)**: each improvement is followed by $m$
evaluation sweeps (`evaluation_sweeps`, default $m=3$).

0. **Input:** the MDP, $\epsilon$, a positive integer $m$ and `max_iter`.
1. **Initialize:** $V_0=0$, the initial policy $\sigma_0$ and $n=0$.
2. **Improve:** choose $\sigma_{n+1}$ greedy with respect to $Q_{V_n}$, using the tie rule.
3. **Evaluate partially:** with $\sigma_{n+1}$ fixed, set $W_0=V_n$ and perform exactly
   $m$ simultaneous sweeps:

   $$W_{j+1}=R^{\sigma_{n+1}}+\beta P^{\sigma_{n+1}}W_j,\qquad j=0,\ldots,m-1.$$

4. **Update:** set $V_{n+1}=W_m$ and compute $Q_{V_{n+1}}$ and $\rho(V_{n+1})$.
5. **Stop or repeat:** if $\rho(V_{n+1})\leq(1-\beta)\epsilon$, return $V_{n+1}$ and a
   policy greedy with respect to $Q_{V_{n+1}}$. Otherwise increment $n$ and return to
   Step 2.

An unchanged policy is not a stopping rule here: its value may still be inaccurate. For
$m=1$ the value updates coincide with VFI, but VFI returns the checked $V_n$ and MPI
the checked $V_{n+1}$, so reported iteration counts can differ by one.
