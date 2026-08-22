"""Shared plumbing for the ECE 444 render-verification harness.

The CDNs (jsdelivr, Google Fonts) are blocked in the course containers, so
reveal.js and MathJax never load on their own. Every checker serves the target
over HTTP and reroutes CDN requests to the vendored npm copies under
scripts/verify/node_modules — run `npm install` in this directory once per
container before using any of them.
"""
import functools
import http.server
import pathlib
import socketserver
import threading

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
NM = HERE / "node_modules"

CONTENT_TYPES = {
    "js": "application/javascript",
    "mjs": "application/javascript",
    "css": "text/css",
    "woff2": "font/woff2",
    "woff": "font/woff",
    "svg": "image/svg+xml",
    "json": "application/json",
}


def require_vendored():
    """Fail loudly rather than silently rendering a deck with no MathJax."""
    if not NM.exists():
        raise SystemExit(
            f"FAIL: {NM} is missing. The CDNs are blocked in this container, so "
            f"reveal.js and MathJax must be vendored.\n"
            f"Run: cd {HERE} && npm install"
        )


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler logs every request to stderr, which buries the
    checker's own output and matches greps meant for it (a request for
    course-slides.css once matched a grep for 'slides')."""

    def log_message(self, *args):
        pass


class _Server(socketserver.TCPServer):
    # Must be a class attribute: TCPServer binds inside __init__, so setting
    # it on the instance afterwards is too late to have any effect.
    allow_reuse_address = True


def serve(directory):
    """Serve `directory` on an ephemeral port; return (httpd, port).

    The port is chosen by the OS rather than derived from the target name.
    A hashed port collides with a server still in TIME_WAIT from an earlier
    run, which surfaces as an unrelated-looking check failure.
    """
    handler = functools.partial(_QuietHandler, directory=str(directory))
    httpd = _Server(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def launch(playwright):
    """Chromium is preinstalled in the course containers; fall back to its path."""
    try:
        return playwright.chromium.launch()
    except Exception:
        return playwright.chromium.launch(executable_path="/opt/pw-browsers/chromium")


def make_cdn_router(missing=None):
    """Route jsdelivr to node_modules and stub out Google Fonts.

    Version pins are stripped: reveal.js@5.1.0/dist/x -> node_modules/reveal.js/dist/x
    """

    def route(r):
        url = r.request.url
        if "cdn.jsdelivr.net/npm/" in url:
            rel = url.split("cdn.jsdelivr.net/npm/", 1)[1].split("?")[0]
            parts = rel.split("/", 1)
            pkg = parts[0].split("@")[0]
            local = NM / pkg / (parts[1] if len(parts) > 1 else "")
            if local.exists():
                ct = CONTENT_TYPES.get(local.suffix[1:], "application/octet-stream")
                r.fulfill(path=str(local), content_type=ct)
                return
            if missing is not None:
                missing.append(url)
            r.abort()
            return
        if "fonts.googleapis.com" in url:
            r.fulfill(body="", content_type="text/css")
            return
        if "fonts.gstatic.com" in url:
            r.abort()
            return
        r.continue_()

    return route
