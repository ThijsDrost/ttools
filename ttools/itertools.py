import math
from typing import Sequence, Iterator
import functools
import operator

import numpy as np


def product(*args: Sequence, stop = True) -> Iterator[tuple]:
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
    >>> list(product([0, 1, 2], [0, 1, 2]))
    [(0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (2, 0), (0, 2), (1, 0), (2, 1)]

    >>> list(product([0, 1], [0, 1, 2]))
    [(0, 0), (1, 1), (0, 2), (1, 0), (0, 1), (1, 2)]

    >>> list(product([0, 1], [0, 1, 2], [0, 1]))
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
        iterator = product(*args[:-1], stop=False)
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


def product3[S, T, U](iterable1: Sequence[S], iterable2: Sequence[T], iterable3: Sequence[U]) -> Iterator[tuple[S, T, U]]:
    """
    Create a generator that yields the combinations of three iterables. The generator will loop through the iterables simultaneously,
    until all combinations are exhausted. This is a special case of :py:func:`product`.
    """
    yield from product(iterable1, iterable2, iterable3, stop = True)


def product2[S, T](iterable1: Sequence[S], iterable2: Sequence[T]) -> Iterator[tuple[S, T]]:
    """
    Create a generator that yields the combinations of two iterables. The generator will loop through the iterables simultaneously,
    until all combinations are exhausted. This is a special case of :py:func:`product`.
    """
    yield from product(iterable1, iterable2, stop = True)


if __name__ == '__main__':
    num = 20
    for i in range(1, num):
        print(f'test \r{i}/{num}', end='')
        for j in range(1, num):
            for k in range(1, num):
                try:
                    result = set(product(np.arange(i), np.arange(j), np.arange(k)))
                except Exception as e:
                    raise Exception(f"Error: {i}, {j}, {k}") from e
                if len(result) != i * j * k:
                    raise ValueError(f"{i} * {j} * {k} = {i * j * k}:\n"
                                     f"S: {len(result)}, {result}\n")
        print('\r', end='')
    print("Test passed")
