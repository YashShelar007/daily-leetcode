from typing import List
from collections import Counter

class Solution:
    def minimumTeachings(self, n: int, languages: List[List[int]], friendships: List[List[int]]) -> int:
        """
        LC 1733. Minimum Number of People to Teach

        Idea:
          - Find 'affected' users (endpoints of friendships with no shared language).
          - Among affected users, count how many already know each language.
          - Teach the language that covers the most affected users.
            Answer = len(affected) - max_covered.

        Time Complexity:  O(m + sum(len(l[u])) over affected)  (≤ ~5e5 here)
        Space Complexity: O(n + m)
        """
        # Users are 1-indexed; store sets for O(1) membership tests
        know = [set()] + [set(langs) for langs in languages]

        # Step 1: who is affected?
        affected = set()
        for u, v in friendships:
            if know[u].isdisjoint(know[v]):
                affected.add(u)
                affected.add(v)

        if not affected:
            return 0

        # Step 2: language coverage among affected users
        freq = Counter()
        for u in affected:
            for lang in know[u]:
                freq[lang] += 1

        max_covered = max(freq.values(), default=0)
        return len(affected) - max_covered
