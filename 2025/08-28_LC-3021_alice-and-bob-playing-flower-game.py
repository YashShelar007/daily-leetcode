from typing import List

class Solution:
    def flowerGame(self, n: int, m: int) -> int:
        """
        LC 3021. Alice and Bob Playing Flower Game

        Observation:
          Each move removes exactly one flower. The total number of moves is x+y.
          Alice (first) wins iff x + y is odd.

        So we need the number of (x, y) with 1 <= x <= n, 1 <= y <= m, and (x + y) odd:
          (#odds in [1..n]) * (#evens in [1..m]) + (#evens in [1..n]) * (#odds in [1..m])

        Counts:
          odds(t)  = (t + 1) // 2
          evens(t) = t // 2

        Time Complexity:  O(1)
        Space Complexity: O(1)
        """
        odds_n, evens_n = (n + 1) // 2, n // 2
        odds_m, evens_m = (m + 1) // 2, m // 2
        return odds_n * evens_m + evens_n * odds_m
