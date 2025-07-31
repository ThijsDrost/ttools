"""
Sort sequences based on another sequence.
"""

from collections.abc import Iterable

from ._protecols import SupportsRichComparisonT


def sort_by(
    sorter: Iterable[SupportsRichComparisonT],
    *to_sort: Iterable,
    key=None,
    reverse=False,
) -> tuple[tuple, ...]:
    """Sort several sequences together based on a sorter sequence."""
    values = sort_together(sorter, *to_sort, key=key, reverse=reverse)
    return values[1:]


def sort_together(
    sorter: Iterable[SupportsRichComparisonT],
    *others: Iterable,
    key=None,
    reverse=False,
) -> tuple[tuple, ...]:
    """Sort several sequences together based on the first sequence."""
    key_sorter = (lambda x: key(x[0])) if key is not None else (lambda x: x[0])

    try:
        zipped = zip(sorter, *others, strict=True)
    except ValueError as e:
        msg = "Could not zip the sequences together. Ensure they are of the same length."
        raise ValueError(msg) from e

    try:
        sorted_values = sorted(zipped, key=key_sorter, reverse=reverse)
    except ValueError as e:
        msg = "Could not sort the values."
        raise ValueError(msg) from e

    return tuple(zip(*sorted_values, strict=False))
