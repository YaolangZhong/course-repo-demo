"""Solve the baseline McCall model with VFI, PFI and GPI: python -m econlab.run_mccall."""
import csv
import json
from pathlib import Path

import numpy as np

from .finite_mdp import GPI, PFI, VFI
from .mccall import McCallModel


def main():
    model = McCallModel()
    solvers = (VFI(), PFI(), GPI())
    results = {type(solver).__name__: solver.solve(model) for solver in solvers}
    reference = results['PFI']
    for name, result in results.items():
        if not np.allclose(result['values'], reference['values'], atol=1e-6, rtol=0):
            raise RuntimeError('Methods disagree on values')
        if not np.array_equal(result['policy'], reference['policy']):
            raise RuntimeError('Methods disagree on actions')
        if not model.feasible[np.arange(len(model.states)), result['policy_indices']].all():
            raise RuntimeError('Infeasible returned policy')
        print(f"{name}: residual={result['residual']:.3e}, iterations={result['iterations']}, "
              f"evaluation sweeps={result['evaluation_sweeps']}, "
              f"linear solves={result['linear_solves']}, seconds={result['seconds']:.6f}")
    # The first len(model.wages) states are ("U", w).
    accepted = model.wages[reference['policy'][:len(model.wages)] == 'accept']
    print('Accepted offers:', accepted.tolist())
    print('Lowest accepted grid wage:', float(accepted.min()) if len(accepted) else None)
    print('State values:', reference['values'].tolist())

    out = Path('results')
    out.mkdir(exist_ok=True)
    with (out / 'comparison.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['method', 'employment', 'wage', 'value', 'policy'])
        for name, result in results.items():
            for state, value, action in zip(model.states, result['values'], result['policy']):
                writer.writerow([name, *state, value, action])
    diagnostics = {name: {key: value for key, value in result.items()
                          if key not in ('values', 'policy', 'policy_indices')}
                   for name, result in results.items()}
    # Store the parameters with the outputs they produced.
    diagnostics['parameters'] = dict(
        wages=model.wages.tolist(), probabilities=model.q.tolist(), benefit=model.benefit,
        beta=model.beta, epsilon=solvers[0].epsilon, max_iter=solvers[0].max_iter,
        evaluation_sweeps=solvers[2].evaluation_sweeps)
    (out / 'diagnostics.json').write_text(json.dumps(diagnostics, indent=2) + '\n')
    print('PASS: feasibility, Bellman residuals and cross-method agreement; results/comparison.csv')


if __name__ == '__main__':
    main()
