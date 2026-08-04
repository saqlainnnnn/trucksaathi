from pathlib import Path
from time import perf_counter

from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty

from extractor import extract_booking
from speech import STTError, transcribe

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

    elapsed = perf_counter() - start

    console.print(
        f"\n✅ Pipeline completed in {elapsed:.2f}s"
    )

    console.print(
        Panel.fit(
            Pretty(extraction.booking.model_dump()),
            title="Booking Extraction",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    main()