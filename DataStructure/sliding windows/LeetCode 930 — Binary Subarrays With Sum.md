# Sliding Window Approaches --- LeetCode

This note contains the approaches for the two problems we just worked
through.\
For each problem, the goal is to preserve the way I first tried to solve
it, explain what was wrong, and then build the correct pattern from that
attempt.

------------------------------------------------------------------------

# 1. LeetCode 1493 --- Longest Subarray of 1's After Deleting One Element

## Problem idea

Given a binary array, delete exactly one element and find the longest
remaining subarray containing only `1`s.

Example:

``` text
nums = [1,1,0,1,1]

Delete 0

=> [1,1,1,1]

Answer = 4
```

------------------------------------------------------------------------

## My First Implementation

``` python
class Solution:
    def longestSubarray(self, nums: list[int]) -> int:
        left = 0
        i = 0
        max_len = 0

        for right in range(len(nums)):
            if nums[right] == 0:
                i += 1

            if i > 1:
                left = right

            max_len = max(max_len, right - left)

        return max_len
```

## What I was trying to do

The idea was:

1.  Maintain a sliding window using `left` and `right`.
2.  Count how many zeroes are inside the window using `i`.
3.  Allow at most one zero.
4.  If there are more than one zero, move `left`.
5.  Because one element must be deleted, use:

``` python
right - left
```

instead of:

``` python
right - left + 1
```

The last part is actually correct.

------------------------------------------------------------------------

## Problem With My Implementation

The main problem is:

``` python
if i > 1:
    left = right
```

When we find the second zero, we cannot simply move `left` to `right`.

We need to remove the **first zero** from the window.

Example:

``` text
nums = [1,1,0,1,0,1]
          ↑     ↑
       first  second
       zero   zero
```

When we reach the second zero, the valid window should start immediately
after the first zero:

``` text
[1,1,0,1,0,1]
      ↑
      first zero

left should move to:

[1,1,0,1,0,1]
        ↑
     after first zero
```

Therefore, we need to remember the position of the previous zero.

------------------------------------------------------------------------

## Correct Sliding Window Approach

``` python
class Solution:
    def longestSubarray(self, nums: list[int]) -> int:
        left = 0
        prev_zero = -1
        max_len = 0

        for right in range(len(nums)):

            if nums[right] == 0:
                left = prev_zero + 1
                prev_zero = right

            max_len = max(max_len, right - left)

        return max_len
```

------------------------------------------------------------------------

## Why `right - left`?

Normally, the length of a window is:

``` text
right - left + 1
```

But this problem says:

> Delete exactly one element.

The window contains at most one zero.

We delete that zero:

``` text
window length - 1

= (right - left + 1) - 1

= right - left
```

So:

``` python
max_len = max(max_len, right - left)
```

is intentional.

------------------------------------------------------------------------

## Dry Run

``` text
nums = [1,1,0,1,1,0,1]
```

    right   value   left   prev_zero   answer
  ------- ------- ------ ----------- --------
        0       1      0          -1        0
        1       1      0          -1        1
        2       0      0           2        2
        3       1      0           2        3
        4       1      0           2        4
        5       0      3           5        4
        6       1      3           5        4

Answer:

``` text
4
```

------------------------------------------------------------------------

## Pattern Learned

When a sliding window is allowed to contain **at most one zero**,
remember:

``` text
previous zero position
```

When another zero appears:

``` python
left = previous_zero + 1
previous_zero = right
```

The important conceptual lesson:

> Don't just count how many invalid elements exist. Sometimes you need
> the position of the previous invalid element to move the window
> correctly.

------------------------------------------------------------------------

# 2. LeetCode 930 --- Binary Subarrays With Sum

## Problem idea

Given a binary array and an integer `goal`, count the number of
non-empty subarrays whose sum is exactly `goal`.

Because the array contains only `0` and `1`:

``` text
sum of subarray = number of 1s in subarray
```

So the real problem is:

> Count subarrays containing exactly `goal` ones.

------------------------------------------------------------------------

## My First Implementation

``` python
class Solution:
    def numSubarraysWithSum(self, nums: list[int], goal: int) -> int:

        left = 0
        counter = 0
        res = 0
        right = 0

        while right < len(nums):

            if nums[right] == 1:
                counter += 1

            if counter == goal:
                a = left

                while a <= right and nums[a] != 1:
                    res += 1
                    a += 1

            if counter > goal:
                counter -= 1

                while left < right and nums[left] != 1:
                    left += 1
                    res += 1

                left += 1

        return res
```

------------------------------------------------------------------------

## What I was trying to do

The idea was actually quite interesting.

I was trying to:

1.  Keep a window using `left` and `right`.
2.  Count the number of `1`s using `counter`.
3.  When:

``` python
counter == goal
```

count the possible starting positions created by leading zeroes. 4.
When:

``` python
counter > goal
```

move `left` forward until the window becomes valid again.

This is close to the correct mathematical idea.

------------------------------------------------------------------------

## The Important Observation

Suppose:

``` text
nums = [0,0,1,0,1,0,0]
```

and:

``` text
goal = 2
```

We need subarrays containing exactly two `1`s.

The first `1` has:

``` text
2 zeroes before it
```

Therefore, there are:

``` text
2 + 1 = 3
```

possible starting positions.

The last `1` has:

``` text
2 zeroes after it
```

Therefore, there are:

``` text
2 + 1 = 3
```

possible ending positions.

Total:

``` text
3 × 3 = 9
```

------------------------------------------------------------------------

## Why My Implementation Has a Problem

When:

``` python
counter == goal
```

my code does:

``` python
a = left

while a <= right and nums[a] != 1:
    res += 1
    a += 1
```

This counts some possible starting positions.

But it does not properly account for the zeroes **after the last `1`**.

Also, when:

``` python
counter > goal
```

the code immediately does:

``` python
counter -= 1
```

But `counter` should only decrease when `left` actually passes a `1`.

This is an important sliding-window rule:

> If your window state represents the contents between `left` and
> `right`, update the state when the pointer actually removes an
> element.

------------------------------------------------------------------------

# Better General Approach: At Most K

A much more reusable solution is:

``` text
exactly K
=
atMost(K) - atMost(K - 1)
```

Why?

Suppose:

``` text
atMost(2)
```

counts all subarrays containing:

``` text
0 ones
1 one
2 ones
```

And:

``` text
atMost(1)
```

counts:

``` text
0 ones
1 one
```

Subtract them:

``` text
atMost(2) - atMost(1)
```

The `0` and `1` cases disappear.

Only:

``` text
exactly 2 ones
```

remain.

------------------------------------------------------------------------

## Correct Implementation

``` python
class Solution:
    def numSubarraysWithSum(self, nums: list[int], goal: int) -> int:

        def atMost(k):
            if k < 0:
                return 0

            left = 0
            count = 0
            res = 0

            for right in range(len(nums)):
                count += nums[right]

                while count > k:
                    count -= nums[left]
                    left += 1

                res += right - left + 1

            return res

        return atMost(goal) - atMost(goal - 1)
```

------------------------------------------------------------------------

## Why `res += right - left + 1`?

After maintaining:

``` text
count <= k
```

the entire window:

``` text
[left ... right]
```

is valid.

Every possible starting position from:

``` text
left
```

through:

``` text
right
```

creates a valid subarray ending at `right`.

Number of possible starts:

``` text
right - left + 1
```

Therefore:

``` python
res += right - left + 1
```

------------------------------------------------------------------------

## Dry Run of `atMost`

Consider:

``` text
nums = [1,0,1]
goal = 2
```

For:

``` text
atMost(2)
```

    right   value   count   left   added
  ------- ------- ------- ------ -------
        0       1       1      0       1
        1       0       1      0       2
        2       1       2      0       3

Total:

``` text
1 + 2 + 3 = 6
```

For:

``` text
atMost(1)
```

the window shrinks when the second `1` arrives.

The difference gives the number of subarrays containing exactly two
`1`s.

------------------------------------------------------------------------

# The Main DSA Lesson From These Two Problems

These two problems look similar because both use sliding windows, but
they teach different things.

## LeetCode 1493

Main idea:

``` text
At most one invalid element
+
remember previous invalid position
```

Pattern:

``` python
if nums[right] == 0:
    left = prev_zero + 1
    prev_zero = right
```

------------------------------------------------------------------------

## LeetCode 930

Main idea:

``` text
Exactly K
=
At Most K - At Most K-1
```

Pattern:

``` python
def atMost(k):
    ...
```

and:

``` python
return atMost(goal) - atMost(goal - 1)
```

------------------------------------------------------------------------

# What I Should Recognize Next Time

When seeing a new sliding-window problem, ask:

### 1. Is it asking for a longest/maximum window?

Think:

``` text
Expand right
Check constraint
Move left when invalid
Track maximum
```

### 2. Is it asking for number of subarrays with an exact count?

Try:

``` text
exactly K
=
atMost(K) - atMost(K-1)
```

### 3. Does moving `left` need information about something that happened earlier?

You may need to store:

``` text
previous position
last occurrence
frequency
```

rather than just a counter.

### 4. Is the array binary?

Remember:

``` text
sum = number of 1s
```

This often makes sliding-window approaches possible.

------------------------------------------------------------------------

# Final Takeaway

The important thing is not to memorize the final code.

Your first attempts were already moving toward the correct ideas:

-   You recognized the **sliding window**.
-   You recognized that zeroes determine the window boundaries.
-   You recognized that multiple starting positions can exist because of
    zeroes.
-   You were trying to count those positions explicitly.

The next step is learning to express those observations with clean
invariants.

The two patterns to keep:

``` text
Previous invalid position
```

and

``` text
Exactly K = AtMost(K) - AtMost(K-1)
```
