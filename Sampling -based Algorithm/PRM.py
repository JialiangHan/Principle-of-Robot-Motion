import Map
import geometry
import random


class PRM:
    def __init__(self, map: Map, n: int, k: int, initial: geometry.Node, goal: geometry.Node):
        self.map = map
        self.number_of_node = n
        self.number_of_neighbors = k
        self.vertices = []
        self.edges = []
        self.initial = initial
        self.goal = goal

    def Roadmap_construction(self):
        while len(self.vertices) < self.number_of_node:
            q_random = self.sampling()
            if self.check_collision(q_random):
                self.vertices.append(q_random)
        for vertex in self.vertices:
            k_nearest_neighbor = self.get_k_nearest_neighbor(vertex)
            for neighbor in k_nearest_neighbor:
                if geometry.Edge(neighbor, vertex) not in self.edges and self.connect(neighbor, vertex):
                    self.edges.append(geometry.Edge(neighbor, vertex))

    def solve_query(self):
        k_nearest_neighbor_initial = self.get_k_nearest_neighbor(self.initial)
        k_nearest_neighbor_goal = self.get_k_nearest_neighbor(self.goal)
        self.vertices.append(self.initial)
        self.vertices.append(self.goal)
        # k_nearest_neighbor should be a heapq
        node_nearest_initial = k_nearest_neighbor_initial.pop
        while k_nearest_neighbor_initial:
            if self.connect(self.initial, node_nearest_initial):
                self.edges.append(geometry.Edge(self.initial, node_nearest_initial))
                break
            else:
                node_nearest_initial = k_nearest_neighbor_initial.pop
        node_nearest_goal = k_nearest_neighbor_goal.pop
        while k_nearest_neighbor_goal:
            if self.connect(self.goal, node_nearest_goal):
                self.edges.append(geometry.Edge(self.goal, node_nearest_goal))
                break
            else:
                node_nearest_goal = k_nearest_neighbor_goal.pop
        path = shorted_path(self.initial, self.goal, prm)
        if path:
            return path
        else:
            return "failure"

    def sampling(self) -> geometry.Node:
        x = random.uniform(self.map.size[0], self.map.size[1])
        y = random.uniform(self.map.size[2], self.map.size[3])
        return geometry.Node(x, y)

    def get_k_nearest_neighbor(self, vertex: geometry.Node) -> list[geometry.Node]:

    def connect(self, node1: geometry.Node, node2: geometry.Node) -> bool:

    def check_collision(self, node: geometry.Node) -> bool:
        for obstacle in self.map.obstacle_list:
            if node_in_polygon(node, obstacle):
                return False
        return True
