# TBOX

TBOX is a small Python utility library for scientific plotting and basic statistics.
It currently provides helpers for Matplotlib styling, custom legends, gradients,
colored arrows, and RMSE computation.

## Installation

From a local checkout:

```bash
python -m pip install .
```

For development:

```bash
python -m pip install -e ".[dev,examples]"
```

## Quick Start

```python
import matplotlib.pyplot as plt
import numpy as np

from tbox import compute_rmse, rainbowarrow, set_plt

set_plt(font_size=12)

y_ref = np.array([1.0, 2.0, 3.0])
y = np.array([1.1, 2.2, 2.8])
print(compute_rmse(y, y_ref))

fig, ax = plt.subplots()
rainbowarrow(ax, start=(0, 0), end=(1, 1), cmap=("tab:blue", "tab:orange"))
plt.show()
```

## Package Contents

- `tbox.stat_basics`: statistical helper functions.
- `tbox.plot_utils`: Matplotlib styling and plotting utilities.
- `examples/`: notebooks showing selected plotting helpers.

## Development

Useful checks before publishing changes:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m compileall tbox
python -m build
```

## License

This project is distributed under the MIT License. See `LICENSE`.
