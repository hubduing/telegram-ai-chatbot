# Telegram AI Chatbot

[![Release](https://img.shields.io/github/v/release/hubduing/telegram-ai-chatbot?style=for-the-badge&logo=github)](https://github.com/hubduing/telegram-ai-chatbot/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram)](https://docs.aiogram.dev/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit)](https://pre-commit.com/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![CI](https://img.shields.io/github/actions/workflow/status/hubduing/telegram-ai-chatbot/lint.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/hubduing/telegram-ai-chatbot/actions)

**Telegram AI Chatbot** is an asynchronous Telegram bot that integrates with OpenAI-compatible LLM APIs. It supports OpenRouter, OpenAI, and any provider that implements the OpenAI API specification. The architecture is designed for extensibility — adding a new provider requires changes to a single file only.

---

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [OpenRouter Setup](#openrouter-setup)
- [Running the Bot](#running-the-bot)
- [Available Commands](#available-commands)
- [Docker Usage](#docker-usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [License](#license)

---

## Description

This bot forwards every user message to a configurable LLM backend, maintains per-user conversation history in SQLite, and persists context across restarts. It supports multiple LLM providers through a unified client interface and falls back to echo mode when no API key is configured.

The project follows modern Python practices: fully asynchronous I/O, type hints throughout, immutable configuration via dataclasses, and retry logic with exponential backoff for API errors.

---

## Features

- **Multi-provider support** — works with OpenRouter, OpenAI, and any OpenAI-compatible API
- **Conversation memory** — retains the last N messages per user (configurable via environment variables)
- **Persistent history** — stores conversation context in SQLite; survives bot restarts
- **Automatic context trimming** — removes the oldest messages when the configured limit is exceeded
- **Typing indicator** — displays a "typing..." status while awaiting the LLM response
- **Graceful degradation** — operates in echo mode when no API key is provided
- **Extensible provider system** — adding a new provider requires editing only `src/llm.py`
- **Fully asynchronous** — all network and database operations use `async` / `await`
- **Containerized deployment** — Docker and Docker Compose support included
- **Automated quality checks** — GitHub Actions pipeline runs Ruff linting and Black formatting on every push

---

## Requirements

- Python 3.10 or later
- A Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather))
- An API key from an LLM provider (OpenRouter is recommended for its free tier)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/hubduing/telegram-ai-chatbot.git
   cd telegram-ai-chatbot
   ```

2. **Create and activate a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create the configuration file**

   ```bash
   cp .env.example .env
   ```

---

## Configuration

All configuration is managed through environment variables in the `.env` file.

| Variable               | Default                                        | Description                                      |
|------------------------|------------------------------------------------|--------------------------------------------------|
| `BOT_TOKEN`            | —                                              | Telegram bot token from @BotFather               |
| `LLM_PROVIDER`         | `openrouter`                                   | Provider name (`openai` or `openrouter`)         |
| `LLM_API_KEY`          | —                                              | API key for the selected provider                |
| `LLM_BASE_URL`         | `https://openrouter.ai/api/v1`                | API base URL                                     |
| `LLM_MODEL`            | `deepseek/deepseek-chat-v3-0324:free`          | Model identifier                                 |
| `MAX_HISTORY_MESSAGES` | `15`                                           | Number of recent messages retained per user      |

Example `.env` file:

```ini
BOT_TOKEN=1234567890:ABCdefGHIjklmNOPqrstUVwxyz
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-v1-your-key-here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=deepseek/deepseek-chat-v3-0324:free
MAX_HISTORY_MESSAGES=15
```

> **Note:** If `LLM_API_KEY` is left empty, the bot starts in echo mode and replies by mirroring the user's input.

---

## OpenRouter Setup

OpenRouter provides access to dozens of LLMs through a single API, including free models.

### 1. Create an Account

Navigate to [openrouter.ai](https://openrouter.ai) and sign up using GitHub, Google, or email.

### 2. Obtain an API Key

1. Log in to your OpenRouter account.
2. Go to the **Keys** page at [https://openrouter.ai/keys](https://openrouter.ai/keys).
3. Click **Create Key**.
4. Copy the generated key (it begins with `sk-or-v1-`).

### 3. Configure the Bot

Set the following values in your `.env` file:

```ini
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-v1-your-copied-key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=deepseek/deepseek-chat-v3-0324:free
```

The default model, `deepseek/deepseek-chat-v3-0324:free`, is available at no cost. You can browse other free and paid models on the [OpenRouter models page](https://openrouter.ai/models).

---

## Running the Bot

```bash
# Option A — run as a Python module
python -m src

# Option B — run the entry script
python run.py

# Option C — run with Docker (see Docker Usage below)
docker compose up --build
```

The bot will connect to Telegram and begin responding to messages immediately.

---

## Available Commands

| Command    | Description                         |
|------------|-------------------------------------|
| `/start`   | Display a welcome message           |
| `/help`    | Show the list of available commands |
| `/clear`   | Erase the current conversation history |

---

## Docker Usage

A `Dockerfile` and `docker-compose.yml` are included for containerized deployment.

```bash
# Build the image and start the container
docker compose up --build

# Run in detached mode (background)
docker compose up -d

# Follow the container logs
docker compose logs -f

# Stop the container
docker compose down
```

The SQLite database file is persisted through a Docker volume, so conversation history is retained across container restarts.

---

## Project Structure

```
telegram-ai-chatbot/
├── .github/
│   ├── workflows/
│   │   └── lint.yml                  # CI pipeline configuration
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md             # Bug report template
│   │   └── feature_request.md        # Feature request template
│   ├── PULL_REQUEST_TEMPLATE.md      # Pull request template
│   └── release.yml                   # Automated release workflow
├── src/
│   ├── __init__.py                   # Package marker
│   ├── __main__.py                   # Entry point for python -m src
│   ├── bot.py                        # Telegram bot handlers
│   ├── config.py                     # Environment configuration (dataclass)
│   ├── database.py                   # SQLite operations
│   └── llm.py                        # Unified LLM client
├── .editorconfig                     # Editor configuration
├── .env.example                      # Environment variable template
├── .gitattributes                    # Git attribute rules
├── .gitignore                        # Ignored files
├── .pre-commit-config.yaml           # Pre-commit hooks
├── Dockerfile                        # Docker image definition
├── LICENSE                           # MIT License
├── README.md                         # This file
├── docker-compose.yml                # Docker Compose configuration
├── pyproject.toml                    # Ruff and Black settings
├── requirements.txt                  # Python dependencies
└── run.py                            # Alternative entry point
```

---

## Screenshots

> *Screenshots are coming soon. Contributions are welcome.*

---

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for more details.