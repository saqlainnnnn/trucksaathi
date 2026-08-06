from __future__ import annotations

from config import settings

from telegram_bot.app import TruckSaathiApp
from telegram_bot.bot import TruckSaathiBot
from telegram_bot.handlers import VoiceHandler


def main() -> None:
    app = TruckSaathiApp()

    handler = VoiceHandler(
        manager=app.manager,
        dashboard=app.dashboard_repository,
    )

    bot = TruckSaathiBot(
        token=settings.telegram_bot_token,
        voice_handler=handler,
    )

    try:
        bot.run()

    finally:
        app.close()


if __name__ == "__main__":
    main()