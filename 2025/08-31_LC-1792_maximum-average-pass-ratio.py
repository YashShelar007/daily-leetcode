from typing import List, Tuple
import heapq

class Solution:
    def maxAverageRatio(self, classes: List[List[int]], extraStudents: int) -> float:
        """
        LC 1792. Maximum Average Pass Ratio

        Idea:
          Always give the next student to the class with the largest *marginal gain*:
              gain(p, t) = (p+1)/(t+1) - p/t
          This gain is diminishing as a class gets more students, so a greedy
          choice with a max-heap is optimal.

        Steps:
          1) Build a max-heap keyed by gain (store as negative for heapq).
          2) Pop the best class, add one student (p+=1, t+=1), push back with new gain.
          3) After distributing all extra students, sum final ratios and divide by n.

        Time Complexity:  O((n + extraStudents) log n)
        Space Complexity: O(n)
        """
        def gain(p: int, t: int) -> float:
            # Marginal improvement if we add one guaranteed pass
            return (p + 1) / (t + 1) - p / t

        # Max-heap using negative gains: entries are (-gain, p, t)
        heap: List[Tuple[float, int, int]] = [(-gain(p, t), p, t) for p, t in classes]
        heapq.heapify(heap)

        # Greedily assign each extra student to the class with highest marginal gain
        for _ in range(extraStudents):
            g, p, t = heapq.heappop(heap)
            p += 1; t += 1
            heapq.heappush(heap, (-gain(p, t), p, t))

        # Compute the final average pass ratio
        total = 0.0
        for _, p, t in heap:
            total += p / t
        return total / len(classes)
