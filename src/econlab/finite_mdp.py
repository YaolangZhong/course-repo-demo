"""Lab 6 finite discounted-MDP solvers; see notes/algorithms/finite_mdp.md."""
from time import perf_counter
import numpy as np


def action_values(model, values):
    return np.where(model.feasible,
                    model.rewards + model.beta * (model.P @ values), -np.inf)


def greedy(Q, policy):
    rows = np.arange(len(policy))
    # Retain the current action on an exact tie; otherwise first maximizer.
    return np.where(Q[rows, policy] == Q.max(axis=1), policy, Q.argmax(axis=1))


class VFI:
    def __init__(self, epsilon=1e-6, max_iter=10000):
        if not np.isfinite(epsilon) or epsilon <= 0 or max_iter < 1:
            raise ValueError('Require positive epsilon and max_iter')
        self.epsilon, self.max_iter = epsilon, max_iter

    def _start(self, model):
        if not 0 <= model.beta < 1:
            raise ValueError('Require 0 <= beta < 1')
        if not np.all(model.feasible.any(axis=1)):
            raise ValueError('Every state needs a feasible action')
        probabilities = model.P[model.feasible]
        if np.any(probabilities < 0) or not np.allclose(probabilities.sum(axis=1), 1):
            raise ValueError('Feasible transition rows must be probabilities')
        return (perf_counter(), np.zeros(len(model.states)),
                model.feasible.argmax(axis=1), (1-model.beta)*self.epsilon)

    def _result(self, model, values, policy, started, iterations, sweeps=0, solves=0):
        residual = float(np.max(abs(action_values(model, values).max(axis=1)-values)))
        if not np.isfinite(residual) or residual > (1-model.beta)*self.epsilon:
            raise RuntimeError('Returned value fails the Bellman residual check')
        return dict(values=values, policy_indices=policy,
                    policy=model.actions[np.arange(len(policy)), policy],
                    residual=residual, error_bound=residual/(1-model.beta),
                    converged=True, iterations=iterations, evaluation_sweeps=sweeps,
                    linear_solves=solves, seconds=perf_counter()-started)

    def solve(self, model):
        started, values, policy, threshold = self._start(model)
        for iteration in range(1, self.max_iter+1):
            Q = action_values(model, values)
            policy = greedy(Q, policy)
            updated = Q.max(axis=1)
            if np.max(abs(updated-values)) <= threshold:
                return self._result(model, values, policy, started, iteration)
            values = updated
        raise RuntimeError('VFI reached max_iter without convergence')


class PFI(VFI):
    def solve(self, model):
        started, values, policy, threshold = self._start(model)
        rows = np.arange(len(values))
        for iteration in range(1, self.max_iter+1):
            values = np.linalg.solve(np.eye(len(values))-model.beta*model.P[rows, policy],
                                     model.rewards[rows, policy])
            updated = greedy(action_values(model, values), policy)
            if np.array_equal(updated, policy):
                return self._result(model, values, policy, started, iteration,
                                    solves=iteration)
            policy = updated
        raise RuntimeError('PFI reached max_iter without convergence')


class GPI(VFI):
    """Modified policy iteration with a fixed number of evaluation sweeps."""
    def __init__(self, epsilon=1e-6, max_iter=10000, evaluation_sweeps=3):
        super().__init__(epsilon, max_iter)
        if not isinstance(evaluation_sweeps, int) or evaluation_sweeps < 1:
            raise ValueError('evaluation_sweeps must be a positive integer')
        self.evaluation_sweeps = evaluation_sweeps

    def solve(self, model):
        started, values, policy, threshold = self._start(model)
        rows = np.arange(len(values))
        for iteration in range(1, self.max_iter+1):
            policy = greedy(action_values(model, values), policy)
            for _ in range(self.evaluation_sweeps):
                values = model.rewards[rows, policy]+model.beta*(model.P[rows, policy] @ values)
            Q = action_values(model, values)
            if np.max(abs(Q.max(axis=1)-values)) <= threshold:
                return self._result(model, values, greedy(Q, policy), started, iteration,
                                    sweeps=iteration*self.evaluation_sweeps)
        raise RuntimeError('GPI reached max_iter without convergence')
