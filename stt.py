from pathlib import Path


class STTError(Exception):
    """Raised when speech transcription fails."""


def transcribe(audio_path: str) -> str:
    """
    Transcribe an audio file using Sarvam AI.

    Args:
        audio_path: Path to local audio file.

    Returns:
        Transcript string.

    Raises:
        STTError
    """
    raise NotImplementedError