# Monotonic Stack — Next Greater Element

## Problem

Given an array `nums`, for every element find the **first greater element to its right**.

If no greater element exists, return `-1`.

### Example

```text
nums = [2, 1, 5, 3, 4]

answer = [5, 5, -1, 4, -1]
```

---

## Core Observation

For every element, we are waiting for some future element that can answer:

> "Are you greater than me?"

When a new element `nums[i]` arrives, it can immediately answer the question for elements on the stack that are smaller than it.

Therefore:

```python
while stack and nums[stack[-1]] < nums[i]:
```

We pop those elements and set their answer to `nums[i]`.

---

## What Does the Stack Represent?

The stack contains **indices of elements that have not found their next greater element yet**.

The values in the stack are maintained in **decreasing order**.

Example:

```text
nums = [5, 3, 1]

stack values:

[5, 3, 1]
```

because:

```text
5 > 3 > 1
```

Therefore this is called a **monotonic decreasing stack**.

---

## Why Do We Pop?

Suppose:

```text
stack = [5, 3, 1]
current = 4
```

`4` can answer:

```text
1 → 4
3 → 4
```

But not:

```text
5 → ?
```

So we pop:

```text
1 → 4
3 → 4
```

and stop when:

```text
5 > 4
```

The remaining `5` is still waiting for a greater element.

---

## Template

```python
stack = []

for i in range(len(nums)):

    while stack and nums[stack[-1]] < nums[i]:
        index = stack.pop()
        answer[index] = nums[i]

    stack.append(i)
```

---

## Complete Solution

```python
class Solution:
    def nextGreater(self, nums: list[int]) -> list[int]:

        n = len(nums)
        answer = [-1] * n

        stack = []

        for i in range(n):

            while stack and nums[stack[-1]] < nums[i]:
                index = stack.pop()
                answer[index] = nums[i]

            stack.append(i)

        return answer
```

---

## Mental Model

Don't memorize the code.

Think:

```text
Current element arrives
        ↓
Can it answer elements waiting in stack?
        ↓
      YES
        ↓
    Pop them
        ↓
Assign current element as their answer
        ↓
Push current element
```

### Key Question

Whenever you see:

> "For every element, find the first/next greater element to the right"

Think:

```text
Elements are waiting
       ↓
Incoming element may resolve them
       ↓
Monotonic Stack
```

---

## Why Not Brute Force?

Brute force:

```python
for i in range(n):
    for j in range(i + 1, n):
        ...
```

Worst case:

```text
O(n²)
```

With the monotonic stack:

```text
Time:  O(n)
Space: O(n)
```

Each element is pushed once and popped at most once.

---

## Pattern Recognition

### Greater on the right

```text
Monotonic decreasing stack
```

### Smaller on the right

```text
Monotonic increasing stack
```

But don't blindly memorize this table.

Instead ask:

> **What causes an element waiting in the stack to get its answer?**

That determines what gets popped.

---

## The Real Pattern

The most important idea:

> **If the current element can resolve the requirement of elements stored in the stack, pop those elements.**

The stack is not just storing numbers.

It stores **unresolved elements waiting for a future answer**.
