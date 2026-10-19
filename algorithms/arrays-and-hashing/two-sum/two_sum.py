def two_sum(nums: list[int], target: int) -> list[int]:
    """Return the indices of the two numbers in nums that add up to target.
 
    Approach: one pass with a hash map from each value seen so far to its
    index. Each number's complement is looked up *before* the number is
    stored, so an element is never paired with itself.
 
    Time:  O(n) average. Each element is visited at most once, and dict
           lookups and inserts are O(1) on average.
    Space: O(n). In the worst case the map holds n - 1 entries before the
           pair is found.
 
    Raises:
        ValueError: if no two numbers in nums add up to target.
    """
    num_to_idx: dict[int, int] = {}
    for cur_idx, cur_num in enumerate(nums):  # at most n iterations
        complement = target - cur_num
        if complement in num_to_idx:  # O(1) average: a hash lookup, not a scan
            return [num_to_idx[complement], cur_idx]
        num_to_idx[cur_num] = cur_idx  # O(1) average insert
    raise ValueError("no two numbers in nums add up to target")