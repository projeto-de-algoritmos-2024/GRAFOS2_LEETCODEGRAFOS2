from heapq import heappop, heappush
from collections import defaultdict


class Solution:
    def findAnswer(self, n, edges):
        graph = self.create_graph(edges)

        dist_from_start = self.dijkstra(0, n, graph)
        dist_from_end = self.dijkstra(n - 1, n, graph)
        shortest_path_length = dist_from_start[n - 1]

        return self.find_edges_in_shortest_paths(
            edges, dist_from_start, dist_from_end, shortest_path_length
        )

    def create_graph(self, edges):
        graph = defaultdict(dict)
        for i, (u, v, w) in enumerate(edges):
            graph[u][v] = (w, i)
            graph[v][u] = (w, i)
        return graph

    def dijkstra(self, start, n, graph):
        distances = {i: float("inf") for i in range(n)}
        distances[start] = 0
        heap = [(0, start)]

        while heap:
            curr_dist, node = heappop(heap)
            if curr_dist > distances[node]:
                continue

            for neighbor, (weight, _) in graph[node].items():
                new_dist = curr_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(heap, (new_dist, neighbor))

        return distances

    def find_edges_in_shortest_paths(
        self, edges, dist_from_start, dist_from_end, shortest_path_length
    ):
        result = [False] * len(edges)

        for i, (u, v, w) in enumerate(edges):
            if (
                dist_from_start[u] + w + dist_from_end[v] == shortest_path_length
                or dist_from_start[v] + w + dist_from_end[u] == shortest_path_length
            ):
                result[i] = True

        return result
