from typing import List, Tuple, Dict
import heapq

class TaskManager:
    """
    LC 3408. Design Task Manager

    Data structures
    ---------------
    - info:   taskId -> (userId, priority)  (source of truth)
    - heap:   max-heap by (priority desc, taskId desc) implemented as
              a min-heap of (-priority, -taskId). We keep stale entries
              and discard them lazily in execTop.

    Rationale
    ---------
    All operations are O(log N) (heap push/pop), while membership/
    validation uses O(1) dict lookups. Lazy deletion avoids expensive
    'decrease-key' operations on heaps.
    """

    def __init__(self, tasks: List[List[int]]):
        # taskId -> (userId, priority)
        self.info: Dict[int, Tuple[int, int]] = {}
        # max-heap of (-priority, -taskId)
        self.heap: List[Tuple[int, int]] = []

        for userId, taskId, priority in tasks:
            self.info[taskId] = (userId, priority)
            heapq.heappush(self.heap, (-priority, -taskId))

    def add(self, userId: int, taskId: int, priority: int) -> None:
        """Add a new task for userId with given priority."""
        self.info[taskId] = (userId, priority)
        heapq.heappush(self.heap, (-priority, -taskId))

    def edit(self, taskId: int, newPriority: int) -> None:
        """Update priority of an existing task (lazy push)."""
        userId, _ = self.info[taskId]
        self.info[taskId] = (userId, newPriority)
        heapq.heappush(self.heap, (-newPriority, -taskId))

    def rmv(self, taskId: int) -> None:
        """Remove a task from the system (heap entry becomes stale)."""
        if taskId in self.info:
            del self.info[taskId]

    def execTop(self) -> int:
        """
        Execute the task with highest (priority, taskId).
        Return the associated userId, or -1 if none exists.
        """
        while self.heap:
            neg_p, neg_tid = heapq.heappop(self.heap)
            taskId = -neg_tid
            priority = -neg_p

            # Discard stale entries (removed or out-of-date priority).
            if taskId in self.info and self.info[taskId][1] == priority:
                userId, _ = self.info.pop(taskId)
                return userId

        return -1
