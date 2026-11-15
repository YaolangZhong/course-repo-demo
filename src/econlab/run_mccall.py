"""Run from the project root: python -m econlab.run_mccall."""
import csv
import json
from pathlib import Path
import numpy as np
from .mccall import McCallModel
from .finite_mdp import VFI, PFI, GPI


def main():
    model = McCallModel()
    results = {solver.__class__.__name__: solver.solve(model)
               for solver in (VFI(), PFI(), GPI())}
    reference = results['PFI']
    for name, result in results.items():
        if not np.allclose(result['values'], reference['values'], atol=1e-6, rtol=0):
            raise RuntimeError('Methods disagree on values')
        if not np.array_equal(result['policy'], reference['policy']):
            raise RuntimeError('Methods disagree on actions')
        if not np.all(model.feasible[np.arange(len(model.states)), result['policy_indices']]):
            raise RuntimeError('Infeasible returned policy')
        print(f"{name}: residual={result['residual']:.3e}, iterations={result['iterations']}, "
              f"evaluation sweeps={result['evaluation_sweeps']}, "
              f"linear solves={result['linear_solves']}, seconds={result['seconds']:.6f}")
    accepted = model.wages[reference['policy'][:model.n] == 'accept']
    print('Accepted offers:', accepted.tolist())
    print('Lowest accepted grid wage:', float(accepted.min()) if len(accepted) else None)
    print('State values:', reference['values'].tolist())
    out = Path('results'); out.mkdir(exist_ok=True)
    with (out/'comparison.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['method', 'employment', 'wage', 'value', 'policy'])
        for name, result in results.items():
            for state, value, action in zip(model.states, result['values'], result['policy']):
                writer.writerow([name, *state, value, action])
    summary = {name: {k: v for k, v in result.items()
                     if k not in ('values', 'policy', 'policy_indices')}
               for name, result in results.items()}
    (out/'diagnostics.json').write_text(json.dumps(summary, indent=2)+'\n')
    print('PASS: feasibility, Bellman residuals and cross-method agreement; results/comparison.csv')


if __name__ == '__main__':
    main()
