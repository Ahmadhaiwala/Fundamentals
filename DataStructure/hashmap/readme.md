Ahmad, if you're revising DSA for your Amazon OA, here are the main HashMap (`dict` in Python) approaches you should recognize when solving LeetCode problems. Since you've already solved around 280 problems, focus on identifying the pattern rather than memorizing individual solutions.

## 7 important HashMap approaches

1\. Frequency Counting

Clue: You need to count occurrences of elements or characters.

```
count[x] = count.get(x, 0) + 1
```

Examples: Majority Element, Top K Frequent Elements, Ransom Note.

Time: Usually O(n)

2\. Complement / Fast Lookup

Clue: Find two elements satisfying a target or condition.

```
if target - x in seen:    return [seen[target - x], i]seen[x] = i
```

Examples: Two Sum, Contains Duplicate.

Time: Usually O(n)

3\. Grouping by a Key

Clue: Group elements that share the same property.

```
groups[key].append(x)
```

Examples: Group Anagrams, Sort Characters By Frequency. Common keys include sorted strings, frequency tuples, and remainders.

4\. Prefix Sum + HashMap

Clue: Count or find subarrays satisfying a sum condition.

```
prefix += xans += freq.get(prefix - k, 0)freq[prefix] = freq.get(prefix, 0) + 1
```

Examples: Subarray Sum Equals K, Contiguous Array. Key insight: A previous prefix sum can help identify the current subarray.

5\. Sliding Window + Frequency Map

Clue: A contiguous substring/subarray with frequency or distinct-element constraints.

```
while len(count) > limit:    count[nums[left]] -= 1    if count[nums[left]] == 0:        del count[nums[left]]    left += 1
```

Examples: Longest Substring Without Repeating Characters, Fruit Into Baskets. Key insight: The map tracks the current window's state.

6\. First / Last Occurrence Tracking

Clue: You need an index, distance, or earliest occurrence.

```
last_seen[x] = i
```

Examples: Longest Consecutive Sequence, Isomorphic Strings. Store indices or first-seen positions instead of just counts.

7\. Mapping Relationships

Clue: Two collections must follow a consistent one-to-one relationship.

```
if a in forward and forward[a] != b:    return Falseforward[a] = b
```

Examples: Isomorphic Strings, Word Pattern. Sometimes you need two maps to enforce a one-to-one mapping.

## How to identify the right approach

| Problem clue                                 | Likely pattern       |
| -------------------------------------------- | -------------------- |
| Count each element                           | Frequency map        |
| Find a pair or check membership              | Lookup / complement  |
| Group equivalent elements                    | Key-based grouping   |
| Contiguous subarray with a sum condition     | Prefix sum + map     |
| Contiguous window with frequency constraints | Sliding window + map |
| Need an element's index or previous position | Index tracking       |
| Match two sequences consistently             | Relationship mapping |

Important distinction: HashMap is a data structure, not necessarily the whole algorithm. Many problems combine it with another technique, especially sliding window, prefix sum, sorting, or heaps.

For your revision, I'd prioritize frequency counting → complement lookup → prefix sum + map → sliding window + map. Then test yourself on mixed problems without knowing the topic beforehand. That's the skill that will help most in an OA.&#x20;