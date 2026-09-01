class Solution:
    def lexPalindromicPermutation(self, s: str, target: str) -> str:
        n = len(s)


        count = [0] * 26

        for ch in s:
            count[ord(ch) - ord('a')] += 1

     
        odd_count = 0
        middle = ""

        for i in range(26):
            if count[i] % 2:
                odd_count += 1
                middle = chr(i + ord('a'))

        if odd_count > 1:
            return ""

        
        half_count = [x // 2 for x in count]
        half_len = n // 2

        target_half = target[:half_len]



        half = []
        remaining = half_count[:]

        for i in range(half_len):
            t = ord(target_half[i]) - ord('a')

            if remaining[t] > 0:
                half.append(t)
                remaining[t] -= 1

            else:
              
                for c in range(t + 1, 26):

                    if remaining[c] > 0:
                        half.append(c)
                        remaining[c] -= 1

                        for x in range(26):
                            half.extend([x] * remaining[x])

                        left = ''.join(
                            chr(x + ord('a'))
                            for x in half
                        )

                        return left + middle + left[::-1]

             
                break

   

        if len(half) == half_len:

            left = ''.join(
                chr(x + ord('a'))
                for x in half
            )

            candidate = left + middle + left[::-1]

            if candidate > target:
                return candidate

   

        i = len(half) - 1

        while i >= 0:

           
            current = half[i]
            remaining[current] += 1

            t = ord(target_half[i]) - ord('a')

           
            for c in range(t + 1, 26):

                if remaining[c] == 0:
                    continue

                half[i] = c
                remaining[c] -= 1

               
                result_half = half[:i + 1]

                for x in range(26):
                    result_half.extend([x] * remaining[x])

                left = ''.join(
                    chr(x + ord('a'))
                    for x in result_half
                )

                return left + middle + left[::-1]

            i -= 1

        return ""