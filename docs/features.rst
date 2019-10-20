Features
========

Execution engines
-----------------


Supported notebook formats
--------------------------


Hiding cell inputs/outputs
--------------------------
You can hide inputs and or outputs of individual cells:

Papermill engine:
^^^^^^^^^^^^^^^^^

Within a jupyter notebook:

* edit cell metadata
* add one of the following `tags`: `hide_input`, `hide_output`, `remove_cell`

::

    {
        "tags": [
            "remove_cell"
        ]
    }

Rmarkdown engine:
^^^^^^^^^^^^^^^^^

* all native input control options
  (e.g. `results='hide'`, `include=FALSE`, `echo=FALSE`) are supported. See the
  `Rmarkdown documentation <https://bookdown.org/yihui/rmarkdown/r-code.html>`_ for more details.

`Jupytext <https://github.com/mwouts/jupytext>`_ automatically converts the
tags to Rmarkdown options for all supported formats.



Parametrized notebooks
----------------------


Papermill engine:
^^^^^^^^^^^^^^^^^

* See the `Papermill documentation <https://papermill.readthedocs.io/en/latest/usage-parameterize.html>`_

Example:

* Add the tag `parameters` to the metadata of a cell in a jupyter notebook.
* Declare default parameters in that cell:

::

    input_file = '/path/to/default_file.csv'


* Use the variable as any other:

::

    import pandas as pd
    pd.read_csv(input_file)



Rmarkdown engine:
^^^^^^^^^^^^^^^^^

* See the `documentation <https://bookdown.org/yihui/rmarkdown/params-declare.html>`_.

Example:

* Declare the parameter to the yaml frontmatter.
* You can set default parameters that will be used when
  the notebook is executed interactively in Rstudio. They will be overwritten
  when running through `reportsrender`.

::

    ---
    title: My Document
    output: html_document
    params:
      input_file: '/path/to/default_file.csv'
    ---

* Access the parameters from the code:

::

    read_csv(params$input_file)


Be compatible with both engines:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes it's possible! You can execute the same notebook with both engines.
Adding parameters is a bit more cumbersome though.

Example (Python notebook stored as `.Rmd` file using *jupytext*):

::

    ---
    title: My Document
    output: html_document
    params:
      input_file: '/path/to/default_file.csv'
    ---

    ```{python tags=c("parameters")}
    try:
        # try to get param from Rmarkdown using reticulate.
        input_file = r.params["input_file"]
    except:
        # won't work if running papermill. Re-declare default parameters.
        input_file = "/path/to/default_file.csv"
    ```


Sharing reports
---------------
github pages...


Combine notebooks into a pipeline
---------------------------------


