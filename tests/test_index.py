from reportsrender.index import _get_title
from reportsrender import render_rmd, render_papermill
from reportsrender.index import build_index


def test_get_title(tmpdir):
    html_file_1 = tmpdir.join("html1.html")
    html_file_2 = tmpdir.join("html2.html.html")
    html_file_1.write(
        """
        <html>
            <head>
                <title class="foo">testtitle</title>
            </head>
        </html>
        """
    )
    html_file_2.write("Doesn't contain a valid title...")

    assert _get_title(str(html_file_1)) == "testtitle"
    assert _get_title(str(html_file_2)) == "html2.html"


def test_build_index(tmpdir):
    out_md = tmpdir.join("index.md")
    out_md2 = tmpdir.join("index_2.md")
    out_html = tmpdir.join("index.html")
    html_files = ["html/01_generate_data.rmd.html", "html/02_analyze_data.rmd.html"]

    build_index(html_files, str(out_md))
    build_index(html_files, str(out_md2), title="My Index")
    build_index(html_files, str(out_html))

    for idx in [out_md, out_md2, out_html]:
        content = idx.read()
        assert "First notebook (in R)" in content
        assert "The second notebook" in content
        assert "01_generate_data.rmd.html" in content
        assert "02_analyze_data.rmd.html" in content

    assert "Index</h1>" in out_html.read()
    assert "html/01_generate_data.rmd.html" in out_md2.read()
    assert out_md2.read().startswith("# My Index")
