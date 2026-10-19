Ahmad, since you're preparing for your Amazon OA and have already solved a good number of sliding-window problems, let's organize the topic into 8 core sliding window patterns. The goal is to see a problem, recognize its pattern, and know which template to apply.

# Sliding Window — 8 important approaches

## 1. Fixed-Size Window

Must know

Clue: Find the maximum, minimum, sum, or average of every subarray/substring of size `k`.

Examples: Maximum Average Subarray I, Find All Anagrams in a String.

```
left = 0window = 0ans = 0for right in range(len(nums)):    window += nums[right]    if right - left + 1 > k:        window -= nums[left]        left += 1    if right - left + 1 == k:        ans = max(ans, window)
```

Core idea: Add the incoming element, remove the outgoing element, and process the window when its size reaches `k`.

Time: \\(O(n)\\)

## 2. Variable Window — Longest Valid Subarray

Must know

Clue: Find the longest contiguous subarray satisfying a condition.

Examples: Longest Substring Without Repeating Characters, Max Consecutive Ones III, Fruit Into Baskets.

```
left = 0ans = 0for right in range(len(nums)):    # Add nums[right] to window    while not valid():        # Remove nums[left] from window        left += 1    ans = max(ans, right - left + 1)
```

Core idea: Expand the right pointer, shrink from the left until the window becomes valid, then update the maximum length.

Remember this template:

Expand → Shrink until valid → Update answer

Time: Usually \\(O(n)\\), provided each element enters and leaves the window at most once.

## 3. Variable Window — Shortest Valid Subarray

Clue: Find the minimum-length contiguous subarray satisfying a condition.

Examples: Minimum Size Subarray Sum, Minimum Window Substring.

```
left = 0ans = float("inf")for right in range(len(nums)):    # Add nums[right]    while valid():        ans = min(ans, right - left + 1)        # Remove nums[left]        left += 1
```

Core idea: Shrink the window while it remains valid to find the shortest possible answer.

Notice the difference from the longest-window pattern:

- Longest: shrink while invalid.
- Shortest: shrink while valid.

Important: For sum-based windows, the standard approach usually assumes non-negative numbers. Negative numbers can break the required monotonic behavior.

## 4. Frequency Map + Sliding Window

Clue: The problem involves character counts, distinct elements, duplicates, or required frequencies.

Examples: Longest Substring Without Repeating Characters, Longest Substring with At Most K Distinct Characters, Permutation in String.

```
count = {}left = 0ans = 0for right in range(len(s)):    count[s[right]] = count.get(s[right], 0) + 1    while len(count) > k:        count[s[left]] -= 1        if count[s[left]] == 0:            del count[s[left]]        left += 1    ans = max(ans, right - left + 1)
```

Core idea: Maintain a frequency map describing the current window.

Key detail: Delete keys whose count reaches zero. Otherwise, `len(count)` won't represent the number of distinct characters correctly.

This is especially important for your revision because it combines two patterns: variable window + HashMap.

## 5. At Most K → Exactly K

Clue: Count the number of subarrays or substrings containing exactly `k` distinct elements, odd numbers, or other qualifying items.

Examples: Subarrays with K Different Integers, Count Number of Nice Subarrays.

The key mathematical trick is:

\\[ \text{exactly}(k)=\text{atMost}(k)-\text{atMost}(k-1) \\]

For example, the number of subarrays with exactly 3 distinct integers equals the number with at most 3 distinct integers minus the number with at most 2.

```
def at_most_k(nums, k):    left = 0    count = {}    ans = 0    for right in range(len(nums)):        x = nums[right]        count[x] = count.get(x, 0) + 1        while len(count) > k:            y = nums[left]            count[y] -= 1            if count[y] == 0:                del count[y]            left += 1        ans += right - left + 1    return ans
```

Then:

```
return at_most_k(nums, k) - at_most_k(nums, k - 1)
```

Here, `right - left + 1` counts all valid subarrays ending at `right`.

## 6. Minimum Window Covering a Target

Clue: Find the smallest substring containing all required characters with the necessary frequencies.

Example: Minimum Window Substring.

```
need = {}for c in t:    need[c] = need.get(c, 0) + 1left = 0have = 0required = len(need)window = {}best = float("inf")for right, c in enumerate(s):    window[c] = window.get(c, 0) + 1    if c in need and window[c] == need[c]:        have += 1    while have == required:        best = min(best, right - left + 1)        x = s[left]        if x in need and window[x] == need[x]:            have -= 1        window[x] -= 1        left += 1
```

Core idea: Track how many distinct required characters currently meet their target frequency. Once all are satisfied, shrink the window to minimize its size.

This pattern is more advanced than ordinary frequency counting because the map must track whether the target requirements are satisfied.

## 7. Sliding Window with a Limited Budget

Clue: You can replace, delete, or modify a limited number of elements to make a window satisfy a condition.

Examples: Longest Repeating Character Replacement, Maximize the Confusion of an Exam, Max Consecutive Ones III.

For character replacement:

```
count = {}left = 0max_freq = 0ans = 0for right, c in enumerate(s):    count[c] = count.get(c, 0) + 1    max_freq = max(max_freq, count[c])    while (right - left + 1) - max_freq > k:        count[s[left]] -= 1        left += 1    ans = max(ans, right - left + 1)
```

The validity condition is:

\\[ \text{window size}-\text{max frequency}\leq k \\]

The difference tells you how many characters need replacing.

Important: This commonly used template intentionally does not decrease `max_freq` when shrinking. That stale maximum still supports the correct maximum-length result, although the maintained window need not always be fully valid at every iteration.

## 8. Multiple Windows / Two Pointers with a Window

Clue: The problem asks for matching anagrams, permutations, or counts of valid substrings, and a single window may not be enough.

Examples: Find All Anagrams in a String, Permutation in String.

For fixed-length anagram matching:

```
from collections import Counterneed = Counter(p)window = Counter()left = 0ans = []for right, c in enumerate(s):    window[c] += 1    if right - left + 1 > len(p):        window[s[left]] -= 1        if window[s[left]] == 0:            del window[s[left]]        left += 1    if right - left + 1 == len(p) and window == need:        ans.append(left)
```

Core idea: Keep the window the same size as the target and compare the frequency distributions.

This version is easy to understand. For large inputs, optimized implementations can compare frequency arrays or track how many character counts currently match.

# Quick revision cheat sheet

| Pattern                 | What to remember                                     |
| ----------------------- | ---------------------------------------------------- |
| Fixed-size              | Add right, remove left when size exceeds `k`         |
| Longest valid           | Shrink while invalid, maximize length                |
| Shortest valid          | Shrink while valid, minimize length                  |
| Frequency map           | Maintain counts and delete zero-count keys           |
| Exactly K               | `atMost(k) - atMost(k-1)`                            |
| Minimum covering window | Track satisfied requirements                         |
| Budget / replacements   | Count how many changes the window needs              |
| Anagram / permutation   | Match frequency distributions in a fixed-size window |

## Test your pattern recognition

## Sliding window mini-quiz

0/5

1\. Find the maximum sum of any subarray of size k.

Fixed-size window

Shortest valid window

Exactly K

2\. Find the longest substring with at most two distinct characters.

Fixed-size window

Variable window + frequency map

Prefix sum

3\. Count subarrays with exactly k distinct integers.

At most(k) - at most(k-1)

Binary search

Fixed-size window

4\. Find the smallest substring containing every character of a target string.

Longest valid window

Minimum covering window

Complement lookup

5\. Find the longest run of 1s after flipping at most k zeros.

Budget-based variable window

Fixed-size window

Prefix sum only

Reset quiz

