from pathlib import Path

from openai import OpenAI

from config import settings
from schemas import BookingExtraction, ValidationResult

PROMPT = Path("prompts/followup.md").read_text(encoding="utf-8")

client = OpenAI(
    api_key=settings.groq_api_key,
    base_url=settings.groq_base_url,
)


def generate_followup(
    booking: BookingExtraction,
    validation: ValidationResult,
) -> str:
    """
    Generate one natural follow-up question for missing or invalid fields.
    """

    if validation.is_complete:
        return "Booking complete."

    context = f"""
Current Booking:

{booking.model_dump_json(indent=2)}

Missing Fields:
{validation.missing_fields}

Low Confidence Fields:
{validation.low_confidence_fields}

Invalid Fields:
{validation.invalid_fields}
"""

    completion = client.chat.completions.create(
        model=settings.llm_model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "user",
                "content": context,
            },
        ],
    )

    return completion.choices[0].message.content.strip()