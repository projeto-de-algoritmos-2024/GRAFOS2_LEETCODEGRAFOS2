class Heap:
    def __init__(self):
        self.heap = []

    def insert(self, weight, node):
        self.heap.append((weight, node))
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def _heapify_down(self, index):
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.heap) and self.heap[left_child][0] < self.heap[smallest][0]:
            smallest = left_child
        if right_child < len(self.heap) and self.heap[right_child][0] < self.heap[smallest][0]:
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def is_empty(self):
        return len(self.heap) == 0


class Solution:
    MOD = 10**9 + 7

    def build_graph(self, edges, n):
        graph = {i: [] for i in range(1, n + 1)}
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
        return graph

    def dijkstra(self, graph, n):
        distances = {i: float('inf') for i in range(1, n + 1)}
        distances[n] = 0

        heap = Heap()
        heap.insert(0, n)

        while not heap.is_empty():
            d, u = heap.extract_min()
            if distances[u] < d:
                continue
            for v, w in graph[u]:
                if distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    heap.insert(distances[v], v)

        return distances

    def countRestrictedPaths(self, n, edges):
        graph = self.build_graph(edges, n)
        distances = self.dijkstra(graph, n)

        sorted_nodes = sorted(range(1, n + 1), key=lambda x: distances[x])

        restricted_paths = [0] * (n + 1)
        restricted_paths[n] = 1

        for node in sorted_nodes:
            for neighbor, weight in graph[node]:
                if distances[node] > distances[neighbor]:
                    restricted_paths[node] = (restricted_paths[node] + restricted_paths[neighbor]) % self.MOD

        return restricted_paths[1]
