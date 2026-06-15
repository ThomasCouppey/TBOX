import numpy as np

from tbox import compute_rmse


def test_compute_rmse_scalar():
    assert compute_rmse(2, 1, normalized=False) == 1


def test_compute_rmse_accepts_array_like_values():
    assert np.isclose(
        compute_rmse([1, 2], [1, 1], normalized=False),
        np.sqrt(0.5),
    )


def test_compute_rmse_normalized_by_reference_range():
    value = compute_rmse([1, 3], [1, 2], normalized=True)

    assert np.isclose(value, np.sqrt(0.5) * 100)

