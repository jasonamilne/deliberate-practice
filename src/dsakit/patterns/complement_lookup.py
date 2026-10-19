"""Complement lookup: find earlier elements that complete the current one.

The pattern
    Scan a sequence once, keeping a hash map from a key of each element seen
    so far to a summary of where that key appeared. At each position, compute
    the key that would complete the current element (its complement) and look
    it up. Look up *before* storing, so an element never matches itself.

What varies between problems
    key         what to remember about each element
    complement  which remembered key would complete the current element
    consume     what to do with each match: take the first one, count them,
                or measure a distance or length using the Seen summary

Cost
    O(n) average time and O(d) space for n elements with d distinct keys,
    since each element costs one average-O(1) lookup and one insert.

Instances in this repo
    Two Sum (LeetCode 1): algorithms/arrays-and-hashing/two-sum
"""

from collections.abc import Callable, Hashable, Iterable, Iterator
from typing import NamedTuple, TypeVar

T = TypeVar("T")


class Seen(NamedTuple):
    """Where a key appeared before the current position.

    Each Seen is an immutable snapshot, so it stays accurate even if you keep
    it after the scan has moved on.
    """

    first: int  # index of the key's first appearance
    last: int  # index of its most recent appearance
    count: int  # how many times it has appeared so far


def _identity(item: T) -> T:
    return item


def complement_scan(
    items: Iterable[T],
    complement: Callable[[T], Hashable],
    key: Callable[[T], Hashable] = _identity,
) -> Iterator[tuple[int, Seen]]:
    """Yield (i, seen) for each position i whose complement appeared earlier.

    seen summarizes the earlier positions whose key equals the complement of
    the item at position i. key defaults to the item itself.

    The scan is lazy: a consumer that stops at the first match (next, any)
    does no work past that point.

    Time:  O(n) average to run to completion. Each step is one dict lookup
           and one insert, both O(1) on average, plus one call each to key
           and complement.
    Space: O(d), where d <= n is the number of distinct keys.
    """
    seen: dict[Hashable, Seen] = {}
    for i, item in enumerate(items):
        wanted = complement(item)
        if wanted in seen:  # look up before storing, so an item never matches itself
            yield i, seen[wanted]
        k = key(item)
        prev = seen.get(k)
        seen[k] = Seen(i, i, 1) if prev is None else Seen(prev.first, i, prev.count + 1)