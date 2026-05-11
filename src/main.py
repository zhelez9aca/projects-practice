"""Entry point for both the local web app and the Telegram bot."""

from __future__ import annotations

import argparse
import asyncio

from practice_bot.config import get_settings
from practice_bot.telegram_app import run_bot
from webapp import run_webapp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TrackSwop Assistant Bot runner")
    parser.add_argument(
        "mode",
        nargs="?",
        default="web",
        choices=("web", "bot"),
        help="Run the local web app or the Telegram bot",
    )
    parser.add_argument("--host", default=None, help="Host for the local web server")
    parser.add_argument("--port", type=int, default=None, help="Port for the local web server")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = get_settings()

    if args.mode == "bot":
        asyncio.run(run_bot(settings))
        return

    web_settings = settings
    if args.host or args.port:
        web_settings = settings.__class__(
            bot_token=settings.bot_token,
            web_host=args.host or settings.web_host,
            web_port=args.port or settings.web_port,
        )

    run_webapp(web_settings)


if __name__ == "__main__":
    main()
