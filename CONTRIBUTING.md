# Contributing to Telegram AI Chatbot

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

- Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template
- Search existing issues to avoid duplicates
- Include steps to reproduce, expected behavior, and environment details

### Suggesting Features

- Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template
- Describe the problem and proposed solution clearly
- Check if the feature aligns with the project's scope

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Ensure code passes linting:
   ```bash
   ruff check src/
   black --check src/
   ```
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request using the [PR template](.github/PULL_REQUEST_TEMPLATE.md)

## Development Setup

```bash
# Clone the repository
git clone https://github.com/hubduing/telegram-ai-chatbot.git
cd telegram-ai-chatbot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install dev tools
pip install ruff black mypy pre-commit

# Install pre-commit hooks
pre-commit install
```

## Code Style

- Follow PEP 8
- Use type hints for all function signatures
- Use `async/await` for all I/O operations
- Keep functions small and focused
- Write descriptive commit messages

## Testing

- Test your changes manually with a real Telegram bot
- Ensure the bot starts without errors
- Verify conversation history works correctly
- Check that error handling is graceful

## Questions?

Open an issue with the label `question` or reach out to the maintainers.