"""Local web server for the practice site and bot simulator."""

from __future__ import annotations

import argparse
import json
import mimetypes
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from practice_bot.config import Settings, get_settings
from practice_bot.engine import PracticeBotEngine


ROOT_DIR = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT_DIR / "site"


class PracticeSiteHandler(SimpleHTTPRequestHandler):
    """Serve the static site and expose a small JSON API."""

    def __init__(self, *args, engine: PracticeBotEngine, directory: str | None = None, **kwargs):
        self.engine = engine
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json({"status": "ok"})
            return
        if path.startswith("/repo/"):
            self._serve_repo_file(path.removeprefix("/repo/"))
            return
        super().do_GET()

    def do_HEAD(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json({"status": "ok"}, send_body=False)
            return
        if path.startswith("/repo/"):
            self._serve_repo_file(path.removeprefix("/repo/"), send_body=False)
            return
        super().do_HEAD()

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/api/chat":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown API route")
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length)

        try:
            payload = json.loads(raw_body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON payload"}, status=HTTPStatus.BAD_REQUEST)
            return

        reply = self.engine.respond(str(payload.get("message", "")))
        self._send_json({"text": reply.text, "suggestions": reply.suggestions})

    def _send_json(
        self,
        payload: dict[str, object],
        status: HTTPStatus = HTTPStatus.OK,
        send_body: bool = True,
    ) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def _serve_repo_file(self, relative_path: str, send_body: bool = True) -> None:
        target = (ROOT_DIR / relative_path).resolve()

        if ROOT_DIR not in target.parents and target != ROOT_DIR:
            self.send_error(HTTPStatus.FORBIDDEN, "Access denied")
            return
        if not target.exists() or not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        data = target.read_bytes()
        mime_type, _ = mimetypes.guess_type(str(target))
        content_type = mime_type or "application/octet-stream"
        if content_type.startswith("text/"):
            content_type = f"{content_type}; charset=utf-8"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if send_body:
            self.wfile.write(data)


def run_webapp(settings: Settings | None = None) -> None:
    current_settings = settings or get_settings()
    engine = PracticeBotEngine()
    handler = partial(PracticeSiteHandler, engine=engine, directory=str(SITE_DIR))
    try:
        server = ThreadingHTTPServer((current_settings.web_host, current_settings.web_port), handler)
    except OSError as exc:
        if exc.errno == 48:
            raise RuntimeError(
                f"Порт {current_settings.web_port} уже занят. "
                f"Запустите сервер на другом порту, например: "
                f"`python3 src/main.py web --port {current_settings.web_port + 1}`"
            ) from exc
        raise

    print(f"TrackSwop site is running on http://{current_settings.web_host}:{current_settings.web_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local practice site.")
    parser.add_argument("--host", default=None, help="Host for the HTTP server")
    parser.add_argument("--port", type=int, default=None, help="Port for the HTTP server")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = get_settings()
    override = Settings(
        bot_token=settings.bot_token,
        web_host=args.host or settings.web_host,
        web_port=args.port or settings.web_port,
    )
    run_webapp(override)


if __name__ == "__main__":
    main()
