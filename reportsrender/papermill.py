#!/usr/bin/env python3

import papermill as pm
import jupytext as jtx
from tempfile import NamedTemporaryFile
from nbconvert.preprocessors import TagRemovePreprocessor
from .pandoc import run_pandoc
from nbformat import NotebookNode
import os


def _prepare_cell_tags(nb: NotebookNode):
    """Transfer jupytext metadata (hide_input etc.)
    to consistent `tags` metadata, that can be
    handled by a nbconvert `TagRemovePreprocessor`.

    This is temporary until there is a consistent solution
    for mwouts/jupytext#337

    Parameters
    ----------
        nb
            jupyter notebook read into dict using `nbformat.read`
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


def _remove_cells(nb: NotebookNode):
    """Remove inputs, outputs or both, depending on the cell-tags.

    Relies on a TagRemovePreprocessor from nbconvert.

    Parameters
    ----------
    nb
        Input notebook.


    Returns
    -------
    nb: NotebookNode
        NotebookNode with cells removed.

    """
    tag_remove_preprocessor = TagRemovePreprocessor(
        remove_cell_tags=["hide_cell", "remove_cell"],
        remove_all_outputs_tags=["hide_output", "remove_output"],
        remove_input_tags=["hide_input", "remove_input"],
    )
    nb, _ = tag_remove_preprocessor.preprocess(nb, None)
    # The tag remove preprocessor only adds `transient: 'remove_source'`
    # to each cell. This option is not understood by pandoc.
    # We will therefore remove the contents from the `source` field.
    for cell in nb.cells:
        try:
            if cell["transient"]["remove_source"]:
                cell["source"] = ""
        except KeyError:
            pass
    return nb


def _run_papermill(nb_path: str, out_file: str, params: dict):
    """execute .ipynb file using papermill and write
    results to out_file in ipynb format.

    See Also
    --------
    papermill.execute_notebook : Execute a notebook using papermill.
    """
    # excplicitly specify the Python 3 kernel to override the notebook-metadata.
    pm.execute_notebook(
        nb_path, out_file, parameters=params, log_output=True, kernel_name="python3"
    )


def render_papermill(input_file: str, output_file: str, params: dict = None):
    """
    Wrapper function to render a jupytext/jupyter notebook
    with papermill and pandoc.

    Parameters
    ----------
        input_file
            path to input file. Can be any format supported by jupytext.
        output_file
            path to output (html) file.
        params
            parameter dictionary that will be passed to papermill.
            See https://papermill.readthedocs.io/en/latest/usage-parameterize.html for more details.
    """

    # Directory the notebook is located in. Will be used as additional resource path for pandoc.
    nb_dir = os.path.abspath(os.path.dirname(input_file))

    with NamedTemporaryFile(suffix=".ipynb") as tmp_nb_converted:
        with NamedTemporaryFile(suffix=".ipynb") as tmp_nb_executed:
            with NamedTemporaryFile(suffix=".ipynb") as tmp_nb_cleaned:
                # convert to ipynb
                nb = jtx.read(input_file)
                jtx.write(nb, tmp_nb_converted.name)
                # execute notebook
                _run_papermill(
                    tmp_nb_converted.name, tmp_nb_executed.name, params=params
                )
                # hide inputs, outputs etc.
                nb_exec = jtx.read(tmp_nb_executed.name)
                _prepare_cell_tags(nb_exec)
                _remove_cells(nb_exec)
                jtx.write(nb_exec, tmp_nb_cleaned.name)
                # convert to html
                run_pandoc(tmp_nb_cleaned.name, output_file, res_path=[nb_dir])
