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


#: Assets that belong to the frame template alone. jupyter-book auto-links
#: every file in `_static`, so without stripping these a frame stylesheet full
#: of bare `body`, `h1`, `p`, `table` and `:root` rules lands on every page in
#: the book and quietly restyles the whole site.
_FRAME_ASSETS = ("frames.css", "frames.js")


def _drop_frame_assets(context):
    """Remove frames.css / frames.js from the auto-linked asset lists.

    Safe on the frame page too: frame.html links its own stylesheet by path.
    """
    for key in ("css_files", "script_files"):
        files = context.get(key)
        if not files:
            continue
        context[key] = [
            f for f in files
            if not any(a in str(getattr(f, "filename", f) or "")
                       for a in _FRAME_ASSETS)
        ]


def choose_template(app, pagename, templatename, context, doctree):
    """Render frame lessons with a chrome-free template."""
    # search.html and genindex.html arrive with doctree None -- they are still
    # ordinary pages that must not pick up the frame stylesheet.
    meta = {} if doctree is None else app.env.metadata.get(pagename, {})
    if "frame_view" not in meta:
        _drop_frame_assets(context)
        return None
    context["is_frame_view"] = True

    # Keep MathJax, drop everything else. The theme's JS expects theme DOM and
    # throws on every selector it owns once the sidebar is gone.
    #
    # This has to be done here, not in the template: Sphinx adds the
    # `window.MathJax = {...}` config as an INLINE script with no filename, so
    # a Jinja filter matching on the name keeps the MathJax file and silently
    # drops its config -- and the page then renders no math at all.
    keep = []
    for js in context.get("script_files", []):
        name = str(getattr(js, "filename", js) or "")
        body = str(getattr(js, "attributes", {}).get("body", "") or "")
        if "mathjax" in name.lower() or "MathJax" in body:
            keep.append(js)
    context["script_files"] = keep
    _drop_frame_assets(context)
    return "frame.html"


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
    app.connect("config-inited", add_template_dir)
    app.add_directive("frame", FrameDirective)
    app.add_directive("depth", DepthDirective)
    app.add_directive("callout", CalloutDirective)
    app.connect("html-page-context", choose_template)
    return {"version": "0.1", "parallel_read_safe": True}
