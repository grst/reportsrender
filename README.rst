Generate reproducible reports from Rmarkdown or jupyter notebooks
=================================================================
|travis| |docs| |black|

.. |travis| image:: https://travis-ci.com/grst/reportsrender.svg?branch=master
    :target: https://travis-ci.com/grst/reportsrender
    :alt: Build Status

.. |docs| image:: https://readthedocs.org/projects/reportsrender/badge/?version=latest
    :target: https://reportsrender.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
    
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: The uncompromising python formatter

Reportsrender allows to create reproducible, consistently looking HTML reports from
both jupyter notebooks and Rmarkdown files. It makes use of `papermill <https://github.com/nteract/papermill>`_
and `Rmarkdown <https://bookdown.org/yihui/rmarkdown/>`_ to execute notebooks and uses
`Pandoc <https://pandoc.org/>`_ to convert them to HTML.

**Features**:
 * two execution engines: papermill and Rmarkdown.
 * support any format supported by `jupytext <https://github.com/mwouts/jupytext>`_.
 * create self-contained HTML that can be shared easily.
 * hide inputs and/or outputs of cells.
 * parametrized reports

See the `documentation <https://reportsrender.readthedocs.io/>`_ for more details!

Getting started
================

* Execute an rmarkdown document to HTML using the Rmarkdown engine

::

    reportsrender --engine=rmd my_notebook.Rmd report.html

* Execute a parametrized jupyter notebook with papermill

::

    reportsrender --engine=papermill jupyter_notebook.ipynb report.html --params="data_file=table.tsv"


.. _cli:

Usage from command line
=======================

::

    reportsrender

    Execute and render a jupyter/Rmarkdown notebook.
    The `index` subcommand generates an index html
    or markdown file that links to html documents.

    Usage:
      reportsrender <notebook> <out_file> [--cpus=<cpus>] [--params=<params>] [--engine=<engine>]
      reportsrender index [--index=<index_file>] [--title=<title>] [--] <html_files>...
      reportsrender --help

    Arguments and options:
      <notebook>            Input notebook to be executed. Can be any format supported by jupytext.
      <out_file>            Output HTML file.
      -h --help             Show this screen.
      --cpus=<cpus>         Number of CPUs to use for Numba/Numpy/OpenBLAS/MKL [default: 1]
      --params=<params>     space-separated list of key-value pairs that will be passed
                            to papermill/Rmarkdown.
                            E.g. "input_file=dir/foo.txt output_file=dir2/bar.html"
      --engine=<engine>     Engine to execute the notebook. [default: auto]

    Arguments and options of the `index` subcommand:
      <html_files>          List of HTML files that will be included in the index. The tool
                            will generate relative links from the index file to these files.
      --index=<index_file>  Path to the index file that will be generated. Will be
                            overwritten if exists. Will auto-detect markdown (.md) and
                            HTML (.html) format based on the extension. [default: index.html]
      --title=<title>       Headline of the index. [default: Index]

    Possible engines are:
      auto                  Use `rmd` engine for `*.Rmd` files, papermill otherwise.
      rmd                   Use `rmarkdown` to execute the notebook. Supports R and
                            python (through reticulate)
      papermill             Use `papermill` to execute the notebook. Works for every
                            kernel available in the jupyter installation.






Installation
============

Conda (recommended):
^^^^^^^^^^^^^^^^^^^^
As this reportsrender dependes on both R and Python packages, I recommend
to install it through `conda <https://docs.conda.io/en/latest/miniconda.html>`_.
The following command will install reportsrender and all its dependencies in the 
current conda environment: 

::

    conda install -c conda-forge grst::reportsrender

If you prefer not to use conda, you can follow the approach below: 


Manual installation:
^^^^^^^^^^^^^^^^^^^^

Get dependencies:
"""""""""""""""""

* Python
* `pandoc`_

For the Rmarkdown render engine additionally
(there is no need to install them if you are not going
to use the Rmarkdown rendeirng engine):

* R and the following packages:

::

    rmarkdown
    reticulate

then, 


Install from  pip:
""""""""""""""""""

::

    pip install reportsrender

or, 

Install from github:
""""""""""""""""""""

::

    pip install flit
    flit installfrom github:grst/reportsrender



