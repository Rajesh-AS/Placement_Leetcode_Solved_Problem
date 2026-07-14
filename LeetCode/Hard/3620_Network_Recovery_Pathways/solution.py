"""
LeetCode 3620
Network Recovery Pathways

Difficulty: Hard

Approach:
Binary search on the minimum edge cost. For each candidate, filter edges
with cost >= mid and only online nodes. Use topological sort + DP on the
filtered DAG to find the minimum total cost path from 0 to n-1. If that
cost <= k, the candidate is feasible. Maximize via binary search.

Time Complexity: O((N + E) * log R)
Space Complexity: O(N + E)
"""

from typing import List
from collections import deque, defaultdict


class Solution:
    def maxWeight(self, n: int, edges: List[List[int]], k: int, online: List[bool]) -> int:
        adj = defaultdict(list)
        all_costs = set()
        for u, v, w in edges:
            adj[u].append((v, w))
            all_costs.add(w)

        sorted_costs = sorted(all_costs)

        def can_achieve(min_cost):
            filtered = defaultdict(list)
            in_degree = [0] * n
            reachable = set()

            for u in range(n):
                if u != 0 and u != n - 1 and not online[u]:
                    continue
                reachable.add(u)

            for u in reachable:
                for v, w in adj[u]:
                    if w >= min_cost and v in reachable:
                        filtered[u].append((v, w))
                        in_degree[v] += 1

            queue = deque()
            for node in reachable:
                if in_degree[node] == 0:
                    queue.append(node)

            topo_order = []
            while queue:
                node = queue.popleft()
                topo_order.append(node)
                for neighbor, _ in filtered[node]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)

            dist = [float('inf')] * n
            dist[0] = 0
            for node in topo_order:
                if dist[node] == float('inf'):
                    continue
                for neighbor, weight in filtered[node]:
                    if dist[node] + weight < dist[neighbor]:
                        dist[neighbor] = dist[node] + weight

            return dist[n - 1] <= k

        if not can_achieve(0):
            return -1

        low, high = 0, len(sorted_costs) - 1
        result = 0
        while low <= high:
            mid = (low + high) // 2
            if can_achieve(sorted_costs[mid]):
                result = sorted_costs[mid]
                low = mid + 1
            else:
                high = mid - 1

        return result
