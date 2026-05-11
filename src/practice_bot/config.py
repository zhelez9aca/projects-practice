"""Environment and runtime settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]


def load_env_file(env_path: Path | None = None) -> None:
    """Load a small .env file without external dependencies."""

    target = env_path or ROOT_DIR / ".env"
    if not target.exists():
        return

    for line in target.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


@dataclass(frozen=True)
class Settings:
    bot_token: str  = "AAHprDh_PXof3fGeV9hst9L86rIywarzxZs"
    web_host: str = "127.0.0.1"
    web_port: int = 8000

    def require_bot_token(self) -> str:
        token = self.bot_token.strip()
        if not token:
            raise RuntimeError(
                "Переменная BOT_TOKEN не задана. Создайте .env в корне репозитория "
                "и добавьте строку BOT_TOKEN=<ваш_токен>."
            )
        return token


def get_settings() -> Settings:
    load_env_file()
    port_value = os.getenv("WEBAPP_PORT", "8000").strip()
    return Settings(
        bot_token=os.getenv("BOT_TOKEN", "8642066577:AAHprDh_PXof3fGeV9hst9L86rIywarzxZs"),
        web_host=os.getenv("WEBAPP_HOST", "127.0.0.1").strip() or "127.0.0.1",
        web_port=int(port_value or "8000"),
    )
