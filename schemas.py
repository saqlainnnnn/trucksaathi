from pydantic import BaseModel, Field


class BookingField(BaseModel):
    """
    Represents a single extracted booking field.
    """

    value: str | None = None
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )
    reason: str | None = None


class BookingExtraction(BaseModel):
    """
    Pure extraction returned by the LLM.
    """

    pickup: BookingField = Field(default_factory=BookingField)
    destination: BookingField = Field(default_factory=BookingField)
    truck_type: BookingField = Field(default_factory=BookingField)
    goods: BookingField = Field(default_factory=BookingField)
    weight: BookingField = Field(default_factory=BookingField)
    pickup_date: BookingField = Field(default_factory=BookingField)
    pickup_time: BookingField = Field(default_factory=BookingField)
    contact_name: BookingField = Field(default_factory=BookingField)
    phone_number: BookingField = Field(default_factory=BookingField)


class BookingDraft(BaseModel):
    """
    Internal application state.
    Will evolve as the conversation progresses.
    """

    booking: BookingExtraction

    status: str = "IN_PROGRESS"

    retries: int = 0

    last_question: str | None = None

    missing_fields: list[str] = Field(default_factory=list)


class ExtractionResult(BaseModel):
    """
    Output returned by the extractor.
    """

    transcript: str

    booking: BookingExtraction

    model: str

    processing_time_ms: float | None = None


class TranscriptionResult(BaseModel):
    """
    Output returned by the STT service.
    """

    transcript: str

    language_code: str | None = None

    language_probability: float | None = None

    request_id: str | None = None