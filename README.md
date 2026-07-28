# Telegram AI Chatbot 🤖

[![Release](https://img.shields.io/github/v/release/hubduing/telegram-ai-chatbot?style=for-the-badge&logo=github)](https://github.com/hubduing/telegram-ai-chatbot/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram)](https://docs.aiogram.dev/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit)](https://pre-commit.com/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Lint](https://img.shields.io/github/actions/workflow/status/hubduing/telegram-ai-chatbot/lint.yml?branch=main&style=for-the-badge&label=lint)](https://github.com/hubduing/telegram-ai-chatbot/actions)

An asynchronous Telegram bot powered by OpenAI-compatible LLM APIs. Supports **OpenRouter**, **OpenAI**, and any OpenAI-compatible provider. Extensible architecture — add new providers by editing a single file.

---

## Features ✨

- **Multi-provider LLM support** — OpenRouter, OpenAI, and any OpenAI-compatible API
- **Conversation memory** — remembers last N messages per user (configurable via `.env`)
- **Persistent history** — context survives bot restarts (SQLite)
- **Auto-cleanup** — old messages trimmed automatically to stay within token limits
- **Typing indicator** — shows "typing..." while waiting for LLM response
- **Echo fallback** — works even without an API key
- **Extensible** — add new providers by editing `src/llm.py` only
- **Fully async** — all I/O uses `async/await`
- **Docker support** — ready-to-use Dockerfile and docker-compose
- **CI/CD** — GitHub Actions linting, automated releases

## Requirements 📋

- Python 3.10+
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- API key from an LLM provider (OpenRouter recommended for free tier)

---

## Quick Start with OpenRouter (Free) 🚀

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
# Option A: using Python module
python -m src

# Option B: using run script
python run.py

# Option C: using Docker
docker compose up --build
```

---

## Usage with OpenAI 🔄

Change `.env` to:

```ini
LLM_PROVIDER=openai
LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo
```

## Commands ⌨️

| Command  | Description                    |
|----------|--------------------------------|
| `/start` | Start working with the bot     |
| `/help`  | Show available commands        |
| `/clear` | Clear conversation history     |

---

## Docker 🐳

```bash
# Build and run
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f
```

The database is persisted via a volume mount. No data loss on restart.

---

## Project Structure 📁

```
telegram-ai-chatbot/
├── .github/
│   ├── workflows/
│   │   └── lint.yml              # GitHub Actions: Ruff + Black
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md         # Bug report template
│   │   └── feature_request.md    # Feature request template
│   ├── PULL_REQUEST_TEMPLATE.md  # PR template
│   └── release.yml               # Auto-release on tag push
├── src/
│   ├── __init__.py               # Package marker
│   ├── __main__.py               # Entry point (python -m src)
│   ├── bot.py                    # Telegram bot logic (handlers)
│   ├── config.py                 # Settings from .env (dataclass)
│   ├── database.py               # SQLite wrapper (history storage)
│   └── llm.py                    # Unified LLM client (providers)
├── .editorconfig                 # Editor settings
├── .env.example                  # Configuration template
├── .gitattributes                # Git attributes
├── .gitignore                    # Ignored files
├── .pre-commit-config.yaml       # Pre-commit hooks
├── Dockerfile                    # Docker image
├── LICENSE                       # MIT License
├── README.md                     # This file
├── docker-compose.yml            # Docker Compose
├── pyproject.toml                # Ruff + Black config
├── requirements.txt              # Python dependencies
└── run.py                        # Alternative entry point
```

---

## Adding a New Provider ➕

Edit only `src/llm.py`:

1. Create a class implementing `LLMClient` protocol (must have `async def chat(self, messages) -> str`)
2. Register it in the `PROVIDERS` dict
3. Set `LLM_PROVIDER` in `.env`

No changes to `bot.py` or any other file are required.

Supported providers: `openai`, `openrouter`.

---

## Repository Topics 🔖

Suggested topics for the repository:

```
telegram-bot   aiogram   openai   openrouter   llm   chatbot
python   asyncio   sqlite   ai   gpt   deepseek   docker
```

---

## Development 🛠️

### Setup

```bash
# Install dev dependencies
pip install ruff black pre-commit

# Install pre-commit hooks
pre-commit install

# Run lint
ruff check src/

# Format code
black src/
```

### Release

```bash
# Create and push a tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically create a release
```

---

## Future Plans 📋

- [x] Docker support
- [x] CI/CD pipeline
- [x] GitHub templates
- [ ] Support for Ollama (local models)
- [ ] Support for Groq
- [ ] Support for Together AI
- [ ] Streaming responses
- [ ] Admin commands
- [ ] Unit tests

---

## Contributing 🤝

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code passes linting checks:

```bash
ruff check src/
black --check src/
```

---

## License 📄

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.