from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from practice_bot.engine import PracticeBotEngine  # noqa: E402


class PracticeBotEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = PracticeBotEngine()

    def test_start_route_returns_project_name(self) -> None:
        reply = self.engine.respond("/start")
        self.assertIn("TrackSwop", reply.text)
        self.assertGreaterEqual(len(reply.suggestions), 3)

    def test_providers_route_contains_core_services(self) -> None:
        reply = self.engine.respond("Провайдеры")
        self.assertIn("Spotify", reply.text)
        self.assertIn("VK Music", reply.text)
        self.assertIn("Local Files", reply.text)

    def test_installation_route_contains_run_command(self) -> None:
        reply = self.engine.respond("Установка")
        self.assertIn("git clone https://github.com/Seregax/TrackSwop.git", reply.text)
        self.assertIn("python src/main.py", reply.text)

    def test_unknown_message_returns_fallback(self) -> None:
        reply = self.engine.respond("непонятный сценарий")
        self.assertIn("Не нашёл сценарий", reply.text)
        self.assertIn("Источники", reply.suggestions)


if __name__ == "__main__":
    unittest.main()
