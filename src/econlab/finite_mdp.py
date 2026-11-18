"""VFI, PFI and GPI for finite discounted MDPs; see notes/algorithms/finite_mdp.md."""
from time import perf_counter

import numpy as np

from .mdp import check_mdp


def action_values(model, V):
    """Q_V(s, a) = R(s, a) + beta * sum_s' P(s' | s, a) V(s'), and -inf where infeasible."""
    return np.where(model.feasible, model.rewards + model.beta * (model.P @ V), -np.inf)


def greedy(Q, sigma):
    """Greedy policy for Q: keep sigma(s) on an exact tie, else the first maximizing column."""
    rows = np.arange(len(sigma))
    return np.where(Q[rows, sigma] == Q.max(axis=1), sigma, Q.argmax(axis=1))


class _Solver:
    """Input checks, initialization and result format shared by the three solvers."""

    def __init__(self, epsilon=1e-6, max_iter=10000):
        if not 0 < epsilon < np.inf or max_iter < 1:
            raise ValueError('Require positive epsilon and max_iter')
        self.epsilon, self.max_iter = epsilon, max_iter

    def _initialize(self, model):
        """Return V_0 = 0, sigma_0 = first feasible action, (1 - beta) * epsilon, start time."""
        check_mdp(model)
        return (np.zeros(len(model.states)), model.feasible.argmax(axis=1),
                (1 - model.beta) * self.epsilon, perf_counter())

    def _result(self, model, V, sigma, residual, started, iterations,
                evaluation_sweeps=0, linear_solves=0):
        """Result dictionary for a value array V whose residual rho(V) passed the check."""
        return dict(values=V, policy_indices=sigma,
                    policy=model.actions[np.arange(len(sigma)), sigma],
                    residual=float(residual), error_bound=float(residual) / (1 - model.beta),
                    converged=True, iterations=iterations,
                    evaluation_sweeps=evaluation_sweeps, linear_solves=linear_solves,
                    seconds=perf_counter() - started)


class VFI(_Solver):
    """Value function iteration: Section 1 of the note."""

    def solve(self, model):
        V, sigma, threshold, started = self._initialize(model)  # Step 1
        for n in range(self.max_iter):
            Q = action_values(model, V)                         # Step 2: Q_n
            V_new, sigma = Q.max(axis=1), greedy(Q, sigma)      # Step 3: V_{n+1}, sigma_{n+1}
            residual = np.max(np.abs(V_new - V))                # Step 4: rho(V_n)
            if residual <= threshold:                           # Steps 5-6: return the checked V_n
                return self._result(model, V, sigma, residual, started, iterations=n + 1)
            V = V_new
        raise RuntimeError('VFI reached max_iter without convergence')


class PFI(_Solver):
    """Policy function iteration: Section 2 of the note."""

    def solve(self, model):
        V, sigma, threshold, started = self._initialize(model)  # Step 1
        rows = np.arange(len(V))
        for n in range(self.max_iter):
            # Step 2: solve (I - beta P^sigma) V = R^sigma
            V = np.linalg.solve(np.eye(len(V)) - model.beta * model.P[rows, sigma],
                                model.rewards[rows, sigma])
            Q = action_values(model, V)
            sigma_new = greedy(Q, sigma)                        # Step 3
            if np.array_equal(sigma_new, sigma):                # Step 4
                residual = np.max(np.abs(Q.max(axis=1) - V))    # Step 5: rho(V_n)
                if not residual <= threshold:
                    raise RuntimeError('PFI: stable policy fails the Bellman residual check')
                return self._result(model, V, sigma, residual, started, iterations=n + 1,
                                    linear_solves=n + 1)
            sigma = sigma_new
        raise RuntimeError('PFI reached max_iter without convergence')


class GPI(_Solver):
    """Modified policy iteration with m = evaluation_sweeps: Section 3 of the note."""

    def __init__(self, epsilon=1e-6, max_iter=10000, evaluation_sweeps=3):
        super().__init__(epsilon, max_iter)
        if not isinstance(evaluation_sweeps, int) or evaluation_sweeps < 1:
            raise ValueError('evaluation_sweeps must be a positive integer')
        self.evaluation_sweeps = evaluation_sweeps

    def solve(self, model):
        V, sigma, threshold, started = self._initialize(model)  # Step 1
        rows = np.arange(len(V))
        for n in range(self.max_iter):
            sigma = greedy(action_values(model, V), sigma)      # Step 2: sigma_{n+1}
            for _ in range(self.evaluation_sweeps):             # Step 3: W_{j+1} = T_sigma W_j
                V = model.rewards[rows, sigma] + model.beta * (model.P[rows, sigma] @ V)
            Q = action_values(model, V)                         # Step 4: V_{n+1} = W_m
            residual = np.max(np.abs(Q.max(axis=1) - V))        # rho(V_{n+1})
            if residual <= threshold:                           # Step 5: return the checked V_{n+1}
                return self._result(model, V, greedy(Q, sigma), residual, started,
                                    iterations=n + 1,
                                    evaluation_sweeps=(n + 1) * self.evaluation_sweeps)
        raise RuntimeError('GPI reached max_iter without convergence')
