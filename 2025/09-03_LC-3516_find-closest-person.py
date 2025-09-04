from typing import *

class Solution:
    def findClosest(self, x: int, y: int, z: int) -> int:
        """
        LC 3516. Find Closest Person

        Return:
          1 if Person 1 (at x) reaches z first,
          2 if Person 2 (at y) reaches z first,
          0 if they arrive at the same time.

        Idea: both move at the same speed ⇒ compare absolute distances to z.

        Time Complexity:  O(1)
        Space Complexity: O(1)
        """
        dx = abs(z - x)
        dy = abs(z - y)
        if dx == dy:
            return 0
        return 1 if dx < dy else 2
