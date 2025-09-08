from typing import List

class Solution:
    def getNoZeroIntegers(self, n: int) -> List[int]:
        """
        LC 1317. Convert Integer to the Sum of Two No-Zero Integers

        Find two integers a, b > 0 with no digit '0' in their decimal
        representation such that a + b = n.

        Time Complexity:  O(n) in the worst case, 
                          but typically returns quickly for small a.
        Space Complexity: O(1)
        """
        def no_zero(x: int) -> bool:
            return "0" not in str(x)

        for a in range(1, n):
            b = n - a
            if no_zero(a) and no_zero(b):
                return [a, b]
        return []
