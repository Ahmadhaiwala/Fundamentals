# LeetCode 1838 — Frequency of the Most Frequent Element

## Problem

Given an integer array `nums` and an integer `k`, you can increment any element by `1` in one operation.

Return the maximum possible frequency of any element after performing at most `k` operations.

---

## Core Pattern

**Sorting + Sliding Window + Cost Formula**

The key idea is to find the largest group of elements that can all be converted into the same value using at most `k` increments.

---

## Step 1: Sort the Array

```text
[1, 4, 8, 13]
```

After sorting, consider a contiguous window:

```text
[1, 4, 8]
```

If we want all elements in this window to become equal, the target should be the **largest element**:

```text
target = 8
```

Why?

Because we can only increment elements. We cannot decrease `8` to `4` or `1`.

So for a sorted window:

```text
target = nums[right]
```

---

## Step 2: Think About the Cost

Suppose:

```text
window = [1, 4, 8]
target = 8
```

Required operations:

```text
1 → 8 = 7
4 → 8 = 4
8 → 8 = 0

total = 11
```

So:

```text
cost = (8 - 1) + (8 - 4) + (8 - 8)
```

We can rewrite this:

```text
cost = 8 + 8 + 8 - (1 + 4 + 8)
```

Therefore:

```text
cost = target * window_size - window_sum
```

This is the important formula.

---

## Step 3: Sliding Window

We maintain a window:

```text
[left ... right]
```

For every new `right`:

1. Add `nums[right]` to `window_sum`.
2. Treat `nums[right]` as the target.
3. Calculate the cost.
4. If the cost is greater than `k`, move `left` forward until the window becomes valid.
5. Record the maximum window size.

The condition is:

```text
nums[right] * window_size - window_sum <= k
```

If this is true, the whole window can be made equal.

If it is false, the window is too expensive, so shrink it.

---

## Step 4: Dry Run

Input:

```text
nums = [1, 4, 8, 13]
k = 5
```

Sorted:

```text
[1, 4, 8, 13]
```

### right = 0

Window:

```text
[1]
```

Cost:

```text
1 * 1 - 1 = 0
```

Valid.

Answer:

```text
1
```

---

### right = 1

Window:

```text
[1, 4]
```

Cost:

```text
4 * 2 - (1 + 4)
= 8 - 5
= 3
```

`3 <= 5`, so valid.

Answer:

```text
2
```

---

### right = 2

Window:

```text
[1, 4, 8]
```

Cost:

```text
8 * 3 - (1 + 4 + 8)
= 24 - 13
= 11
```

But:

```text
11 > 5
```

Invalid.

Shrink from the left:

```text
[4, 8]
```

Cost:

```text
8 * 2 - (4 + 8)
= 16 - 12
= 4
```

Valid.

Answer remains:

```text
2
```

---

### right = 3

Window:

```text
[4, 8, 13]
```

Cost:

```text
13 * 3 - (4 + 8 + 13)
= 39 - 25
= 14
```

Invalid.

Remove `4`:

```text
[8, 13]
```

Cost:

```text
13 * 2 - (8 + 13)
= 26 - 21
= 5
```

Valid.

Answer:

```text
2
```

---

# Final Algorithm

```text
1. Sort nums.
2. Initialize left = 0.
3. Maintain window_sum.
4. Move right from 0 to n-1.
5. Add nums[right] to window_sum.
6. Calculate:

   cost = nums[right] * (right - left + 1) - window_sum

7. While cost > k:
      remove nums[left]
      left += 1

8. Update:
      answer = max(answer, window_size)

9. Return answer.
```

---

## Python Solution

```python
class Solution:
    def maxFrequency(self, nums: list[int], k: int) -> int:
        nums.sort()

        left = 0
        window_sum = 0
        ans = 0

        for right in range(len(nums)):
            window_sum += nums[right]

            while nums[right] * (right - left + 1) - window_sum > k:
                window_sum -= nums[left]
                left += 1

            ans = max(ans, right - left + 1)

        return ans
```

---

## Complexity

Sorting:

```text
O(n log n)
```

Sliding window:

```text
O(n)
```

Total:

```text
O(n log n)
```

Space:

```text
O(1)
```

apart from the sorting implementation's internal space.

---

## Pattern to Remember

When you see:

- You can only **increase** values.
- You want the **maximum number of equal elements**.
- There is a limited operation budget.
- You can choose any elements to increment.

Think:

```text
SORT
  ↓
SLIDING WINDOW
  ↓
TARGET = RIGHTMOST / LARGEST VALUE
  ↓
COST = TARGET × WINDOW_SIZE - WINDOW_SUM
  ↓
COST > K → SHRINK LEFT
  ↓
MAX WINDOW SIZE
```

### Most Important Insight

Don't think:

> "How do I increment each element?"

Think:

> "For this target, how many elements can I afford to bring up to it?"

That shift turns the problem into a sliding-window problem.
