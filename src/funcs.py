from functools import reduce
from typing import Callable, Sequence


def pipe[T](data, *fns: Callable[[T], T]):
    result = data
    for f in fns:
        result = f(result)
    return result


def every[T](predicate: Callable[[T], bool], data: Sequence[T]) -> bool:
    return reduce(lambda acc, cur: acc and predicate(cur), data, True)


# like index, but for many potential substrings. The one that occurs first is given
# if not found, an empty string and -1 are returned
def earliest_index_in(substrs: Sequence[str], search: str) -> tuple[str, int]:
    earliest = ("", -1)
    earliest_index = float("inf")

    for s in substrs:
        index = search.index(s)
        if index < earliest_index:
            earliest = (s, index)

    return earliest
