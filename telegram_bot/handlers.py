from __future__ import annotations

from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from conversation.manager import ConversationManager


class VoiceHandler:
    """
    Telegram update handlers.
    """

    def __init__(
        self,
        manager: ConversationManager,
    ) -> None:
        self._manager = manager

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        print("✅ /start received")

        await update.message.reply_text(
            "🚛 Welcome to TruckSaathi!\n\n"
            "Send me a voice message to book a truck."
        )

    async def help(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        print("ℹ️ /help received")

        await update.message.reply_text(
            "Simply send a voice message.\n"
            "I'll collect the booking details step by step."
        )

    async def handle_voice(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        print("🎤 Voice update received")

        if update.message is None:
            return

        if update.message.voice is None:
            print("❌ No voice found")
            return

        user_id = str(update.effective_chat.id)

        audio_path = Path("temp") / f"{user_id}.ogg"
        audio_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        telegram_file = await context.bot.get_file(
            update.message.voice.file_id,
        )

        await telegram_file.download_to_drive(
            custom_path=str(audio_path),
        )

        print(f"⬇ Downloaded to {audio_path}")

        try:
            response = self._manager.process(
                user_id=user_id,
                audio_path=audio_path,
            )

        except Exception as exc:
            print(exc)

            await update.message.reply_text(
                str(exc),
            )
            return

        with open(
            response.reply_audio_path,
            "rb",
        ) as audio:
            await update.message.reply_voice(
                voice=audio,
            )

        print("✅ Reply sent")