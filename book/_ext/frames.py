"""Frame-view lessons: `:::{frame}` / `:::{present}` / `:::{depth}` plus a
chrome-free template.

INERT until a lesson opts in. A page renders normally unless its front matter
carries `frame_view: true`; only then is the sidebar-free template used. So
this can sit in the build with nothing using it.

The point is that a frame lesson stays an ordinary Sphinx page. It keeps
MathJax, cross-references, the search index, and the TOC -- including the
prev/next links, which is how a chrome-free page still offers navigation.

See project/FRAMES_ARCHITECTURE.md for the design and what is still open.
"""
import re

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util.osutil import relative_uri


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
        # frame > wrap > content, because the layout centers a measured column
        # inside a full-viewport box; one element cannot do both jobs.
        inner = nodes.container()
        inner["classes"] = ["wrap"]
        if self.arguments:
            # NOT nodes.title: docutils asserts that a title's parent is a
            # section, and a frame is a container. rubric is precisely the
            # node for a heading that does not open a section.
            inner += nodes.rubric(text=self.arguments[0])
        self.state.nested_parse(self.content, self.content_offset, inner)
        cut = _cut(inner)
        outer = nodes.container()
        # :class: belongs to the FRAME, not the inner column -- that is what an
        # author means by `:class: viz-frame`.
        outer["classes"] = ["frame"] + self.options.get("class", [])
        if cut:
            outer["classes"].append("cut")
        outer["ids"] = [self._frame_id()]
        outer += inner
        return [outer]

    def _frame_id(self):
        """A stable anchor per frame, so a URL can name one.

        Without an id frames.js had nothing to put in the hash and wrote a bare
        "#" on every frame change -- which is why deep links never worked and
        why the call threw in a sandboxed document.

        Slugged from the title rather than numbered, so a link survives frames
        being reordered; numbered only as a fallback, and suffixed on a clash.
        """
        title = self.arguments[0] if self.arguments else ""
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        doc = self.state.document
        seen = doc.attributes.setdefault("ece444_frame_ids", {})
        count = doc.attributes.get("ece444_frame_count", 0) + 1
        doc.attributes["ece444_frame_count"] = count
        if not slug:
            # An untitled frame -- the opening title card -- gets its position.
            return "frame-%d" % count
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        return "frame-" + (slug if n == 0 else "%s-%d" % (slug, n + 1))


class DepthDirective(_Wrapper):
    default_class = "depth"


class PresentDirective(_Wrapper):
    """:::{present} -- what a frame shows on screen in present mode.

    The inverse of `depth`, and the one that inverts the default. A frame
    with no present block shows everything but its depth, which is how the
    lesson pages were first converted: the prose was wrapped in frames, so the
    prose is what the class saw, 60-90 words a screen. A frame that carries
    one or more present blocks shows ONLY those (plus its title); everything
    else in the frame becomes depth, without the author wrapping it. The
    lesson text is untouched either way -- read mode shows the whole frame in
    document order -- so the present layer is a view, not a second copy.
    """
    default_class = "present"


def _has_class(node, cls):
    return isinstance(node, nodes.container) and cls in node.get("classes", [])


def _cut(inner):
    """Apply the present layer to a parsed frame body. Returns True if it did.

    With at least one `present` child, the body is regrouped:

    * consecutive present blocks are wrapped in one `stage` container, so two
      of them sit side by side in present mode (key points beside the figure
      -- Neil's brief, 2026-09-03) and stack on a phone;
    * every run of anything else is wrapped in a `depth` container, so the
      existing "More detail +" expander, the print rules and check_frames all
      see it as what it now is: material the screen does not carry;
    * the rubric and any explicit `depth` block stay where they are.

    Document order is preserved throughout, which is what keeps read mode
    reading as the page the author wrote.
    """
    kids = list(inner.children)
    if not any(_has_class(k, "present") for k in kids):
        return False
    out, run, stage = [], [], []

    def flush_run():
        if run:
            d = nodes.container()
            d["classes"] = ["depth", "depth-cut"]
            d.extend(run)
            out.append(d)
            run.clear()

    def flush_stage():
        if stage:
            st = nodes.container()
            st["classes"] = ["stage"]
            st.extend(stage)
            out.append(st)
            stage.clear()

    for k in kids:
        if isinstance(k, nodes.rubric) or _has_class(k, "depth"):
            flush_run(); flush_stage(); out.append(k)
        elif _has_class(k, "present"):
            flush_run(); stage.append(k)
        else:
            flush_stage(); run.append(k)
    flush_run(); flush_stage()
    inner.children = []
    inner.extend(out)
    return True


class CalloutDirective(_Wrapper):
    default_class = "callout"


#: The shell's own assets. jupyter-book auto-links every file in `_static`, so
#: without stripping these a stylesheet full of bare `body`, `h1`, `p`, `table`
#: and `:root` rules lands on every page in the book -- including the theme
#: pages -- and quietly restyles things it was never meant to touch. Both
#: templates link what they need by path instead.
_SHELL_ASSETS = ("shell.css", "frames.css", "page.css",
                 "shell.js", "frames.js", "page.js")

#: Kept on a reading page. page.html links shell/page/custom by path, so the
#: only stylesheet still wanted from the auto-linked list is the syntax
#: coloring Sphinx generates for the configured pygments style -- easy to
#: miss, because without it code blocks still lay out, they just quietly lose
#: every color.
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


def _site_nav(app, pagename):
    """The other sites this one sits beside, for the HUD's site button.

    The course used to announce itself with a mark in the top-left corner that
    the five modules sprang out of. It was the wrong thing in the wrong place
    twice over: it covered the first line of every page, and the modules were
    already one tap away in the index overlay. The bar at the bottom is where
    the controls live, so the identity goes there too -- and once it is a
    button in a bar, the useful thing behind it is not the modules again but
    the rest of the site.

    Configured in _config.yml, not derived: these are sibling sites, and this
    build knows nothing about them. The entry marked `here: true` is this book
    -- it is linked to the book's own root doc so the link works from a local
    unzipped build as well as from the published site, and its label is what
    the button itself shows.
    """
    entries = getattr(app.config, "ece444_site_nav", None) or []
    here_uri = app.builder.get_target_uri(pagename)
    out = []
    for e in entries:
        here = bool(e.get("here"))
        url = e.get("url", "")
        if here:
            url = relative_uri(here_uri,
                               app.builder.get_target_uri(app.config.root_doc))
        out.append({"label": e.get("label", ""), "url": url, "current": here})
    return out


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
        context["site_nav"] = _site_nav(app, pagename)
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
    context["site_nav"] = _site_nav(app, pagename)
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
    # The HUD's site nav. Empty by default, and the button is then not
    # rendered at all -- a book built outside this site has no siblings.
    app.add_config_value("ece444_site_nav", [], "html")
    app.connect("config-inited", add_template_dir)
    app.add_directive("frame", FrameDirective)
    app.add_directive("depth", DepthDirective)
    app.add_directive("present", PresentDirective)
    app.add_directive("callout", CalloutDirective)
    app.connect("html-page-context", choose_template)
    return {"version": "0.1", "parallel_read_safe": True}
