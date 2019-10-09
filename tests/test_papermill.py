#!/usr/bin/env python3
"""
Test the pipeline results:
  * does hiding inputs and outputs work as expected?
"""

from reportsrender.papermill import render_papermill, _remove_cells, _prepare_cell_tags
import nbformat
from pprint import pprint


def test_remove_cells():
    """Test that removing and keeping outputs works properly. """
    nb = nbformat.from_dict(
        {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {"hide_input": True},
                    "source": "# REMOVE_CELL",
                },
                {
                    "cell_type": "markdown",
                    "metadata": {"tags": ["hide_input"]},
                    "source": "# REMOVE_CELL",
                },
                {
                    "cell_type": "markdown",
                    "metadata": {"tags": ["remove_input"]},
                    "source": "# REMOVE_CELL",
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "outputs": [
                        {
                            "data": {
                                "image/png": "base64",
                                "text/plain": "INCLUDE_OUTPUT_01",
                            }
                        }
                    ],
                    "source": "# INCLUDE_INPUT_01",
                },
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["remove_cell"]},
                    "outputs": [
                        {"data": {"image/png": "base64", "text/plain": "REMOVE_CELL"}}
                    ],
                    "source": "# REMOVE_CELL",
                },
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["hide_output"]},
                    "outputs": [
                        {"data": {"image/png": "base64", "text/plain": "REMOVE_CELL"}}
                    ],
                    "source": "# INCLUDE_INPUT_02",
                },
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 0,
        }
    )

    _prepare_cell_tags(nb)
    nb2 = _remove_cells(nb)

    assert nb2 == nb

    str_repr = str(nb)

    pprint(nb)

    assert "INCLUDE_OUTPUT_01" in str_repr
    assert "INCLUDE_INPUT_01" in str_repr
    assert "INCLUDE_INPUT_02" in str_repr
    assert "REMOVE_CELL" not in str_repr


def test_render_papermill():
    with open("results/02_analyze_data_rmd/report.html") as f:
        report_rmd = f.read()

    with open("results/02_analyze_data_papermill/report.html") as f:
        report_papermill = f.read()

    # assert "ECHO_FALSE" not in contents, "{}: hide input works".format(name)
    # assert "RESULTS_HIDE" not in contents, "{}: hide output works".format(name)
    # assert "ECHO_TRUE_01" in contents, "{}, show input works".format(name)
    # assert "ECHO_TRUE_02" in contents, "{}, show input works".format(name)
    # assert "RESULTS_SHOW_01" in contents, "{}, show results works".format(name)
    # assert "RESULTS_SHOW_02" in contents, "{}, show results works".format(name)
