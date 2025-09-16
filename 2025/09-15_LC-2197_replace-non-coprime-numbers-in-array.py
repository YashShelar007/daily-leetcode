from typing import List
import math

class Solution:
    def replaceNonCoprimes(self, nums: List[int]) -> List[int]:
        """
        LC 2197. Replace Non-Coprime Numbers in Array

        Idea (stack):
          - Iterate left to right, maintain a stack of the finalized prefix.
          - For each x:
              while stack not empty and gcd(stack[-1], x) > 1:
                  x = lcm(stack[-1], x); pop()
              push x
          - This works because any new LCM may now combine with the previous top, so
            we keep merging backward until the top is coprime with x.

        Why this beats pop/insert-in-place:
          - Avoids O(n) middle operations repeatedly → linear-time passes with small
            constant gcd cost.

        Time Complexity:  O(n * T_gcd) (amortized; each element pushed/popped a few times)
        Space Complexity: O(n) for the stack
        """
        st: List[int] = []
        for x in nums:
            # Merge backwards while not coprime
            while st:
                g = math.gcd(st[-1], x)
                if g == 1:
                    break
                x = (st[-1] // g) * x  # lcm without overflow risk in Python
                st.pop()
            st.append(x)
        return st
