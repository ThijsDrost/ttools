import math
from typing import Sequence, Iterator, overload, Any
import functools
import operator

import numpy as np


@overload
def sim_product[S, T, U, V, W](iterable1: Sequence[S], iterable2: Sequence[T], iterable3: Sequence[U], iterable4: Sequence[V], iterable5: Sequence[W], *, stop: bool = True) -> Iterator[tuple[S, T, U, V, W]]:
    ...

@overload
def sim_product[S, T, U, V](iterable1: Sequence[S], iterable2: Sequence[T], iterable3: Sequence[U], iterable4: Sequence[V], *, stop: bool = True) -> Iterator[tuple[S, T, U, V]]:
    ...

@overload
def sim_product[S, T, U](iterable1: Sequence[S], iterable2: Sequence[T], iterable3: Sequence[U], *, stop: bool = True) -> Iterator[tuple[S, T, U]]:
    ...

@overload
def sim_product[S, T](iterable1: Sequence[S], iterable2: Sequence[T], *, stop: bool = True) -> Iterator[tuple[S, T]]:
    ...

@overload
def sim_product[S](iterable1: Sequence[S], *, stop: bool = True) -> Iterator[tuple[S,]]:
    ...


def sim_product(*args: Sequence, stop=True) -> Iterator[tuple]:
    """
    Create a generator that yields all the combinations of the given iterables.

    Parameters
    ----------
    args:  Sequence
        The sequences to combine.
    stop: bool
        When true, the iterator loops back to the beginning when all possibilities have been yielded, thus it never stops.
        When false, it will raise a StopIteration exception when all possibilities have been yielded.

    Yields
    ------
    tuple
        A tuple containing one element from each of the input sequences, in a specific order.

    Notes
    -----
    It will return the same cartesian product as :external+python:py:func:`itertools.product`, but in a different order.

    Examples
    --------
    >>> list(sim_product([0, 1, 2], [0, 1, 2]))
    [(0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (2, 0), (0, 2), (1, 0), (2, 1)]

    >>> list(sim_product([0, 1], [0, 1, 2]))
    [(0, 0), (1, 1), (0, 2), (1, 0), (0, 1), (1, 2)]

    >>> list(sim_product([0, 1], [0, 1, 2], [0, 1]))
    [(0, 0, 0), (1, 1, 1), (0, 2, 0), (1, 0, 1), (0, 1, 0), (1, 2, 1), (0, 0, 1), (1, 1, 0), (0, 2, 1), (1, 0, 0), (0, 1, 1), (1, 2, 0)]
    """
    if len(args) == 1:
        # Only one iterable, simply yield the values from that iterable
        index = 0
        args_len = len(args[0])
        while True:
            yield args[0][index],  # Comma to make it a tuple
            if stop and index == args_len - 1:
                raise StopIteration
            index = (index + 1) % args_len
    else:
        # More than one iterable, get the generator for the combinations of the first n-1 iterables
        iterator = sim_product(*args[:-1], stop=False)
        first_iterator_len = functools.reduce(operator.mul, map(len, args[:-1]))

        # The number of iterations before values are repeated (when nothing is done to fix this)
        lcm = math.lcm(first_iterator_len, len(args[-1]))
        index = 0
        start = 0
        iters = 0

        len_val = len(args[-1])
        reset_val = first_iterator_len * len_val
        while True:
            yield *next(iterator), args[-1][index % len_val]
            index += 1
            iters += 1

            if iters % lcm == 0:
                # The new value would be a repeat, so we need to move the start index to prevent repetition
                start += 1
                index = start

            if iters == reset_val:
                if stop:
                    raise StopIteration
                # We have looped through all the unique combinations, so we need to reset to the start
                index, start, iters = 0, 0, 0

def sim_product_list(*args: Sequence, num: int = None) -> list[tuple]:
    """
    Create a list of all the combinations of the given iterables. Uses `sim_product` to generate the combinations.

    Parameters
    ----------
    args:  Sequence
        The sequences to combine.
    num: int, optional
        The number of elements to generate. If None, it will generate all combinations. If num is larger that the number
        of unique combinations, the list will contain non-unique combinations.

    Returns
    -------
    list[tuple]
        A list containing tuples with one element from each of the input sequences, in a specific order.
    """
    if num is None:
        return list(sim_product(*args, stop=True))
    if not isinstance(num, int) or num < 1:
        raise ValueError(f'`num` should be a positive integer or None, got {num}')
    iterator = sim_product(*args, stop=False)
    return [tuple(next(iterator)) for _ in range(num)]


if __name__ == '__main__':
    num = 20
    for i in range(1, num):
        print(f'test \r{i}/{num}', end='')
        for j in range(1, num):
            for k in range(1, num):
                try:
                    result = set(sim_product(np.arange(i), np.arange(j), np.arange(k)))
                except Exception as e:
                    raise Exception(f"Error: {i}, {j}, {k}") from e
                if len(result) != i * j * k:
                    raise ValueError(f"{i} * {j} * {k} = {i * j * k}:\n"
                                     f"S: {len(result)}, {result}\n")
        print('\r', end='')
    print("Test passed")
