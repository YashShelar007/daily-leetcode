from typing import List
import math

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        """
        LC 3495. Minimum Operations to Make Array Elements Zero

        Operation: pick any two numbers a, b and replace with floor(a/4), floor(b/4).
        For a single number x, the number of steps to reach 0 by repeatedly x//=4 is:
            steps(x) = k+1  where 4^k <= x <= 4^{k+1}-1.
        For a range [l..r], total per-number steps S = sum_{i=l..r} steps(i).
        Since each operation processes 2 'steps', minimal ops = ceil(S / 2).

        We compute prefix F(x) = sum_{i=1..x} steps(i) using blocks:
            for block k: [start=4^k .. end=4^{k+1}-1], each contributes (k+1)*count
        Then answer for a query [l,r] is: ceil((F(r) - F(l-1)) / 2).

        Time:  O(Q * log_4(max r)), Space: O(1)
        """

        def steps_sum(x: int) -> int:
            """F(x) = total steps for all numbers in [1..x]."""
            if x <= 0:
                return 0
            total = 0
            k = 0
            start = 1           # 4^k
            while True:
                next_start = start * 4      # 4^{k+1}
                end = next_start - 1
                if x >= end:
                    # take the whole block [start..end]
                    total += (end - start + 1) * (k + 1)
                    k += 1
                    start = next_start
                else:
                    # take partial block [start..x]
                    total += (x - start + 1) * (k + 1)
                    break
            return total

        ans = 0
        for l, r in queries:
            s = steps_sum(r) - steps_sum(l - 1)
            ans += math.ceil(s / 2)
        return ans
