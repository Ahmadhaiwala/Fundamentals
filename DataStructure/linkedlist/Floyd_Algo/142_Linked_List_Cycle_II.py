
from typing import Optional


# LeetCode provides ListNode:
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:
    def detectCycle(self, head: Optional["ListNode"]) -> Optional["ListNode"]:
        slow = fast = head

        # Phase 1: Detect a cycle and find a meeting point.
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow is fast:
                # Phase 2: Find the cycle entry.
                slow = head

                while slow is not fast:
                    slow = slow.next
                    fast = fast.next

                return slow

        return None
