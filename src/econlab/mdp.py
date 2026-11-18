"""Common finite-MDP input; see notes/algorithms/finite_mdp.md."""
import numpy as np


def check_mdp(model):
    """Raise ValueError unless model satisfies the note's common finite-MDP input."""
    N, M = len(model.states), model.rewards.shape[-1]
    if not (model.actions.shape == model.feasible.shape == model.rewards.shape == (N, M)
            and model.P.shape == (N, M, N)):
        raise ValueError('Require actions, feasible and rewards of shape (N, M) '
                         'and P of shape (N, M, N)')
    if not 0 <= model.beta < 1:
        raise ValueError('Require 0 <= beta < 1')
    if not model.feasible.any(axis=1).all():
        raise ValueError('Every state needs a feasible action')
    if not np.isfinite(model.rewards[model.feasible]).all():
        raise ValueError('Feasible rewards must be finite')
    rows = model.P[model.feasible]  # one row P(. | s, a) per feasible pair (s, a)
    if (rows < 0).any() or not np.allclose(rows.sum(axis=1), 1):
        raise ValueError('Feasible transition rows must be probabilities')


class MDP:
    """Finite MDP stored as arrays with one row per state and one column per action."""

    def __init__(self, states, actions, rewards, P, beta, feasible=None):
        self.states = states                              # length N: state labels
        self.actions = np.asarray(actions)                # (N, M): action labels
        self.rewards = np.asarray(rewards, dtype=float)   # (N, M): R(s, a)
        self.P = np.asarray(P, dtype=float)               # (N, M, N): P(s' | s, a)
        self.beta = beta
        self.feasible = (np.ones(self.rewards.shape, dtype=bool) if feasible is None
                         else np.asarray(feasible, dtype=bool))  # (N, M): a in A(s)
        check_mdp(self)
