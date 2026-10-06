# LeetCode 1358 — Number of Substrings Containing All Three Characters

## Problem

Given a string `s` consisting only of characters `'a'`, `'b'`, and `'c'`, return the number of substrings that contain **at least one `a`, at least one `b`, and at least one `c`**.

### Example

```text
Input:  s = "abcabc"
Output: 10
```

---

## Approach — Sliding Window

### Core Idea

Use a **sliding window** with two pointers:

- `left` → start of the current window
- `right` → end of the current window
- `freq` → stores the frequency of characters currently inside the window
- `res` → total number of valid substrings

We expand the window by moving `right`.

Whenever the current window contains all three characters (`a`, `b`, and `c`), it is a valid window.

The important observation is:

> If `s[left:right+1]` contains all three characters, then every substring starting at `left` and ending from `right` through the end of the string is also valid.

Therefore, the number of valid substrings contributed by this window is:

```python
len(s) - right
```

---

## Your Implementation

```python
class Solution:
    def numberOfSubstrings(self, s):
        left = 0
        res = 0
        freq = {}

        for right in range(len(s)):
            freq[s[right]] = freq.get(s[right], 0) + 1

            while len(freq) == 3:
                res += len(s) - right

                freq[s[left]] -= 1

                if freq[s[left]] == 0:
                    del freq[s[left]]

                left += 1

        return res
```

---

## Step-by-Step Explanation

### 1. Initialize the window

```python
left = 0
res = 0
freq = {}
```

- `left = 0` → window starts from index `0`
- `res = 0` → no valid substrings counted yet
- `freq = {}` → no characters inside the window

---

### 2. Expand the window

```python
for right in range(len(s)):
    freq[s[right]] = freq.get(s[right], 0) + 1
```

Move `right` from left to right.

For every new character, increase its frequency.

For example:

```text
s = "abcabc"
```

After processing the first three characters:

```text
window = "abc"
freq = {
    'a': 1,
    'b': 1,
    'c': 1
}
```

Now:

```python
len(freq) == 3
```

so the window contains all three required characters.

---

## 3. Count valid substrings

```python
while len(freq) == 3:
    res += len(s) - right
```

This is the **most important part of the problem**.

Suppose:

```text
s = "abcabc"
      ^
    right = 2
```

Current window:

```text
"abc"
```

Since it already contains `a`, `b`, and `c`, these are all valid:

```text
abc
abca
abcab
abcabc
```

There are:

```text
6 - 2 = 4
```

valid substrings starting at `left = 0`.

Therefore:

```python
res += len(s) - right
```

---

## 4. Shrink the window

After counting, we try to move `left` forward:

```python
freq[s[left]] -= 1
```

Then, if its frequency becomes zero:

```python
if freq[s[left]] == 0:
    del freq[s[left]]
```

Finally:

```python
left += 1
```

Why do this?

Because there might be **another valid window** with a larger `left`.

For example:

```text
abcabc
^^^
```

After counting `"abc"`, remove the first `a`:

```text
abcabc
 ^^^
```

The window is now `"bc"` and is no longer valid.

So we stop shrinking and continue expanding `right`.

---

# Dry Run

Consider:

```text
s = "abcabc"
```

### `right = 0`

```text
window = "a"
freq = {a: 1}
```

Not valid.

```text
res = 0
```

---

### `right = 1`

```text
window = "ab"
freq = {a: 1, b: 1}
```

Not valid.

```text
res = 0
```

---

### `right = 2`

```text
window = "abc"
freq = {a: 1, b: 1, c: 1}
```

Valid.

```python
res += 6 - 2
```

```text
res = 4
```

Now shrink:

```text
remove 'a'
window = "bc"
```

Only two distinct characters remain.

Stop shrinking.

---

### `right = 3`

Add `'a'`:

```text
window = "bca"
freq = {b: 1, c: 1, a: 1}
```

Valid.

```text
res += 6 - 3
res += 3
```

```text
res = 7
```

Shrink:

```text
remove 'b'
window = "ca"
```

Stop.

---

### `right = 4`

Add `'b'`:

```text
window = "cab"
```

Valid.

```text
res += 6 - 4
res += 2
```

```text
res = 9
```

Shrink:

```text
window = "ab"
```

Stop.

---

### `right = 5`

Add `'c'`:

```text
window = "abc"
```

Valid.

```text
res += 6 - 5
res += 1
```

```text
res = 10
```

Final answer:

```text
10
```

---

# Why `len(s) - right`?

This is the key trick.

If the current window `[left, right]` already contains all three characters, then extending the ending position can **never remove characters**.

For:

```text
abcabc
```

if `[0, 2]` = `"abc"` is valid, then:

```text
[0, 2] = "abc"
[0, 3] = "abca"
[0, 4] = "abcab"
[0, 5] = "abcabc"
```

are all valid.

Number of possible ending positions:

```text
right, right+1, ..., n-1
```

which is:

```text
n - right
```

So:

```python
res += len(s) - right
```

---

# Complexity

### Time Complexity

```text
O(n)
```

Although there is a `for` loop and a `while` loop, `left` only moves forward.

Both `left` and `right` move at most `n` times.

Therefore:

```text
O(n)
```

### Space Complexity

```text
O(1)
```

Because the string contains only three possible characters:

```text
a, b, c
```

So `freq` can contain at most 3 entries.

---

# Pattern to Remember

This problem is a great example of the:

```text
Sliding Window + Counting Valid Extensions
```

pattern.

When you see:

> Count the number of substrings/subarrays satisfying some condition.

Think:

1. Expand `right`
2. Track the current window
3. When the window becomes valid, count how many valid extensions exist
4. Move `left` to find more valid windows

For this problem:

```python
while len(freq) == 3:
    res += len(s) - right
    # shrink from left
```

The unusual part is that we **count before shrinking**.

---

# Final Template

```python
class Solution:
    def numberOfSubstrings(self, s):
        left = 0
        res = 0
        freq = {}

        for right in range(len(s)):
            freq[s[right]] = freq.get(s[right], 0) + 1

            while len(freq) == 3:
                res += len(s) - right

                freq[s[left]] -= 1

                if freq[s[left]] == 0:
                    del freq[s[left]]

                left += 1

        return res
```

## One-Line Memory Trick

> **Once a window has `a + b + c`, count all possible endings (`n - right`), then shrink from the left.**
