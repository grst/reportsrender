#!/usr/bin/env python3
"""
Test the pipeline results:
  * does hiding inputs and outputs work as expected?
"""


with open("results/02_analyze_data_rmd/report.html") as f:
    report_rmd = f.read()

with open("results/02_analyze_data_papermill/report.html") as f:
    report_papermill = f.read()


report_dict = {"papermill": report_papermill, "report_rmd": report_rmd}

for name, contents in report_dict.items():
    assert "ECHO_FALSE" not in contents, "{}: hide input works".format(name)
    assert "RESULTS_HIDE" not in contents, "{}: hide output works".format(name)
    assert "ECHO_TRUE_01" in contents, "{}, show input works".format(name)
    assert "ECHO_TRUE_02" in contents, "{}, show input works".format(name)
    assert "RESULTS_SHOW_01" in contents, "{}, show results works".format(name)
    assert "RESULTS_SHOW_02" in contents, "{}, show results works".format(name)
