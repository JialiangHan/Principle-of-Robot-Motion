import PRM
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

    def get_min_dist(self, current_node: geometry.Node, node_list: list[geometry.Node]) -> geometry.Node:
