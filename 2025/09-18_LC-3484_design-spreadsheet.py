from typing import Dict, List

class Spreadsheet:
    """
    LC 3484. Design Spreadsheet

    Data structures
    ---------------
    - sheet: dict mapping column 'A'..'Z' -> list of row values.
             Each list has length = rows, initialized to 0.

    Helper methods
    --------------
    - _get_cell(ref): resolve a cell reference like 'B10' to its int value.
    - _val(term): resolve either a non-negative integer literal or a cell reference.

    Rationale
    ---------
    - setCell / resetCell are O(1) assignments into the underlying row list.
    - getValue parses the formula "=X+Y" and resolves each operand in O(1).
    - Overall complexity: O(1) per operation.
    """

    def __init__(self, rows: int):
        # Initialize 26 columns A..Z, each with `rows` 0's
        self.rows = rows
        self.sheet: Dict[str, List[int]] = {
            chr(c): [0] * rows for c in range(ord('A'), ord('Z') + 1)
        }

    def _get_cell(self, ref: str) -> int:
        """Resolve a cell reference like 'B10' -> value."""
        col, r = ref[0], int(ref[1:]) - 1
        return self.sheet[col][r]

    def _val(self, term: str) -> int:
        """Resolve either a literal integer or a cell reference."""
        return int(term) if term[0].isdigit() else self._get_cell(term)

    def setCell(self, cell: str, value: int) -> None:
        """Set the given cell (e.g. 'A1') to a value."""
        col, r = cell[0], int(cell[1:]) - 1
        self.sheet[col][r] = value

    def resetCell(self, cell: str) -> None:
        """Reset the given cell (e.g. 'A1') to 0."""
        col, r = cell[0], int(cell[1:]) - 1
        self.sheet[col][r] = 0

    def getValue(self, formula: str) -> int:
        """Evaluate a formula of the form '=X+Y'."""
        assert formula[0] == '='
        x, y = formula[1:].split('+', 1)
        return self._val(x) + self._val(y)
