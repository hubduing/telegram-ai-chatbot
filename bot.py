import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from config import BOT_TOKEN, MAX_HISTORY_MESSAGES
from database import init_db, add_message, get_history, clear_history, trim_history
from services.llm import create_llm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

llm = create_llm()

SYSTEM_PROMPT: str = (
    "You are a helpful and polite assistant. "
    "Respond in the same language the user writes in. "
    "Provide detailed but concise answers."
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "👋 Hello! I am an AI-powered bot.\n\n"
        "Just send me a message and I will reply.\n"
        "I remember the context of our conversation (last "
        f"{MAX_HISTORY_MESSAGES} messages).\n\n"
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
        "The bot remembers the last "
        f"{MAX_HISTORY_MESSAGES} messages in the conversation."
    )


@dp.message(Command("clear"))
async def cmd_clear(message: types.Message) -> None:
    user_id: int = message.from_user.id
    await clear_history(user_id)
    logger.info("History cleared for user %s", user_id)
    await message.answer("✅ Conversation history cleared. Starting fresh!")


@dp.message()
async def handle_message(message: types.Message) -> None:
    user_id: int = message.from_user.id
    user_text: str = message.text or ""

    if not user_text.strip():
        return

    await bot.send_chat_action(chat_id=user_id, action="typing")

    try:
        await add_message(user_id, "user", user_text)
        await trim_history(user_id, max_messages=MAX_HISTORY_MESSAGES)

        if llm:
            history: list[dict[str, str]] = await get_history(
                user_id, limit=MAX_HISTORY_MESSAGES
            )

            messages_for_api: list[dict[str, str]] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            messages_for_api.extend(history)

            reply_text = await llm.chat(messages_for_api)

            await add_message(user_id, "assistant", reply_text)
            await message.answer(reply_text, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.answer(
                f"🤖 Echo: {user_text}\n\n"
                "_(LLM API key is not configured. "
                "Set LLM_API_KEY in .env to enable AI replies.)_"
            )

    except Exception as e:
        logger.error("Error processing message from %s: %s", user_id, e)
        await message.answer(
            "😔 Sorry, an error occurred while processing your request. "
            "Please try again later.\n\n"
            "If the error persists, check:\n"
            "• LLM API key (may be invalid)\n"
            "• Account balance\n"
            "• Server availability"
        )


async def main() -> None:
    await init_db()
    logger.info("Bot started and ready to work!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())