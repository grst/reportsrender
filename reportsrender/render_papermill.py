#!/usr/bin/env python3
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

import papermill as pm
import jupytext as jtx
import os
from os import path
import nbformat
from tempfile import NamedTemporaryFile
from nbconvert import HTMLExporter
from nbconvert.preprocessors import TagRemovePreprocessor
from docopt import docopt
from util import set_cpus, parse_params
from shutil import copyfile
from subprocess import call


def prepare_cell_tags(nb):
    """Transfer jupytext metadata (hide_input etc.)
    to consistent `tags` metadata, that can be
    handled by a nbconvert `TagRemovePreprocessor`.

    This is temporary until there is a consistent solution
    for mwouts/jupytext#337

    Args:
        nb: jupyter notebook read into dict using `nbformat.read`
    """

    def _fix_metadata(cell):
        m = cell["metadata"]
        tags = m.get("tags", list())
        if "hide_input" in m and m["hide_input"]:
            tags.append("hide_input")
        if "hide_output" in m and m["hide_output"]:
            # jupytext converts rmarkdown `include=FALSE` incorrectly.
            tags.append("remove_cell")
        if "results" in m and m["results"].strip("'" + '"') == "hide":
            tags.append("hide_output")
        m["tags"] = list(set(tags))

    for cell in nb["cells"]:
        _fix_metadata(cell)


def run_papermill(nb_path, out_file, params):
    """execute .ipynb file using papermill and write
    results to out_file in ipynb format.
    """
    # excplicitly specify the Python 3 kernel to override the notebook-metadata.
    pm.execute_notebook(
        nb_path, out_file, parameters=params, log_output=True, kernel_name="python3"
    )


def convert_to_html_nbconvert(nb_path, out_file):
    """convert executed ipynb file to html document. """
    with open(nb_path) as f:
        nb = nbformat.read(f, as_version=4)

    html_exporter = HTMLExporter()
    tag_remove_preprocessor = TagRemovePreprocessor(
        remove_cell_tags=["remove_cell"],
        remove_all_outputs_tags=["hide_output"],
        remove_input_tags=["hide_input"],
    )
    html_exporter.template_file = "full"
    html_exporter.register_preprocessor(tag_remove_preprocessor, enabled=True)

    html, resources = html_exporter.from_notebook_node(nb)

    with open(out_file, "w") as f:
        f.write(html)


def convert_to_html_pandoc(nb_path, out_file):
    cmd = """
          pandoc \
            +RTS -K512m -RTS \
            {input_file} \
            --output {output_file} \
            --email-obfuscation none \
            --self-contained \
            --mathjax \
            --variable 'mathjax-url:https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML' \
            --variable 'lightbox:true' \
            --variable 'thumbnails:true' \
            --variable 'gallery:false' \
            --variable 'cards:true' \
            --standalone \
            --section-divs \
            --table-of-contents \
            --toc-depth 1 \
            --template {html_template} \
#            --css {css_template} \
            --highlight-style pygments \
    """

    template_path = path.join(
        path.abspath(path.dirname(__file__)),
        "templates/adaptive-bootstrap/standalone.html",
    )
    css_path = path.join(
        path.abspath(path.dirname(__file__)),
        "templates/adaptive-bootstrap/template.css",
    )

    call(
        cmd.format(
            input_file=nb_path,
            output_file=out_file,
            html_template=template_path,
            css_template=css_path,
        ),
        shell=True,
    )


def render_papermill(input_file, output_file, params=None):
    """
    Wrapper function to render a jupytext/jupyter notebook
    with papermill and nbconvert.

    Args:
        input_file: path to input (.py/.Rmd/.md/.../.ipynb) file
        output_file: path to output (html) file.
        params: dictionary that will be passed to papermill.
    """

    with NamedTemporaryFile(suffix=".ipynb") as tmp_nb_converted:
        with NamedTemporaryFile(suffix=".ipynb") as tmp_nb_executed:
            nb = jtx.read(input_file)
            prepare_cell_tags(nb)
            jtx.write(nb, tmp_nb_converted.name)
            run_papermill(tmp_nb_converted.name, tmp_nb_executed.name, params=params)
            convert_to_html_pandoc(tmp_nb_executed.name, output_file)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    params = parse_params(arguments["--params"])

    set_cpus(arguments["--cpus"])

    render_papermill(arguments["<notebook>"], arguments["<out_file>"], params)
