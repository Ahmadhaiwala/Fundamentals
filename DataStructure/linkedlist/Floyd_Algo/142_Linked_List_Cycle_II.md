
# LeetCode 142 — Linked List Cycle II

**Pattern:** Linked List · Floyd's Cycle Detection · Two Pointers

## Problem

Return the node where a linked list's cycle begins. Return `None` if no cycle exists.

## Approach 1: Visited Set

Store previously visited node references in a set. If a node appears again, return that node.

- **Time:** O(n)
- **Space:** O(n)

## Approach 2: Floyd's Cycle Detection

### Phase 1 — Detect the cycle

- `slow` moves one node at a time.
- `fast` moves two nodes at a time.
- If `fast` or `fast.next` becomes `None`, no cycle exists.
- If `slow is fast`, a cycle exists and the pointers have met inside it.

### Phase 2 — Find the cycle entry

1. Reset `slow` to `head`.
2. Keep `fast` at the meeting point.
3. Move both pointers one node at a time.
4. Their next meeting point is the cycle entry.

Use `is` to compare node identity, not node values.

## Why Does Phase 2 Work?

Let:

- `L` = distance from the head to the cycle entry.
- `x` = distance from the cycle entry to the meeting point.
- `C` = cycle length.
- `d` = distance travelled by `slow` when the pointers meet.

At the meeting point, `slow` travels `d` edges and `fast` travels `2d` edges. Their distance difference is a whole number of cycle lengths:

`2d - d = kC`

Therefore:

`d = kC`

Since `d = L + x`:

`L + x = kC`

Rearranging:

`L = kC - x = (k - 1)C + (C - x)`

The distance from the meeting point forward to the cycle entry is `C - x` (modulo a complete lap). Thus, the distance from the head to the entry equals that distance plus some complete cycle laps.

So, when one pointer resets to the head and both pointers move one step at a time, they meet at the cycle entry.

**This relationship is derived from the pointer speeds and cycle length; it is not an assumption.**

## Complexity Comparison

| Approach | Time | Extra Space |
|---|---|---|
| Visited set | O(n) | O(n) |
| Floyd's algorithm | O(n) | O(1) |

## Quick Recall

- Detect a cycle: slow/fast pointers.
- Find the entry: reset one pointer to the head; advance both one step at a time.
- No cycle: return `None`.
