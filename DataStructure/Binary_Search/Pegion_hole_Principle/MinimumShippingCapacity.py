class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:

        low = max(weights)
        high = sum(weights)

        while low <= high:

            mid = (low + high) // 2

            days_needed = 1
            current_weight = 0

            for weight in weights:

                if current_weight + weight <= mid:
                    current_weight += weight

                else:
                    days_needed += 1
                    current_weight = weight

            if days_needed <= days:
                high = mid - 1
            else:
                low = mid + 1

        return low