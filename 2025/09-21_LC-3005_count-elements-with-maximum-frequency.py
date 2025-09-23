from typing import List
from collections import Counter

class Solution:
    """
    LC 3005. Count Elements With Maximum Frequency

    Problem
    -------
    Given an array of positive integers, return the total number of
    elements that belong to the most frequent values in the array.

    Example:
    --------
    nums = [1,2,2,3,1,4]
    - Frequencies: {1:2, 2:2, 3:1, 4:1}
    - Max frequency = 2
    - Elements with freq == 2 are 1 and 2 → total count = 4

    Approach
    --------
    - Count frequencies using Counter
    - Find the maximum frequency
    - Sum counts of all elements whose frequency equals that maximum

    Complexity
    ----------
    - Time:  O(n)  (one pass to count, one pass to sum)
    - Space: O(n)  (for the frequency map)
    """

    def maxFrequencyElements(self, nums: List[int]) -> int:
        freq = Counter(nums)
        max_freq = max(freq.values())
        return sum(v for v in freq.values() if v == max_freq)
