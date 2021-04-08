import heapq
import random

import matplotlib.pyplot as plt

import Edge
import Map
import Node
import Plot
import distance
import geometry


class PRM:
    def __init__(self, map: Map, n: int, k: int, initial: Node.Node, goal: Node.Node):
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
                if Edge.Edge(neighbor[0], vertex) not in self.edges and self.connect(neighbor[0], vertex):
                    self.edges.append(Edge.Edge(neighbor[0], vertex))

    def solve_query(self):
        k_nearest_neighbor_initial = self.get_k_nearest_neighbor(self.initial, self.number_of_neighbors)
        k_nearest_neighbor_goal = self.get_k_nearest_neighbor(self.goal, self.number_of_neighbors)
        self.vertices.append(self.initial)
        self.vertices.append(self.goal)
        # k_nearest_neighbor should be a heapq
        node_nearest_initial = k_nearest_neighbor_initial.pop(0)
        while k_nearest_neighbor_initial:
            if self.connect(self.initial, node_nearest_initial[0]):
                self.edges.append(Edge.Edge(self.initial, node_nearest_initial[0]))
                break
            else:
                node_nearest_initial = k_nearest_neighbor_initial.pop(0)
        node_nearest_goal = k_nearest_neighbor_goal.pop(0)
        while k_nearest_neighbor_goal:
            if self.connect(self.goal, node_nearest_goal[0]):
                self.edges.append(Edge.Edge(self.goal, node_nearest_goal[0]))
                break
            else:
                node_nearest_goal = k_nearest_neighbor_goal.pop(0)

    def sampling(self) -> Node.Node:
        x = random.uniform(self.map.size[0], self.map.size[1])
        y = random.uniform(self.map.size[2], self.map.size[3])
        return Node.Node(x, y)

    def get_k_nearest_neighbor(self, vertex: Node.Node, k: int) -> list:
        distance_list = {}
        for node in self.vertices:
            if node != vertex:
                distance_list[node] = distance.dist(node, vertex)
        k_nearest_neighbor = heapq.nsmallest(k, distance_list.items(), key=lambda x: x[1])
        self.neighbors[vertex] = k_nearest_neighbor
        return k_nearest_neighbor

    def connect(self, node1: Node.Node, node2: Node.Node) -> bool:
        edge = Edge.Edge(node1, node2)
        if self.edge_collision_check(edge):
            return True
        else:
            return False

    def edge_collision_check(self, edge: Edge.Edge) -> bool:
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

    def check_collision(self, node: Node.Node) -> bool:
        """
        false: collisoin
        true: collision free
        """
        for obstacle in self.map.obstacle_list:
            if geometry.node_in_polygon(node, obstacle):
                return False
        return True

    def Plot(self):
        self.map.Plot()
        Plot.plot_Node(self.initial)
        Plot.plot_Node(self.goal)
        for node in self.vertices:
            Plot.plot_Node(node)
        for edge in self.edges:
            Plot.plot_Edge(edge)
        plt.show()
