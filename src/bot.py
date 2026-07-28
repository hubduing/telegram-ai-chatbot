import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from src.config import settings
from src.database import init_db, add_message, get_history, clear_history, trim_history
from src.llm import create_llm

logger = logging.getLogger(__name__)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

llm = create_llm()

SYSTEM_PROMPT = (
    "You are a helpful and polite assistant. "
    "Respond in the same language the user writes in. "
    "Provide detailed but concise answers."
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "👋 Hello! I am an AI-powered bot.\n\n"
        "Just send me a message and I will reply.\n"
        f"I remember the context of our conversation (last "
        f"{settings.max_history_messages} messages).\n\n"
        "Available commands:\n"
        "/clear — clear conversation history\n"
        "/help — show this help"
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    await message.answer(
        "🤖 Available commands:\n\n"
        "/start — start working with the bot\n"
        "/help — show this help\n"
        "/clear — clear conversation history\n\n"
        f"The bot remembers the last "
        f"{settings.max_history_messages} messages in the conversation."
    )


@dp.message(Command("clear"))
async def cmd_clear(message: types.Message) -> None:
    user_id = message.from_user.id
    await clear_history(user_id)
    logger.info("History cleared for user %s", user_id)
    await message.answer("✅ Conversation history cleared. Starting fresh!")


async def _build_messages(user_id: int) -> list[dict[str, str]]:
    history = await get_history(user_id, limit=settings.max_history_messages)
    return [{"role": "system", "content": SYSTEM_PROMPT}, *history]


@dp.message()
async def handle_message(message: types.Message) -> None:
    user_id = message.from_user.id
    text = (message.text or "").strip()

    if not text:
        return

    await bot.send_chat_action(chat_id=user_id, action="typing")

    try:
        await add_message(user_id, "user", text)
        await trim_history(user_id, max_messages=settings.max_history_messages)

        if llm is None:
            await message.answer(
                f"🤖 Echo: {text}\n\n"
                "_(LLM API key is not configured. "
                "Set LLM_API_KEY in .env to enable AI replies.)_"
            )
            return

        messages = await _build_messages(user_id)
        reply = await llm.chat(messages)

        await add_message(user_id, "assistant", reply)
        await message.answer(reply, parse_mode=ParseMode.MARKDOWN)

    except Exception:
        logger.exception("Error processing message from user %s", user_id)
        await message.answer(
            "😔 Sorry, an error occurred while processing your request.\n"
            "Please try again later.\n\n"
            "If the error persists, check:\n"
            "• LLM API key (may be invalid)\n"
            "• Account balance\n"
            "• Server availability"
        )


async def main() -> None:
    await init_db()
    logger.info("Bot started")
    await dp.start_polling(bot)