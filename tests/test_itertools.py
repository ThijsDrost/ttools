import sys

sys.path.append(".")  # Adjust the path to import from the parent directory

from ttools.itertools import sim_product

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