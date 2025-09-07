from typing import List

class Solution:
    def sumZero(self, n: int) -> List[int]:
        """
        LC 1304. Find N Unique Integers Sum up to Zero

        Construct n distinct integers summing to 0 by pairing (+i, -i).
        If n is odd, include 0.

        Time Complexity:  O(n)
        Space Complexity: O(n)
        """
        ans: List[int] = []
        for i in range(1, n // 2 + 1):
            ans.extend([i, -i])
        if n % 2 == 1:
            ans.append(0)
        return ans
