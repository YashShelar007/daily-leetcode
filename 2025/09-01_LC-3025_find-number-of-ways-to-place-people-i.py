from typing import List

class Solution:
    def numberOfPairs(self, points: List[List[int]]) -> int:
        """
        LC 3025. Find the Number of Ways to Place People I

        Count ordered pairs (A, B) such that:
          • A is on the upper-left side of B  → ax <= bx and ay >= by, and not equal
          • The closed axis-aligned rectangle [ax..bx] × [by..ay] contains no other points
            (including the border).

        Brute-force:
          Try every (i, j) with A=points[i], B=points[j] that satisfy the pos. relation,
          then scan to ensure the rectangle is empty.

        Time Complexity:  O(n^3)   (n≤50 is fine)
        Space Complexity: O(1)
        """
        n = len(points)
        ans = 0

        for i in range(n):
            ax, ay = points[i]
            for j in range(n):
                if i == j:
                    continue
                bx, by = points[j]

                # A must be strictly upper-left in at least one axis, and not identical
                if not (ax <= bx and ay >= by and (ax < bx or ay > by)):
                    continue

                # Rectangle must be empty including borders
                empty = True
                for k in range(n):
                    if k == i or k == j:
                        continue
                    x, y = points[k]
                    if ax <= x <= bx and by <= y <= ay:
                        empty = False
                        break

                if empty:
                    ans += 1

        return ans
