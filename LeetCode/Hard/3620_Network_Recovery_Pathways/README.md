# LeetCode 3620 - Network Recovery Pathways

**Difficulty:** Hard

## Problem Link

[https://leetcode.com/problems/network-recovery-pathways/](https://leetcode.com/problems/network-recovery-pathways/)

## Approach

Combine **binary search on the answer** with **shortest path on a DAG**.

1. **Binary search** over the possible minimum edge cost values. For each candidate `mid`, determine if there exists a valid path from node `0` to node `n-1` where every edge cost ≥ `mid` and the total path cost ≤ `k`, using only online intermediate nodes.
2. **Feasibility check**: Filter edges to only those with cost ≥ `mid`. Perform **topological sort** on the DAG, then use **DP** to find the minimum total cost path from node `0` to node `n-1`. If `min_cost[n-1] ≤ k`, the candidate is feasible.
3. **Maximize** the minimum edge cost through binary search.

## Time Complexity

O((N + E) × log R) — where R is the range of edge costs, N is nodes, E is edges.

## Space Complexity

O(N + E) — for adjacency list, in-degree array, and DP table.
