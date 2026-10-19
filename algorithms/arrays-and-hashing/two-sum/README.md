# Two Sum

**Source:** [LeetCode 1](https://leetcode.com/problems/two-sum/) · Easy

**Pattern:** Arrays and hashing

## Problem
Given a list of integers and a target, return the indices of the two numbers that add up to the target.

## Approach
Brute force checks every pair, which is O(n²). But each number x has exactly one partner, target − x, so I can turn the pair search into one lookup per element: have I already seen target − x? A hash map from value to index answers that in O(1) on average, so one pass gives O(n) time and O(n) space. I look up before storing, so an element never pairs with itself.

Complement lookup...

## Complexity
Time and space for your final approach, with a line of reasoning.

## What I learned
The cue that should point you to this pattern next time.