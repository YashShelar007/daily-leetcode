from typing import List

class Solution:
    def spellchecker(self, wordlist: List[str], queries: List[str]) -> List[str]:
        """
        LC 966. Vowel Spellchecker

        Precedence for each query:
          1) Exact (case-sensitive) match → return that word.
          2) Case-insensitive match → return the FIRST word in wordlist with that lowercase.
          3) Vowel-error match: after replacing every vowel in the query with '*'
             (on lowercase), match against the FIRST word in wordlist with same pattern.
          4) Otherwise return "".

        Implementation:
          - exact: set(wordlist)
          - case_map: lowercase -> first word with that lowercase
          - vowel_map: devoweled(lowercase) -> first word
          - devowel(x): replace aeiou with '*'

        Time Complexity:  O(W + Q * L), where
          W = total chars in wordlist, Q = #queries, L = max word length (≤ 7)
        Space Complexity: O(W)
        """
        vowels = set("aeiou")

        def devowel(s: str) -> str:
            return "".join('*' if c in vowels else c for c in s)

        # 1) Exact matches
        exact = set(wordlist)

        # 2) First-occurrence maps
        case_map = {}     # lowercase -> first word with that lowercase
        vowel_map = {}    # devoweled(lowercase) -> first word

        for w in wordlist:
            low = w.lower()
            case_map.setdefault(low, w)
            vowel_map.setdefault(devowel(low), w)

        ans: List[str] = []
        for q in queries:
            if q in exact:
                ans.append(q)
                continue

            low = q.lower()
            if low in case_map:
                ans.append(case_map[low])
                continue

            ans.append(vowel_map.get(devowel(low), ""))

        return ans
