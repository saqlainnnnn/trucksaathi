from mimetypes import guess_type
from pathlib import Path

import requests

from config import settings
from schemas import TranscriptionResult


class STTError(Exception):
    """Raised when speech transcription fails."""


def transcribe(audio_path: str | Path) -> TranscriptionResult:
    """
    Transcribe a local audio file using Sarvam AI.
    """

    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    headers = {
        "api-subscription-key": settings.sarvam_api_key,
    }

    data = {
        "model": "saaras:v3",
        "mode": "transcribe",
    }

    mime_type, _ = guess_type(audio_path)

    if mime_type is None:
        mime_type = "application/octet-stream"

    try:
        with audio_path.open("rb") as audio_file:
            print(
                f"[STT] Uploading {audio_path.name} ({mime_type})"
            )

            files = {
                "file": (
                    audio_path.name,
                    audio_file,
                    mime_type,
                )
            }

            response = requests.post(
                settings.sarvam_stt_url,
                headers=headers,
                files=files,
                data=data,
                timeout=60,
            )

        response.raise_for_status()

        payload = response.json()

        print("[STT] Response:")
        print(payload)

        transcript = payload.get("transcript")

        if not transcript:
            raise STTError(
                "Sarvam returned an empty transcript."
            )

        return TranscriptionResult(
            transcript=transcript,
            language_code=payload.get("language_code"),
            language_probability=payload.get(
                "language_probability"
            ),
            request_id=payload.get("request_id"),
        )

    except requests.Timeout as exc:
        raise STTError(
            "Sarvam request timed out."
        ) from exc

    except requests.HTTPError as exc:
        message = (
            exc.response.text
            if exc.response
            else str(exc)
        )
        raise STTError(
            f"Sarvam HTTP Error:\n{message}"
        ) from exc

    except requests.RequestException as exc:
        raise STTError(
            f"Network error: {exc}"
        ) from exc

    except ValueError as exc:
        raise STTError(
            "Sarvam returned invalid JSON."
        ) from exc