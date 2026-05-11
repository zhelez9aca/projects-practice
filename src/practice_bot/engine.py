"""Intent routing for the TrackSwop documentation bot."""

from __future__ import annotations

from dataclasses import dataclass

from practice_bot.content import (
    ABOUT_TEXT,
    ARCHITECTURE,
    BOT_NAME,
    CONTACTS_TEXT,
    GOALS,
    INSTALLATION_STEPS,
    JOURNAL,
    KEY_FEATURES,
    LOCAL_TEXT,
    MODIFICATION_TEXT,
    PROJECT_NAME,
    PROJECT_TAGLINE,
    PROVIDERS_SUMMARY,
    QUICK_ACTIONS,
    SECURITY_TEXT,
    SOURCES,
    SPOTIFY_TEXT,
    STATUS_TEXT,
    TARGET_USERS,
    TECH_STACK,
    TESTS_TEXT,
    VK_TEXT,
)


@dataclass(frozen=True)
class BotReply:
    text: str
    suggestions: list[str]


def _bulleted(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


class PracticeBotEngine:
    """Keyword-based engine reused by the web demo and Telegram bot."""

    def respond(self, message: str) -> BotReply:
        token = self._normalize(message)
        routes = (
            (("start", "/start", "меню", "главное меню"), self._start),
            (("help", "/help", "помощь", "что умеешь"), self._help),
            (("о проекте", "/about", "about", "описание проекта", "trackswop"), self._about),
            (("пользователи", "для кого", "аудитория"), self._users),
            (("цели", "goals"), self._goals),
            (("возможности", "функции", "features"), self._features),
            (("архитектура", "mvvm", "слои"), self._architecture),
            (("провайдеры", "сервисы", "providers"), self._providers),
            (("spotify",), self._spotify),
            (("vk music", "vk", "вк"), self._vk),
            (("local files", "local", "локальные файлы", "локальный"), self._local),
            (("установка", "запуск", "installation"), self._installation),
            (("безопасность", "tokenstore", "токены"), self._security),
            (("тесты", "проверка", "tests"), self._tests),
            (("журнал", "прогресс", "этапы работы"), self._journal),
            (("статус", "roadmap", "project status"), self._status),
            (("контакты", "автор", "issues"), self._contacts),
            (("источники", "ресурсы", "ссылки", "docs"), self._sources),
            (("модификация", "доработка", "вариативная часть"), self._modification),
        )

        for variants, handler in routes:
            if any(self._matches(token, variant) for variant in variants):
                return handler()

        return self._fallback(message)

    @staticmethod
    def _normalize(message: str) -> str:
        return " ".join((message or "").strip().lower().split())

    @staticmethod
    def _matches(token: str, variant: str) -> bool:
        if token == variant:
            return True
        return f" {variant} " in f" {token} "

    def _start(self) -> BotReply:
        text = (
            f"{BOT_NAME}\n"
            f"Проект-источник: {PROJECT_NAME}\n"
            f"{PROJECT_TAGLINE}\n\n"
            "Бот собран по документации и исходникам TrackSwop и помогает быстро "
            "разобраться в назначении проекта, архитектуре, провайдерах, установке "
            "и источниках."
        )
        return BotReply(text=text, suggestions=QUICK_ACTIONS[:6])

    def _help(self) -> BotReply:
        text = (
            "Поддерживаемые команды:\n"
            "/start, /help, О проекте, Пользователи, Цели, Возможности, "
            "Архитектура, Провайдеры, Spotify, VK Music, Local Files, "
            "Установка, Безопасность, Тесты, Статус, Источники.\n\n"
            "Ответы основаны на README TrackSwop, коде провайдеров и Spotify guide."
        )
        return BotReply(text=text, suggestions=["О проекте", "Архитектура", "Источники"])

    def _about(self) -> BotReply:
        return BotReply(text=ABOUT_TEXT, suggestions=["Пользователи", "Цели", "Возможности"])

    def _users(self) -> BotReply:
        text = f"Кому полезен TrackSwop:\n{_bulleted(TARGET_USERS)}"
        return BotReply(text=text, suggestions=["Цели", "Возможности", "Провайдеры"])

    def _goals(self) -> BotReply:
        text = f"Цели проекта:\n{_bulleted(GOALS)}"
        return BotReply(text=text, suggestions=["Архитектура", "Провайдеры", "Статус"])

    def _features(self) -> BotReply:
        text = (
            f"Ключевые возможности TrackSwop:\n{_bulleted(KEY_FEATURES)}\n\n"
            f"Стек:\n{_bulleted(TECH_STACK)}"
        )
        return BotReply(text=text, suggestions=["Архитектура", "Spotify", "Local Files"])

    def _architecture(self) -> BotReply:
        text = (
            f"Архитектура TrackSwop:\n{_bulleted(ARCHITECTURE)}\n\n"
            "По исходникам центральный реестр ServiceRegistry регистрирует built-in "
            "фабрики для spotify, vk и local."
        )
        return BotReply(text=text, suggestions=["Провайдеры", "Безопасность", "Тесты"])

    def _providers(self) -> BotReply:
        text = f"Поддерживаемые провайдеры:\n{_bulleted(PROVIDERS_SUMMARY)}"
        return BotReply(text=text, suggestions=["Spotify", "VK Music", "Local Files"])

    def _spotify(self) -> BotReply:
        return BotReply(text=SPOTIFY_TEXT, suggestions=["Установка", "Безопасность", "Источники"])

    def _vk(self) -> BotReply:
        return BotReply(text=VK_TEXT, suggestions=["Провайдеры", "Архитектура", "Источники"])

    def _local(self) -> BotReply:
        return BotReply(text=LOCAL_TEXT, suggestions=["Провайдеры", "Архитектура", "Тесты"])

    def _installation(self) -> BotReply:
        text = (
            "Установка и запуск TrackSwop по README:\n"
            f"{_bulleted(INSTALLATION_STEPS)}"
        )
        return BotReply(text=text, suggestions=["Spotify", "Тесты", "Источники"])

    def _security(self) -> BotReply:
        return BotReply(text=SECURITY_TEXT, suggestions=["Spotify", "Архитектура", "Источники"])

    def _tests(self) -> BotReply:
        return BotReply(text=TESTS_TEXT, suggestions=["Статус", "Архитектура", "Источники"])

    def _journal(self) -> BotReply:
        lines = "\n\n".join(
            f"{index}. {title}\n{summary}" for index, (title, summary) in enumerate(JOURNAL, start=1)
        )
        text = f"Три этапа выполнения проектной практики:\n\n{lines}"
        return BotReply(text=text, suggestions=["Модификация", "Источники", "О проекте"])

    def _status(self) -> BotReply:
        return BotReply(text=STATUS_TEXT, suggestions=["Возможности", "Тесты", "Источники"])

    def _contacts(self) -> BotReply:
        return BotReply(text=CONTACTS_TEXT, suggestions=["Источники", "Статус", "О проекте"])

    def _sources(self) -> BotReply:
        lines = "\n".join(f"- {title}: {url}" for title, url in SOURCES)
        text = f"Источники для сайта и бота:\n{lines}"
        return BotReply(text=text, suggestions=["О проекте", "Spotify", "Архитектура"])

    def _modification(self) -> BotReply:
        return BotReply(text=MODIFICATION_TEXT, suggestions=["Журнал", "Источники", "О проекте"])

    def _fallback(self, message: str) -> BotReply:
        raw = (message or "").strip() or "пустой запрос"
        text = (
            f"Не нашёл сценарий для сообщения: «{raw}».\n\n"
            "Попробуйте один из вариантов: О проекте, Возможности, Архитектура, "
            "Провайдеры, Spotify, VK Music, Local Files, Установка или Источники."
        )
        return BotReply(text=text, suggestions=["О проекте", "Провайдеры", "Источники"])
