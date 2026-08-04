from pathlib import Path

import requests

from config import settings


class TTSError(Exception):
    """Raised when text-to-speech synthesis fails."""


def synthesize(
    text: str,
    output_path: str | Path,
) -> Path:
    """
    Convert text into speech using Smallest.ai.

    Args:
        text: Text to synthesize.
        output_path: Path where the generated audio will be saved.

    Returns:
        Path to the generated audio file.

    Raises:
        TTSError
    """

    if not text.strip():
        raise TTSError("Cannot synthesize empty text.")

    output_path = Path(output_path)

    headers = {
        "Authorization": f"Bearer {settings.smallest_api_key}",
        "Content-Type": "application/json",
        "Accept": "audio/wav",
    }

    payload = {
        "text": text,
        "voice_id": settings.tts_voice_id,
        "model": settings.tts_model,
        "sample_rate": settings.tts_sample_rate,
        "speed": 1.0,
        "language": settings.tts_language,
        "output_format": settings.tts_output_format,
    }

    try:
        response = requests.post(
            settings.smallest_tts_url,
            headers=headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_bytes(response.content)

        return output_path

    except requests.Timeout as exc:
        raise TTSError(
            "Smallest.ai request timed out."
        ) from exc

    except requests.HTTPError as exc:

        response = exc.response

        if response is not None:
            message = response.text
        else:
            message = str(exc)

        raise TTSError(
            f"Smallest.ai HTTP Error:\n{message}"
        ) from exc

    except requests.RequestException as exc:
        raise TTSError(
            f"Network error: {exc}"
        ) from exc


def synthesize_followup(
    question: str,
) -> Path:
    """
    Generate spoken follow-up audio.
    """

    return synthesize(
        question,
        "output/followup.wav",
    )


def synthesize_confirmation() -> Path:
    """
    Generate spoken booking confirmation.
    """

    confirmation = (
        "Aapki truck booking safalta se confirm ho gayi hai. Dhanyavaad."
    )

    return synthesize(
        confirmation,
        "output/confirmation.wav",
    )