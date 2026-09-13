"""A local web front end for the NEC engines.

The design constraint is the lab PC: no npm, no build step, no install beyond
Python. So this is `http.server` from the standard library serving a static
page, and a handful of JSON endpoints that wrap the same functions the CLI
calls. Start it and a browser opens on the tool.

It binds 127.0.0.1 by default and it will not execute a deck it did not
generate: the API takes model parameters, not NEC cards. The deck is shown in
the page so it can be copied into 4nec2, which keeps the cards the interface
the lesson says they are without turning this into a remote-execution service.
"""

from __future__ import annotations

import json
import math
import os
import socket
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .api import Api, DeckError, _gloss_json
from .engine import EngineError
from .reference import HALF_WAVE

STATIC = Path(__file__).parent / "static"
_TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript",
          ".css": "text/css", ".svg": "image/svg+xml", ".ico": "image/x-icon"}


def make_handler(api: Api):
    class Handler(BaseHTTPRequestHandler):
        server_version = "nec_lab"

        def log_message(self, fmt, *args):   # quiet: the page is the interface
            pass

        def _send(self, code: int, body: bytes, ctype: str):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/":
                path = "/index.html"
            if path == "/api/engine":
                return self._send(200, json.dumps(api.engine_info({})).encode(),
                                  "application/json")
            target = (STATIC / path.lstrip("/")).resolve()
            if not str(target).startswith(str(STATIC.resolve())) or not target.is_file():
                return self._send(404, b"not found", "text/plain")
            self._send(200, target.read_bytes(),
                       _TYPES.get(target.suffix, "application/octet-stream"))

        def do_POST(self):
            name = self.path.split("?")[0].removeprefix("/api/")
            try:
                n = int(self.headers.get("Content-Length", 0))
                req = json.loads(self.rfile.read(n) or b"{}")
                body = json.dumps(api.dispatch(name, req)).encode()
            except EngineError as exc:
                return self._send(500, json.dumps({"error": str(exc)}).encode(),
                                  "application/json")
            except Exception as exc:  # a bad number in a form field, usually
                return self._send(
                    400, json.dumps({"error": f"{type(exc).__name__}: {exc}"}).encode(),
                    "application/json")
            self._send(200, body, "application/json")

    return Handler


def _is_wsl() -> bool:
    """WSL: a Linux userland with no Linux browser and a Windows one next door."""
    if os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSL_INTEROP"):
        return True
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except OSError:
        return False


def _open_browser(url: str) -> None:
    """Open the page, and above all do it quietly.

    Under WSL, `webbrowser` reaches for xdg-open, which tries sixteen Linux
    browsers that are not installed and prints a "not found" line for each. The
    service started perfectly; the log reads like a crash. So the opener is
    ours: hand the URL to Windows under WSL, use the platform's own opener
    elsewhere, and if none of it works, say nothing -- the banner has already
    printed the address, which is all the student needs.
    """
    if _is_wsl():
        attempts = [["wslview", url],                       # wslu, if installed
                    ["explorer.exe", url],                  # always present
                    ["powershell.exe", "-NoProfile", "-Command",
                     f"Start-Process '{url}'"]]
    elif sys.platform == "darwin":
        attempts = [["open", url]]
    elif sys.platform == "win32":
        attempts = [["cmd", "/c", "start", "", url]]
    else:
        attempts = [["xdg-open", url]]
    for argv in attempts:
        try:
            subprocess.run(argv, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=15, check=False)
            return
        except (OSError, subprocess.TimeoutExpired):
            continue


def _in_container() -> bool:
    """Are we inside a container? Then our own addresses are not the ones to
    hand out -- students reach the host, on whatever port it published."""
    if Path("/.dockerenv").exists():
        return True
    try:
        return "docker" in Path("/proc/1/cgroup").read_text()
    except OSError:
        return False


def _reachable_urls(host: str, port: int) -> list[str]:
    """The addresses a browser can actually be pointed at.

    Binding 0.0.0.0 means "every interface", which is not something anyone can
    type. When the service is shared with a room -- the container does exactly
    this -- the banner has to name the addresses students should use, or the
    first five minutes of the lab are spent finding them.
    """
    if host not in ("0.0.0.0", "::", ""):
        return [f"http://{host}:{port}/"]
    addrs: list[str] = []
    try:
        _, _, ips = socket.gethostbyname_ex(socket.gethostname())
        addrs += [ip for ip in ips if not ip.startswith("127.")]
    except OSError:
        pass
    if not addrs:
        # No name resolution (common in a container): ask the routing table
        # which address it would use to reach the outside world. Nothing is
        # sent -- a UDP socket connect just picks the interface.
        try:
            probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            probe.connect(("8.8.8.8", 9))    # nothing is sent; this only
                                             # asks which interface would be used
            addrs.append(probe.getsockname()[0])
            probe.close()
        except OSError:
            pass
    return [f"http://{a}:{port}/" for a in dict.fromkeys(addrs)] \
        + [f"http://127.0.0.1:{port}/"]


def serve(host: str = "127.0.0.1", port: int = 8444, engine=None,
          open_browser: bool = True, public_url: str | None = None) -> None:
    from .engine import pick_engine

    engine = engine or pick_engine()
    httpd = ThreadingHTTPServer((host, port), make_handler(Api(engine)))
    public_url = public_url or os.environ.get("NEC_LAB_PUBLIC_URL") or None
    urls = _reachable_urls(host, port)
    print(f"nec_lab -- {engine.describe()}")
    if public_url:
        # A container, or a box behind a name: the address students type is not
        # one this process can discover, so whoever deployed it says what it is.
        print(f"hand out {public_url}   (ctrl-c to stop)")
    elif len(urls) == 1:
        print(f"open {urls[0]}   (ctrl-c to stop)")
    else:
        print("open one of these   (ctrl-c to stop):")
        for u in urls:
            print(f"    {u}")
        print("shared mode: students on the same network use the address above "
              "that matches this machine")
    if _is_wsl():
        print("      (WSL: open that address in your Windows browser)")
    # Measured with ten simultaneous requests: PyNEC holds the GIL through the
    # solve, so a shared server serializes; nec2c runs as subprocesses and uses
    # every core. Same answers either way -- the selftest checks that -- but the
    # worst-case wait was 5.4 s against 1.6 s on four cores.
    if host in ("0.0.0.0", "::") and engine.name == "PyNEC":
        from .engine import ExecutableEngine

        if ExecutableEngine().available():
            print("      (serving a room: --engine exe spreads solves across "
                  "cores; PyNEC holds one)")
    if _in_container() and not public_url:
        print("note: this is a container -- the addresses above are the "
              "container's own.\n      Students need the host's address and "
              "the port it published. Set\n      NEC_LAB_PUBLIC_URL to have "
              "that printed here instead.")
    if open_browser:
        threading.Timer(0.6, lambda: _open_browser(urls[0])).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
