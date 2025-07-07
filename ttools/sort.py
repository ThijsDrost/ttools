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
        sorted_values = sorted(zip(sorter, *others, strict=True), key=key_sorter, reverse=reverse)
    except ValueError as e:
        raise ValueError('The lengths of the lists must be the same.') from e
    return tuple(zip(*sorted_values))