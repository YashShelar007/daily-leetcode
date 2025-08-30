from typing import List

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        """
        LC 36. Valid Sudoku

        Validate a partially-filled 9x9 Sudoku board:
          - Each row has no duplicate digits 1–9.
          - Each column has no duplicate digits 1–9.
          - Each 3x3 box has no duplicate digits 1–9.
        Dots '.' are empty cells and ignored.

        Implementation:
          Use 9 sets for rows, 9 for columns, and 9 for 3x3 boxes.
          Box index = (r // 3) * 3 + (c // 3).

        Time Complexity:  O(81) ≈ O(1)        (fixed-size board)
        Space Complexity: O(1)                 (at most 81 digits across 27 sets)
        """
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]  # 3x3 sub-boxes

        for r in range(9):
            for c in range(9):
                ch = board[r][c]
                if ch == '.':
                    continue
                b = (r // 3) * 3 + (c // 3)   # map to 0..8

                # if seen in any of row/col/box → invalid
                if ch in rows[r] or ch in cols[c] or ch in boxes[b]:
                    return False

                rows[r].add(ch)
                cols[c].add(ch)
                boxes[b].add(ch)

        return True
