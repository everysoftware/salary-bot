import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.config import settings
from src.handlers import routers


def start_polling(bot: Bot, dp: Dispatcher) -> None:
    asyncio.run(dp.start_polling(bot))


def main() -> None:
    logging.basicConfig(level=settings.logging_level, stream=sys.stdout)

    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_routers(*routers)

    start_polling(bot, dp)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
