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

    reportsrender rmd my_notebook.Rmd report.html

* Execute a parametrized jupyter notebook with papermill

::

    reportsrender papermill jupyter_notebook.ipynb report.html --params="data_file=table.tsv"


**TODO** add example notebooks.


Usage from command line
=======================

::

    reportsrender

    Execute and render a jupyter/Rmarkdown notebook.
    
    Usage:
      reportsrender <notebook> <out_file> [options]
      reportsrender --help

    Options:
      -h --help             Show this screen.
      --cpus=<cpus>         Number of CPUs to use for Numba/Numpy/OpenBLAS/MKL [default: 1]
      --params=<params>     space-separated list of key-value pairs that will be passed
                            to papermill/Rmarkdown.
                            E.g. "input_file=dir/foo.txt output_file=dir2/bar.html"
      --engine=<engine>     Engine to execute the notebook. [default: auto]

    Possible engines are:
        auto            Use `rmd` engine for `*.Rmd` files, papermill otherwise.
        rmd             Use `rmarkdown` to execute the notebook. Supports R and
                        python (through reticulate)
        papermill       User `papermill` to execute the notebook. Works for every
                        kernel available in the jupyter installation.






Installation
============

Conda (recommended):
^^^^^^^^^^^^^^^^^^^^
As this package dependes on both R and Python packages, I recommend
to install the package through `conda <https://docs.conda.io/en/latest/miniconda.html>`_.

I yet need to create a conda package and upload it on conda-forge, but you can create the following environment
and install the package:

::

    conda create -c bioconda -c conda-forge -n reportsrender \
          "python>=3.6" \
          "r-base>=3.5" \
          r-rmarkdown \
          r-reticulate \
          r-bookdown \
          flit \
          pandoc

    conda activate reportsrender
    flit installfrom github:grst/reportsrender




Manual install:
^^^^^^^^^^^^^^^

Get dependencies:
"""""""""""""""""

* Python
* `pandoc`_

For the Rmarkdown render engine additionally:

* R and the following packages:

::

    rmarkdown
    reticulate


Install from github:
""""""""""""""""""""

::

    pip install flit
    flit installfrom github:grst/reportsrender



