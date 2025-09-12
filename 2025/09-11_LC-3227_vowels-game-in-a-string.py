from typing import *

class Solution:
    def doesAliceWin(self, s: str) -> bool:
        """
        LC 3227. Vowels Game in a String

        Game:
          - Alice removes any non-empty substring with an ODD number of vowels.
          - Bob removes any non-empty substring with an EVEN number of vowels.
          - Alice moves first; optimal play; last mover wins.

        Observation:
          - If the string has no vowels, Alice has no legal move ⇒ she loses.
          - If the string has at least one vowel, Alice can remove a 1-length
            vowel substring (odd=1), guaranteeing at least one move and, under
            optimal play, a win for this impartial take-turns setup.

        Therefore: Alice wins iff s contains at least one vowel.

        Time Complexity:  O(n)
        Space Complexity: O(1)
        """
        vowels = set("aeiou")
        return any(ch in vowels for ch in s)
