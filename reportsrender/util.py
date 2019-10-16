"""
Helper functions for the render scripts.
"""

import os
import shlex


def _set_cpus(n_cpus):
    """Set environment variables for numba and numpy """
    n_cpus = str(n_cpus)
    os.environ["MKL_THREADING_LAYER"] = "GNU"
    os.environ["MKL_NUM_cpus"] = n_cpus
    os.environ["NUMEXPR_NUM_cpus"] = n_cpus
    os.environ["OMP_NUM_cpus"] = n_cpus
    os.environ["NUMBA_NUM_cpus"] = n_cpus


def _parse_params(params):
    """Parse a whitespace-separated key-value list into a dictionary"""
    return dict(token.split("=") for token in shlex.split(params))
