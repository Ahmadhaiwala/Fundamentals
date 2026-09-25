# 2831. Find the Longest Equal Subarray

## Problem

You are given a `0-indexed` integer array `nums` and an integer `k`.

You may delete at most `k` elements from a subarray.

Find the maximum length of a subarray that can be made equal, meaning all remaining elements are the same.

---

## Core Idea

This is a **Variable Size Sliding Window + Frequency Map** problem.

For every window:

```text
[left ... right]
```

we want to know:

> How many elements must be removed to make the entire window contain only one value?

Suppose the window has:

- `window_size` elements
- the most frequent value appears `maxf` times

Then we can keep those `maxf` elements and delete everything else.

Therefore:

```text
elements_to_delete = window_size - maxf
```

If:

```text
window_size - maxf <= k
```

the window is valid.

If:

```text
window_size - maxf > k
```

the window is too large, so we move `left` forward.

---

## Why `maxf` Matters

We do **not** care which value becomes the final equal value.

We simply choose the value that already occurs the most times inside the current window.

Example:

```text
nums = [1, 2, 2, 3, 2]
```

For the whole window:

```text
1 → 1 time
2 → 3 times
3 → 1 time
```

So:

```text
window_size = 5
maxf = 3
```

To make everything equal to `2`, delete:

```text
5 - 3 = 2
```

elements.

So if `k >= 2`, this window is valid.

---

# Approach

We maintain three things:

### 1. `left`

The left boundary of the sliding window.

```python
left = 0
```

### 2. `frequencies`

A hash map storing how many times each number occurs in the current window.

```python
frequencies = {}
```

For example:

```text
window = [1, 2, 2, 3]

frequencies = {
    1: 1,
    2: 2,
    3: 1
}
```

### 3. `maxf`

The maximum frequency of any value seen in the current window.

```python
maxf = 0
```

Whenever we add `nums[right]`:

```python
frequencies[nums[right]] = frequencies.get(nums[right], 0) + 1

maxf = max(maxf, frequencies[nums[right]])
```

---

# Algorithm

For every `right`:

1. Add `nums[right]` to the frequency map.
2. Update `maxf`.
3. Calculate how many elements need to be removed:

```text
(right - left + 1) - maxf
```

4. If that number is greater than `k`, shrink the window:

```python
frequencies[nums[left]] -= 1
left += 1
```

5. Continue expanding the window.
6. `maxf` represents the largest number of equal elements we can keep in a valid window.
7. Return `maxf`.

---

# Code

```python
class Solution:
    def longestEqualSubarray(self, nums: List[int], k: int) -> int:
        frequencies = {}
        left = 0
        maxf = 0

        for right in range(len(nums)):
            frequencies[nums[right]] = frequencies.get(nums[right], 0) + 1

            maxf = max(maxf, frequencies[nums[right]])

            if right - left + 1 - maxf > k:
                frequencies[nums[left]] -= 1
                left += 1

        return maxf
```

---

# Dry Run

Consider:

```text
nums = [1, 3, 2, 3, 3, 2, 3]
k = 2
```

We want the longest group of equal values after deleting at most `2` elements.

### Step 1

Window:

```text
[1]
```

Frequencies:

```text
{1: 1}
```

```text
window_size = 1
maxf = 1
deletions = 1 - 1 = 0
```

Valid.

---

### Step 2

Window:

```text
[1, 3]
```

Frequencies:

```text
{1: 1, 3: 1}
```

```text
window_size = 2
maxf = 1
deletions = 2 - 1 = 1
```

Valid because:

```text
1 <= k
```

---

### Step 3

Window:

```text
[1, 3, 2]
```

Frequencies:

```text
{1: 1, 3: 1, 2: 1}
```

```text
window_size = 3
maxf = 1
deletions = 3 - 1 = 2
```

Still valid.

---

### Step 4

Window:

```text
[1, 3, 2, 3]
```

Frequencies:

```text
{1: 1, 3: 2, 2: 1}
```

Now:

```text
window_size = 4
maxf = 2
deletions = 4 - 2 = 2
```

Valid.

We can delete:

```text
1
2
```

and keep:

```text
3, 3
```

---

### Step 5

Window:

```text
[1, 3, 2, 3, 3]
```

Frequencies:

```text
{1: 1, 3: 3, 2: 1}
```

```text
window_size = 5
maxf = 3
deletions = 5 - 3 = 2
```

Valid.

We can delete:

```text
1
2
```

and keep:

```text
3, 3, 3
```

So the answer is currently:

```text
3
```

---

### Step 6

Add another `2`:

```text
[1, 3, 2, 3, 3, 2]
```

Frequencies:

```text
{1: 1, 3: 3, 2: 2}
```

```text
window_size = 6
maxf = 3
deletions = 6 - 3 = 3
```

But:

```text
3 > k
```

So the window is invalid.

Shrink from the left:

```text
remove 1
left += 1
```

New window:

```text
[3, 2, 3, 3, 2]
```

The window becomes valid again.

---

# The Important Formula

This is the main thing to remember:

```text
required deletions = window length - frequency of most common element
```

or:

```python
(right - left + 1) - maxf
```

### Why?

Suppose:

```text
window = [2, 3, 2, 4, 2]
```

Frequency:

```text
2 → 3
3 → 1
4 → 1
```

The best target is `2`.

Keep:

```text
2, 2, 2
```

Delete:

```text
3, 4
```

Therefore:

```text
deletions = 5 - 3
           = 2
```

---

# Why Sliding Window Works

The condition is:

```text
window_size - maxf <= k
```

As the right pointer moves:

```text
window_size
```

can increase.

If the number of required deletions becomes greater than `k`, the current window cannot be used.

So we move:

```text
left →
```

until the window becomes valid again.

This gives us a **dynamic window**:

```text
expand → invalid → shrink → valid → expand
```

---

# Important Observation About `maxf`

You may notice something interesting in the code:

```python
maxf = max(maxf, frequencies[nums[right]])
```

We don't decrease `maxf` when `left` moves.

At first this can look wrong.

But it is safe for this problem.

Why?

We only use `maxf` to determine the maximum achievable equal-subarray length. A stale `maxf` may temporarily make the current window look more favorable than it actually is, but the algorithm still maintains the correct maximum answer.

The standard sliding-window solution relies on this monotonic behavior.

---

# Complexity

Let:

```text
n = len(nums)
```

### Time Complexity

```text
O(n)
```

Each element:

- enters the window once
- can leave the window once

So the total number of operations is linear.

### Space Complexity

```text
O(n)
```

In the worst case, every number is different and the frequency map stores `n` values.

---

# Pattern Recognition

This problem belongs to:

```text
Sliding Window
      ↓
Variable-size Window
      ↓
Frequency Map
      ↓
Keep the Most Frequent Element
      ↓
Delete the Rest
```

When you see a problem asking something like:

> "Find the longest subarray that can become valid after changing/deleting at most `k` elements"

immediately consider:

```text
window_size - best_frequency
```

For this specific problem, the operation is deletion, so:

```text
elements to delete = window_size - max_frequency
```

---

# Mental Template

For similar problems, think:

```python
left = 0
freq = {}
best = 0

for right in range(len(nums)):

    # add right
    freq[nums[right]] += 1

    # update best frequency
    best = max(best, freq[nums[right]])

    # invalid window?
    while/right-condition:
        # remove left
        freq[nums[left]] -= 1
        left += 1

    # update answer
```

For this problem:

```python
if right - left + 1 - maxf > k:
    frequencies[nums[left]] -= 1
    left += 1
```

The key equation is:

```text
WINDOW SIZE - MAX FREQUENCY <= K
```

That's the entire heart of the solution.
