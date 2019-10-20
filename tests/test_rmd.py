from reportsrender.rmd import render_rmd, _run_rmarkdown


def test_run_rmarkdown(tmp_path):
    """Test that running Rmarkdown generates a .utf8.md file. """
    in_file = "notebooks/01_generate_data.Rmd"
    md_file = _run_rmarkdown(in_file, tmp_path)
    assert md_file.endswith(".utf8.md")
    with open(md_file) as f:
        text = f.read()
        assert "library" in text


def test_render_rmd(tmp_path):
    in_file = "notebooks/01_generate_data.Rmd"
    out_file = tmp_path / "report.html"
    # params = {"input_file": "notebooks/iris.tsv"}
    render_rmd(in_file, out_file, dict())


def test_render_rmd_ipynb(tmp_path):
    in_file = "notebooks/01_generate_data.ipynb"
    out_file = tmp_path / "report.html"
    # params = {"input_file": "notebooks/iris.tsv"}
    render_rmd(in_file, out_file, dict())


def test_render_rmd_py(tmp_path):
    """Render a notebook that contains python code with
    reticulate. """
    in_file = "notebooks/02_analyze_data.Rmd"
    out_file = tmp_path / "report.html"
    params = {"input_file": "notebooks/iris.tsv"}

    render_rmd(in_file, out_file, params)

    result = out_file.read_text()

    assert "ECHO_FALSE" not in result
    assert "RESULTS_HIDE" not in result
    assert "ECHO_TRUE_01" in result
    assert "ECHO_TRUE_02" in result
    assert "RESULTS_SHOW_01" in result
    assert "RESULTS_SHOW_02" in result
