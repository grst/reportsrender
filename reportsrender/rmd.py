from subprocess import check_call
from shutil import copyfile
from tempfile import NamedTemporaryFile, TemporaryDirectory
from .pandoc import run_pandoc, RES_PATH
import os
import re


def _literal_to_r_str(value):
    """Convert a python value to a corresponding R string.

    >>> _literal_to_r_str(True)
    "TRUE"
    >>> _literal_to_r_str(6)
    "8"
    >>> _literal_to_r_str("test")
    "'test'"
    """
    _literal_to_str = {True: "TRUE", False: "FALSE", None: "NULL"}
    try:
        return _literal_to_str[value]
    except KeyError:
        # quote a string
        if isinstance(value, str):
            return "'{}'".format(value)
        else:
            return str(value)


def _run_rmarkdown(input_file: str, out_dir: str, params: dict = None):
    """
    Run rmarkdown to execute a `.Rmd` file.

    Will not execute pandoc but write a markdown file and associated resources
    to the output directory.

    Parameters
    ----------
    input_file
        input (Rmarkdown) file.
    out_dir
        output directory in that the markdown and resource files will be written.
    params
        Parameter dictionary passed to rmarkdown.
        See https://bookdown.org/yihui/rmarkdown/parameterized-reports.html for more details.

    Returns
    -------
    md_file: str
        Path to output-markdown file. Will be absolute path if `out_dir` is absolute and
        relative if `out_dir` is relative.

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


def render_rmd(input_file: str, output_file: str, params: dict = None):
    """
    Wrapper function to render an Rmarkdown document with
    the R `rmarkdown` package and convert it to HTML using pandoc
    and a custom template.

    Parameters
    ----------
        input_file
            path to input (Rmd) file
        output_file
            path to output (html) file
        params
            Dictionary that will be passed to `params` arg of `rmarkdown::render`.
            See https://bookdown.org/yihui/rmarkdown/parameterized-reports.html for more details.
    """
    with TemporaryDirectory() as tmp_dir:
        md_file = _run_rmarkdown(input_file, tmp_dir, params)
        run_pandoc(md_file, output_file, res_path="{}:{}".format(tmp_dir, RES_PATH))
