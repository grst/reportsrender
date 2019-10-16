from subprocess import check_call
from shutil import copyfile
from tempfile import NamedTemporaryFile, TemporaryDirectory
from .pandoc import run_pandoc, RES_PATH
import os
import re


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


def _run_rmarkdown(input_file, out_dir, params=None):
    """
    Run rmarkdown to create
    Parameters
    ----------
    input_file
    out_dir: output directory in that the markdown and resource files will be written.
    params

    Returns
    -------

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
    tmp_input_file = os.path.join(out_dir, os.path.basename(input_file))
    copyfile(input_file, tmp_input_file, follow_symlinks=True)

    rmd_cmd = (
        "rmarkdown::render('{input_file}', "
        "   run_pandoc=FALSE, "
        "   clean=FALSE, "
        "   knit_root_dir='{work_dir}', "
        "   params=list({params}))"
    ).format(
        input_file=os.path.abspath(tmp_input_file),
        params=param_str,
        # required to set the workdir explicitly. Will work in the temp directory
        # otherwise.
        work_dir=os.getcwd(),
    )

    cmd = ["Rscript", "--vanilla", "-e", rmd_cmd]
    check_call(cmd)

    p = re.compile("\.Rmd$")
    md_file = p.sub(".utf8.md", tmp_input_file)

    return md_file


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
    with TemporaryDirectory() as tmp_dir:
        md_file = _run_rmarkdown(input_file, tmp_dir, params)
        run_pandoc(md_file, output_file, res_path="{}:{}".format(tmp_dir, RES_PATH))
