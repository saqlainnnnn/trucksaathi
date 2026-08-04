from rich.table import Table

from schemas import BookingExtraction, ValidationResult


def booking_table(booking: BookingExtraction) -> Table:
    table = Table(title="📦 Extracted Booking")

    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")
    table.add_column("Confidence", justify="center")
    table.add_column("Reason")

    for field_name, field in booking:
        table.add_row(
            field_name,
            field.value or "-",
            f"{field.confidence:.2f}",
            field.reason or "-",
        )

    return table


def validation_table(
    booking: BookingExtraction,
    validation: ValidationResult,
) -> Table:

    table = Table(title="✅ Validation")

    table.add_column("Field", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Notes")

    for field_name, field in booking:
        status = "✅"
        note = ""

        if field_name in validation.missing_fields:
            status = "❌"
            note = "Missing"

        elif field_name in validation.low_confidence_fields:
            status = "⚠️"
            note = "Low confidence"

        else:
            for issue in validation.invalid_fields:
                if issue.field == field_name:
                    status = "❌"
                    note = issue.reason
                    break

        table.add_row(
            field_name,
            status,
            note,
        )

    return table
