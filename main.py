from pathlib import Path
from time import perf_counter

from rich.console import Console
from rich.panel import Panel

from llm.extractor import extract_booking
from llm.followup import generate_followup
from speech import STTError, transcribe
from speech.tts import (
    TTSError,
    synthesize_confirmation,
    synthesize_followup,
)
from ui import (
    booking_table,
    validation_table,
)
from validation.validator import validate_booking

console = Console()


def main() -> None:
    console.rule("[bold cyan]🚛 TruckSaathi")

    audio = Path("sample_audio/full context hyd to blr.m4a")

    console.print(f"🎤 Transcribing [bold]{audio.name}[/bold]")

    pipeline_start = perf_counter()

    #
    # STT
    #

    try:
        transcription = transcribe(audio)

    except STTError as exc:
        console.print(f"[bold red]STT Error:[/bold red] {exc}")
        return

    console.print(
        Panel.fit(
            transcription.transcript,
            title="📝 Transcript",
            border_style="green",
        )
    )

    #
    # Extraction
    #

    console.print("\n🧠 Extracting booking...")

    extraction = extract_booking(
        transcription.transcript,
    )


    validation = validate_booking(
        extraction.booking,
    )

    console.print()

    console.print(
        booking_table(
            extraction.booking,
        )
    )

    #
    # Validation
    #

    validation = validate_booking(
        extraction.booking,
    )

    console.print()

    console.print(
        validation_table(
            extraction.booking,
            validation,
        )
    )

    #
    # Follow-up / Confirmation
    #

    try:
        if validation.is_complete:
            console.print("\n[bold green]🎉 Booking Complete[/bold green]")

            audio_path = synthesize_confirmation()

            console.print(f"\n🔊 Confirmation saved to [cyan]{audio_path}[/cyan]")

        else:
            question = generate_followup(
                extraction.booking,
                validation,
            )

            console.print()

            console.print(
                Panel.fit(
                    question,
                    title="🤖 Follow-up",
                    border_style="yellow",
                )
            )

            audio_path = synthesize_followup(
                question,
            )

            console.print(f"\n🔊 Follow-up saved to [cyan]{audio_path}[/cyan]")

    except TTSError as exc:
        console.print(f"\n[bold red]TTS Error:[/bold red] {exc}")

    #
    # Pipeline metrics
    #

    elapsed = perf_counter() - pipeline_start

    console.print(f"\n✅ Pipeline completed in [bold]{elapsed:.2f}s[/bold]")


if __name__ == "__main__":
    main()
