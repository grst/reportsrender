"""Execute and Render notebooks as HTML reports. """
from get_version import get_version

__version__ = get_version(__file__)
del get_version

__author__ = "Gregor Sturm"


from .papermill import render_papermill
from .rmd import render_rmd
from .pandoc import run_pandoc
