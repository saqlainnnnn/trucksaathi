from pathlib import Path
from time import perf_counter

from rich.console import Console
from rich.panel import Panel

from extractor import extract_booking
from speech import STTError, transcribe
from ui import booking_table, validation_table
from validator import validate_booking

console = Console()


def main() -> None:

    console.rule("[bold cyan]🚛 TruckSaathi")

    audio = Path("sample_audio/full context hyd to blr.m4a")

    console.print(f"🎤 Transcribing [bold]{audio.name}[/bold]")

    start = perf_counter()

    try:
        transcription = transcribe(audio)

    except STTError as exc:
        console.print(f"[red]{exc}[/red]")
        return

    console.print(
        Panel.fit(
            transcription.transcript,
            title="Transcript",
            border_style="green",
        )
    )

    console.print("\n🧠 Extracting booking...")

    extraction = extract_booking(
        transcription.transcript,
    )

    console.print()

    console.print(
        booking_table(
            extraction.booking,
        )
    )

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

    elapsed = perf_counter() - start

    if validation.is_complete:
        console.print("\n[bold green]🎉 Booking Complete[/bold green]")
    else:
        console.print("\n[bold red]⚠ Booking Incomplete[/bold red]")

    console.print(
        f"\n✅ Pipeline completed in {elapsed:.2f}s"
    )


if __name__ == "__main__":
    main()