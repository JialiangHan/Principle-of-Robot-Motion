import heapq

import PRM
import Plot
import distance
import geometry


class Dijkstra:
    def __init__(self, map: PRM):
        self.initial = map.initial
        self.goal = map.goal
        self.vertices = map.vertices
        self.edges = map.edges
        self.path = []
        self.neighbors = map.neighbors
        self.close_list = []

    def shorted_path(self):
        # use Dijkstra
        current_node = self.initial
        while current_node != self.goal:
            successor_list = self.get_successor(current_node)
            successor_min_dist = self.get_min_dist(current_node, successor_list)
            self.path.append(geometry.Edge(current_node, successor_min_dist))
            self.close_list.append(current_node)
            current_node = successor_min_dist

    def get_successor(self, current_node: geometry.Node) -> list[geometry.Node]:
        if current_node == self.initial:
            current_node.successor.append(self.neighbors[self.initial])
            for node in self.neighbors[self.initial]:
                node.predecessor.append(self.initial)
        else:
            result = self.neighbors[current_node]
            for node in result:
                if node not in current_node.predecessor:
                    current_node.successor.append(node)
        return current_node.successor

    @staticmethod
    def get_min_dist(current_node: geometry.Node, node_list: list[geometry.Node]) -> geometry.Node:
        d = {}
        for node in node_list:
            d[node] = distance.dist(current_node, node)
        min_node = heapq.nsmallest(1, d.items(), key=lambda x: x[1])
        return min_node

    def Plot(self):
        for edge in self.path:
            Plot.plot_Edge(edge)
