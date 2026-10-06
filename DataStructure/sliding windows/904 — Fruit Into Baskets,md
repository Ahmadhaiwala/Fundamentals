Absolutely. This is **LeetCode 904 — Fruit Into Baskets**, and your implementation is a clean **variable-size sliding window** solution. I’ll keep the explanation focused on the exact logic you used.

```md
# LeetCode 904 — Fruit Into Baskets

## Problem

You are given an integer array `fruits`, where:

```text
fruits[i] = type of fruit on the i-th tree
```

You have **two baskets**, and each basket can hold only one type of fruit.

You want to collect fruits from a **contiguous range of trees**.

Therefore, the goal is:

> Find the longest contiguous subarray containing at most **2 distinct values**.

### Example

```text
Input:
fruits = [1,2,1,2,3]

Output:
4
```

The longest valid subarray is:

```text
[1,2,1,2]
```

It contains only two fruit types: `1` and `2`.

---

# Approach — Sliding Window

This is a classic **variable-size sliding window** problem.

We maintain a window:

```text
[left ... right]
```

and a dictionary that stores the frequency of each fruit type inside the current window.

```python
count = {}
```

The important condition is:

```python
len(count) <= 2
```

because we have only **two baskets**.

---

# Core Idea

We expand the window using `right`.

For every fruit:

```python
count[fruits[right]] = count.get(fruits[right], 0) + 1
```

This adds the current fruit to our window.

If the window contains more than two fruit types:

```python
while len(count) > 2:
```

the window is invalid.

So we shrink it from the left.

```python
count[fruits[left]] -= 1
left += 1
```

Once the window becomes valid again, we calculate its length:

```python
right - left + 1
```

and update the answer:

```python
res = max(res, right - left + 1)
```

---

# Your Implementation

```python
class Solution:
    def totalFruit(self, fruits: list[int]) -> int:
        count = {}
        res = 0
        left = 0

        for right in range(len(fruits)):
            count[fruits[right]] = count.get(fruits[right], 0) + 1

            while len(count) > 2:
                count[fruits[left]] -= 1

                if count[fruits[left]] == 0:
                    del count[fruits[left]]

                left += 1

            res = max(res, right - left + 1)

        return res
```

---

# Dry Run

Consider:

```text
fruits = [1,2,1,2,3]
```

Initially:

```text
left = 0
res = 0
count = {}
```

---

## right = 0

Add `1`.

```text
count = {1: 1}
```

Distinct types:

```text
1
```

Valid.

Window:

```text
[1]
```

Length:

```text
1
```

```text
res = 1
```

---

## right = 1

Add `2`.

```text
count = {
    1: 1,
    2: 1
}
```

Distinct types:

```text
2
```

Still valid.

Window:

```text
[1,2]
```

Length:

```text
2
```

```text
res = 2
```

---

## right = 2

Add another `1`.

```text
count = {
    1: 2,
    2: 1
}
```

Window:

```text
[1,2,1]
```

Only two types.

Length:

```text
3
```

```text
res = 3
```

---

## right = 3

Add another `2`.

```text
count = {
    1: 2,
    2: 2
}
```

Window:

```text
[1,2,1,2]
```

Still only two types.

Length:

```text
4
```

```text
res = 4
```

---

## right = 4

Add `3`.

```text
count = {
    1: 2,
    2: 2,
    3: 1
}
```

Now:

```text
len(count) = 3
```

which is invalid because we only have two baskets.

So we shrink from the left.

### Remove `fruits[left]`

Currently:

```text
left = 0
fruits[left] = 1
```

Decrease its frequency:

```text
count = {
    1: 1,
    2: 2,
    3: 1
}
```

Still three types.

Move:

```text
left = 1
```

Remove `2`:

```text
count = {
    1: 1,
    2: 1,
    3: 1
}
```

Still three types.

Move:

```text
left = 2
```

Remove `1`:

```text
count = {
    1: 0,
    2: 1,
    3: 1
}
```

Frequency became zero, so delete it:

```python
del count[1]
```

Now:

```text
count = {
    2: 1,
    3: 1
}
```

Two types → valid.

Current window:

```text
[1,2,3]
    ↑
  left
```

Actually, after the removals the active window is:

```text
[1,2,3]
```

with `left = 2`, so the values are:

```text
fruits[2:5] = [1,2,3]
```

Length:

```text
5 - 2 = 3
```

Therefore:

```text
res = max(4, 3)
    = 4
```

Final answer:

```text
4
```

---

# Why Do We Delete From the Dictionary?

This part is extremely important:

```python
if count[fruits[left]] == 0:
    del count[fruits[left]]
```

We aren't just tracking frequencies.

We are using:

```python
len(count)
```

to determine the number of **distinct fruit types**.

For example:

```text
count = {
    1: 0,
    2: 2,
    3: 1
}
```

Technically the dictionary has three keys.

But there are only two actual fruit types in the window:

```text
2 and 3
```

Therefore we must remove the zero-frequency key:

```python
del count[1]
```

so:

```text
len(count) == 2
```

correctly represents the number of distinct types.

---

# Why `while` Instead of `if`?

We use:

```python
while len(count) > 2:
```

because adding a new fruit can make the window invalid by more than what one left movement can fix.

We keep removing from the left until:

```text
number of distinct fruits <= 2
```

The invariant is:

> After the `while` loop finishes, the current window is always valid.

---

# Why `right - left + 1`?

The current window is:

```text
[left ... right]
```

For example:

```text
left  = 2
right = 5
```

Indices:

```text
2  3  4  5
```

There are:

```text
5 - 2 + 1 = 4
```

elements.

Therefore:

```python
window_length = right - left + 1
```

---

# The Sliding Window Pattern

This problem gives you a very useful general template:

```python
left = 0
res = 0
count = {}

for right in range(len(fruits)):

    # Expand window
    count[fruits[right]] = count.get(fruits[right], 0) + 1

    # Restore validity
    while invalid_condition:

        count[fruits[left]] -= 1

        if count[fruits[left]] == 0:
            del count[fruits[left]]

        left += 1

    # Update answer
    res = max(res, right - left + 1)
```

For this problem:

```text
invalid_condition = len(count) > 2
```

---

# Pattern Recognition

When you see a problem saying something like:

> "Find the longest contiguous subarray with at most K distinct elements."

Think:

```text
Variable-size Sliding Window
+
Frequency Map
```

For this problem:

```text
K = 2
```

So:

```python
while len(count) > 2:
```

---

# Complexity

## Time Complexity

```text
O(n)
```

`right` moves from left to right once.

`left` also only moves forward.

So even though there is a nested `while` loop, each element is added and removed at most once.

Therefore:

```text
O(n)
```

## Space Complexity

At most 3 distinct fruit types temporarily exist in the dictionary before shrinking.

Since the maximum number of allowed types is fixed at 2:

```text
O(1)
```

---

# Key Takeaway

The entire problem can be reduced to:

```text
Longest subarray
        ↓
At most 2 distinct elements
        ↓
Sliding Window
        ↓
Frequency Map
        ↓
If distinct > 2
        ↓
Move left until valid
```

The three most important lines are:

```python
count[fruits[right]] = count.get(fruits[right], 0) + 1

while len(count) > 2:
    ...

res = max(res, right - left + 1)
```

### LeetCode

**Problem:** 904 — Fruit Into Baskets

**Pattern:** Variable-Size Sliding Window + Frequency Map

**Time:** `O(n)`

**Space:** `O(1)`
```