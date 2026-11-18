"""McCall job search as a finite MDP; see notes/models/mccall.md."""
import numpy as np

from .mdp import MDP

ACCEPT, REJECT, WORK = 0, 1, 2  # action columns


class McCallModel(MDP):
    """States ("U", w) then ("E", w), one of each per wage offer w."""

    def __init__(self, wages=(1, 2, 3, 4, 5),
                 probabilities=(0.1, 0.2, 0.4, 0.2, 0.1), benefit=1.0, beta=0.9):
        self.wages = np.array(wages, dtype=float)
        self.q = np.array(probabilities, dtype=float)
        self.benefit = benefit
        W = len(self.wages)
        states = [("U", w) for w in self.wages.tolist()] + [("E", w) for w in self.wages.tolist()]
        actions = np.tile(["accept", "reject", "work"], (2 * W, 1))
        feasible = np.zeros((2 * W, 3), dtype=bool)
        rewards = np.zeros((2 * W, 3))
        P = np.zeros((2 * W, 3, 2 * W))
        for i, w in enumerate(self.wages):
            U, E = i, W + i  # rows of ("U", w) and ("E", w)
            feasible[U, [ACCEPT, REJECT]] = True
            rewards[U, ACCEPT] = w
            P[U, ACCEPT, E] = 1          # accept: employed at w
            rewards[U, REJECT] = benefit
            P[U, REJECT, :W] = self.q    # reject: new offer w' with probability q(w')
            feasible[E, WORK] = True
            rewards[E, WORK] = w
            P[E, WORK, E] = 1            # work: employment is permanent
        super().__init__(states, actions, rewards, P, beta, feasible)
