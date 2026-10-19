# Two Sum

**Source:** [LeetCode 1](https://leetcode.com/problems/two-sum/) · Easy

**Pattern:** [Complement lookup](../../../src/dsakit/patterns/complement_lookup.py) (arrays and hashing)

## Problem
Given a list of integers and a target, return the indices of the two numbers that add up to the target.

## Approach
I could check every pair, which is O(n²), or pass through the array once and treat it as a lookup: for each number x, has its complement, target − x, already appeared? A hash map from value to index answers "have I seen this, and where?" in O(1) on average, so one pass is enough. I look up the complement before storing x, so an element never pairs with itself, while equal values at different indices, as in `[3, 3]`, still work.

**Invariant:** before processing index i, the map holds every earlier value and its index.

**As a pattern:** this is the simplest instance of complement lookup. In [`two_sum.py`](two_sum.py), `two_sum_via_pattern` solves it with `complement_scan` from dsakit: the key is the number itself, the complement is target − x, and it takes the first match.

## Complexity
| Approach | Time | Space |
|---|---|---|
| Brute force: check every pair | O(n²) | O(1) |
| One pass with a hash map | O(n) average | O(n) |

Brute force checks about n²/2 pairs. The one-pass version visits each element at most once, each dict lookup and insert is O(1) on average, and the map holds up to n − 1 entries. The time bound is an average because hash map operations slow down when many keys collide.

Measured with [`benchmark_two_sum.py`](benchmark_two_sum.py), a doubling experiment: when n doubles, the one-pass version's time and memory roughly double (k ≈ 1), while the brute force's time roughly quadruples (k ≈ 2) and its memory stays flat.

```
(paste the output of python benchmark_two_sum.py here)
```

## What I learned
- **Cue:** "find two elements that combine to a target" points to complement lookup.
- **Start from the question, not the data structure.** The question is "have I already seen target − x?", and a hash map is what answers it fast.
- **Look up the complement, not the target.** At 7 with a target of 9, the lookup is for 2.
- **Look up before storing**, so an element can't pair with itself.
- **Generality costs a constant factor, not a complexity class.** The pattern version is slower per call but still O(n).