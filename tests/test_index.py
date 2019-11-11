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
    # html_files = [str(html_rmd), str(html_papermill)]
    # build_index(html_files, str(index_md))
    # build_index(html_files, str(index_md2), title="My Index", rel_dir="results")
    # build_index(html_files, str(index_html))
    #
    # for idx in [index_md, index_md2, index_html]:
    #     content = idx.read()
    #     assert "A Novel Approach to Finding Black Cats in Dark Rooms (Rmd)" in content
    #     assert (
    #         "A Novel Approach to Finding Black Cats in Dark Rooms (Papermill)"
    #         in content
    #     )
    #     assert "papermill.html" in content
    #     assert "rmd.html" in content
    #
    # assert "Index</h1>" in index_html.read()
    # assert "results/papermill.html" in index_md2.read()
    # assert index_md2.read().startswith("# My Index")
    pass
