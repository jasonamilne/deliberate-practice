"""Tests for complement_scan that don't depend on any particular problem.

The main test runs the scan against a brute-force version of the same
contract on random inputs, using several key and complement functions. If
the scan agrees with brute force for arbitrary choices, it holds for
whatever choices a new problem plugs in.
"""

import random
from itertools import count

import pytest

from dsakit.patterns.complement_lookup import Seen, complement_scan


def brute_force_scan(items, complement, key=lambda x: x):
    """Same contract as complement_scan, computed directly in O(n^2) time."""
    for i, item in enumerate(items):
        earlier = [j for j in range(i) if key(items[j]) == complement(item)]
        if earlier:
            yield i, Seen(first=earlier[0], last=earlier[-1], count=len(earlier))


CHOICES = {
    "identity key, shifted complement": (lambda x: x, lambda x: 3 - x),
    "identity key and complement": (lambda x: x, lambda x: x),
    "modular key and complement": (lambda x: x % 5, lambda x: -x % 5),
}


@pytest.mark.parametrize("choice", CHOICES)
@pytest.mark.parametrize("seed", range(25))
def test_agrees_with_brute_force_on_random_inputs(choice, seed):
    key, complement = CHOICES[choice]
    rng = random.Random(seed)
    items = [rng.randint(-10, 10) for _ in range(rng.randint(0, 40))]
    expected = list(brute_force_scan(items, complement, key))
    assert list(complement_scan(items, complement, key)) == expected


def test_never_matches_an_item_with_itself():
    assert list(complement_scan([3], complement=lambda x: 6 - x)) == []
    assert list(complement_scan([7], complement=lambda x: x)) == []


def test_summary_tracks_first_last_and_count():
    assert list(complement_scan([7, 7, 7], complement=lambda x: x)) == [
        (1, Seen(first=0, last=0, count=1)),
        (2, Seen(first=0, last=1, count=2)),
    ]


def test_stops_when_the_consumer_stops():
    # count() never ends, so this would hang if the scan weren't lazy.
    assert next(complement_scan(count(), complement=lambda x: 10 - x)) == (6, Seen(4, 4, 1))