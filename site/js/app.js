const messagesElement = document.getElementById("chat-messages");
const suggestionsElement = document.getElementById("chat-suggestions");
const formElement = document.getElementById("chat-form");
const inputElement = document.getElementById("chat-input");
const modeBadgeElement = document.getElementById("mode-badge");
const commandButtons = document.querySelectorAll("[data-command]");

const routes = [
  {
    patterns: ["start", "/start", "меню", "главное меню"],
    text:
      "TrackSwop Assistant Bot\nПроект-источник: TrackSwop\nTelegram-бот и web-справочник по документации проекта TrackSwop.\n\nБот собран по документации и исходникам TrackSwop и помогает быстро разобраться в назначении проекта, архитектуре, провайдерах, установке и источниках.",
    suggestions: ["О проекте", "Возможности", "Архитектура", "Провайдеры"],
  },
  {
    patterns: ["о проекте", "/about", "about", "описание проекта", "trackswop"],
    text:
      "TrackSwop — расширяемое десктопное приложение для импорта, экспорта и управления музыкальными плейлистами между несколькими платформами: Spotify, VK Music и локальными файлами.\n\nПроект прячет различия между API музыкальных сервисов за единым интерфейсом и строится вокруг модульной архитектуры провайдеров. Это позволяет добавлять новые сервисы без переписывания основного приложения.",
    suggestions: ["Пользователи", "Цели", "Возможности"],
  },
  {
    patterns: ["пользователи", "для кого", "аудитория"],
    text:
      "Кому полезен TrackSwop:\n- разработчики, которые делают интеграции с музыкальными сервисами;\n- пользователи, переносящие плейлисты между платформами;\n- десктопные приложения, которым нужен единый слой работы с музыкой;\n- проекты, где важна расширяемая архитектура провайдеров.",
    suggestions: ["Цели", "Возможности", "Провайдеры"],
  },
  {
    patterns: ["цели", "goals"],
    text:
      "Цели проекта:\n- дать единый интерфейс для нескольких музыкальных сервисов;\n- обеспечить надёжный импорт и экспорт плейлистов;\n- безопасно хранить токены авторизации;\n- сохранить расширяемую provider-based архитектуру;\n- поддерживать тестируемую и сопровождаемую кодовую базу.",
    suggestions: ["Архитектура", "Провайдеры", "Статус"],
  },
  {
    patterns: ["возможности", "функции", "features"],
    text:
      "Ключевые возможности TrackSwop:\n- динамическая генерация форм на основе спецификаций провайдера;\n- шифрование токенов через Fernet и хранение в tokens.json;\n- реестр провайдеров для Spotify, VK Music и локальных файлов;\n- импорт и экспорт плейлистов между поддерживаемыми сервисами;\n- нормализация метаданных треков;\n- отслеживание прогресса переноса и базовая статистика.\n\nСтек:\n- Python 3.9+\n- PySide6\n- Spotipy\n- vk_api\n- Cryptography\n- Mutagen",
    suggestions: ["Архитектура", "Spotify", "Local Files"],
  },
  {
    patterns: ["архитектура", "mvvm", "слои"],
    text:
      "Архитектура TrackSwop:\n- presentation layer: Qt-виджеты и ViewModel по MVVM;\n- domain layer: сущности Playlist и Track;\n- service layer: провайдеры Spotify, VK и Local Files;\n- infrastructure layer: TokenStore, конфигурация и логирование;\n- ServiceRegistry как центральный реестр доступных сервисов.\n\nПо исходникам ServiceRegistry регистрирует built-in фабрики для spotify, vk и local.",
    suggestions: ["Провайдеры", "Безопасность", "Тесты"],
  },
  {
    patterns: ["провайдеры", "сервисы", "providers"],
    text:
      "Поддерживаемые провайдеры:\n- Spotify: OAuth2, чтение плейлистов, создание плейлистов, добавление треков.\n- VK Music: авторизация по token + user_id, чтение и экспорт плейлистов.\n- Local Files: импорт из директории и подпапок, экспорт не поддерживается.",
    suggestions: ["Spotify", "VK Music", "Local Files"],
  },
  {
    patterns: ["spotify"],
    text:
      "Spotify-провайдер в TrackSwop использует OAuth2 через браузер. В документации описаны шаги: создать приложение в Spotify Developer Dashboard, получить Client ID и Client Secret, настроить Redirect URI и пройти авторизацию.\n\nПоддерживаемые операции:\n- чтение пользовательских плейлистов;\n- получение треков из плейлиста;\n- создание новых плейлистов;\n- добавление треков в плейлист;\n- экспорт в другие сервисы.\n\nТокены кешируются и хранятся в зашифрованном виде через Fernet.",
    suggestions: ["Установка", "Безопасность", "Источники"],
  },
  {
    patterns: ["vk music", "vk", "вк"],
    text:
      "VK Music в TrackSwop работает через token-based авторизацию: нужны token и user_id. Провайдер получает плейлисты пользователя, читает треки, создаёт плейлисты и добавляет в них найденные треки.\n\nЕсли прямой доступ к трекам плейлиста недоступен, код использует fallback: поиск по названию плейлиста или трека через VK API.",
    suggestions: ["Провайдеры", "Архитектура", "Источники"],
  },
  {
    patterns: ["local files", "local", "локальные файлы", "локальный"],
    text:
      "Local Files-провайдер импортирует музыку из локальной директории. Он поддерживает:\n- корневой плейлист '.' со всеми треками из выбранной папки;\n- плейлисты по подпапкам на один уровень глубины.\n\nСоздание плейлистов и экспорт в локальный источник не поддерживаются.",
    suggestions: ["Провайдеры", "Архитектура", "Тесты"],
  },
  {
    patterns: ["установка", "запуск", "installation"],
    text:
      "Установка и запуск TrackSwop по README:\n- git clone https://github.com/Seregax/TrackSwop.git\n- cd TrackSwop\n- python -m venv venv\n- source venv/bin/activate\n- pip install -r requirements.txt\n- python src/main.py",
    suggestions: ["Spotify", "Тесты", "Источники"],
  },
  {
    patterns: ["безопасность", "tokenstore", "токены"],
    text:
      "Безопасность в TrackSwop завязана на TokenStore:\n- токены шифруются через Fernet перед записью в tokens.json;\n- ключ берётся из переменной окружения TRACKSWOP_MASTER_KEY;\n- если ключ не задан, в dev-режиме генерируется временный ключ с предупреждением;\n- документация Spotify рекомендует не коммитить credentials и хранить чувствительные данные в переменных окружения.",
    suggestions: ["Spotify", "Архитектура", "Источники"],
  },
  {
    patterns: ["тесты", "проверка", "tests"],
    text:
      "В TrackSwop уже есть тесты для ключевых компонентов:\n- Spotify service;\n- TokenStore.\n\nКоманды из README:\n- pytest\n- python -m unittest",
    suggestions: ["Статус", "Архитектура", "Источники"],
  },
  {
    patterns: ["статус", "roadmap", "project status"],
    text:
      "Статус проекта по README: active development.\n\nЧто уже отмечено как реализованное:\n- базовая архитектура приложения;\n- интеграция Spotify;\n- система хранения токенов;\n- unit-тесты для ключевых сервисов.\n\nЧто ещё в работе:\n- дополнительные провайдеры;\n- дальнейшие улучшения UI.",
    suggestions: ["Возможности", "Тесты", "Источники"],
  },
  {
    patterns: ["контакты", "автор", "issues"],
    text:
      "Основной проект по дисциплине: TrackSwop\nРепозиторий: https://github.com/Seregax/TrackSwop\nАвтор TrackSwop: Seregax\nОбратная связь по проекту: https://github.com/Seregax/TrackSwop/issues",
    suggestions: ["Источники", "Статус", "О проекте"],
  },
  {
    patterns: ["источники", "ресурсы", "ссылки", "docs"],
    text:
      "Источники для сайта и бота:\n- Основной репозиторий TrackSwop: https://github.com/Seregax/TrackSwop\n- Главный README проекта: https://github.com/Seregax/TrackSwop/blob/main/README.md\n- Spotify Integration Guide: https://github.com/Seregax/TrackSwop/blob/main/src/model/services/providers/spotify/README.md\n- Раздел Issues: https://github.com/Seregax/TrackSwop/issues\n- Spotify Web API Documentation: https://developer.spotify.com/documentation/web-api\n- Spotipy Documentation: https://spotipy.readthedocs.io/\n- OAuth2 Guide for Spotify: https://developer.spotify.com/documentation/general/guides/authorization/",
    suggestions: ["О проекте", "Spotify", "Архитектура"],
  },
];

function normalize(text) {
  return String(text || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ");
}

function matches(token, pattern) {
  if (token === pattern) {
    return true;
  }

  return ` ${token} `.includes(` ${pattern} `);
}

function fallbackReply(message) {
  const token = normalize(message);
  const route = routes.find(({ patterns }) =>
    patterns.some((pattern) => matches(token, pattern)),
  );

  if (route) {
    return { text: route.text, suggestions: route.suggestions };
  }

  return {
    text:
      `Не нашёл сценарий для сообщения: «${String(message || "").trim() || "пустой запрос"}».\n\n` +
      "Попробуйте один из вариантов: О проекте, Возможности, Архитектура, Провайдеры, Spotify, VK Music, Local Files, Установка или Источники.",
    suggestions: ["О проекте", "Провайдеры", "Источники"],
  };
}

function renderMessage(role, text) {
  const message = document.createElement("article");
  message.className = `message ${role}`;
  message.textContent = text;
  messagesElement.appendChild(message);
  messagesElement.scrollTop = messagesElement.scrollHeight;
}

function renderSuggestions(suggestions) {
  suggestionsElement.innerHTML = "";

  suggestions.forEach((label) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "suggestion";
    button.textContent = label;
    button.addEventListener("click", () => handleUserMessage(label));
    suggestionsElement.appendChild(button);
  });
}

async function fetchReply(message) {
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    modeBadgeElement.textContent = "API online";
    modeBadgeElement.style.background = "rgba(46, 167, 154, 0.18)";
    modeBadgeElement.style.color = "#80dfd6";
    return await response.json();
  } catch (error) {
    modeBadgeElement.textContent = "Fallback mode";
    modeBadgeElement.style.background = "rgba(198, 163, 88, 0.12)";
    modeBadgeElement.style.color = "#f3d287";
    return fallbackReply(message);
  }
}

async function handleUserMessage(message) {
  const trimmed = String(message || "").trim();
  if (!trimmed) {
    return;
  }

  renderMessage("user", trimmed);
  inputElement.value = "";

  const reply = await fetchReply(trimmed);
  renderMessage("assistant", reply.text);
  renderSuggestions(reply.suggestions || []);
}

async function detectMode() {
  try {
    const response = await fetch("/api/health");
    if (!response.ok) {
      throw new Error("health check failed");
    }
    modeBadgeElement.textContent = "API online";
    modeBadgeElement.style.background = "rgba(46, 167, 154, 0.18)";
    modeBadgeElement.style.color = "#80dfd6";
  } catch (error) {
    modeBadgeElement.textContent = "Fallback mode";
    modeBadgeElement.style.background = "rgba(198, 163, 88, 0.12)";
    modeBadgeElement.style.color = "#f3d287";
  }
}

formElement.addEventListener("submit", (event) => {
  event.preventDefault();
  handleUserMessage(inputElement.value);
});

commandButtons.forEach((button) => {
  button.addEventListener("click", () => handleUserMessage(button.dataset.command));
});

renderMessage(
  "assistant",
  "TrackSwop Assistant Bot готов. Спросите про архитектуру, Spotify, провайдеров, установку или источники проекта.",
);
renderSuggestions(["О проекте", "Архитектура", "Провайдеры", "Источники"]);
detectMode();
