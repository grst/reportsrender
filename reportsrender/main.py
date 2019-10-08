"""render_papermill.py

Execute and render a jupyter/jupytext notebook using papermill.

Usage:
  render_papermill.py <notebook> <out_file> [options]
  render_papermill.py (-h | --help)

Options:
  -h --help             Show this screen.
  --cpus=<cpus>         Number of CPUs to use for Numba/Numpy. [default: 1]
  --params=<params>     space-separated list of key-value pairs. E.g.
                        "input_file=dir/foo.txt output_file=dir2/bar.html"

"""

from docopt import docopt
from .util import set_cpus, parse_params
from .papermill import render_papermill
from .rmd import render_rmd

if __name__ == "__main__":
    arguments = docopt(__doc__)
    params = parse_params(arguments["--params"])

    set_cpus(arguments["--cpus"])

    render_papermill(arguments["<notebook>"], arguments["<out_file>"], params)
