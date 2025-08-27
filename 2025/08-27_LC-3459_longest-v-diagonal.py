from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Longest 'V' along diagonals with at most one clockwise turn.

        Grid cells contain values in {0,1,2}. A valid V-path:
          - Moves along one diagonal direction, optionally makes one clockwise turn
            to the adjacent diagonal, then continues.
          - Values along the path alternate as …, 0, 2, 0, 2… (legs),
            with the turning (apex) cell being 1.
          - We count path length in number of cells visited.

        DP idea (per starting direction k):
          1) Precompute straight-line lengths s0/s2 for the *clockwise* direction
             (the leg after turning), where sX[i][j] = max length starting at (i,j)
             if the next expected value is X and we keep going straight.
          2) Compute best-with-one-turn tables b0/b2/b1 for the current direction:
             - b0/b2 allow either keep-straight or turn-now (using s2/s0 from step 1).
             - b1 tracks best length if current cell is apex (expects 1 here).
          3) Take the max over all directions.

        Time Complexity:  O(n*m) — constant-factor 4 passes over the grid
        Space Complexity: O(n*m) — DP tables

        Args:
            grid: n x m integer matrix with values in {0,1,2}.

        Returns:
            Maximum length of such a V-path.
        """
        n, m = len(grid), len(grid[0])

        # diagonals in clockwise order: NE, SE, SW, NW
        DIRS = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

        def iter_order(di: int, dj: int):
            """
            Iterate cells so that (i+di, j+dj) is processed before (i, j).
            This ensures DP transitions 'forward' are ready.
            """
            ir = range(n-1, -1, -1) if di > 0 else range(n)
            jr = range(m-1, -1, -1) if dj > 0 else range(m)
            for i in ir:
                for j in jr:
                    yield i, j

        def inb(i: int, j: int) -> bool:
            return 0 <= i < n and 0 <= j < m

        def straight_for_dir(dir_idx: int):
            """
            For a given direction, compute the best straight-only lengths
            when expecting 0 (s0) or 2 (s2) at the current cell.
            """
            di, dj = DIRS[dir_idx]
            s0 = [[0] * m for _ in range(n)]
            s2 = [[0] * m for _ in range(n)]

            for i, j in iter_order(di, dj):
                ni, nj = i + di, j + dj
                if grid[i][j] == 0:
                    s0[i][j] = 1 + (s2[ni][nj] if inb(ni, nj) else 0)
                if grid[i][j] == 2:
                    s2[i][j] = 1 + (s0[ni][nj] if inb(ni, nj) else 0)
            return s0, s2

        ans = 0

        # Process each starting direction k.
        for k in range(4):
            di, dj = DIRS[k]
            cw = (k + 1) % 4                     # clockwise direction index
            s0_cw, s2_cw = straight_for_dir(cw)  # straight tables for the *turned* leg

            # bestX: best length starting at (i,j) expecting value X along dir k,
            #        allowed to make at most one clockwise turn in the future.
            b0 = [[0] * m for _ in range(n)]
            b2 = [[0] * m for _ in range(n)]
            b1 = [[0] * m for _ in range(n)]

            for i, j in iter_order(di, dj):
                ni, nj = i + di, j + dj                         # next if we keep going straight
                ci, cj = i + DIRS[cw][0], j + DIRS[cw][1]       # next if we turn now

                # Expecting 0 at (i,j)
                if grid[i][j] == 0:
                    keep = b2[ni][nj] if inb(ni, nj) else 0
                    turn = s2_cw[ci][cj] if inb(ci, cj) else 0
                    b0[i][j] = 1 + max(keep, turn)

                # Expecting 2 at (i,j)
                if grid[i][j] == 2:
                    keep = b0[ni][nj] if inb(ni, nj) else 0
                    turn = s0_cw[ci][cj] if inb(ci, cj) else 0
                    b2[i][j] = 1 + max(keep, turn)

                # Apex: expecting 1 at (i,j) → next expected is 2
                if grid[i][j] == 1:
                    keep = b2[ni][nj] if inb(ni, nj) else 0
                    turn = s2_cw[ci][cj] if inb(ci, cj) else 0
                    b1[i][j] = 1 + max(keep, turn)
                    if b1[i][j] > ans:
                        ans = b1[i][j]

        return ans
