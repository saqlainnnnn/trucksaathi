from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

from openai import OpenAI
from pydantic import ValidationError

from config import settings
from schemas import (
    BookingExtraction,
    ExtractionResult,
)

PROMPT = Path("prompts/extraction.md").read_text(encoding="utf-8")

client = OpenAI(
    api_key=settings.groq_api_key,
    base_url=settings.groq_base_url,
)


class ExtractionError(Exception):
    """Raised when booking extraction fails."""


def extract_booking(
    transcript: str,
    model: str | None = None,
) -> ExtractionResult:
    """
    Extract structured logistics booking information from a transcript.

    Args:
        transcript: STT transcript.
        model: Optional model override.

    Returns:
        ExtractionResult

    Raises:
        ExtractionError
    """

    if not transcript.strip():
        raise ExtractionError("Transcript is empty.")

    model = model or settings.llm_model

    start = perf_counter()

    try:
        completion = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": PROMPT,
                },
                {
                    "role": "user",
                    "content": transcript,
                },
            ],
        )

        message = completion.choices[0].message

        if message.content is None:
            raise ExtractionError("LLM returned an empty response.")

        payload = json.loads(message.content)

        booking = BookingExtraction.model_validate(payload)

        elapsed = (perf_counter() - start) * 1000

        return ExtractionResult(
            transcript=transcript,
            booking=booking,
            model=model,
            processing_time_ms=elapsed,
        )

    except json.JSONDecodeError as exc:
        raise ExtractionError("LLM returned invalid JSON.") from exc

    except ValidationError as exc:
        raise ExtractionError(
            f"Structured output validation failed:\n{exc}"
        ) from exc

    except Exception as exc:
        raise ExtractionError(str(exc)) from exc