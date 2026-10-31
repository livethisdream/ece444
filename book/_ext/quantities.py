"""Plain quantities in the body font.

Inline math that holds only a number -- with at most a sign, a degree sign, a
percent, or a unit in \\text{} -- renders in MathJax's Computer Modern, so
$30^\\circ$, $-13.3$ dB, and $1.2\\ \\text{m}$ each stood out from the sans
sentence around them. Neil, 2026-10-31: fix it. This turns each such inline
math node into plain text in the body font at build time, so the sources keep
the course's $...$ convention and nothing has to be re-edited. Anything with a
symbol in it ($\\theta_0 = 30^\\circ$, $2D^2/\\lambda$) stays math, and so does
every display equation.

    $30^\\circ$            -> 30°
    $-13.3$               -> −13.3        (a true minus sign)
    $\\pm 1$               -> ±1
    $1.2\\ \\text{m}$        -> 1.2 m        (a no-break space, never a thin one)
    $50\\%$                -> 50%

The result is a <span class="qty">, which shell.css keeps on one line.
Off switch: ``ece444_plain_quantities: false`` under sphinx.config in
_config.yml puts every quantity back in MathJax.
"""

import re

from docutils import nodes

NUMBER = r"(?P<sign>[-+]|\\pm\s*)?\s*(?P<num>\d[\d,]*(?:\.\d+)?)"
SUFFIX = (r"(?P<suffix>\^\\circ|\^\{\\circ\}|\\%"
          r"|(?:\\ |~|\s)+\\text\{(?P<unit>[^{}\\$]*)\})?")
QUANTITY = re.compile(r"^\s*" + NUMBER + r"\s*" + SUFFIX + r"\s*$")

NBSP = " "


def plain(tex):
    """The text a plain quantity reads as, or None if the math is more than one."""
    m = QUANTITY.match(tex)
    if not m:
        return None
    sign = (m.group("sign") or "").strip()
    sign = {"-": "−", "+": "+", "\\pm": "±"}.get(sign, "")
    suffix = m.group("suffix") or ""
    if suffix in ("^\\circ", "^{\\circ}"):
        tail = "°"
    elif suffix == "\\%":
        tail = "%"
    elif m.group("unit") is not None:
        tail = NBSP + m.group("unit").strip()
    else:
        tail = ""
    return sign + m.group("num") + tail


def convert(app, doctree):
    if not app.config.ece444_plain_quantities:
        return
    for node in list(doctree.findall(nodes.math)):
        text = plain(node.astext())
        if text is not None:
            node.replace_self(nodes.inline(text, text, classes=["qty"]))


def setup(app):
    app.add_config_value("ece444_plain_quantities", True, "env")
    app.connect("doctree-read", convert)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
