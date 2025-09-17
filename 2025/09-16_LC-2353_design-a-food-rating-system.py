from typing import List
import heapq
from collections import defaultdict

class FoodRatings:
    """
    LC 2353. Design a Food Rating System

    Approach: per-cuisine max-heap with lazy deletion
      - Keep current truth in two dicts:
          food2cuisine[food] -> cuisine
          food2rating[food]  -> rating
      - For each cuisine, maintain a heap of (-rating, name).
        We *never* remove old entries on update; instead, we push a fresh
        pair and discard stale tops when answering highestRated.

    Tie-break: Python compares tuple elements left→right, so (-rating, name)
    ensures higher rating first; for equal ratings, lexicographically smaller
    name wins.

    Complexity:
      - changeRating:  O(log k) where k = #items of that cuisine
      - highestRated:  Amortized O(log k) due to lazy pops
      - Space:         O(n) for heaps + maps
    """
    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.food2cuisine = {}
        self.food2rating = {}
        self.cuisine_heap = defaultdict(list)  # cuisine -> [(-rating, name), ...]

        for f, c, r in zip(foods, cuisines, ratings):
            self.food2cuisine[f] = c
            self.food2rating[f] = r
            heapq.heappush(self.cuisine_heap[c], (-r, f))

    def changeRating(self, food: str, newRating: int) -> None:
        self.food2rating[food] = newRating
        c = self.food2cuisine[food]
        heapq.heappush(self.cuisine_heap[c], (-newRating, food))

    def highestRated(self, cuisine: str) -> str:
        h = self.cuisine_heap[cuisine]
        # Pop until the heap top reflects the current rating
        while h and -h[0][0] != self.food2rating[h[0][1]]:
            heapq.heappop(h)
        return h[0][1]
