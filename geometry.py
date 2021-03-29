from distance import dist


def cross_product(list1, list2):
    result = list1[0] * list2[1] - list1[1] * list2[0]
    return result


def intersect(edge1, edge2):
    # determine if edge1 and edge2 are intersect each other
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
        if cross_product(CA, CD) * cross_product(CB, CD) <= 0:
            return True
        else:
            return False


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)


class Vertex:
    def __init__(self, node, edge=None):
        self.node = node
        self.edge_position = None
        self.edge = edge
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
        self.slope = 0
        self.intercept = 0
        self.calculate()

    def calculate(self):
        if self.start.x == self.end.x:
            self.slope = float("inf")
            self.intercept = float("-inf")
        elif self.start.y == self.end.y:
            self.slope = 0
            self.intercept = self.start.y
        else:
            self.slope = (self.start.y - self.end.y) / (self.start.x - self.end.x)
            self.intercept = self.start.y - self.slope * self.start.x


class Polygon:
    def __init__(self, edge_list):
        self.vertices = []
        self.edge = edge_list
        self.get_vertices()

    def get_vertices(self):
        for edge in self.edge:
            if Vertex(edge.start, edge) not in self.vertices:
                self.vertices.append(Vertex(edge.start, edge))
            if Vertex(edge.end, edge) not in self.vertices:
                self.vertices.append(Vertex(edge.end, edge))
