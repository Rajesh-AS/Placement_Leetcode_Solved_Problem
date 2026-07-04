/*
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
*/

import java.util.*;

class Solution {
    public int maxWeight(int n, int[][] edges, int k, boolean[] online) {
        List<int[]>[] adj = new ArrayList[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        TreeSet<Integer> allCosts = new TreeSet<>();

        for (int[] edge : edges) {
            adj[edge[0]].add(new int[]{edge[1], edge[2]});
            allCosts.add(edge[2]);
        }

        List<Integer> sortedCosts = new ArrayList<>(allCosts);

        if (!canAchieve(n, adj, online, 0, k)) return -1;

        int low = 0, high = sortedCosts.size() - 1, result = 0;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (canAchieve(n, adj, online, sortedCosts.get(mid), k)) {
                result = sortedCosts.get(mid);
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return result;
    }

    private boolean canAchieve(int n, List<int[]>[] adj, boolean[] online, int minCost, int k) {
        int[] inDegree = new int[n];
        List<int[]>[] filtered = new ArrayList[n];
        for (int i = 0; i < n; i++) filtered[i] = new ArrayList<>();

        Set<Integer> reachable = new HashSet<>();
        for (int i = 0; i < n; i++) {
            if (i == 0 || i == n - 1 || online[i]) reachable.add(i);
        }

        for (int u : reachable) {
            for (int[] edge : adj[u]) {
                int v = edge[0], w = edge[1];
                if (w >= minCost && reachable.contains(v)) {
                    filtered[u].add(new int[]{v, w});
                    inDegree[v]++;
                }
            }
        }

        Queue<Integer> queue = new LinkedList<>();
        for (int node : reachable) {
            if (inDegree[node] == 0) queue.offer(node);
        }

        List<Integer> topoOrder = new ArrayList<>();
        while (!queue.isEmpty()) {
            int node = queue.poll();
            topoOrder.add(node);
            for (int[] edge : filtered[node]) {
                if (--inDegree[edge[0]] == 0) queue.offer(edge[0]);
            }
        }

        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;

        for (int node : topoOrder) {
            if (dist[node] == Long.MAX_VALUE) continue;
            for (int[] edge : filtered[node]) {
                int v = edge[0], w = edge[1];
                if (dist[node] + w < dist[v]) {
                    dist[v] = dist[node] + w;
                }
            }
        }
        return dist[n - 1] <= k;
    }
}
