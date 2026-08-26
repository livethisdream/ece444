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


def choose_template(app, pagename, templatename, context, doctree):
    """Render frame lessons with a chrome-free template."""
    if doctree is None:
        return None
    meta = app.env.metadata.get(pagename, {})
    if "frame_view" in meta:
        context["is_frame_view"] = True
        return "frame.html"
    return None


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
