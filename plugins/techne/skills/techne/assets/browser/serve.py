#!/usr/bin/env python3
"""Serve Techne browser exercises and record local learner events."""

from __future__ import annotations

import html
import json
import os
import sys
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
LESSONS = ROOT / "lessons"
EVENTS = ROOT.parent / "events" / "browser.jsonl"
PORT = int(os.environ.get("TECHNE_PORT", "8787"))
MAX_BODY = 256 * 1024


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802 - stdlib handler API
        if urlparse(self.path).path == "/":
            self._lesson_index()
            return
        super().do_GET()

    def do_POST(self):  # noqa: N802 - stdlib handler API
        if urlparse(self.path).path != "/api/event":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self.send_error(400, "Invalid Content-Length")
            return

        if length <= 0 or length > MAX_BODY:
            self.send_error(413)
            return

        try:
            event = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(event, dict):
                raise ValueError("JSON object expected")
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self.send_error(400, str(exc))
            return

        event["at"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
        EVENTS.parent.mkdir(parents=True, exist_ok=True)
        with EVENTS.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")

        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _lesson_index(self):
        LESSONS.mkdir(parents=True, exist_ok=True)
        links = []
        for path in sorted(LESSONS.glob("*.html")):
            label = html.escape(path.stem.replace("-", " ").title())
            href = "/lessons/" + html.escape(path.name, quote=True)
            links.append(f'<li><a href="{href}">{label}</a></li>')

        content = "".join(links) or "<li>Aucune activité navigateur n’est encore ouverte.</li>"
        document = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Techne — activités</title><link rel="stylesheet" href="/assets/course.css"></head>
<body><main><p class="eyebrow">TECHNE</p><h1>Activités navigateur</h1><ul>{content}</ul></main></body></html>"""
        payload = document.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        if self.command == "POST":
            sys.stderr.write("· réponse Techne enregistrée localement\n")


def main() -> None:
    LESSONS.mkdir(parents=True, exist_ok=True)
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    print(f"Activités Techne : http://localhost:{PORT}")
    print(f"Réponses locales : {EVENTS}")
    print("Ctrl+C pour arrêter.")
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nArrêté.")


if __name__ == "__main__":
    main()
