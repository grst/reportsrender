import pkg_resources
import os
from subprocess import check_call


RES_PATH = pkg_resources.resource_filename(__package__, "templates/adaptive-bootstrap")
DEFAULT_TEMPLATE = os.path.join(RES_PATH, "standalone.html")
DEFAULT_CSS = os.path.join(RES_PATH, "template.css")


def run_pandoc(
    in_file,
    out_file,
    res_path=RES_PATH,
    template_name=DEFAULT_TEMPLATE,
    css_name=DEFAULT_CSS,
):
    """
    Run pandoc
    """
    cmd = """
          pandoc \
            +RTS -K512m -RTS \
            {input_file} \
            --output {output_file} \
            --email-obfuscation none \
            --self-contained \
            --mathjax \
            --variable 'mathjax-url:https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML' \
            --variable 'lightbox:true' \
            --variable 'thumbnails:true' \
            --variable 'gallery:false' \
            --variable 'cards:true' \
            --standalone \
            --section-divs \
            --table-of-contents \
            --toc-depth 1 \
            --template {html_template} \
            --css {css_file} \
            --resource-path {res_path} \
            --highlight-style pygments \
    """
    cmd2 = cmd.format(
        input_file=in_file,
        output_file=out_file,
        html_template=template_name,
        css_file=css_name,
        res_path=res_path,
    )
    check_call(cmd2, shell=True)
