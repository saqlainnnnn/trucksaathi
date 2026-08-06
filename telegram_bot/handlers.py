from __future__ import annotations

import subprocess
import time
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from conversation.manager import ConversationManager
from dashboard.repository import DashboardRepository


class VoiceHandler:
    """
    Telegram update handlers.
    """

    def __init__(
        self,
        manager: ConversationManager,
        dashboard: DashboardRepository,
    ) -> None:
        self._manager = manager
        self._dashboard = dashboard

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        print("✅ /start received")

        if update.message is None:
            return

        await update.message.reply_text(
            "🚛 Welcome to TruckSaathi!\n\n"
            "Send me a voice message to book a truck."
        )

    async def help(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        if update.message is None:
            return

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
            return

        user_id = str(update.effective_chat.id)

        temp_dir = Path("temp")
        temp_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        ogg_path = temp_dir / f"{user_id}.ogg"
        wav_path = temp_dir / f"{user_id}.wav"

        #
        # Telegram Stage
        #

        telegram_start = time.perf_counter()

        self._dashboard.stage_started(
            "telegram_in",
        )

        self._dashboard.log(
            "Telegram update received.",
        )

        telegram_file = await context.bot.get_file(
            update.message.voice.file_id,
        )

        await telegram_file.download_to_drive(
            custom_path=str(ogg_path),
        )

        print(f"⬇ Downloaded to {ogg_path}")

        self._dashboard.log(
            "Voice note downloaded.",
        )

        self._dashboard.stage_finished(
            "telegram_in",
            (
                time.perf_counter()
                - telegram_start
            )
            * 1000,
        )

        #
        # FFmpeg Stage
        #

        ffmpeg_start = time.perf_counter()

        self._dashboard.stage_started(
            "ffmpeg",
        )

        print("🎵 Converting to WAV...")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(ogg_path),
                "-ar",
                "16000",
                "-ac",
                "1",
                str(wav_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print(f"✅ Converted to {wav_path}")

        self._dashboard.stage_finished(
            "ffmpeg",
            (
                time.perf_counter()
                - ffmpeg_start
            )
            * 1000,
        )

        self._dashboard.log(
            "Audio converted to WAV.",
        )

        #
        # Process conversation
        #

        try:
            response = self._manager.process(
                user_id=user_id,
                audio_path=wav_path,
            )

        except Exception as exc:
            print(exc)

            await update.message.reply_text(
                str(exc),
            )
            return

        #
        # Telegram Reply Stage
        #

        reply_start = time.perf_counter()

        self._dashboard.stage_started(
            "telegram_out",
        )

        with open(
            response.reply_audio_path,
            "rb",
        ) as audio:
            await update.message.reply_voice(
                voice=audio,
            )

        self._dashboard.stage_finished(
            "telegram_out",
            (
                time.perf_counter()
                - reply_start
            )
            * 1000,
        )

        self._dashboard.log(
            "Reply sent to Telegram.",
        )

        print("✅ Reply sent")