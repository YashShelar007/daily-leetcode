from typing import List, Tuple, Dict
from collections import defaultdict, Counter
import heapq

class MovieRentingSystem:
    """
    LC 1912. Design Movie Rental System

    Data structures
    ---------------
    - price:        {(shop, movie) -> price}  (immutable after init)
    - avail:        movie -> min-heap of (price, shop) for *unrented* copies
    - del_avail:    movie -> Counter for lazy-deleting entries from avail heaps
    - rented:       global min-heap of [price, shop, movie] for all *rented* copies
    - del_rented:   Counter for lazy-deleting entries from the global rented heap

    Ordering rules
    --------------
    - For "search(movie)":   cheapest price asc, then shop asc  (we return up to 5 shops)
    - For "report()":        cheapest price asc, then shop asc, then movie asc (top 5)

    Rationale
    ---------
    We keep all candidates in heaps and mark removed items in a "delete map" (lazy deletion).
    Popping is done only when an item reaches the heap top and is marked stale. This avoids
    costly arbitrary deletions from heaps while guaranteeing asymptotically optimal ops.

    Complexity
    ----------
    - search:  O(k log n) worst-case (k <= 5) due to up to 5 pop/push after cleaning
    - rent:    O(log n)
    - drop:    O(log n)
    - report:  O(k log n) with k <= 5
    Memory ~ O(total entries) for heaps + maps.
    """

    def __init__(self, n: int, entries: List[List[int]]):
        # price lookup for (shop, movie)
        self.price: Dict[Tuple[int, int], int] = {}

        # per-movie heap of available copies: (price, shop)
        self.avail: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        # lazy deletion for avail
        self.del_avail: Dict[int, Counter] = defaultdict(Counter)

        # global heap of rented copies: [price, shop, movie]
        self.rented: List[List[int]] = []
        # lazy deletion for rented
        self.del_rented: Counter = Counter()

        for shop, movie, p in entries:
            self.price[(shop, movie)] = p
            heapq.heappush(self.avail[movie], (p, shop))

    # ----- internal helpers -------------------------------------------------

    def _clean_avail_top(self, movie: int) -> None:
        """Remove stale items from the top of the movie's available heap."""
        h = self.avail[movie]
        ban = self.del_avail[movie]
        while h and ban.get(h[0], 0) > 0:
            item = heapq.heappop(h)
            ban[item] -= 1
            if ban[item] == 0:
                del ban[item]

    def _clean_rented_top(self) -> None:
        """Remove stale items from the top of the global rented heap."""
        while self.rented and self.del_rented.get(tuple(self.rented[0]), 0) > 0:
            item = heapq.heappop(self.rented)
            t = tuple(item)
            self.del_rented[t] -= 1
            if self.del_rented[t] == 0:
                del self.del_rented[t]

    # ----- API --------------------------------------------------------------

    def search(self, movie: int) -> List[int]:
        """Return up to 5 shops with an unrented copy of `movie` (price asc, shop asc)."""
        self._clean_avail_top(movie)
        h = self.avail[movie]
        res: List[int] = []
        popped: List[Tuple[int, int]] = []

        while h and len(res) < 5:
            self._clean_avail_top(movie)
            if not h:
                break
            p, shop = heapq.heappop(h)
            res.append(shop)
            popped.append((p, shop))

        # restore heap
        for item in popped:
            heapq.heappush(h, item)

        return res

    def rent(self, shop: int, movie: int) -> None:
        """Rent a copy: remove it from `avail` (lazily) and push into `rented` heap."""
        p = self.price[(shop, movie)]
        self.del_avail[movie][(p, shop)] += 1
        heapq.heappush(self.rented, [p, shop, movie])

    def drop(self, shop: int, movie: int) -> None:
        """Return a copy: add back to `avail` heap and mark the rented tuple as deleted."""
        p = self.price[(shop, movie)]
        heapq.heappush(self.avail[movie], (p, shop))
        self.del_rented[(p, shop, movie)] += 1

    def report(self) -> List[List[int]]:
        """Return up to 5 cheapest rented movies as [shop, movie]."""
        self._clean_rented_top()
        res: List[List[int]] = []
        cache: List[List[int]] = []

        while self.rented and len(res) < 5:
            self._clean_rented_top()
            if not self.rented:
                break
            p, shop, movie = heapq.heappop(self.rented)
            res.append([shop, movie])
            cache.append([p, shop, movie])

        # restore heap
        for item in cache:
            heapq.heappush(self.rented, item)

        return res
