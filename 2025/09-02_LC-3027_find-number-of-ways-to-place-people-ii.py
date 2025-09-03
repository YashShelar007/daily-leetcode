from typing import List

class Solution:
    def numberOfPairs(self, points: List[List[int]]) -> int:
        """
        LC 3027. Find the Number of Ways to Place People II

        We need ordered pairs (A,B) with:
          • A is upper-left of B: ax <= bx and ay >= by, and not identical
          • The CLOSED rectangle [ax..bx] × [by..ay] contains only A and B

        Trick:
          Coordinates are up to 1e9, so we compress x and y separately.
          Build a sparse occupancy grid on compressed coords and a 2D prefix sum.
          For each ordered pair (A,B) with the orientation condition, check that
          rect_sum(Ax,By,Bx,Ay) == 2.

        Complexity:
          Let n = number of points, X = #unique x, Y = #unique y (≤ n).
          Building grid + prefix: O(X*Y). Pair scan: O(n^2) with O(1) queries.
          Space: O(X*Y). With n ≤ 1000, this is well within limits.
        """
        n = len(points)

        # Coordinate compression
        xs = sorted({x for x, _ in points})
        ys = sorted({y for _, y in points})
        x_id = {x: i for i, x in enumerate(xs)}
        y_id = {y: i for i, y in enumerate(ys)}

        X, Y = len(xs), len(ys)

        # Occupancy grid and compressed indices of each point
        grid = [[0] * Y for _ in range(X)]
        comp = []
        for x, y in points:
            ix, iy = x_id[x], y_id[y]
            grid[ix][iy] = 1
            comp.append((ix, iy))

        # 2D prefix sum: ps[i+1][j+1] = sum over grid[0..i][0..j]
        ps = [[0] * (Y + 1) for _ in range(X + 1)]
        for i in range(X):
            row_sum = 0
            for j in range(Y):
                row_sum += grid[i][j]
                ps[i + 1][j + 1] = ps[i][j + 1] + row_sum

        def rect_sum(x1: int, y1: int, x2: int, y2: int) -> int:
            """Sum over closed rectangle [x1..x2] × [y1..y2] in compressed space."""
            return (
                ps[x2 + 1][y2 + 1]
                - ps[x1][y2 + 1]
                - ps[x2 + 1][y1]
                + ps[x1][y1]
            )

        # Count ordered pairs
        ans = 0
        for i in range(n):
            ax, ay = comp[i]
            for j in range(n):
                if i == j:
                    continue
                bx, by = comp[j]

                # A upper-left of B (allow equality on one axis, not both)
                if ax <= bx and ay >= by and (ax < bx or ay > by):
                    if rect_sum(ax, by, bx, ay) == 2:
                        ans += 1

        return ans
