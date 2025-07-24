from collections.abc import Callable, Generator, Iterable, Sequence
from typing import Any, TypeVar

from ._protecols import SupportsAllComparisonT

T = TypeVar("T")
S = TypeVar("S")


def _none_key(key: Callable[[T], Any], default: T) -> Callable[[T], SupportsAllComparisonT]:
    """
    Creates a new key function that returns a default value if the input is None, the original value (with the key
    applied if given) otherwise.
    """
    if key is None:

        def new_key(x):
            if x is None:
                return default
            return x
    else:

        def new_key(x):
            if x is None:
                return default
            return key(x)

    return new_key


def _none_yielder(values: Iterable[T], key: Callable[[T], S], default: T) -> Generator[T | S, None, None]:
    """Yields values from the iterable, applying a key function if provided, while replacing None values with a
    default value."""
    if key is None:
        for val in values:
            if val is None:
                yield default
            else:
                yield val
    else:
        for val in values:
            if val is None:
                yield default
            else:
                yield key(val)


def arg_none_max(values: Sequence[T], *, key: Callable[[T], SupportsAllComparisonT] | None = None) -> int | None:
    """
    Returns the first index of the minimum value in the sequence, using the build-in `min` function, while ignoring
    None values.

    Parameters
    ----------
    values : Sequence[T]
        The sequence of values to search.
    key : Callable[[T], Any]
        An optional one argument key function to extract a comparison key from each element in the sequence. If None,
        the elements themselves are compared.

    Returns
    -------
    int | None
        The index of the maximum value in the sequence, or None if all values are None.
    """
    return _arg_none_minmax(max, values, float("-inf"), key=key)


def arg_none_min(values: Sequence[T], *, key: Callable[[T], Any] | None = None) -> int | None:
    """
    Finds the first index of the minimum value in the sequence, using the build-in `min` function, while ignoring
    None values.

    Parameters
    ----------
    values : Sequence[T]
        The sequence of values to search.
    key : Callable[[T], Any]
        An optional one argument key function to extract a comparison key from each element in the sequence. If None,
        the elements themselves are compared.

    Returns
    -------
    int | None
        The index of the minimum value in the sequence, or None if all values are None.
    """
    return _arg_none_minmax(min, values, float("inf"), key=key)


def _arg_none_minmax(
    func: callable,
    values: Iterable[T],
    default: T,
    *,
    key: Callable[[T], SupportsAllComparisonT] | None = None,
) -> int | None:
    if not isinstance(values, Iterable):
        msg = "`values` must be an iterable"
        raise TypeError(msg)

    if isinstance(values, Iterable) and not isinstance(values, Sequence):
        max_val = default
        max_idx = None
        for index, val in enumerate(values):
            if val is None:
                continue
            if func(max_val, val) != max_val:
                max_val = val
                max_idx = index
        return max_idx
    if len(values) == 0:
        msg = "`values` should be non-empty"
        raise ValueError(msg)
    if hasattr(values, "index"):
        yielder = _none_yielder(values, key, default)
        res = func(yielder)
        if res == default:
            return None
        return values.index(res)
    new_key = _none_key(key, default)
    index = func(range(len(values)), key=new_key)
    if values[index] is None:
        return None
    return index


def arg_max(values: Sequence[T], *, key: Callable[[T], SupportsAllComparisonT] | None = None) -> int:
    """
    Finds the first index of the minimum value in the sequence, using the build-in `min` function.

    Parameters
    ----------
    values : Sequence[T]
        The sequence of values to search.
    key : Callable[[T], Any]
        An optional one argument key function to extract a comparison key from each element in the sequence. If None,
        the elements themselves are compared.
    """
    return _argfunc(max, values, key=key)


def arg_min(values: Sequence[T], *, key: Callable[[T], SupportsAllComparisonT] | None = None) -> int:
    """
    Finds the first index of the minimum value in the sequence, using the build-in `min` function.

    Parameters
    ----------
    values : Sequence[T]
        The sequence of values to search.
    key : Callable[[T], Any]
        An optional one argument key function to extract a comparison key from each element in the sequence. If None,
        the elements themselves are compared.

    Returns
    -------
    int
        The index of the minimum value in the sequence.
    """
    return _argfunc(min, values, key=key)


def _argfunc(
    func: callable,
    values: Iterable[T],
    *,
    key: Callable[[T], SupportsAllComparisonT] | None = None,
) -> int:
    if not isinstance(values, Iterable):
        msg = "`values` should be an iterable"
        raise TypeError(msg)
    if isinstance(values, Sequence) and len(values) == 0:
        msg = "`values` should be non-empty"
        raise ValueError(msg)

    if hasattr(values, "index"):
        return values.index(func(values, key=key))
    if isinstance(values, Sequence):
        return func(range(len(values)), key=values.__getitem__)
    if isinstance(values, Iterable):
        values_iter = iter(values)
        try:
            max_val = next(values_iter)
        except StopIteration:
            msg = "`values` should be non-empty"
            raise ValueError(msg)

        max_idx = 0
        for index, val in enumerate(values_iter, start=1):
            if val is None:
                continue
            if func(max_val, val) != max_val:
                max_val = val
                max_idx = index
        return max_idx
    msg = "`values` should be non-empty"
    raise TypeError(msg)


def _none_minmax(
    func: callable,
    values: Sequence[T],
    default: T,
    *,
    key: Callable[[T], SupportsAllComparisonT] | None = None,
) -> int | None:
    if not isinstance(values, Iterable):
        msg = "`values` should be a iterable"
        raise TypeError(msg)
    yielder = _none_yielder(values, key, default)
    try:
        res = func(yielder)
    except BaseException as e:
        msg = "Invalid input for function"
        raise ValueError(msg) from e
    if res == default:
        return None
    return res


def none_min(values: Sequence[T], *, key: Callable[[T], SupportsAllComparisonT] | None = None) -> T | None:
    """
    Finds the minimum value in the sequence, ignoring None values.

    Parameters
    ----------
    values : Sequence[T]
        The sequence of values to search.
    key : Callable[[T], Any]
        An optional one argument key function to extract a comparison key from each element in the sequence. If None,
        the elements themselves are compared.

    Returns
    -------
    T | None
        The minimum value in the sequence, or None if all values are None.

    Notes
    -----
    If all the values are `inf`, the function will also return None.
    """
    return _none_minmax(min, values, float("inf"), key=key)


def none_max[T](values: Sequence[T], *, key: Callable[[T], Any] | None = None) -> T | None:
    """
    Finds the maximum value in the sequence, ignoring None values.

    Parameters
    ----------
    values : Sequence[T]
        The sequence of values to search.
    key : Callable[[T], Any]
        An optional one argument key function to extract a comparison key from each element in the sequence. If None,
        the elements themselves are compared.

    Returns
    -------
    T | None
        The maximum value in the sequence, or None if all values are None.

    Notes
    -----
    If all the values are `-inf`, the function will also return None.
    """
    return _none_minmax(max, values, float("-inf"), key=key)
