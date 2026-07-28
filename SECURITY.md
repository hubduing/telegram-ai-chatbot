# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.x     | Yes                |
| < 1.0   | No                 |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not** open a public issue for security vulnerabilities.

Instead, please email the maintainer directly at: **security@hubduing.dev**

Include the following information:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You will receive a response within 48 hours. If the issue is confirmed, we will work on a patch and release it as soon as possible.

## Security Best Practices

When contributing or deploying this bot:

- Never commit `.env` files or API keys to version control
- Use environment variables for all secrets
- Rotate API keys regularly
- Use the latest stable Python version
- Keep dependencies up to date
- Run the bot in a container when possible
- Limit bot permissions to only what is necessary