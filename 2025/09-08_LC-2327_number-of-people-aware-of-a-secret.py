from typing import List

class Solution:
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        """
        LC 2327. Number of People Aware of a Secret

        dp[day] = #people who first learn the secret on `day` (1-indexed).
        sharers  = rolling count of people who can share on `day`:
                   +dp[day - delay] (start sharing)
                   -dp[day - forget] (just forgot; can’t share)

        Transition:
          For day >= 2, everyone who can share today tells exactly one new person:
            dp[day] = sharers

        Answer:
          Sum of dp over the last (forget - 1) days: those still remembering at day n.

        Time Complexity:  O(n)
        Space Complexity: O(n)
        """
        MOD = 10**9 + 7
        dp = [0] * (n + 1)
        dp[1] = 1

        sharers = 0  # people eligible to share on current day

        for day in range(1, n + 1):
            if day - delay >= 1:
                sharers = (sharers + dp[day - delay]) % MOD
            if day - forget >= 1:
                sharers = (sharers - dp[day - forget]) % MOD  # Python keeps it in [0, MOD)

            if day >= 2:
                dp[day] = sharers

        start = max(1, n - forget + 1)
        return sum(dp[start : n + 1]) % MOD
