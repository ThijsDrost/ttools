from typing import Protocol

class Addable[T](Protocol):
    def __add__(self: T, other: T) -> T: ...