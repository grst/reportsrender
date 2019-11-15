from reportsrender.cli import main
import pytest
import docopt
import os
import shutil


def test_no_args():
    with pytest.raises(docopt.DocoptExit):
        main([])


def test_render(tmp_path):
    out_file = tmp_path / "output.html"
    main(["notebooks/01_generate_data.Rmd", str(out_file)])
    result = out_file.read_text()
    assert "First notebook" in result


def test_render_options(tmp_path):
    out_file = tmp_path / "output.html"
    main(
        [
            "notebooks/02_analyze_data.Rmd",
            str(out_file),
            "--engine=papermill",
            "--cpus=2",
            "--params='input_file=notebooks/iris.tsv'",
        ]
    )
    result = out_file.read_text()

    assert (
        "<pre><code>## The 0th Fibonacci number is 0" not in result
    ), "Papermill does not ouput text in <pre><code> tags and does not start with '##'."
    assert "he 0th Fibonacci number is 0" in result


def test_index_no_args():
    with pytest.raises(docopt.DocoptExit):
        main(["index"])


@pytest.mark.parametrize("filename", ["the_index.html", "index.md"])
def test_index(filename, tmp_path):
    out_file = tmp_path / filename
    main(
        [
            "index",
            "html/01_generate_data.rmd.html",
            "html/02_analyze_data.rmd.html",
            "--index={}".format(str(out_file)),
            "--title='A cool title'",
        ]
    )
    result = out_file.read_text()

    assert "html/01_generate_data.rmd.html" in result
    assert "html/02_analyze_data.rmd.html" in result
    assert "A cool title" in result
    assert "The second notebook" in result


def test_index_paths(tmpdir):
    """Test if the index function correctly computes the
    relative paths to the HTML files.

    Our mock file structure

    ```
        .
        ├── html2
        │   └── html_file2.html
        └── index
            ├── html_file3.html
            ├── html1
            │   └── html_file1.html
            └── index.md
    ```

    """
    index_dir = tmpdir.mkdir("index")
    html_file1 = index_dir.mkdir("html1").join("html_file1.html")
    html_file2 = tmpdir.mkdir("html2").join("html_file2.html")
    html_file3 = index_dir.join("html_file3.html")

    shutil.copyfile("html/01_generate_data.rmd.html", html_file1)
    shutil.copyfile("html/02_analyze_data.rmd.html", html_file2)
    shutil.copyfile("html/02_analyze_data.rmd.html", html_file3)

    index_file_rel = index_dir.join("index.rel.md")
    index_file_abs = index_dir.join("index.abs.md")

    main(
        [
            "index",
            "html1/html_file1.html",
            "../html2/html_file2.html",
            "html_file3.html" "--index={}".format(index_file_rel),
        ]
    )

    main(
        [
            "index",
            os.path.abspath(html_file1),
            os.path.abspath(html_file2),
            os.path.abspath(html_file3),
            "--index={}".format(os.path.abspath(index_file_abs)),
        ]
    )

    result_rel = index_file_rel.read()
    result_abs = index_file_abs.read()

    assert result_abs == result_rel

    assert "../html2/html_file2.html" in result_abs
    assert "html1/html_file1.html" in result_abs
