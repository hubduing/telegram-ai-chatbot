import asyncio
import logging

from src.bot import main as run_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    asyncio.run(run_bot())