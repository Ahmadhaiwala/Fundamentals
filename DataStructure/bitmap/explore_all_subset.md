Ahhh yeah 😂 then don't re-learn this as a DFS problem.

Since you're doing **bit manipulation / bitmap**, LeetCode 78 is actually a nice opportunity to solve the **same problem using bits**.

The key connection is:

> **A subset is just a binary mask.**

For `nums = [1,2,3]`, there are `2^3 = 8` subsets, so enumerate masks from `0` to `7`.

```text
mask     binary     subset
 0        000        []
 1        001        [1]
 2        010        [2]
 3        011        [1,2]
 4        100        [3]
 5        101        [1,3]
 6        110        [2,3]
 7        111        [1,2,3]
```

The bit position tells us whether to include the corresponding element.

```text
nums = [1, 2, 3]
        ↑  ↑  ↑
bit     0  1  2
```

So for:

```text
mask = 5
```

binary:

```text
101
```

Bit `0` = `1` → take `nums[0] = 1`

Bit `1` = `0` → skip `nums[1] = 2`

Bit `2` = `1` → take `nums[2] = 3`

Therefore:

```text
[1,3]
```

### Bitmap solution

```python
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        ans = []

        for mask in range(1 << n):
            subset = []

            for i in range(n):
                if mask & (1 << i):
                    subset.append(nums[i])

            ans.append(subset)

        return ans
```

The important line is:

```python
if mask & (1 << i):
```

You're basically asking:

> **"Is bit `i` turned on in this mask?"**

For example:

```text
mask = 5

5       = 101
1 << 0  = 001
           &
          101
          ---
          001  → yes
```

So take `nums[0]`.

Then:

```text
1 << 1 = 010

101
010
---
000  → no
```

Skip `nums[1]`.

Then:

```text
1 << 2 = 100

101
100
---
100  → yes
```

Take `nums[2]`.

---

### And THIS is the bitmap pattern you should remember

```python
for mask in range(1 << n):
    for i in range(n):
        if mask & (1 << i):
            # nums[i] is selected
```

This pattern will show up **everywhere** in bitmask problems.

DFS:

```text
take / don't take
```

Bitmask:

```text
1 / 0
```

They're literally representing the **same decision tree**, just encoded differently.

So since you've already done 78 with DFS, I'd actually recommend **not spending time on the DFS again**. Use this problem to get comfortable translating:

**DFS decision → binary mask → bit operations.**
