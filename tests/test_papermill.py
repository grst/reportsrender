#!/usr/bin/env python3
"""
Test the pipeline results:
  * does hiding inputs and outputs work as expected?
"""

from reportsrender.papermill import render_papermill


def test_remove_cells():
    pass


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
