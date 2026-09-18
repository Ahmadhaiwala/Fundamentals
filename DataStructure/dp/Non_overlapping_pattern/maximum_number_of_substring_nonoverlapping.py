class Solution:

  def maxNumOfSubstrings(self, s: str) -> list[str]:
    n = len(s)
    left = {c: -1 for c in 'abcdefghijklmnopqrstuvwxyz'}
    right = {c: -1 for c in 'abcdefghijklmnopqrstuvwxyz'}

    for i, c in enumerate(s):
      if left[c] == -1:
        left[c] = i
      right[c] = i

    def get_valid_interval(i):
     
      r = right[s[i]]
      j = i
      while j <= r:
        c = s[j]
        if left[c] < i:
          return -1  
        r = max(r, right[c])
        j += 1
      return r

    intervals = []
    for i in range(n):
      if i == left[s[i]]:
        r = get_valid_interval(i)
        if r != -1:
          intervals.append((i, r))

   
    intervals.sort(key=lambda x: x[1])

    res = []
    prev_end = -1
    for start, end in intervals:
      if start > prev_end:
        res.append(s[start : end + 1])
        prev_end = end

    return res
