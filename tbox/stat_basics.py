"""Basic statistical helper functions."""

import numpy as np

from typing_extensions import Literal

__all__ = ["compute_rmse"]


def compute_rmse(s, s_ref, normalized:bool=True, ntype:Literal["vrange", "mean"]="vrange"):
    """Compute the root mean square error between values and references.

    Parameters
    ----------
    s : scalar or array-like
        Values to compare against ``s_ref``.
    s_ref : scalar or array-like
        Reference values. For array-like inputs, the RMSE is computed along
        axis 0.
    normalized : bool, default=True
        If ``True``, return a percentage normalized by either the reference
        value range or mean.
    ntype : {"vrange", "mean"}, default="vrange"
        Normalization method for array-like inputs. ``"vrange"`` divides by
        ``max(s_ref) - min(s_ref)``; ``"mean"`` divides by ``mean(s_ref)``.

    Returns
    -------
    float or numpy.ndarray
        RMSE value. When ``normalized`` is ``True``, the result is expressed as
        a percentage.
    """
    if not np.iterable(s):
        rmse_ = np.abs(s-s_ref)
        if normalized:
            rmse_ /= s_ref
            rmse_ *= 100
        return rmse_
    s = np.asarray(s)
    s_ref = np.asarray(s_ref)
    error = s-s_ref
    rmse_ = np.mean(error**2, axis=0)**0.5
    if normalized:
        if ntype == "vrange":
            rmse_ /= (np.max(s_ref)-np.min(s_ref))
        else:
            rmse_ /= (np.mean(s_ref))
        rmse_ *= 100
    return rmse_
