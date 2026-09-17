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
STATE = ROOT.parent / "STATE.json"
PORT = int(os.environ.get("TECHNE_PORT", "8787"))
MAX_BODY = 256 * 1024

# Learner-facing server strings; unknown languages fall back to English.
MESSAGES = {
    "en": {
        "empty": "No browser activity is open yet.",
        "title": "Techne — activities",
        "heading": "Browser activities",
        "recorded": "· Techne answer recorded locally",
        "url": "Techne activities: {url}",
        "events": "Local answers: {path}",
        "stop_hint": "Ctrl+C to stop.",
        "stopped": "Stopped.",
    },
    "fr": {
        "empty": "Aucune activité navigateur n’est encore ouverte.",
        "title": "Techne — activités",
        "heading": "Activités navigateur",
        "recorded": "· réponse Techne enregistrée localement",
        "url": "Activités Techne : {url}",
        "events": "Réponses locales : {path}",
        "stop_hint": "Ctrl+C pour arrêter.",
        "stopped": "Arrêté.",
    },
}


def learner_language() -> str:
    try:
        language = json.loads(STATE.read_text(encoding="utf-8")).get("language")
    except (OSError, ValueError):
        language = None
    return language if isinstance(language, str) and language else "en"


LANGUAGE = learner_language()
TEXT = MESSAGES.get(LANGUAGE.split("-")[0].lower(), MESSAGES["en"])


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

        content = "".join(links) or f"<li>{html.escape(TEXT['empty'])}</li>"
        document = f"""<!doctype html>
<html lang="{html.escape(LANGUAGE, quote=True)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TEXT['title'])}</title><link rel="stylesheet" href="/assets/course.css"></head>
<body><main><p class="eyebrow">TECHNE</p><h1>{html.escape(TEXT['heading'])}</h1><ul>{content}</ul></main></body></html>"""
        payload = document.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        if self.command == "POST":
            sys.stderr.write(TEXT["recorded"] + "\n")


def main() -> None:
    LESSONS.mkdir(parents=True, exist_ok=True)
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    print(TEXT["url"].format(url=f"http://localhost:{PORT}"))
    print(TEXT["events"].format(path=EVENTS))
    print(TEXT["stop_hint"])
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n" + TEXT["stopped"])


if __name__ == "__main__":
    main()
