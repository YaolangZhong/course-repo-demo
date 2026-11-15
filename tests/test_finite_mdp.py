"""Economic and numerical behavior checks independent of solver implementation."""
import unittest
from types import SimpleNamespace
import numpy as np
from econlab.mccall import McCallModel
from econlab.finite_mdp import VFI, PFI, GPI


class FiniteMDPChecks(unittest.TestCase):
    def test_mccall_analytical_solution(self):
        model = McCallModel()
        # Assuming offers 4 and 5 are accepted, solve the scalar rejection recursion.
        reject = (1 + .9*(.2*4 + .1*5)/.1)/(1-.9*.7)
        self.assertTrue(30 < reject < 40)  # Verify that the assumed threshold is consistent.
        expected = np.r_[np.maximum(model.wages/.1, reject), model.wages/.1]
        for solver in (VFI(), PFI(), GPI(), GPI(evaluation_sweeps=1)):
            with self.subTest(solver=solver):
                result = solver.solve(model)
                np.testing.assert_allclose(result['values'], expected, atol=1e-6, rtol=0)
                self.assertEqual(result['policy'][:5].tolist(), ['reject']*3+['accept']*2)
                self.assertEqual(result['policy'][5:].tolist(), ['work']*5)
                self.assertLessEqual(result['residual'], (1-model.beta)*solver.epsilon)

    def test_generic_mdp_mask_and_exact_tie(self):
        # No model class dependency. A masked action promises a deliberately huge reward.
        model = SimpleNamespace(states=['s'], actions=np.array([['bad', 'a', 'b']]),
                                feasible=np.array([[False, True, True]]),
                                rewards=np.array([[1000., 2., 2.]]),
                                P=np.ones((1,3,1)), beta=.5)
        for solver in (VFI(), PFI(), GPI()):
            result = solver.solve(model)
            self.assertAlmostEqual(result['values'][0], 4, delta=1e-6)
            self.assertEqual(result['policy'].tolist(), ['a'])
        model.beta = 0
        self.assertEqual(VFI().solve(model)['values'][0], 2)

    def test_iteration_cap_is_failure(self):
        for solver in (VFI(max_iter=1), PFI(max_iter=1), GPI(max_iter=1)):
            with self.assertRaises(RuntimeError):
                solver.solve(McCallModel())

    def test_invalid_transition_rejected(self):
        model = McCallModel()
        model.P[0,0,:] = 0
        for solver in (VFI(), PFI(), GPI()):
            with self.assertRaises(ValueError):
                solver.solve(model)
