from __future__ import annotations

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from telegram_bot.handlers import VoiceHandler


class TruckSaathiBot:
    """
    Telegram bot.
    """

    def __init__(
        self,
        token: str,
        voice_handler: VoiceHandler,
    ) -> None:
        self._application = (
            Application.builder()
            .token(token)
            .build()
        )

        self._application.add_handler(
            CommandHandler(
                "start",
                voice_handler.start,
            )
        )

        self._application.add_handler(
            CommandHandler(
                "help",
                voice_handler.help,
            )
        )

        self._application.add_handler(
            MessageHandler(
                filters.VOICE,
                voice_handler.handle_voice,
            )
        )

    def run(self) -> None:
        print("🚛 TruckSaathi Bot Started")

        self._application.run_polling()