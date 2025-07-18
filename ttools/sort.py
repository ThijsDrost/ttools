from typing import Iterable

from ._protecols import SupportsRichComparisonT

def sort_by(sorter: Iterable[SupportsRichComparisonT], *to_sort: Iterable, key=None, reverse=False) -> tuple[tuple, ...]:
    """
    Sort several sequences together based on a sorter sequence.
    """
    values = sort_together(sorter, *to_sort, key=key, reverse=reverse)
    return values[1:]


def sort_together(sorter: Iterable[SupportsRichComparisonT], *others: Iterable, key=None, reverse=False) -> tuple[tuple, ...]:
    if key is not None:
        key_sorter = lambda x: key(x[0])
    else:
        key_sorter = lambda x: x[0]
    try:
        zipped = zip(sorter, *others, strict=True)
    except ValueError as e:
        raise ValueError('Could not zip the sequences together. Ensure they are of the same length.') from e
    try:
        sorted_values = sorted(zipped, key=key_sorter, reverse=reverse)
    except ValueError as e:
        raise ValueError('Could not sort the values.') from e
    return tuple(zip(*sorted_values))