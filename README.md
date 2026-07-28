# Telegram AI Chatbot 🤖

An asynchronous Telegram bot powered by OpenAI-compatible LLM APIs (OpenRouter, OpenAI, and more).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue)](https://docs.aiogram.dev/)

## Features

- **Multi-provider LLM support** — works with OpenRouter, OpenAI, and any OpenAI-compatible API
- **Conversation memory** — remembers last N messages per user (configurable, stored in SQLite)
- **Persistent history** — context survives bot restarts thanks to SQLite
- **Auto-cleanup** — old messages are automatically trimmed to stay within token limits
- **Typing indicator** — shows "typing..." while waiting for the LLM response
- **Echo fallback** — works even without an API key (echo mode)
- **Extensible** — add new providers by editing a single file
- **Fully async** — all I/O operations use `async/await`

## Requirements

- Python 3.10+
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- API key from an LLM provider (OpenRouter recommended for free tier)

## Quick Start with OpenRouter (Free)

### 1. Register on OpenRouter

1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up (GitHub / Google / email)
3. Top up your balance ($1 minimum) or use free models

### 2. Get an API Key

1. Log in to your OpenRouter account
2. Navigate to **Keys** → [https://openrouter.ai/keys](https://openrouter.ai/keys)
3. Click **Create Key**
4. Copy the key (starts with `sk-or-v1-`)

### 3. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/hubduing/telegram-ai-chatbot.git
cd telegram-ai-chatbot

# Install dependencies
pip install -r requirements.txt

# Create .env from the example
cp .env.example .env
```

### 4. Edit `.env`

```ini
BOT_TOKEN=1234567890:ABCdefGHIjklmNOPqrstUVwxyz        # From @BotFather
LLM_PROVIDER=openrouter                                 # Provider name
LLM_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   # Your OpenRouter key
LLM_BASE_URL=https://openrouter.ai/api/v1               # API endpoint
LLM_MODEL=deepseek/deepseek-chat-v3-0324:free           # Free model
MAX_HISTORY_MESSAGES=15                                 # Context depth
```

### 5. Run

```bash
python -m src
# or
python run.py
```

## Usage with OpenAI

Change `.env` to:

```ini
LLM_PROVIDER=openai
LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo
```

## Commands

| Command  | Description                    |
|----------|--------------------------------|
| `/start` | Start working with the bot     |
| `/help`  | Show available commands        |
| `/clear` | Clear conversation history     |

## Project Structure

```
telegram-ai-chatbot/
├── src/
│   ├── __init__.py          # Package marker
│   ├── __main__.py          # Entry point (python -m src)
│   ├── bot.py               # Telegram bot logic (handlers)
│   ├── config.py            # Settings from .env (dataclass)
│   ├── database.py          # SQLite wrapper (history storage)
│   └── llm.py               # Unified LLM client (providers)
├── .env.example             # Configuration template
├── .gitignore
├── LICENSE                  # MIT License
├── README.md
├── requirements.txt
└── run.py                   # Alternative entry point
```

## Adding a New Provider

Edit only `src/llm.py`:

1. Create a class implementing `LLMClient` protocol (must have `async def chat(self, messages) -> str`)
2. Register it in the `PROVIDERS` dict
3. Set `LLM_PROVIDER` in `.env`

No changes to `bot.py` or any other file are required.

## Screenshots

> *Screenshots coming soon. Contributions welcome!*

## Future Plans

- [ ] Support for Ollama (local models)
- [ ] Support for Groq
- [ ] Support for Together AI
- [ ] Streaming responses
- [ ] Admin commands
- [ ] Docker support
- [ ] CI/CD pipeline

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.