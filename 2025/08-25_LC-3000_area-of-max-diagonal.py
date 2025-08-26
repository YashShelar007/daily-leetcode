from typing import List

class Solution:
    def areaOfMaxDiagonal(self, dimensions: List[List[int]]) -> int:
        """
        Return the area of the rectangle that has the maximum diagonal length.
        If multiple rectangles share the same (maximum) diagonal length, return
        the one with the largest area.

        We compare by squared diagonal (l^2 + w^2) to avoid sqrt, which is
        faster and avoids floating-point issues.

        Args:
            dimensions: List of [length, width] integer pairs.

        Returns:
            The area (int) of the rectangle satisfying the criteria.

        Time Complexity:  O(n), where n = len(dimensions)
        Space Complexity: O(1), constant extra space
        """
        max_diag_sq = -1  # largest diagonal^2 seen so far
        best_area = 0     # area associated with max diag^2 (tie-broken by area)

        for l, w in dimensions:
            diag_sq = l * l + w * w     # squared diagonal (no sqrt)
            area = l * w

            # Primary key: larger diag_sq; Secondary key: larger area
            if diag_sq > max_diag_sq or (diag_sq == max_diag_sq and area > best_area):
                max_diag_sq = diag_sq
                best_area = area

        return best_area
