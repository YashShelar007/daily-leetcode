from typing import List, Dict
from collections import defaultdict, deque

class Solution:
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        """
        LC 3446. Sort Matrix by Diagonals

        Rule:
          - Bottom-left triangle (including main diagonal) → each diagonal sorted in NON-INCREASING order.
          - Top-right triangle → each diagonal sorted in NON-DECREASING order.

        Trick:
          Group by diagonal key k = i - j (all cells on a ↘︎ diagonal share k).
          If k >= 0  (i >= j)  → bottom-left → sort DESC.
          If k < 0   (i < j)   → top-right   → sort ASC.

        Time Complexity:  O(n^2 log n)  (sum of sorts over all diagonals)
        Space Complexity: O(n^2)        (stores all diagonal buckets)
        """
        n = len(grid)
        diags: Dict[int, List[int]] = defaultdict(list)

        # bucket values by diagonal id (i - j)
        for i in range(n):
            for j in range(n):
                diags[i - j].append(grid[i][j])

        # sort each diagonal according to region rule
        for k, vals in diags.items():
            vals.sort(reverse=(k >= 0))   # bottom-left (k>=0) → non-increasing
            diags[k] = deque(vals)        # deque for O(1) pops from the left

        # write back in traversal order
        for i in range(n):
            for j in range(n):
                grid[i][j] = diags[i - j].popleft()

        return grid
