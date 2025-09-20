from collections import deque, defaultdict
from bisect import bisect_left, bisect_right
from typing import List, Tuple, Deque, Dict, Set

class Router:
    """
    LC 3508. Implement Router

    Goal
    ----
    Design a router that stores up to `memoryLimit` packets and supports:
      - addPacket(source, destination, timestamp) -> bool
      - forwardPacket() -> [source, destination, timestamp] or []
      - getCount(destination, startTime, endTime) -> int
    with queries for addPacket coming in non-decreasing timestamp order.

    Data structures
    ---------------
    - q:     deque of packets in arrival order (FIFO): (src, dst, ts).
             This is the ground truth for the buffer content & eviction order.
    - seen:  set of (src, dst, ts) to reject duplicates in O(1).
    - ts:    destination -> list of timestamps (append-only, non-decreasing).
             We never physically delete timestamps; instead we advance a start
             pointer. This keeps getCount fast via binary search.
    - start: destination -> first valid index in ts[dest] (i.e., how many oldest
             timestamps for that destination have been evicted/forwarded).

    Rationale
    ---------
    * addPacket:
        - O(1) amortized for push + O(1) duplicate check.
        - If full, evict oldest from q in O(1); mark as removed by bumping
          start[dst] (lazy deletion) so ts arrays remain sorted and contiguous.
    * forwardPacket:
        - Pop from q in O(1) and bump start[dst]. Also remove from `seen`.
    * getCount:
        - Use bisect over ts[dst] with lo=start[dst] to ignore old entries:
          O(log K), where K is current #timestamps tracked for that destination.

    Complexity
    ----------
    - addPacket / forwardPacket: O(1) amortized
    - getCount: O(log K) per query
    - Space: O(N) for at most 1e5 operations (bounded by problem constraints)
    """

    def __init__(self, memoryLimit: int):
        self.cap: int = memoryLimit
        self.q: Deque[Tuple[int, int, int]] = deque()     # (src, dst, ts)
        self.seen: Set[Tuple[int, int, int]] = set()      # to detect duplicates

        self.ts: Dict[int, List[int]] = defaultdict(list) # dst -> timestamps
        self.start: Dict[int, int] = defaultdict(int)     # dst -> first valid idx

    def _evict_one(self) -> None:
        """
        Remove the oldest packet in FIFO order.
        Adjust per-destination start pointer (lazy delete from ts arrays).
        """
        src, dst, ts = self.q.popleft()
        self.seen.remove((src, dst, ts))
        self.start[dst] += 1

    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        """
        Add packet if it’s not a duplicate. If buffer is full, evict oldest.
        Return True on success, False if duplicate (same src, dst, ts).
        """
        key = (source, destination, timestamp)
        if key in self.seen:
            return False

        if len(self.q) == self.cap:
            self._evict_one()

        self.q.append(key)
        self.seen.add(key)

        # Append keeps per-destination timestamps sorted thanks to non-decreasing input
        self.ts[destination].append(timestamp)
        # self.start[destination] is already tracked (default 0)
        return True

    def forwardPacket(self) -> List[int]:
        """
        Forward (remove) the next packet in FIFO order.
        Return [source, destination, timestamp], or [] if empty.
        """
        if not self.q:
            return []
        src, dst, ts = self.q.popleft()
        self.seen.remove((src, dst, ts))
        self.start[dst] += 1
        return [src, dst, ts]

    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        """
        Count packets (still stored) with given destination and timestamp in [startTime, endTime].
        We search over ts[dst] starting from start[dst] to ignore evicted/forwarded ones.
        """
        arr = self.ts.get(destination)
        if not arr:
            return 0

        lo = self.start[destination]
        # Standard half-open range counting with bisect
        L = bisect_left(arr, startTime, lo=lo)
        R = bisect_right(arr, endTime, lo=lo)
        return R - L
