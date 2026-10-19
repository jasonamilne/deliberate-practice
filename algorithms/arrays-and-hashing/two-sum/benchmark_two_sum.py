"""Measure how two_sum's running time and memory grow with input size.

Run from this folder:

    python benchmark_two_sum.py

This is a doubling experiment: run the function on inputs of size n, 2n,
4n, ... and compare each measurement with the previous one. If cost grows
like n^k, doubling n multiplies it by about 2^k, so:

    x time ~ 2  (k ~ 1)  means O(n) time
    x time ~ 4  (k ~ 2)  means O(n^2) time
    x mem  ~ 2           means O(n) extra space
    x mem  ~ 1           means O(1) extra space

A brute-force version runs alongside as a baseline, so the difference in
growth rates is measured, not just claimed.
"""

import math
import timeit
import tracemalloc

from two_sum import two_sum


def two_sum_brute_force(nums: list[int], target: int) -> list[int]:
    """Baseline: check every pair. O(n^2) time, O(1) extra space."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    raise ValueError("no two numbers in nums add up to target")


def worst_case_input(n: int) -> tuple[list[int], int]:
    """Return (nums, target) where the only valid pair is the last two elements.

    Both functions then do their maximum work: the hash map visits all n
    elements, and the brute force checks all n(n - 1)/2 pairs. The filler
    values 0..n-3 are too small to reach the target with each other or with
    either of the last two values, so the answer is unique.
    """
    return list(range(n - 2)) + [4 * n, 6 * n], 10 * n


def seconds_per_call(func, nums: list[int], target: int) -> float:
    """Average seconds per call, taking the best of three timing runs."""
    timer = timeit.Timer(lambda: func(nums, target))
    calls, _ = timer.autorange()  # enough calls to run for at least 0.2 s
    return min(timer.repeat(repeat=3, number=calls)) / calls


def peak_bytes(func, nums: list[int], target: int) -> int:
    """Peak memory allocated while func runs, not counting the input itself."""
    tracemalloc.start()
    func(nums, target)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def doubling_experiment(func, sizes: list[int]) -> None:
    """Print time and memory at each size, with growth versus the previous size."""
    print(f"\n{func.__name__}")
    print(f"{'n':>8}  {'time/call':>11}  {'x time':>6}  {'k':>5}  {'peak mem':>11}  {'x mem':>5}")
    prev_secs = prev_mem = None
    for n in sizes:
        nums, target = worst_case_input(n)
        assert sorted(func(nums, target)) == [n - 2, n - 1]  # correct before timed
        secs = seconds_per_call(func, nums, target)
        mem = peak_bytes(func, nums, target)

        row = f"{n:>8,}  {secs * 1e3:>9.3f}ms  "
        if prev_secs:
            ratio = secs / prev_secs
            row += f"{ratio:>6.2f}  {math.log2(ratio):>5.2f}  "
        else:
            row += f"{'-':>6}  {'-':>5}  "
        row += f"{mem:>10,}B  "
        row += f"{mem / prev_mem:>5.2f}" if prev_mem else f"{'-':>5}"
        print(row)
        prev_secs, prev_mem = secs, mem


if __name__ == "__main__":
    doubling_experiment(two_sum, [1_000 * 2**i for i in range(7)])  # 1,000 to 64,000
    doubling_experiment(two_sum_brute_force, [200 * 2**i for i in range(5)])  # 200 to 3,200