from pathlib import Path
from time import perf_counter

from rich.console import Console
from rich.panel import Panel

from conversation.manager import ConversationManager
from conversation.merge import MergeEngine
from conversation.store import MemorySessionStore
from llm.extractor import extract_booking
from llm.followup import generate_followup
from speech.stt import STTError, transcribe
from speech.tts import (
    TTSError,
    synthesize_confirmation,
    synthesize_followup,
)
from ui import booking_table

from validation.validator import validate_booking

console = Console()


def main() -> None:
    console.rule("[bold cyan]🚛 TruckSaathi")

    audio = Path("sample_audio/deliberate incomplete bom to pune.m4a")

    manager = ConversationManager(
        store=MemorySessionStore(),
        merge_engine=MergeEngine(),
        stt=transcribe,
        extractor=extract_booking,
        validator=validate_booking,
        followup_generator=generate_followup,
        followup_tts=synthesize_followup,
        confirmation_tts=synthesize_confirmation,
    )

    pipeline_start = perf_counter()

    try:
        response = manager.process(
            user_id="demo-user",
            audio_path=audio,
        )

    except STTError as exc:
        console.print(f"[bold red]STT Error:[/bold red] {exc}")
        return

    except TTSError as exc:
        console.print(f"[bold red]TTS Error:[/bold red] {exc}")
        return

    console.print(
        Panel.fit(
            response.transcript,
            title="📝 Transcript",
            border_style="green",
        )
    )

    console.print()

    console.print(
        booking_table(
            response.booking,
        )
    )

    console.print()

    console.print(
        Panel.fit(
            response.reply_text,
            title="🤖 Assistant",
            border_style="yellow",
        )
    )

    console.print(
        f"\n🔊 Audio saved to [cyan]{response.reply_audio_path}[/cyan]"
    )

    elapsed = perf_counter() - pipeline_start

    console.print(
        f"\n✅ Pipeline completed in [bold]{elapsed:.2f}s[/bold]"
    )


if __name__ == "__main__":
    main()