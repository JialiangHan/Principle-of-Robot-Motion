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
        a = np.array([[edge1.A, edge1.B], [edge2.A, edge2.B]])
        b = np.array([[-edge1.C], [-edge2.C]])
        result = np.linalg.solve(a, b)
        result = Node(result[0], result[1])
        return result


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: " + str(self.x)[:4] + ", y: " + str(self.y)[:4]


class Vertex:
    def __init__(self, node, edge_list=None):
        self.node = node
        self.edge_position = {}
        self.edge_list = edge_list
        self.check_position(node, edge_list)

    def __str__(self):
        return "x:" + str(self.node.x)[:4] + ",y:" + str(self.node.y)[:4] + ",position:" + str(self.edge_position)

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
    def __init__(self, start: Node, end: Node):
        # we want to make sure p is always the left startoint
        if start.x < end.x:
            self.start = start
            self.end = end
        elif start.x > end.x:
            self.start = end
            self.end = start
        else:
            if start.y < end.y:
                self.start = start
                self.end = end
            else:
                self.start = end
                self.end = start
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

    def aboveLine(self, node: Node) -> bool:
        """
        Return true if node lies above line segment 'self'.
        http://stackoverflow.com/enduestions/3838319/how-can-i-check-if-a-node-is-below-a-line-or-not
        :param node:
        :return:
        """
        v1x = self.end.x - self.start.x  # Vector 1.x
        v1y = self.end.y - self.start.y  # Vector 1.y
        v2x = self.end.x - node.x  # Vector 2.x
        v2y = self.end.y - node.y  # Vector 2.y
        xp = v1x * v2y - v1y * v2x  # Cross product
        # when its larger than zero, return false
        # so we assume that if it lies on the line that it is "above"
        if xp > 0:
            return False
        else:
            return True

    def belowOther(self, other) -> bool:
        if self.aboveLine(other.start) and self.aboveLine(other.end):
            return True
        if not other.aboveLine(self.start) and not other.aboveLine(self.end):
            return True
        return False

    def __gt__(self, other):
        return not self.belowOther(other)

    def __repr__(self):
        return '<Segment start:%s end:%s>' % (self.start.__str__(), self.end.__str__())


class Polygon:
    def __init__(self, edge_list):
        self.vertices = []
        self.edge = edge_list
        self.get_vertices()

    def get_vertices(self):
        dict = {}
        for edge in self.edge:
            dict[edge.start] = []
            dict[edge.end] = []
        for edge in self.edge:
            dict[edge.start].append(edge)
            dict[edge.end].append(edge)
        for key, value in dict.items():
            self.vertices.append(Vertex(key, value))


def left_or_right(vertex, edge):
    """
    output is left,right, location of an edge compared to vertex
    """
    result = []
    list_node = [edge.start, edge.end]
    for i in range(len(list_node)):
        if vertex.node == list_node[i]:
            if vertex.node.x > list_node[1 - i].x:
                result.append("left")
            else:
                result.append("right")
    return result


def edge_in_polygon(edge: Edge, polygon: Polygon) -> bool:
    if polygon is None:
        return False
    else:
        if edge in polygon.edge:
            return True
        else:
            return False


def vertex_in_obstacle(vertex: Vertex, obstacle_list: list) -> Polygon:
    for obstacle in obstacle_list:
        if vertex in obstacle.vertices:
            return obstacle
    return None
