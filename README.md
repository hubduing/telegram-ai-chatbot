# Telegram AI Bot

Асинхронный Telegram-бот с поддержкой различных LLM-провайдеров (OpenAI, OpenRouter и других OpenAI-совместимых API).

## Возможности

- Отправка сообщений в LLM (OpenAI / OpenRouter / любые OpenAI-совместимые API)
- Хранение истории диалога в SQLite (контекст сохраняется после перезапуска)
- Автоматическая очистка старого контекста (не более N последних сообщений)
- Команда `/clear` для очистки истории пользователя
- Индикатор "печатает..." во время ожидания ответа
- Легко добавлять новых провайдеров (Ollama, Groq, Together AI и др.)

## Требования

- Python 3.10+
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- API ключ от LLM-провайдера

## Быстрый старт с OpenRouter (бесплатно)

### 1. Регистрация на OpenRouter

1. Перейдите на [openrouter.ai](https://openrouter.ai)
2. Зарегистрируйтесь (можно через GitHub или Google)
3. Пополните баланс (минимально $1) или используйте бесплатные модели

### 2. Получение API Key

1. Войдите в аккаунт OpenRouter
2. Перейдите в раздел **Keys** (https://openrouter.ai/keys)
3. Нажмите **Create Key**
4. Скопируйте полученный ключ

### 3. Настройка проекта

```bash
# Клонировать или скопировать файлы проекта
# Установить зависимости
pip install -r requirements.txt

# Создать файл .env из примера
cp .env.example .env
```

### 4. Заполнение .env

Отредактируйте файл `.env`:

```
BOT_TOKEN=your_telegram_bot_token_here        # Токен от @BotFather
LLM_PROVIDER=openrouter                        # Провайдер
LLM_API_KEY=sk-or-v1-...                       # Ваш ключ OpenRouter
LLM_BASE_URL=https://openrouter.ai/api/v1      # Базовый URL
LLM_MODEL=deepseek/deepseek-chat-v3-0324:free  # Бесплатная модель
MAX_HISTORY_MESSAGES=15                        # Глубина контекста
```

### 5. Запуск

```bash
python bot.py
```

Бот запущен и готов к работе!

## Использование с OpenAI

Просто измените параметры в `.env`:

```
LLM_PROVIDER=openai
LLM_API_KEY=sk-...                              # Ваш OpenAI API ключ
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo
```

## Команды

- `/start` — начать работу с ботом
- `/help` — показать справку
- `/clear` — очистить историю диалога

## Добавление нового провайдера

Чтобы добавить нового провайдера (например, Ollama, Groq, Together AI),
нужно изменить только файл `services/llm.py`:

1. Создайте класс-клиент, реализующий метод `async def chat(self, messages) -> str`
2. Зарегистрируйте его в словаре `PROVIDERS`
3. Укажите провайдер в `.env`

Код бота (`bot.py`) менять не нужно.

## Структура проекта

```
├── bot.py                 # Основная логика Telegram-бота
├── config.py              # Загрузка конфигурации из .env
├── database.py            # Работа с SQLite (история диалогов)
├── services/
│   ├── __init__.py
│   └── llm.py             # Унифицированный LLM-клиент
├── .env.example           # Пример файла конфигурации
├── .gitignore
├── requirements.txt
└── README.md