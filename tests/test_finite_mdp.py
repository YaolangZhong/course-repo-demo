"""McCall and finite-MDP checks that do not rely on any one solver's output."""
import unittest
from types import SimpleNamespace

import numpy as np

from econlab.finite_mdp import GPI, PFI, VFI, action_values, greedy
from econlab.mccall import McCallModel

SOLVERS = (VFI, PFI, GPI)


def reservation_wage(wages, q, b, beta):
    """w-bar of notes/models/mccall.md in closed form, without an MDP solver.

    If exactly the offers wages[k:] are accepted, the value of rejecting, h, solves
    h = b + beta * (sum_{i<k} q_i * h + sum_{i>=k} q_i * w_i / (1 - beta)), and
    w-bar = (1 - beta) * h. Exactly one k accepts precisely the offers w >= w-bar.
    """
    consistent = []
    for k in range(len(wages) + 1):
        h = (b + beta * q[k:] @ wages[k:] / (1 - beta)) / (1 - beta * q[:k].sum())
        w_bar = (1 - beta) * h
        if np.all(wages[:k] < w_bar) and np.all(wages[k:] >= w_bar):
            consistent.append(w_bar)
    (w_bar,) = consistent
    return w_bar


class McCallChecks(unittest.TestCase):
    def test_model_arrays(self):
        model = McCallModel()
        self.assertEqual(model.states[0], ("U", 1.0))
        self.assertEqual(model.states[-1], ("E", 5.0))
        self.assertEqual(model.actions[model.feasible].tolist(),
                         ['accept', 'reject'] * 5 + ['work'] * 5)

    def test_solvers_match_reservation_wage(self):
        model = McCallModel()
        w_bar = reservation_wage(model.wages, model.q, model.benefit, model.beta)
        self.assertAlmostEqual(w_bar, 127 / 37, places=12)  # about 3.4324
        accept = model.wages >= w_bar
        self.assertEqual(model.wages[accept].tolist(), [4.0, 5.0])
        employed = model.wages / (1 - model.beta)
        expected = np.r_[np.where(accept, employed, w_bar / (1 - model.beta)), employed]
        rows = np.arange(len(model.states))
        for solver in (VFI(), PFI(), GPI(), GPI(evaluation_sweeps=1)):
            with self.subTest(solver=type(solver).__name__,
                              m=getattr(solver, 'evaluation_sweeps', None)):
                result = solver.solve(model)
                np.testing.assert_allclose(result['values'], expected, atol=1e-6, rtol=0)
                self.assertEqual(result['policy'].tolist(),
                                 np.where(accept, 'accept', 'reject').tolist() + ['work'] * 5)
                self.assertTrue(model.feasible[rows, result['policy_indices']].all())
                # Recompute rho(V) for the returned array rather than trusting the report.
                residual = np.max(np.abs(action_values(model, result['values']).max(axis=1)
                                         - result['values']))
                self.assertLessEqual(residual, (1 - model.beta) * solver.epsilon)
                self.assertAlmostEqual(result['residual'], residual, delta=1e-12)
                self.assertLessEqual(result['error_bound'], solver.epsilon)

    def test_work_counts(self):
        model = McCallModel()
        vfi, pfi = VFI().solve(model), PFI().solve(model)
        gpi = GPI(evaluation_sweeps=4).solve(model)
        self.assertEqual((vfi['evaluation_sweeps'], vfi['linear_solves']), (0, 0))
        self.assertEqual((pfi['evaluation_sweeps'], pfi['linear_solves']), (0, pfi['iterations']))
        self.assertEqual((gpi['evaluation_sweeps'], gpi['linear_solves']),
                         (4 * gpi['iterations'], 0))


class FiniteMDPChecks(unittest.TestCase):
    def test_other_mdp_without_model_class(self):
        # Two states, columns (stay, move, jump). "jump" is infeasible but would pay 1000.
        # Staying in s1 pays 1 forever (value 2); in s0 staying (0 + beta * 0) loses to
        # moving to s1 (0 + beta * 2 = 1).
        P = np.zeros((2, 3, 2))
        P[0, 0, 0] = P[1, 0, 1] = P[0, 1, 1] = P[1, 1, 0] = P[:, 2, 0] = 1
        model = SimpleNamespace(states=['s0', 's1'],
                                actions=np.array([['stay', 'move', 'jump']] * 2),
                                feasible=np.array([[True, True, False]] * 2),
                                rewards=np.array([[0., 0., 1000.], [1., 0., 1000.]]),
                                P=P, beta=0.5)
        for solver in SOLVERS:
            with self.subTest(solver=solver.__name__):
                result = solver().solve(model)
                np.testing.assert_allclose(result['values'], [1, 2], atol=1e-6, rtol=0)
                self.assertEqual(result['policy'].tolist(), ['move', 'stay'])

    def test_tie_rule(self):
        Q = np.array([[2., 2., -np.inf], [1., 2., 2.]])
        self.assertEqual(greedy(Q, np.array([1, 2])).tolist(), [1, 2])  # exact tie: keep
        self.assertEqual(greedy(Q, np.array([0, 0])).tolist(), [0, 1])  # else first maximizer
        nearly = np.array([[2., 2. + 1e-12]])
        self.assertEqual(greedy(nearly, np.array([0])).tolist(), [1])   # near-ties are not ties

    def test_max_iter_is_failure(self):
        for solver in SOLVERS:
            with self.subTest(solver=solver.__name__), self.assertRaises(RuntimeError):
                solver(max_iter=1).solve(McCallModel())

    def test_invalid_input_rejected(self):
        no_probability_row, no_feasible_action = McCallModel(), McCallModel()
        no_probability_row.P[0, 0, :] = 0
        no_feasible_action.feasible[0, :] = False
        for solver in SOLVERS:
            for model in (no_probability_row, no_feasible_action):
                with self.subTest(solver=solver.__name__), self.assertRaises(ValueError):
                    solver().solve(model)


if __name__ == '__main__':
    unittest.main()
