from typing import List

class Solution:
    def sortVowels(self, s: str) -> str:
        """
        LC 2785. Sort Vowels in a String

        Keep consonants fixed and sort only the vowels (a,e,i,o,u in both cases)
        in nondecreasing ASCII order, then place them back into their original
        indices.

        Steps:
          1) Collect positions of vowels and the vowel chars.
          2) Sort the collected vowels (Python's default string sort is ASCII).
          3) Write them back at the recorded positions.

        Time Complexity:  O(n + k log k), where k is the # of vowels (k ≤ n)
        Space Complexity: O(n) for the output list (or O(k) extra beyond input)
        """
        vowels = set("AEIOUaeiou")

        pos, vals = [], []
        for i, ch in enumerate(s):
            if ch in vowels:
                pos.append(i)
                vals.append(ch)

        vals.sort()  # ASCII nondecreasing

        res = list(s)
        for i, ch in zip(pos, vals):
            res[i] = ch
        return "".join(res)
