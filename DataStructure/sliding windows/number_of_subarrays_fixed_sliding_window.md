# 1343. Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold

## Problem

You are given:

- an integer array `arr`
- an integer `k`
- an integer `threshold`

Find the number of contiguous subarrays of size exactly `k` whose average is greater than or equal to `threshold`.

---

# Core Idea

This is a **Fixed-Size Sliding Window** problem.

Every subarray must have exactly:

```text
k elements
```

So instead of calculating the sum of every possible subarray from scratch, maintain the sum of the current window.

For example:

```text
arr = [2, 2, 2, 2, 5, 5]
k = 3
```

First window:

```text
[2, 2, 2]
```

Then slide one position:

```text
[2, 2, 2]
   ↓
[2, 2, 5]
```

We remove the element leaving from the left and add the new element entering from the right.

---

# The Sliding Window Formula

Suppose the current window is:

```text
arr[i-k : i]
```

Its sum can be updated using:

```python
window += arr[i] - arr[i-k]
```

Meaning:

```text
new window sum
    =
old window sum
    - element leaving
    + element entering
```

This avoids repeatedly calculating:

```python
sum(arr[i:i+k])
```

---

# Approach

First calculate the sum of the first `k` elements:

```python
window = sum(arr[:k])
```

Then move the window across the array.

For each window:

```python
if window / k >= threshold:
    count += 1
```

After checking the current window:

```python
window += arr[i] - arr[i-k]
```

This slides the window one position to the right.

---

# Why We Check Before Sliding

At the beginning:

```python
window = sum(arr[:k])
```

This represents the **first window**:

```text
arr[0 ... k-1]
```

When the loop starts:

```python
for i in range(k, len(arr)):
```

the current `window` is still the previous window.

So we first check it:

```python
if window / k >= threshold:
    count += 1
```

Then we slide:

```python
window += arr[i] - arr[i-k]
```

After the update, `window` represents the next window.

---

# Dry Run

Consider:

```text
arr = [2, 2, 2, 2, 5, 5]
k = 3
threshold = 3
```

We need windows of size `3`.

---

## Initial Window

```text
[2, 2, 2]
```

Sum:

```text
window = 6
```

Average:

```text
6 / 3 = 2
```

Since:

```text
2 < 3
```

don't count it.

---

## Slide 1

Remove:

```text
arr[0] = 2
```

Add:

```text
arr[3] = 2
```

Update:

```python
window = 6 + 2 - 2
       = 6
```

New window:

```text
[2, 2, 2]
```

Average:

```text
6 / 3 = 2
```

Not counted.

---

## Slide 2

Remove:

```text
arr[1] = 2
```

Add:

```text
arr[4] = 5
```

Update:

```python
window = 6 + 5 - 2
       = 9
```

New window:

```text
[2, 2, 5]
```

Average:

```text
9 / 3 = 3
```

Since:

```text
3 >= 3
```

count it.

```text
count = 1
```

---

## Slide 3

Remove:

```text
arr[2] = 2
```

Add:

```text
arr[5] = 5
```

Update:

```python
window = 9 + 5 - 2
       = 12
```

New window:

```text
[2, 5, 5]
```

Average:

```text
12 / 3 = 4
```

Valid.

```text
count = 2
```

Final answer:

```text
2
```

---

# Your Code

```python
class Solution:
    def numOfSubarrays(self, arr: list[int], k: int, threshold: int) -> int:
        window = sum(arr[:k])
        count = 0

        for i in range(k, len(arr)):
            if window / k >= threshold:
                count += 1

            window += arr[i] - arr[i-k]

        if window / k >= threshold:
            count += 1

        return count
```

---

# Understanding the Loop

The loop:

```python
for i in range(k, len(arr)):
```

starts at `k`.

Why?

Because the first window already contains:

```text
indices 0 → k-1
```

So the first new element entering the window is:

```text
arr[k]
```

That's why:

```python
i = k
```

is the correct starting point.

---

# Why Is There Another Check After the Loop?

This part is important:

```python
if window / k >= threshold:
    count += 1
```

Inside the loop, we:

1. check the current window
2. slide the window

So after the final iteration, we have already slid into the **last window**, but we haven't checked it yet.

That's why we need the final check.

Think of it as:

```text
CHECK → SLIDE
CHECK → SLIDE
CHECK → SLIDE
LAST WINDOW → CHECK
```

---

# Alternative Version

You can also structure the solution so every window is checked immediately after it is created.

For example:

```python
class Solution:
    def numOfSubarrays(self, arr: list[int], k: int, threshold: int) -> int:
        window = sum(arr[:k])
        count = 0

        for i in range(k - 1, len(arr)):
            if window >= threshold * k:
                count += 1

            if i + 1 < len(arr):
                window += arr[i + 1] - arr[i - k + 1]

        return count
```

This version avoids division.

Instead of:

```python
window / k >= threshold
```

we use:

```python
window >= threshold * k
```

These are mathematically equivalent.

---

# Why Avoid Division?

This:

```python
window / k >= threshold
```

can be rewritten as:

```text
window >= threshold × k
```

Example:

```text
window = 15
k = 3
threshold = 5
```

Instead of:

```text
15 / 3 >= 5
```

we can simply check:

```text
15 >= 5 × 3
15 >= 15
```

This is also a clean integer-based comparison.

For this problem, either approach is perfectly fine.

---

# Fixed-Size Sliding Window Pattern

This problem is a textbook example of:

```text
Fixed Window Size = k
```

General template:

```python
window = sum(arr[:k])

for i in range(k, len(arr)):

    # process current window

    # slide window
    window += arr[i] - arr[i-k]
```

The important part is:

```python
arr[i]       # element entering
arr[i-k]     # element leaving
```

---

# Visualizing the Window

Suppose:

```text
arr = [1, 2, 3, 4, 5, 6]
k = 3
```

The windows are:

```text
[1, 2, 3]
       ↓
[2, 3, 4]
       ↓
[3, 4, 5]
       ↓
[4, 5, 6]
```

Instead of recalculating each sum:

```text
1 + 2 + 3
2 + 3 + 4
3 + 4 + 5
4 + 5 + 6
```

we update:

```text
6
6 - 1 + 4 = 9
9 - 2 + 5 = 12
12 - 3 + 6 = 15
```

This is the entire optimization.

---

# Brute Force vs Sliding Window

## Brute Force

For every starting position:

```python
for i in range(len(arr) - k + 1):
    window = sum(arr[i:i+k])
```

Each `sum()` takes `O(k)`.

Overall:

```text
O(n × k)
```

---

## Sliding Window

Calculate the first sum once:

```python
window = sum(arr[:k])
```

Then every movement takes `O(1)`:

```python
window += arr[i] - arr[i-k]
```

Overall:

```text
O(n)
```

This is the key reason sliding window is useful.

---

# Complexity

Let:

```text
n = len(arr)
```

### Time Complexity

```text
O(n)
```

We traverse the array once.

### Space Complexity

```text
O(1)
```

Only a few variables are maintained.

---

# Pattern Recognition

When you see:

> Find/count subarrays of exactly size `k`

think:

```text
FIXED SLIDING WINDOW
```

When you see:

> Find the maximum/minimum/average/sum of every window of size `k`

think:

```text
FIXED SLIDING WINDOW
```

When you see:

> Count how many windows of size `k` satisfy some condition

think:

```text
FIXED SLIDING WINDOW
```

---

# Mental Model

For a fixed-size window, remember:

```text
START
  ↓
Create first window
  ↓
Process window
  ↓
Remove left element
  ↓
Add new right element
  ↓
Process next window
  ↓
Repeat
```

The core operation is always:

```python
window += incoming - outgoing
```

For an array:

```python
window += arr[i] - arr[i-k]
```

---

# Key Takeaways

### 1. Fixed `k` → Fixed Sliding Window

```text
window size = k
```

### 2. Don't recalculate the entire sum

Instead:

```python
window += incoming - outgoing
```

### 3. For averages

You can check:

```python
window / k >= threshold
```

or more cleanly:

```python
window >= threshold * k
```

### 4. The first window must be initialized

```python
window = sum(arr[:k])
```

### 5. Be careful with the last window

If you check before sliding, remember to check the final window after the loop.

---

# One-Line Pattern

If you remember only one thing from this problem:

```text
Fixed-size window → remove left + add right → process window
```

or in code:

```python
window += arr[i] - arr[i-k]
```
