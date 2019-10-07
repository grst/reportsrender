#!/usr/bin/env python3
"""render_rmd.py

Execute and render a parametrized Rmarkdown notebook.

Usage:
  render_rmd.py <notebook> <out_file> [options]
  render_rmd.py (-h | --help)

Options:
  -h --help             Show this screen.
  --cpus=<cpus>         Number of CPUs to use for Numba/Numpy. [default: 1]
  --params=<params>     space-separated list of key-value pairs. E.g.
                        "input_file=dir/foo.txt output_file=dir2/bar.html"

"""

from docopt import docopt
from util import set_cpus, parse_params
from subprocess import call
from shutil import copyfile
import os


def _literal_to_r_str(value):
    """Convert a python value to a corresponding R string"""
    _literal_to_str = {True: "TRUE", False: "FALSE", None: "NULL"}
    try:
        return _literal_to_str[value]
    except KeyError:
        # quote a string
        if isinstance(value, str):
            return "'{}'".format(value)
        else:
            return str(value)


def render_rmd(input_file, output_file, params=None):
    """
    Wrapper function to render an Rmarkdown document the way I want it to.
    In particular, this function uses a custom template and allows to pass
    parameters to a parametrized report.
    Args:
        input_file: path to input (Rmd) file
        output_file: path to output (html) file
        params: dictionary that will be passed to `params` arg of `rmarkdown::render`.
    """
    param_str = ""
    if params is not None:
        param_str = ", ".join(
            [
                "{}={}".format(key, _literal_to_r_str(value))
                for key, value in params.items()
            ]
        )

    # work around https://github.com/rstudio/rmarkdown/issues/1508
    tmp_input_file = input_file + ".copy.Rmd"
    copyfile(input_file, tmp_input_file, follow_symlinks=True)

    rmd_cmd = (
        "rmarkdown::render('{input_file}', "
        "   output_file='{output_file}', "
        "   output_format=rmdformats::material(self_contained=TRUE), "
        #        "   output_format=bookdown::html_document2(), "
        # "   knit_root_dir='{root_dir}', "
        "   params = list({params}))"
    ).format(
        input_file=os.path.abspath(tmp_input_file),
        output_file=os.path.abspath(output_file),
        params=param_str,
    )

    cmd = ["Rscript", "--vanilla", "-e", rmd_cmd]

    call(cmd)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    params = parse_params(arguments["--params"])

    set_cpus(arguments["--cpus"])

    render_rmd(arguments["<notebook>"], arguments["<out_file>"], params)
