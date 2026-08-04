from pathlib import Path
from time import perf_counter

from rich.console import Console
from rich.panel import Panel

from speech import STTError, transcribe

console = Console()


def main() -> None:
    console.rule("[bold cyan]🚛 TruckSaathi")

    audio = Path("sample_audio/full context hyd to blr.m4a")

    console.print(f"🎤 Transcribing [bold]{audio.name}[/bold]")

    start = perf_counter()

    try:
        result = transcribe(audio)

    except STTError as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    elapsed = perf_counter() - start

    console.print(f"✅ Completed in {elapsed:.2f}s")

    console.print(
        Panel.fit(
            result.transcript,
            title="Transcript",
            border_style="green",
        )
    )

    if result.language_code:
        console.print(f"Language : {result.language_code}")

    if result.language_probability is not None:
        console.print(
            f"Confidence : {result.language_probability:.2f}"
        )


if __name__ == "__main__":
    main()