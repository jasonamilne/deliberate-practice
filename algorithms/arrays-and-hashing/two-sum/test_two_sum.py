import pytest

from two_sum import two_sum, two_sum_via_pattern

SOLUTIONS = [two_sum, two_sum_via_pattern]


@pytest.mark.parametrize("solve", SOLUTIONS)
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),  # must not pair index 0 with itself
        ([3, 3], 6, [0, 1]),  # equal values at different indices are fine
    ],
)
def test_two_sum(solve, nums, target, expected):
    # Any order is allowed, so compare sorted indices.
    assert sorted(solve(nums, target)) == expected


@pytest.mark.parametrize("solve", SOLUTIONS)
def test_raises_when_no_pair_exists(solve):
    with pytest.raises(ValueError):
        solve([1, 2, 3], 100)