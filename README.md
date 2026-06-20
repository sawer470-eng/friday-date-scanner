# 🎬 Friday Date Scanner

CLI-приложение, которое анализирует Instagram-профиль и подбирает 5 сериалов/фильмов на вечер с Netflix и HBO Max. Использует LLM (Groq или Claude) для анализа интересов и Watchmode API для проверки доступности контента на стримингах.

В репозитории **две версии** одного и того же проекта с идентичным UX:
- 🟢 `version-groq/` — **бесплатная**, на Groq + Llama 3.3 70B
- 🔵 `version-claude/` — **платная**, на Anthropic Claude Sonnet 4.5 (выше качество)

---

## 📑 Содержание

- [Что это и как работает](#-что-это-и-как-работает)
- [Архитектура приложения](#-архитектура-приложения)
- [Технологический стек](#-технологический-стек)
- [Установка и запуск (Groq)](#-установка-и-запуск-groq)
- [Промты: как создавались](#-промты-как-создавались)
- [Промты Groq vs Claude](#-промты-groq-vs-claude)
- [Переход с Groq на Claude](#-переход-с-groq-на-claude)
- [Выход из песочницы Claude](#-выход-из-песочницы-claude)
- [Структура файлов](#-структура-файлов)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Что это и как работает

Приложение делает 4 шага:

1. **Загружает профиль Instagram** — через `instaloader` (реальный аккаунт) или из `mock_profiles.json` (тестовые данные: bio, посты, подписчики).
2. **Анализирует интересы через LLM** — отправляет данные профиля в Groq или Claude с инструкцией подобрать 5 тайтлов под вкус человека.
3. **Проверяет доступность на стримингах** — для каждой рекомендации делает запрос в Watchmode API и оставляет только то, что есть на Netflix или HBO Max.
4. **Выводит таблицу в терминал** — красивый вывод через `rich` с названиями, годом, жанром, платформой и причиной выбора.

### Пример запуска
```bash
python main.py scan anna_arts
```

### Пример вывода
```
┌─────────────── Friday Date Scanner ───────────────┐
│ Анализирую профиль: @anna_arts                    │
└───────────────────────────────────────────────────┘
OK Профиль: Anna Petrova
  Bio: Художница, кофейные зёрна, винил
  Подписчиков: 2847

OK Рекомендаций получено: 5
OK На Netflix/HBO Max найдено: 3

           Рекомендации на вечер
┌───┬──────────────────────┬──────┬──────────┬──────────┐
│ № │ Название             │ Год  │ Платформа│ Почему   │
├───┼──────────────────────┼──────┼──────────┼──────────┤
│ 1 │ Эйфория              │ 2019 │ HBO Max  │ ...      │
│   │ Euphoria             │      │          │          │
└───┴──────────────────────┴──────┴──────────┴──────────┘
```

---

## 🏗 Архитектура приложения

```
┌─────────────┐
│  main.py    │  ← CLI-интерфейс (argparse + rich)
└──────┬──────┘
       │
       ├──→ ┌──────────────┐
       │    │ instagram.py │  загрузка профиля (mock или реальный)
       │    └──────────────┘
       │
       ├──→ ┌──────────────┐    ┌────────────────┐
       │    │ analyzer.py  │───→│ Groq / Claude  │  LLM-анализ
       │    └──────────────┘    └────────────────┘
       │           │
       │           ↓
       │    JSON: [{title_en, title_ru, year, genre, ...}]
       │
       ├──→ ┌──────────────┐    ┌────────────────┐
       │    │ streaming.py │───→│ Watchmode API  │  проверка платформы
       │    └──────────────┘    └────────────────┘
       │
       └──→ Таблица в терминал (rich)
```

### Файлы и их роли

| Файл | Роль |
|---|---|
| `main.py` | CLI: парсит команды (`scan`, `list-profiles`), оркеструет пайплайн |
| `config.py` | Загружает ключи из `.env`, валидирует их |
| `instagram.py` | Грузит профиль: mock из JSON или реальный через `instaloader` |
| `analyzer.py` | Шлёт промт в LLM, парсит JSON-ответ с рекомендациями |
| `streaming.py` | Запрашивает Watchmode, фильтрует по Netflix/HBO Max, нормализует названия |
| `mock_profiles.json` | Тестовые профили: `anna_arts`, `max_tech`, `lena_cozy` |
| `.env` | API-ключи (не коммитится) |
| `.env.example` | Шаблон ключей для других разработчиков |

---

## 🛠 Технологический стек

| Компонент | Технология |
|---|---|
| Язык | Python 3.14 |
| CLI | `argparse` + `rich` (цветной вывод и таблицы) |
| LLM (Groq) | `openai` SDK через Groq endpoint, модель `llama-3.3-70b-versatile` |
| LLM (Claude) | `anthropic` SDK, модель `claude-sonnet-4-5` |
| Instagram | `instaloader` |
| Стриминги | Watchmode API (1000 бесплатных запросов/мес) |
| Конфиг | `python-dotenv` |
| HTTP | `requests` |

### `requirements.txt` (Groq-версия)
```
openai>=1.50.0
instaloader>=4.12
rich>=13.7
python-dotenv>=1.0
requests>=2.31
```

---

## 🚀 Установка и запуск (Groq)

### 1. Клонирование и окружение
```bash
git clone https://github.com/ТВОЙ_ЮЗЕРНЕЙМ/friday-date-scanner.git
cd friday-date-scanner/version-groq
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Получение ключей

**Groq API** (бесплатно):
- Зайди на https://console.groq.com/keys
- **Create API Key** → скопируй (40 символов)

**Watchmode API** (1000 запросов/мес бесплатно):
- Зайди на https://api.watchmode.com/
- Зарегистрируйся → получи ключ из личного кабинета

### 3. Настройка `.env`
```bash
cp .env.example .env
```
Открой `.env` и впиши:
```
GROQ_API_KEY=gsk_твой_ключ_groq
GROQ_MODEL=llama-3.3-70b-versatile
WATCHMODE_API_KEY=твой_ключ_watchmode
IG_LOGIN=
IG_PASSWORD=
```

### 4. Запуск
```bash
python main.py list-profiles          # показать тестовые профили
python main.py scan anna_arts         # анализ профиля
python main.py scan max_tech
python main.py scan lena_cozy
```

---

## ✍️ Промты: как создавались

Промт для LLM — это **самая критичная часть приложения**. От него зависит, вернёт ли модель валидный JSON, правильные ли названия фильмов и не сломается ли поиск в Watchmode.

### Эволюция промта (3 итерации)

**Итерация 1 — наивный промт:**
```
Проанализируй профиль и порекомендуй 5 сериалов на вечер.
```
❌ **Проблема:** модель возвращала текст вместо JSON, названия были на русском вперемешку с английским, иногда добавляла фильмы не с Netflix.

**Итерация 2 — добавили JSON-формат:**
```
Верни 5 рекомендаций в формате JSON: 
{"recommendations": [{"title": "...", "year": ..., ...}]}
```
❌ **Проблема:** Groq возвращал русские названия (`"Очень странные дела"`), но Watchmode API ищет только по английским названиям IMDb → 0 совпадений.

**Итерация 3 — финальная (разделение языков):**
- Заставили модель возвращать **два названия**: `title_en` (для поиска) и `title_ru` (для отображения)
- Добавили **явные примеры** в системный промт
- Жёстко ограничили список платформ: **только Netflix и HBO Max**
- Запретили markdown-обёртку ` ```json `

✅ **Результат:** стабильный JSON, корректные английские названия для API, красивый русский вывод для пользователя.

---

## 🆚 Промты Groq vs Claude

Оба промта решают одну задачу, но различаются по структуре передачи в API.

### Groq (через OpenAI SDK)

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_msg}
]
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    response_format={"type": "json_object"},  # принудительный JSON
    temperature=0.7,
)
text = response.choices[0].message.content
```

### Claude (через Anthropic SDK)

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    system=SYSTEM_PROMPT,        # system передаётся отдельно!
    messages=[{"role": "user", "content": user_msg}],
)
text = response.content[0].text
```

### Общий SYSTEM_PROMPT (одинаковый для обеих версий)

```
Ты рекомендательный движок для свиданий. Анализируешь Instagram-профиль 
и подбираешь 5 сериалов или фильмов на вечер.

КРИТИЧЕСКИ ВАЖНО:
1. Рекомендуй ТОЛЬКО контент с Netflix или HBO Max.
2. Для каждого тайтла указывай ДВА названия:
   - title_en: официальное английское название как в IMDb (для API)
     Примеры: "Stranger Things", "The Last of Us", "Breaking Bad"
   - title_ru: русское прокатное название для отображения
     Примеры: "Очень странные дела", "Одни из нас", "Во все тяжкие"
3. Возвращай ТОЛЬКО валидный JSON, без markdown-обёртки.

Формат:
{
  "recommendations": [
    {
      "title_en": "Stranger Things",
      "title_ru": "Очень странные дела",
      "year": 2016,
      "genre": "Sci-fi / Horror",
      "platform_hint": "Netflix",
      "reason": "Почему подходит этому профилю (на русском)",
      "mood": "Атмосфера вечера"
    }
  ]
}
```

### Ключевые различия в работе с промтами

| Аспект | Groq | Claude |
|---|---|---|
| `system` | Внутри `messages` с ролью `system` | Отдельный параметр `system=` |
| Принудительный JSON | `response_
