from typing import List

class Solution:
    def maxFreqSum(self, s: str) -> int:
        """
        LC 3541. Find Most Frequent Vowel and Consonant

        Idea:
          - Count frequencies of all letters.
          - Track the maximum frequency among vowels and consonants separately.
          - Return their sum.
        
        Time Complexity:  O(n + 26) ~ O(n)   (n = len(s), ≤ 100)
        Space Complexity: O(26)              (fixed alphabet size)
        """
        vowels = set("aeiou")
        freq = [0] * 26

        # count frequency of each letter
        for ch in s:
            freq[ord(ch) - 97] += 1

        max_vowel, max_cons = 0, 0
        for i in range(26):
            ch = chr(97 + i)
            if ch in vowels:
                max_vowel = max(max_vowel, freq[i])
            else:
                max_cons = max(max_cons, freq[i])

        return max_vowel + max_cons
