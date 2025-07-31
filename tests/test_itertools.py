import sys
import random

sys.path.append(".")  # Adjust the path to import from the parent directory

from ttools.itertools import sim_product
from ttools.min_max import *
from ttools.sort import sort_by

def test_sim_product():
    num = 20
    for i in range(1, num):
        for j in range(1, num):
            for k in range(1, num):
                try:
                    result = set(x for x in sim_product(list(range(i)), list(range(j)), list(range(k))))
                except Exception as e:
                    msg = f"Error: {i}, {j}, {k}"
                    raise ValueError(msg) from e
                if len(result) != i * j * k:
                    msg = f"{i} * {j} * {k} = {i * j * k}:\nS: {len(result)}, {result}\n"
                    raise ValueError(msg)


def test_min_max():
    for _ in range(10):
        values = [random.randint(0, 100) for _ in range(100)]

        max_value = max(values)
        min_value = min(values)
        assert(max_value == values[arg_max(values)])
        assert(min_value == values[arg_min(values)])
        assert(max_value == values[arg_none_max(values)])
        assert(min_value == values[arg_none_min(values)])

        for i in range(20):
            values[random.randint(0, 99)] = None

        max_value = values[arg_none_max(values)]
        min_value = values[arg_none_min(values)]
        assert(all(x is None or x <= max_value for x in values))
        assert(all(x is None or min_value <= x for x in values))

        max_value = none_max(values)
        min_value = none_min(values)
        assert(all(x is None or x <= max_value for x in values))
        assert(all(x is None or min_value <= x for x in values))


def test_sort():
    values = list(range(100))
    vals = values.copy()
    random.shuffle(values)
    val2 = sort_by(values, values.copy())[0]
    assert(all(x == y for x, y in zip(vals, val2)))