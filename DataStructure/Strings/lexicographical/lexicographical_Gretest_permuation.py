class Solution:
    def lexGreaterPermutation(self, s: str, target: str) -> str:
        count = [0] * 26

        for ch in s:
            count[ord(ch) - ord('a')] += 1

        n = len(s)

        def backtrack(pos, greater):
            if pos == n:
                return "" if greater else None

            start = 0

            # If prefix is already greater, choose smallest available char.
            # If prefix is equal, we need to ensure we don't become smaller.
            if not greater:
                start = ord(target[pos]) - ord('a')

            for c in range(start, 26):
                if count[c] == 0:
                    continue

                # If prefix is equal and we choose a smaller char -> invalid
                if not greater and c < ord(target[pos]) - ord('a'):
                    continue

                count[c] -= 1

                new_greater = greater or (
                    c > ord(target[pos]) - ord('a')
                )

                suffix = backtrack(pos + 1, new_greater)

                if suffix is not None:
                    count[c] += 1
                    return chr(c + ord('a')) + suffix

                count[c] += 1

            return None

        ans = backtrack(0, False)

        return ans if ans is not None else ""