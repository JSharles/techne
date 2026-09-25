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
PROGRESS_VIEW = ROOT / "progress.json"
PORT = int(os.environ.get("TECHNE_PORT", "8787"))
MAX_BODY = 256 * 1024

# Learner-facing server strings; unknown languages fall back to English.
MESSAGES = {
    "en": {
        "empty": "No browser activity is open yet.",
        "title": "Techne — activities",
        "heading": "Browser activities",
        "progress_link": "My progress",
        "progress_title": "Techne — my progress",
        "progress_heading": "My progress",
        "progress_empty": "Nothing recorded yet. Your first activities will fill this page.",
        "progress_legend": "A subject moves up only on work you did yourself.",
        "not_started": "Not started",
        "discovered": "Discovered",
        "assisted": "With help",
        "independent": "Independent",
        "transferred": "Transferred",
        "blocked": "Blocked",
        "due_reviews": "Due reviews",
        "due_on": "due",
        "domain.ts": "TypeScript", "domain.js": "JavaScript", "domain.react": "React",
        "domain.next": "Next.js", "domain.nest": "NestJS & backend", "domain.sql": "SQL & data",
        "domain.dsa": "Algorithms", "domain.test": "Tests & debugging", "domain.flow": "Delivery flow",
        "domain.arch": "Architecture",
        "domain.survey": "Survey", "domain.py": "Python", "domain.svc": "Services",
        "domain.llm": "LLM applications", "domain.rag": "Retrieval", "domain.agent": "Agents",
        "domain.eval": "Evaluation & operations",
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
        "progress_link": "Ma progression",
        "progress_title": "Techne — ma progression",
        "progress_heading": "Ma progression",
        "progress_empty": "Rien d’enregistré pour l’instant. Tes premières activités rempliront cette page.",
        "progress_legend": "Un sujet ne monte que sur du travail que tu as fait toi-même.",
        "not_started": "Pas abordé",
        "discovered": "Découvert",
        "assisted": "Avec aide",
        "independent": "Autonome",
        "transferred": "Transféré",
        "blocked": "Bloqué",
        "due_reviews": "Révisions à faire",
        "due_on": "pour le",
        "domain.ts": "TypeScript", "domain.js": "JavaScript", "domain.react": "React",
        "domain.next": "Next.js", "domain.nest": "NestJS et backend", "domain.sql": "SQL et données",
        "domain.dsa": "Algorithmique", "domain.test": "Tests et debugging", "domain.flow": "Git, revue et CI",
        "domain.arch": "Architecture",
        "domain.survey": "Survol", "domain.py": "Python", "domain.svc": "Services",
        "domain.llm": "Applications LLM", "domain.rag": "Recherche documentaire", "domain.agent": "Agents",
        "domain.eval": "Évaluation et production",
        "recorded": "· réponse Techne enregistrée localement",
        "url": "Activités Techne : {url}",
        "events": "Réponses locales : {path}",
        "stop_hint": "Ctrl+C pour arrêter.",
        "stopped": "Arrêté.",
    },
}


DOMAIN_ORDER = (
    "ts", "js", "react", "next", "nest", "sql", "dsa", "test", "flow", "arch", "survey",
    "py", "svc", "llm", "rag", "agent", "eval",
)
STATE_ORDER = ("transferred", "independent", "assisted", "blocked", "discovered", "not_started")


def read_progress() -> dict:
    """Read the view state.py renders; the server never opens the store."""
    try:
        view = json.loads(PROGRESS_VIEW.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return view if isinstance(view, dict) else {}


def learner_language() -> str:
    language = read_progress().get("language")
    return language if isinstance(language, str) and language else "en"


LANGUAGE = learner_language()
TEXT = MESSAGES.get(LANGUAGE.split("-")[0].lower(), MESSAGES["en"])


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802 - stdlib handler API
        route = urlparse(self.path).path
        if route == "/":
            self._lesson_index()
            return
        if route == "/progress":
            self._progress()
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
<body><main><p class="eyebrow">TECHNE</p><h1>{html.escape(TEXT['heading'])}</h1><ul>{content}</ul>
<p><a href="/progress">{html.escape(TEXT['progress_link'])}</a></p></main></body></html>"""
        payload = document.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _progress(self):
        """Render the mastery map from the progress view, grouped by subject domain."""
        progress = read_progress()
        mastery = progress.get("mastery")
        groups: dict[str, list[tuple[str, str, str]]] = {}
        if isinstance(mastery, dict):
            for subject, entry in sorted(mastery.items()):
                if not isinstance(entry, dict):
                    continue
                domain, _, name = subject.partition(".")
                groups.setdefault(domain, []).append(
                    (name or subject, entry.get("state", "not_started"), entry.get("last_evidence_at") or "")
                )

        sections = []
        ordered = sorted(groups, key=lambda name: (DOMAIN_ORDER.index(name) if name in DOMAIN_ORDER else 99, name))
        for domain in ordered:
            subjects = groups[domain]
            subjects.sort(key=lambda row: (STATE_ORDER.index(row[1]) if row[1] in STATE_ORDER else 9, row[0]))
            rows = "".join(
                f"<tr><td>{html.escape(name.replace('-', ' '))}</td>"
                f'<td><span class="state {html.escape(state, quote=True)}">{html.escape(TEXT.get(state, state))}</span></td>'
                f"<td>{html.escape(seen[:10])}</td></tr>"
                for name, state, seen in subjects
            )
            label = TEXT.get(f"domain.{domain}", domain)
            sections.append(f"<h2>{html.escape(label)}</h2><table>{rows}</table>")

        reviews = progress.get("reviews_due") if isinstance(progress.get("reviews_due"), list) else []
        today = datetime.now().astimezone().date().isoformat()
        due = sorted((item for item in reviews if str(item.get("due_on", "")) <= today), key=lambda item: item["due_on"])
        if due:
            items = "".join(
                f"<li>{html.escape(str(item['subject']))} <small>{html.escape(TEXT['due_on'])} {html.escape(str(item['due_on']))}</small></li>"
                for item in due
            )
            sections.insert(0, f"<h2>{html.escape(TEXT['due_reviews'])}</h2><ul>{items}</ul>")

        content = "".join(sections) or f"<p>{html.escape(TEXT['progress_empty'])}</p>"
        document = f"""<!doctype html>
<html lang="{html.escape(LANGUAGE, quote=True)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TEXT['progress_title'])}</title><link rel="stylesheet" href="/assets/course.css"></head>
<body><main><p class="eyebrow">TECHNE</p><h1>{html.escape(TEXT['progress_heading'])}</h1>
<p class="lede">{html.escape(TEXT['progress_legend'])}</p>{content}</main></body></html>"""
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
