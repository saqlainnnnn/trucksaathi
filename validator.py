import re

from schemas import (
    BookingExtraction,
    ValidationIssue,
    ValidationResult,
)

REQUIRED_FIELDS = (
    "pickup",
    "destination",
    "truck_type",
    "weight",
    "pickup_date",
)

CONFIDENCE_THRESHOLD = 0.70

WEIGHT_PATTERN = re.compile(
    r"\d+(\.\d+)?\s*(kg|kgs|kilogram|kilograms|ton|tons|tonne|tonnes|टन|किलो)",
    re.IGNORECASE,
)


def validate_booking(
    booking: BookingExtraction,
) -> ValidationResult:
    """
    Validate a booking extracted by the LLM.
    """

    missing_fields: list[str] = []
    low_confidence_fields: list[str] = []
    invalid_fields: list[ValidationIssue] = []

    #
    # Required fields
    #

    for field_name in REQUIRED_FIELDS:

        field = getattr(booking, field_name)

        if not field.value:
            missing_fields.append(field_name)
            continue

        if field.confidence < CONFIDENCE_THRESHOLD:
            low_confidence_fields.append(field_name)

    #
    # Phone number
    #

    if booking.phone_number.value:

        digits = re.sub(
            r"\D",
            "",
            booking.phone_number.value,
        )

        if len(digits) != 10:

            invalid_fields.append(
                ValidationIssue(
                    field="phone_number",
                    reason="Phone number must contain exactly 10 digits.",
                )
            )

    #
    # Weight
    #

    if booking.weight.value and not WEIGHT_PATTERN.search(
        booking.weight.value
    ):
        invalid_fields.append(
            ValidationIssue(
                field="weight",
                reason="Weight should contain a numeric value and unit.",
            )
        )

    #
    # Truck type validation
    #

    if (
        booking.truck_type.value
        and len(booking.truck_type.value.strip()) < 2
    ):
        invalid_fields.append(
            ValidationIssue(
                field="truck_type",
                reason="Truck type appears invalid.",
            )
        )

    #
    # Pickup & Destination sanity check
    #

    if (
        booking.pickup.value
        and booking.destination.value
        and booking.pickup.value.strip().lower()
        == booking.destination.value.strip().lower()
    ):

        invalid_fields.append(
            ValidationIssue(
                field="destination",
                reason="Pickup and destination cannot be the same.",
            )
        )

    return ValidationResult(
        is_complete=(
            len(missing_fields) == 0
            and len(low_confidence_fields) == 0
            and len(invalid_fields) == 0
        ),
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        invalid_fields=invalid_fields,
    )