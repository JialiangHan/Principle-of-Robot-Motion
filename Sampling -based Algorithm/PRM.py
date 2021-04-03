import heapq
import random

import Map
import distance
import geometry


class PRM:
    def __init__(self, map: Map, n: int, k: int, initial: geometry.Node, goal: geometry.Node):
        self.map = map
        self.number_of_node = n
        self.number_of_neighbors = k
        self.vertices = []
        self.edges = []
        self.initial = initial
        self.goal = goal
        self.neighbors = {}

    def Roadmap_construction(self):
        while len(self.vertices) < self.number_of_node:
            q_random = self.sampling()
            if self.check_collision(q_random):
                self.vertices.append(q_random)
        for vertex in self.vertices:
            k_nearest_neighbor = self.get_k_nearest_neighbor(vertex, self.number_of_neighbors)
            for neighbor in k_nearest_neighbor:
                if geometry.Edge(neighbor, vertex) not in self.edges and self.connect(neighbor, vertex):
                    self.edges.append(geometry.Edge(neighbor, vertex))

    def solve_query(self):
        k_nearest_neighbor_initial = self.get_k_nearest_neighbor(self.initial, self.number_of_neighbors)
        k_nearest_neighbor_goal = self.get_k_nearest_neighbor(self.goal, self.number_of_neighbors)
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

    def sampling(self) -> geometry.Node:
        x = random.uniform(self.map.size[0], self.map.size[1])
        y = random.uniform(self.map.size[2], self.map.size[3])
        return geometry.Node(x, y)

    def get_k_nearest_neighbor(self, vertex: geometry.Node, k: int) -> list[geometry.Node]:
        distance_list = {}
        for node in self.vertices:
            distance_list[node] = distance.dist(node, vertex)
        k_nearest_neighbor = heapq.nsmallest(k, distance_list.items(), key=lambda x: x[1])
        self.neighbors[vertex] = k_nearest_neighbor
        return k_nearest_neighbor

    def connect(self, node1: geometry.Node, node2: geometry.Node) -> bool:
        edge = geometry.Edge(node1, node2)
        if self.edge_collision_check(edge):
            return True
        else:
            return False

    def edge_collision_check(self, edge: geometry.Edge) -> bool:
        """

        :param edge:
        :return: False: edge collide with obstacle
        True: collision free
        """
        for obstacle in self.map.obstacle_list:
            for edge1 in obstacle.edge_list:
                if geometry.intersect(edge, edge1):
                    return False
        return True

    def check_collision(self, node: geometry.Node) -> bool:
        for obstacle in self.map.obstacle_list:
            if geometry.node_in_polygon(node, obstacle):
                return False
        return True
