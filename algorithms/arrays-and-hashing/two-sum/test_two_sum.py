import pytest

from two_sum import two_sum


@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),  # must not pair index 0 with itself
        ([3, 3], 6, [0, 1]),  # equal values at different indices are fine
    ],
)
def test_two_sum(nums, target, expected):
    # Any order is allowed, so compare sorted indices.
    assert sorted(two_sum(nums, target)) == expected

def test_two_sum_raises_when_no_pair_exists():
    with pytest.raises(TypeError):
        two_sum([1, 2, 3], 100)