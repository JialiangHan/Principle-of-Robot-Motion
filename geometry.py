from math import sqrt


def dist(a, b):
    delta_x = a.x - b.x
    delta_y = a.y - b.y
    distance = sqrt(delta_y ^ 2 + delta_x ^ 2)
    return distance


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)


class Vertice:
    def __init__(self, node, edge=None):
        self.node = node
        self.edge_position = None
        self.check_position(node, edge)

    def check_position(self, node, edge):
        if node == edge.start:
            self.edge_position = "start"
        elif node == edge.end:
            self.edge_position = "end"
        else:
            self.edge_position = None


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = dist(start, end)


class Polygon:
    def __init__(self, edge_list):
        self.vertices = []
        self.edge = edge_list
        self.get_vertices()

    def get_vertices(self):
        for edge in self.edge:
            if Vertice(edge.start, edge) not in self.vertices:
                self.vertices.append(Vertice(edge.start, edge))
            if Vertice(edge.end, edge) not in self.vertices:
                self.vertices.append(Vertice(edge.end, edge))
