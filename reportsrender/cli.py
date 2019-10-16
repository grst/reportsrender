"""reportsrender

Execute and render a jupyter/Rmarkdown notebook.

Usage:
  reportsrender <engine> <notebook> <out_file> [options]
  reportsrender --help

Options:
  -h --help             Show this screen.
  --cpus=<cpus>         Number of CPUs to use for Numba/Numpy/OpenBLAS/MKL [default: 1]
  --params=<params>     space-separated list of key-value pairs that will be passed
                        to papermill/Rmarkdown.
                        E.g. "input_file=dir/foo.txt output_file=dir2/bar.html"

Possible engines are:
    rmd             Use `rmarkdown` to execute the notebook. Supports R and
                    python (through reticulate)
    papermill       User `papermill` to execute the notebook. Works for every
                    kernel available in the jupyter installation.

"""

from docopt import docopt
from .util import _set_cpus, _parse_params
from .papermill import render_papermill
from .rmd import render_rmd
import sys


def main():
    arguments = docopt(__doc__)
    params = (
        _parse_params(arguments["--params"])
        if arguments["--params"] is not None
        else dict()
    )
    _set_cpus(arguments["--cpus"])

    if arguments["<engine>"] == "rmd":
        render_rmd(arguments["<notebook>"], arguments["<out_file>"], params)
    elif arguments["<engine>"] == "papermill":
        render_papermill(arguments["<notebook>"], arguments["<out_file>"], params)
    else:
        print(
            "Please specify a valid engine. See `reportsrender --help` for more details. ",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
