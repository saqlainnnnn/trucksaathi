from __future__ import annotations

from schemas import BookingExtraction


class MergeEngine:
    """
    Merges booking information across conversation turns.

    Rules:
    - Never overwrite a populated field with an empty one.
    - Fill missing fields.
    - If both fields have values, the newer value wins.
    """

    def merge(
        self,
        current: BookingExtraction,
        incoming: BookingExtraction,
    ) -> BookingExtraction:
        merged = current.model_copy(deep=True)

        for field_name in BookingExtraction.model_fields:
            current_field = getattr(merged, field_name)
            incoming_field = getattr(incoming, field_name)

            if incoming_field.value is None:
                continue

            setattr(merged, field_name, incoming_field)

        return merged