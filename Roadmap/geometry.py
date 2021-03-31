from distance import dist
import numpy as np


def cross_product(list1, list2):
    result = list1[0] * list2[1] - list1[1] * list2[0]
    return result


def intersect(edge1, edge2):
    x_max_1 = max(edge1.start.x, edge1.end.x)
    x_min_1 = min(edge1.start.x, edge1.end.x)
    y_max_1 = max(edge1.start.y, edge1.end.y)
    y_min_1 = min(edge1.start.y, edge1.end.y)
    x_max_2 = max(edge2.start.x, edge2.end.x)
    x_min_2 = min(edge2.start.x, edge2.end.x)
    y_max_2 = max(edge2.start.y, edge2.end.y)
    y_min_2 = min(edge2.start.y, edge2.end.y)
    if x_max_2 < x_min_1 or y_max_2 < y_min_1:
        return False
    elif x_max_1 < x_min_2 or y_max_1 < y_min_2:
        return False
    else:
        CA = [edge2.start.x - edge1.start.x, edge2.start.y - edge1.start.y]
        CD = [edge1.end.x - edge1.start.x, edge1.end.y - edge1.start.y]
        CB = [edge2.end.x - edge1.start.x, edge2.end.y - edge1.start.y]
        if cross_product(CA, CD) * cross_product(CB, CD) < 0:
            return True
        else:
            return False


def intersection(edge1, edge2):
    """
    this function return intersection node of two edges
    input type: two edges
    output type: a node
    """
    if intersect(edge1, edge2):
        a = np.array([edge1.A, edge1.B], [edge2.A, edge2.B])
        b = np.array([-edge1.C], [-edge2.C])
        result = np.linalg.solve(a, b)
        result = Node(result[0], result[1])
        return result


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)


class Vertex:
    def __init__(self, node, edge_list=None):
        self.node = node
        self.edge_position = {}
        self.edge_list = edge_list
        self.check_position(node, edge_list)

    def __str__(self):
        return "x:" + str(self.node.x) + ",y:" + str(self.node.y) + ",position:" + str(self.edge_position)

    def __gt__(self, other):
        if self.node.x != other.node.x:
            return self.node.x > other.node.x
        else:
            return self.node.y > other.node.y

    def check_position(self, node, edge_list):
        for edge in edge_list:
            if node == edge.start:
                self.edge_position[edge] = "start"
            else:
                self.edge_position[edge] = "end"


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = dist(start, end)
        # line function: Ax+By+C=0
        self.A = 0
        self.B = 0
        self.C = 0
        self.calculate()

    def calculate(self):
        if self.start.x == self.end.x:
            self.A = 1
            self.B = 0
            self.C = -self.start.x
        elif self.start.y == self.end.y:
            self.A = 0
            self.B = 1
            self.C = -self.start.y
        else:
            self.A = -(self.start.y - self.end.y) / (self.start.x - self.end.x)
            self.B = 1
            self.C = -self.A * self.start.x - self.B * self.start.y


class Polygon:
    def __init__(self, edge_list):
        self.vertices = []
        self.edge = edge_list
        self.get_vertices()

    def get_vertices(self):
        dict = {}
        for edge in self.edge:
            dict[edge.start]=[]
            dict[edge.end]=[]
        for edge in self.edge:
            dict[edge.start].append(edge)
            dict[edge.end].append(edge)
            # if Vertex(edge.start, edge) not in self.vertices:
            #     self.vertices.append(Vertex(edge.start, edge))
            # if Vertex(edge.end, edge) not in self.vertices:
            #     self.vertices.append(Vertex(edge.end, edge))
        for key,value in dict.items():
            self.vertices.append(Vertex(key,value))