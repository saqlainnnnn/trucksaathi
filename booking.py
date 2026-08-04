from copy import deepcopy

from schemas import BookingExtraction


def merge_booking(
    previous: BookingExtraction,
    current: BookingExtraction,
) -> BookingExtraction:
    """
    Merge two extraction results.

    New values overwrite old values only if they exist.
    """

    merged = deepcopy(previous)

    for field_name, field in current:
        if field.value:
            setattr(
                merged,
                field_name,
                field,
            )

    return merged
