from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        LC 37. Sudoku Solver

        Approach:
          Backtracking with constraint sets for rows/cols/boxes.
          At each step pick the empty cell with the *fewest* valid digits (MRV),
          try each candidate, and recurse. Undo on failure.

        Data:
          rows[r], cols[c], boxes[b] store digits placed in that unit.
          Box id: (r // 3) * 3 + (c // 3).

        Correctness:
          We only place a digit if it's absent from row/col/box. The problem
          guarantees a unique solution; search terminates when all empties filled.

        Complexity:
          Worst-case exponential (backtracking), but MRV + forward checking make it
          very fast on typical inputs. Space is O(81) for sets and recursion.
        """
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empties: List[tuple[int,int]] = []

        box_id = lambda r, c: (r // 3) * 3 + (c // 3)

        # initialize sets and collect empty cells
        for r in range(9):
            for c in range(9):
                v = board[r][c]
                if v == '.':
                    empties.append((r, c))
                else:
                    rows[r].add(v)
                    cols[c].add(v)
                    boxes[box_id(r, c)].add(v)

        def best_index(start: int) -> int:
            """Return index in empties[start:] with the fewest candidates."""
            best_i, best_cnt = start, 10
            for i in range(start, len(empties)):
                r, c = empties[i]
                b = box_id(r, c)
                # candidates = digits not present in any unit
                cnt = 9 - len(rows[r] | cols[c] | boxes[b])
                if cnt < best_cnt:
                    best_cnt, best_i = cnt, i
                    if best_cnt == 1:
                        break
            return best_i

        def dfs(k: int = 0) -> bool:
            if k == len(empties):
                return True

            # choose the MRV cell and bring it to position k
            i = best_index(k)
            empties[k], empties[i] = empties[i], empties[k]
            r, c = empties[k]
            b = box_id(r, c)

            # iterate candidates
            used = rows[r] | cols[c] | boxes[b]
            for d in '123456789':
                if d in used:
                    continue
                board[r][c] = d
                rows[r].add(d); cols[c].add(d); boxes[b].add(d)
                if dfs(k + 1):
                    return True
                # backtrack
                board[r][c] = '.'
                rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)
            return False

        dfs()
