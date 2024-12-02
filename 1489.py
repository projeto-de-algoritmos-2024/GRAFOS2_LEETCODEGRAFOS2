class Heap:
    def __init__(self):
        self.heap = []

    def insert(self, weight, origin, destination, edge_index):
        self.heap.append((weight, origin, destination, edge_index))
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
    def prim_algorithm_with_exclusion(self, n, edges, exclude_edge_index=None):
        graph = {i: [] for i in range(n)}
        for index, (u, v, weight) in enumerate(edges):
            if index != exclude_edge_index:
                graph[u].append((v, weight, index))
                graph[v].append((u, weight, index))

        visited = set()
        mst_edges = []
        total_weight = 0
        heap = Heap()

        visited.add(0)
        for neighbor, weight, edge_index in graph[0]:
            heap.insert(weight, 0, neighbor, edge_index)

        while not heap.is_empty():
            weight, u, v, edge_index = heap.extract_min()

            if v in visited:
                continue

            visited.add(v)
            mst_edges.append((u, v, weight, edge_index))
            total_weight += weight

            for neighbor, weight, edge_index in graph[v]:
                if neighbor not in visited:
                    heap.insert(weight, v, neighbor, edge_index)

        if len(visited) < n:
            return None, float('inf') 

        return mst_edges, total_weight


    def find_critical_edges(self, n, edges):
        original_mst, original_weight = self.prim_algorithm_with_exclusion(n, edges)
        if original_mst is None:
            return []

        critical_edges = []

        for _, _, _, edge_index in original_mst:
            _, new_weight = self.prim_algorithm_with_exclusion(n, edges, exclude_edge_index=edge_index)

            if new_weight > original_weight:
                critical_edges.append(edge_index)

        return critical_edges


    def prim_algorithm_with_inclusion(self, n, edges, include_edge=None):
        graph = {i: [] for i in range(n)}
        for index, (u, v, weight) in enumerate(edges):
            graph[u].append((v, weight, index))
            graph[v].append((u, weight, index))

        visited = set()
        mst_edges = []
        total_weight = 0
        heap = Heap()

        if include_edge is not None:
            u, v, weight = edges[include_edge]
            mst_edges.append((u, v, weight, include_edge))
            total_weight += weight
            visited.add(u)
            visited.add(v)
            for neighbor, weight, edge_index in graph[u]:
                if neighbor not in visited:
                    heap.insert(weight, u, neighbor, edge_index)
            for neighbor, weight, edge_index in graph[v]:
                if neighbor not in visited:
                    heap.insert(weight, v, neighbor, edge_index)
        else:
            visited.add(0)
            for neighbor, weight, edge_index in graph[0]:
                heap.insert(weight, 0, neighbor, edge_index)

        while not heap.is_empty():
            weight, u, v, edge_index = heap.extract_min()

            if v in visited:
                continue

            visited.add(v)
            mst_edges.append((u, v, weight, edge_index))
            total_weight += weight

            for neighbor, weight, edge_index in graph[v]:
                if neighbor not in visited:
                    heap.insert(weight, v, neighbor, edge_index)

        if len(visited) < n:
            return None, float('inf')  

        return mst_edges, total_weight


    def find_pseudo_critical_edges(self, n, edges):
        original_mst, original_weight = self.prim_algorithm_with_exclusion(n, edges)
        if original_mst is None:
            return []
        pseudo_critical_edges = []

        for index, (u, v, weight) in enumerate(edges):
            _, new_weight = self.prim_algorithm_with_inclusion(n, edges, include_edge=index)

            if new_weight == original_weight:
                pseudo_critical_edges.append(index)

        return pseudo_critical_edges

    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        critical_edges = self.find_critical_edges(n, edges)
        pseudo_critical_edges = [x for x in self.find_pseudo_critical_edges(n, edges) if x not in critical_edges]

        return critical_edges, pseudo_critical_edges

