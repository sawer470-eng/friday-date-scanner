# 🎬 Friday Date Scanner — Groq Edition

> CLI-приложение для анализа Instagram-профиля и подбора сериалов/фильмов для свидания.  
> Работает на бесплатной модели **Groq Llama 3.3 70B** + **Watchmode API** для проверки доступности на Netflix и HBO Max.

---

## 📑 Содержание

1. [Установка и запуск](#-установка-и-запуск)
2. [Промпты — генерация проекта и системные](#-промпты)
3. [Архитектура и стек](#-архитектура)
4. [Переход из песочницы в боевой режим](#-переход-из-песочницы-в-боевой-режим)

---

## 🚀 Установка и запуск

### Требования
- **Python 3.10+** (рекомендуется 3.12 или 3.14)
- **macOS / Linux / Windows**
- API-ключи: **Groq** (бесплатно) и **Watchmode** (бесплатно, 1000 запросов/мес)

### Шаг 1. Клонирование и переход в папку

```bash
git clone <repo-url>
cd friday-date-scanner/version-groq
cat > README.md << 'MDEOF'
# 🎬 Friday Date Scanner — Groq Edition

> CLI-приложение для анализа Instagram-профиля и подбора сериалов/фильмов для свидания.
> Работает на бесплатной модели **Groq Llama 3.3 70B** + **Watchmode API** для проверки доступности на Netflix и HBO Max.

---

## 📑 Содержание

1. [Установка и запуск](#-установка-и-запуск)
2. [Промпты — генерация проекта и системные](#-промпты)
3. [Архитектура и стек](#-архитектура)
4. [Переход из песочницы в боевой режим](#-переход-из-песочницы-в-боевой-режим)

---

## 🚀 Установка и запуск

### Требования
- **Python 3.10+** (рекомендуется 3.12 или 3.14)
- **macOS / Linux / Windows**
- API-ключи: **Groq** (бесплатно) и **Watchmode** (бесплатно, 1000 запросов/мес)

### Шаг 1. Клонирование и переход в папку

\`\`\`bash
git clone <repo-url>
cd friday-date-scanner/version-groq
\`\`\`

### Шаг 2. Виртуальное окружение

\`\`\`bash
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows
\`\`\`

### Шаг 3. Зависимости

\`\`\`bash
pip install -r requirements.txt
\`\`\`

Установятся: openai, instaloader, rich, python-dotenv, requests.

### Шаг 4. API-ключи

Создайте файл `.env` в папке `version-groq/`:

\`\`\`env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile
WATCHMODE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
\`\`\`

**Где взять ключи:**
- Groq: https://console.groq.com/keys (бесплатно, без карты)
- Watchmode: https://api.watchmode.com/ (Free tier — 1000 req/month)

### Шаг 5. Запуск

\`\`\`bash
# Сканировать mock-профиль (песочница)
python main.py scan -u anna_arts
python main.py scan -u max_tech

# Список доступных mock-профилей
python main.py list-profiles
\`\`\`

---

## 🧠 Промпты

### A. Мета-промпт для генерации проекта

> Этот промпт можно отдать любому AI-ассистенту, чтобы он сгенерировал такой же проект с нуля.

\`\`\`
Создай CLI-приложение Friday Date Scanner на Python 3.12+ со следующей архитектурой:

ЦЕЛЬ:
Анализатор Instagram-профиля, который на основе биографии, интересов и постов
рекомендует 5 сериалов/фильмов для свидания, доступных на Netflix и HBO Max.

СТЕК version-groq:
- openai SDK (для Groq через base_url=https://api.groq.com/openai/v1)
- instaloader — реальный парсинг Instagram (опционально)
- rich — красивый CLI-вывод (панели, таблицы, цвета)
- python-dotenv — загрузка .env
- requests — Watchmode API

ФАЙЛЫ:
- main.py — точка входа, CLI на argparse, команды: scan, list-profiles
- config.py — загрузка .env через python-dotenv
- instagram.py — режим песочницы (читает mock_profiles.json) + заготовка под instaloader
- analyzer.py — Groq-клиент + JSON Schema для рекомендаций
- streaming.py — Watchmode API + локальный fallback-словарь
- mock_profiles.json — 2 тестовых профиля (anna_arts, max_tech)
- requirements.txt
- .env.example
- .gitignore (venv, .env, __pycache__, *.pyc)

ОСОБЕННОСТИ:
- Groq должен возвращать ТОЛЬКО английские IMDb-названия (title_en)
  + русский перевод (title_ru), иначе Watchmode не найдёт.
- Рекомендации фильтруются — оставляем только Netflix и HBO Max.
- response_format={"type": "json_object"} для гарантированного JSON.
- Вывод через rich.Panel с эмодзи, цветами, разделителями.
\`\`\`

### B. Системный промпт analyzer.py (используется в боевом коде)

\`\`\`text
You are a TV show and movie recommendation expert for date nights.

⚠️ STRICT RULES:
1. Recommend ONLY shows/movies available on Netflix OR HBO Max (Max).
2. DO NOT recommend Apple TV+, Disney+, Amazon Prime, Hulu, Paramount+ exclusives.
3. "title_en" MUST be the ORIGINAL ENGLISH title (Latin alphabet, IMDb format).
4. "title_ru" is the Russian translation for display.

GOOD EXAMPLES (Netflix/HBO only):
✅ Stranger Things (Netflix), Wednesday (Netflix), Money Heist (Netflix)
✅ House of the Dragon (HBO), The Last of Us (HBO), Succession (HBO)
✅ Euphoria (HBO), The White Lotus (HBO), Bridgerton (Netflix)

BAD EXAMPLES (DO NOT RECOMMEND):
❌ Ted Lasso (Apple TV+) — NOT on Netflix/HBO
❌ The Mandalorian (Disney+) — NOT on Netflix/HBO
❌ The Boys (Amazon) — NOT on Netflix/HBO
❌ The Bear (Hulu) — NOT on Netflix/HBO

Return STRICTLY this JSON:
{
  "recommendations": [
    {
      "title_en": "English IMDb title",
      "title_ru": "Русское название",
      "year": 2022,
      "genre": "Genre",
      "platform_hint": "Netflix" or "HBO Max",
      "reason": "Почему подходит (на русском, 2-3 предложения)",
      "mood": "Атмосфера (на русском)"
    }
  ]
}

Return exactly 5 recommendations, ALL available on Netflix or HBO Max.
\`\`\`

### C. User-промпт (формируется динамически)

\`\`\`text
Analyze this Instagram profile and recommend 5 shows/movies for a date.

PROFILE:
{JSON профиля из mock_profiles.json или Instaloader}

CRITICAL: Only recommend titles available on Netflix or HBO Max.
title_en must be in English (Latin alphabet) for API search.
reason and mood — на русском языке.
\`\`\`

---

## 🏗 Архитектура

### Стек

| Слой | Технология |
|------|------------|
| Язык | Python 3.10+ |
| AI-модель | Groq Llama 3.3 70B Versatile |
| AI SDK | OpenAI Python SDK (через Groq base_url) |
| Streaming API | Watchmode API |
| Парсинг IG | Instaloader (в боевом режиме) |
| CLI UI | Rich (панели, цвета, таблицы) |
| Конфиг | python-dotenv |

### Структура проекта

\`\`\`
version-groq/
├── main.py              # Точка входа, CLI-команды
├── config.py            # Загрузка .env
├── instagram.py         # Источник профилей (mock или Instaloader)
├── analyzer.py          # Groq + JSON Schema + системный промпт
├── streaming.py         # Watchmode + локальный fallback Netflix/HBO
├── mock_profiles.json   # Тестовые профили
├── requirements.txt
├── .env                 # API-ключи (gitignored)
├── .env.example
├── .gitignore
└── README.md
\`\`\`

### Поток данных

\`\`\`
main.py → instagram.py → analyzer.py (Groq) → streaming.py (Watchmode) → main.py (rich output)
\`\`\`

### Ключевые навыки в коде

- **Structured output** — response_format JSON для гарантированного формата
- **Двуязычные поля** — title_en для поиска в API, title_ru для пользователя
- **Каскадный fallback** — Watchmode → локальный словарь → platform_hint от модели
- **Нормализация строк** — fuzzy-matching названий (артикль the, регистр, пунктуация)
- **Защищённая загрузка ключей** — .env + .gitignore
- **Rich CLI** — панели с эмодзи, цветные бэйджи платформ

---

## 🔄 Переход из песочницы в боевой режим

Сейчас приложение читает профили из `mock_profiles.json`.
Чтобы подключить **реальный Instagram через Instaloader**, отредактируйте **один файл**: `instagram.py`.

### Текущая заглушка

\`\`\`python
def get_profile(username, config):
    with open("mock_profiles.json", "r", encoding="utf-8") as f:
        profiles = json.load(f)
    if username not in profiles:
        raise ValueError(f"Профиль '{username}' не найден")
    return profiles[username]
\`\`\`

### Боевой код с Instaloader

\`\`\`python
import instaloader

def get_profile(username, config):
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_comments=False,
        save_metadata=False,
        quiet=True
    )

    ig_login = config.get("IG_LOGIN")
    ig_password = config.get("IG_PASSWORD")
    if ig_login and ig_password:
        try:
            L.login(ig_login, ig_password)
        except Exception as e:
            print(f"⚠ Не удалось войти: {e}")

    profile = instaloader.Profile.from_username(L.context, username)

    posts_text = []
    for i, post in enumerate(profile.get_posts()):
        if i >= 12:
            break
        if post.caption:
            posts_text.append(post.caption[:300])

    return {
        "username": profile.username,
        "full_name": profile.full_name,
        "bio": profile.biography,
        "followers": profile.followers,
        "posts_count": profile.mediacount,
        "recent_posts": posts_text,
        "is_private": profile.is_private,
    }
\`\`\`

Затем добавьте в `.env`:

\`\`\`env
IG_LOGIN=your_instagram_login
IG_PASSWORD=your_instagram_password
\`\`\`

⚠ **Важно:** Instagram может временно блокировать аккаунт за частые API-запросы. Используйте отдельный технический аккаунт.

---

## 📝 Лицензия

MIT
