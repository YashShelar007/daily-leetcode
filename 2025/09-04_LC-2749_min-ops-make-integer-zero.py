from typing import *

class Solution:
    def makeTheIntegerZero(self, num1: int, num2: int) -> int:
        """
        LC 2749. Minimum Operations to Make the Integer Zero

        In one operation choose i in [0, 60] and do:
            num1 -= (2^i + num2)

        After k operations:
            num1_final = num1 - k*num2 - sum(2^{i_j})  (j = 1..k)
        Let n = num1 - k*num2. We need n = sum of k powers of two (repetitions allowed).
        That's possible iff:
            popcount(n) <= k  and  n >= k      (need at least k ones)

        Try k from 0..60 (enough to cover limits).

        Time:  O(60)    Space: O(1)
        """
        if num1 == 0:
            return 0

        for k in range(1, 61):
            n = num1 - k * num2
            if n < 0 and num2 > 0:
                # increasing k will only shrink n further; impossible from here on
                break
            if n >= k and n.bit_count() <= k:
                return k
        return -1
