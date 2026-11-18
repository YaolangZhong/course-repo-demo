# McCall job search

An unemployed worker observes a wage offer $w$ and chooses whether to accept it.
Offers are independent draws from a finite set $\mathcal W$ with probabilities $q(w)$.
Accepting pays $w$ now and in every later period; employment is permanent. Rejecting
pays the unemployment benefit $b$ now and brings a new offer next period. The worker
maximizes expected discounted income with discount factor $0<\beta<1$.

## States, actions, rewards and transitions

The full state is $(U,w)$ for an unemployed worker holding offer $w$ and $(E,w)$ for a
worker employed at wage $w$:

$$
S=\lbrace (U,w),(E,w):w\in\mathcal W\rbrace .
$$

| State | Feasible action | Reward | Next state |
| --- | --- | --- | --- |
| $(U,w)$ | accept | $w$ | $(E,w)$ with probability 1 |
| $(U,w)$ | reject | $b$ | $(U,w')$ with probability $q(w')$ |
| $(E,w)$ | work | $w$ | $(E,w)$ with probability 1 |

All other transition probabilities are zero. There is no job separation, no saving and
no search cost.

## Bellman equation

Employment is absorbing, so $V^\sigma((E,w))=w/(1-\beta)$ under every policy $\sigma$.
The optimal value of an unemployed worker satisfies

$$
V^{\ast}((U,w))=\max\left\lbrace \frac{w}{1-\beta},\ b+\beta\sum_{w'\in\mathcal W}q(w')V^{\ast}((U,w'))\right\rbrace .
$$

Accepting is optimal exactly when $w\geq\bar w$, where the reservation wage is

$$
\bar w=(1-\beta)\left[b+\beta\sum_{w'\in\mathcal W}q(w')V^{\ast}((U,w'))\right].
$$

## Baseline configuration

Baseline values of $\mathcal W$, $q$, $b$ and $\beta$, named as in `McCallModel`:

```python
wages = (1, 2, 3, 4, 5)
probabilities = (0.1, 0.2, 0.4, 0.2, 0.1)
benefit = 1.0
beta = 0.9
```
