from heapq import heappop, heappush
from collections import defaultdict, deque


class Solution:
    def findAnswer(self, n, edges):
        graph = self.create_graph(edges)
        reverse_graph = self.create_reverse_graph(edges)

        sccs = self.find_sccs(n, graph, reverse_graph)

        if self.is_connected_in_same_scc(sccs, 0, n - 1):
            dist_from_start = self.dijkstra(0, n, graph)
            dist_from_end = self.dijkstra(n - 1, n, graph)
            shortest_path_length = dist_from_start[n - 1]

            return self.find_edges_in_shortest_paths(
                edges, dist_from_start, dist_from_end, shortest_path_length
            )

        return [False] * len(edges)

    def create_graph(self, edges):
        graph = defaultdict(dict)
        for i, (u, v, w) in enumerate(edges):
            graph[u][v] = (w, i)
            graph[v][u] = (w, i)
        return graph

    def create_reverse_graph(self, edges):
        reverse_graph = defaultdict(dict)
        for i, (u, v, w) in enumerate(edges):
            reverse_graph[v][u] = (w, i)
            reverse_graph[u][v] = (w, i)
        return reverse_graph

    def find_sccs(self, n, graph, reverse_graph):
        visited = [False] * n
        order = []

        def dfs1(node):
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs1(neighbor)
            order.append(node)

        for i in range(n):
            if not visited[i]:
                dfs1(i)

        visited = [False] * n
        sccs = []

        def dfs2(node, component):
            visited[node] = True
            component.append(node)
            for neighbor in reverse_graph[node]:
                if not visited[neighbor]:
                    dfs2(neighbor, component)

        while order:
            node = order.pop()
            if not visited[node]:
                component = []
                dfs2(node, component)
                sccs.append(component)

        return sccs

    def is_connected_in_same_scc(self, sccs, start, end):
        for component in sccs:
            if start in component and end in component:
                return True
        return False

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
