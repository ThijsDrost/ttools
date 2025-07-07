from typing import Iterable, overload, Any
import functools
import operator
import math

from _protecols import Addable

def flatten_2D(value: Iterable[Iterable[Any]], /) -> list[Any]:
    """
    Flatten an iterator of iterators
    """
    return [item for sublist in value for item in sublist]


def flatten_iter(value: Iterable, /, *, max_dept=math.inf) -> Iterable:
    """
    Flatten an arbitrary depth iterator

    Parameters
    ----------
    value : Iterable
        The iterable to flatten.
    max_dept : int, optional
        The maximum depth to flatten. Defaults to infinity, meaning it will flatten all levels.
    """
    if max_dept <= 0:
        yield value
        return

    for item in value:
        if isinstance(item, Iterable):
            yield from flatten_iter(item, max_dept=max_dept-1)
        else:
            yield item


def flatten(value: Iterable, /, *, max_dept=math.inf) -> list:
    """
    Flatten an arbitrary depth iterator

    Parameters
    ----------
    value : Iterable
        The iterable to flatten.
    max_dept : int, optional
        The maximum depth to flatten. Defaults to infinity, meaning it will flatten all levels.
    """
    return list(flatten_iter(value, max_dept=max_dept))


def transpose(iterable: Iterable[Iterable[Any]], /) -> list[list[Any]]:
    """
    Transpose an iterable of iterables.
    """
    return list(map(list, zip(*iterable)))


@overload
def dot(vec1: Iterable[float], vec2: Iterable[float]) -> float:
    ...

@overload
def dot[T: Addable](vec1: Iterable[T], vec2: Iterable[T]) -> T:
    ...

def dot[T](vec1: Iterable[T], vec2: Iterable[T], /,) -> T:
    """
    Returns the dot product of two vectors.

    Raises
    ------
    ValueError
        When the two vectors are not of the same length.
    TypeError
        When the values in the two vecs cannot be added together.
    """
    try:
        return functools.reduce(operator.add, [a * b for a, b in zip(vec1, vec2, strict=True)])
    except ValueError as e:
        raise ValueError('Both vectors must have the same length') from e