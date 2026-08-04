from pydantic import BaseModel, Field


class BookingField(BaseModel):
    value: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: str = ""


class BookingDraft(BaseModel):
    pickup: BookingField = Field(default_factory=BookingField)
    destination: BookingField = Field(default_factory=BookingField)
    truck_type: BookingField = Field(default_factory=BookingField)
    goods: BookingField = Field(default_factory=BookingField)
    weight: BookingField = Field(default_factory=BookingField)
    pickup_date: BookingField = Field(default_factory=BookingField)
    pickup_time: BookingField = Field(default_factory=BookingField)
    contact_name: BookingField = Field(default_factory=BookingField)
    phone_number: BookingField = Field(default_factory=BookingField)


class TranscriptionResult(BaseModel):
    transcript: str
    language_code: str | None = None
    language_probability: float | None = None
    request_id: str | None = None