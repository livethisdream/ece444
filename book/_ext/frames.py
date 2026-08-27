"""Frame-view lessons: `:::{frame}` / `:::{depth}` plus a chrome-free template.

INERT until a lesson opts in. A page renders normally unless its front matter
carries `frame_view: true`; only then is the sidebar-free template used. So
this can sit in the build with nothing using it.

The point is that a frame lesson stays an ordinary Sphinx page. It keeps
MathJax, cross-references, the search index, and the TOC -- including the
prev/next links, which is how a chrome-free page still offers navigation.

See project/FRAMES_ARCHITECTURE.md for the design and what is still open.
"""
from docutils import nodes
from docutils.parsers.rst import Directive, directives


class _Wrapper(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {"class": directives.class_option}
    node_class = None
    default_class = ""

    def run(self):
        node = nodes.container()
        node["classes"] = [self.default_class] + self.options.get("class", [])
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class FrameDirective(_Wrapper):
    """:::{frame} Title -- the title is an argument, not a nested heading.

    docutils demotes a header inside a container to a rubric, so a frame's
    title cannot be written as `## Title` in the body. Making it an argument
    is also truer: it names the frame rather than opening a subsection.
    """
    default_class = "frame"
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self):
        # frame > wrap > content, because the layout centres a measured column
        # inside a full-viewport box; one element cannot do both jobs.
        inner = nodes.container()
        inner["classes"] = ["wrap"]
        if self.arguments:
            # NOT nodes.title: docutils asserts that a title's parent is a
            # section, and a frame is a container. rubric is precisely the
            # node for a heading that does not open a section.
            inner += nodes.rubric(text=self.arguments[0])
        self.state.nested_parse(self.content, self.content_offset, inner)
        outer = nodes.container()
        # :class: belongs to the FRAME, not the inner column -- that is what an
        # author means by `:class: viz-frame`.
        outer["classes"] = ["frame"] + self.options.get("class", [])
        outer += inner
        return [outer]


class DepthDirective(_Wrapper):
    default_class = "depth"


class CalloutDirective(_Wrapper):
    default_class = "callout"


#: The shell's own assets. jupyter-book auto-links every file in `_static`, so
#: without stripping these a stylesheet full of bare `body`, `h1`, `p`, `table`
#: and `:root` rules lands on every page in the book -- including the theme
#: pages -- and quietly restyles things it was never meant to touch. Both
#: templates link what they need by path instead.
_SHELL_ASSETS = ("shell.css", "frames.css", "page.css", "frames.js", "page.js")

#: Kept on a reading page. page.html links shell/page/custom by path, so the
#: only stylesheet still wanted from the auto-linked list is the syntax
#: colouring Sphinx generates for the configured pygments style -- easy to
#: miss, because without it code blocks still lay out, they just quietly lose
#: every colour.
_PAGE_KEEP_CSS = ("pygments.css",)

#: viz-autosize.js measures the widget iframes with a ResizeObserver. Reading
#: pages need it; do not reimplement it in page.js.
_PAGE_KEEP_JS = ("viz-autosize.js",)


def _asset_name(f):
    return str(getattr(f, "filename", f) or "")


def _is_mathjax(f):
    """MathJax arrives as two entries: the CDN file, and an inline config with
    no filename at all. Matching on the name alone keeps the library and drops
    its configuration, and the page then renders no math."""
    name = _asset_name(f)
    body = str(getattr(f, "attributes", {}).get("body", "") or "")
    return "mathjax" in name.lower() or "MathJax" in body


def _drop_shell_assets(context):
    """Remove the shell's own files from the auto-linked lists.

    Safe on the shell pages too: their templates link them by path.
    """
    for key in ("css_files", "script_files"):
        files = context.get(key)
        if not files:
            continue
        context[key] = [
            f for f in files
            if not any(a in _asset_name(f) for a in _SHELL_ASSETS)
        ]


def _keep_only(context, key, predicate):
    files = context.get(key)
    if files:
        context[key] = [f for f in files if predicate(f)]


def _breadcrumb(app, pagename):
    """The module a page belongs to, for the breadcrumb chip.

    Computed here rather than in Jinja because the theme emits no breadcrumb
    nav to borrow, and Sphinx's `parents` does not carry the module: in this
    book a module overview is a chapter, a sibling of its lessons, not their
    ancestor. The directory is the reliable signal.
    """
    head = pagename.split("/")[0]
    if head == pagename:
        return None
    for candidate in (head + "/index", head):
        if candidate == pagename:
            continue
        title = app.env.titles.get(candidate)
        if title is not None:
            text = title.astext()
            # A module's own title is its full name -- "Module 1 -- Foundations
            # of Electromagnetics and Antennas". As a breadcrumb only the label
            # before the dash earns its width; the rest is in the overlay.
            for dash in ("\u2014", "\u2013", " - "):
                if dash in text:
                    text = text.split(dash)[0]
                    break
            for suffix in (" overview", " Overview"):
                if text.endswith(suffix):
                    text = text[: -len(suffix)]
            return text.strip()
    return None


def choose_template(app, pagename, templatename, context, doctree):
    """Route a page to the frame template, the reading template, or the theme.

    Three cases, in order:

    * `frame_view: true` in front matter -> frame.html, the scroll-snap lesson.
    * the shell is on and the page has not opted out -> page.html.
    * anything else -> the theme, untouched.

    `ece444_shell: false` in _config.yml puts the whole site back on the theme
    in one line, and `shell: false` in a page's front matter does the same for
    that page alone.
    """
    # search.html and genindex.html arrive with doctree None. They have no
    # front matter and no body, so they stay on the theme for now -- but they
    # must still be stripped of the shell's stylesheets.
    meta = {} if doctree is None else app.env.metadata.get(pagename, {})

    if "frame_view" in meta:
        context["is_frame_view"] = True
        # The theme's JS expects theme DOM and throws on every selector it owns
        # once the sidebar is gone. Keep MathJax, drop the rest.
        _keep_only(context, "script_files", _is_mathjax)
        _drop_shell_assets(context)
        return "frame.html"

    shell_on = getattr(app.config, "ece444_shell", True)
    opted_out = str(meta.get("shell", "")).lower() in ("false", "no", "0")
    if doctree is None or not shell_on or opted_out:
        _drop_shell_assets(context)
        return None

    context["crumb_module"] = _breadcrumb(app, pagename)
    _keep_only(context, "script_files",
               lambda f: _is_mathjax(f) or any(a in _asset_name(f) for a in _PAGE_KEEP_JS))
    _keep_only(context, "css_files",
               lambda f: any(a in _asset_name(f) for a in _PAGE_KEEP_CSS))
    _drop_shell_assets(context)
    return "page.html"


def add_template_dir(app, config=None):
    """Append, never replace.

    Two traps here, both of which fail with TemplateNotFound:

    1. Declaring templates_path in _config.yml OVERWRITES the one jupyter-book
       builds, which is where the theme's own partials live -- the build then
       dies inside pydata_sphinx_theme looking for toggle-primary-sidebar.html.
       Append to it instead.
    2. Append on `builder-inited` and it is already too late: the builder
       constructs its Jinja loader from templates_path during init. Use
       `config-inited`, which fires while the config is still malleable.
    """
    if "_templates" not in app.config.templates_path:
        app.config.templates_path.append("_templates")


def setup(app):
    # The kill switch. One line in _config.yml puts the site back on the theme.
    app.add_config_value("ece444_shell", True, "html")
    app.connect("config-inited", add_template_dir)
    app.add_directive("frame", FrameDirective)
    app.add_directive("depth", DepthDirective)
    app.add_directive("callout", CalloutDirective)
    app.connect("html-page-context", choose_template)
    return {"version": "0.1", "parallel_read_safe": True}
